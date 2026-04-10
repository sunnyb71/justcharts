from flask import Flask, jsonify, request, send_from_directory, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
import yfinance as yf
import requests as req
import math
import re
import time
import uuid
import json
import os
import secrets
from pathlib import Path
from datetime import date as _dt_date, datetime as _dt_datetime

# ── Database backend: PostgreSQL (production) or SQLite (local / tests) ───────
_DATABASE_URL = os.environ.get('DATABASE_URL', '')
# Render supplies postgres:// but psycopg2 requires postgresql://
if _DATABASE_URL.startswith('postgres://'):
    _DATABASE_URL = 'postgresql://' + _DATABASE_URL[len('postgres://'):]

_USE_PG = bool(_DATABASE_URL)

if _USE_PG:
    import psycopg2
    import psycopg2.extensions
    _PH             = '%s'
    _NOW            = 'NOW()'
    _NOW_1H         = "NOW() + INTERVAL '1 hour'"
    _IntegrityError = psycopg2.IntegrityError
else:
    import sqlite3
    _PH             = '?'
    _NOW            = "datetime('now')"
    _NOW_1H         = "datetime('now', '+1 hour')"
    _IntegrityError = sqlite3.IntegrityError
    _WL_DB          = Path(__file__).parent / 'watchlists.db'

# ── Secret key: env var in production, file-backed locally ───────────────────
_secret_env = os.environ.get('SECRET_KEY', '')
if _secret_env:
    _SECRET_KEY = _secret_env.encode()
else:
    _SECRET_KEY_FILE = Path(__file__).parent / '.secret_key'
    if _SECRET_KEY_FILE.exists():
        _SECRET_KEY = _SECRET_KEY_FILE.read_bytes()
    else:
        _SECRET_KEY = os.urandom(24)
        try:
            _SECRET_KEY_FILE.write_bytes(_SECRET_KEY)
        except Exception:
            pass


# ── DB helpers ────────────────────────────────────────────────────────────────
def _wl_con():
    """Open a DB connection and ensure the schema exists."""
    if _USE_PG:
        con = psycopg2.connect(_DATABASE_URL)
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id            SERIAL PRIMARY KEY,
                username      TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at    TIMESTAMPTZ DEFAULT NOW()
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS watchlists (
                client_id  TEXT NOT NULL,
                name       TEXT NOT NULL,
                tickers    TEXT NOT NULL,
                updated_at TIMESTAMPTZ DEFAULT NOW(),
                PRIMARY KEY (client_id, name)
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS password_resets (
                token      TEXT PRIMARY KEY,
                username   TEXT NOT NULL,
                expires_at TIMESTAMPTZ NOT NULL
            )
        ''')
    else:
        con = sqlite3.connect(_WL_DB)
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at    TEXT DEFAULT (datetime('now'))
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS watchlists (
                client_id  TEXT NOT NULL,
                name       TEXT NOT NULL,
                tickers    TEXT NOT NULL,
                updated_at TEXT DEFAULT (datetime('now')),
                PRIMARY KEY (client_id, name)
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS password_resets (
                token      TEXT PRIMARY KEY,
                username   TEXT NOT NULL,
                expires_at TEXT NOT NULL
            )
        ''')
    con.commit()
    return con


def _exec(con, sql, params=()):
    """Execute a parameterised query on either a sqlite3 or psycopg2 connection."""
    cur = con.cursor()
    cur.execute(sql, params)
    return cur


def _owner_id():
    """'u:<id>' when logged in, raw cid UUID when anonymous, None if neither."""
    user_id = session.get('user_id')
    if user_id:
        return f'u:{user_id}'
    return request.cookies.get('cid')


def _migrate_anon(con, cid, user_id):
    """Copy anonymous watchlists to a newly-logged-in user (skip name conflicts)."""
    if not cid:
        return
    rows = _exec(con,
        f'SELECT name, tickers, updated_at FROM watchlists WHERE client_id = {_PH}',
        (cid,)
    ).fetchall()
    owner = f'u:{user_id}'
    for name, tickers, updated_at in rows:
        exists = _exec(con,
            f'SELECT 1 FROM watchlists WHERE client_id = {_PH} AND name = {_PH}',
            (owner, name)
        ).fetchone()
        if not exists:
            _exec(con,
                f'INSERT INTO watchlists (client_id, name, tickers, updated_at) VALUES ({_PH}, {_PH}, {_PH}, {_PH})',
                (owner, name, tickers, updated_at)
            )
    con.commit()


# ── In-memory response cache (90 s TTL) ─────────────────────────────────────
_cache: dict = {}
_CACHE_TTL   = 90  # seconds

def _cache_get(key):
    entry = _cache.get(key)
    if entry and time.time() - entry['ts'] < _CACHE_TTL:
        return entry['data']
    return None

def _cache_set(key, data):
    _cache[key] = {'data': data, 'ts': time.time()}


def _safe(v, dec=2):
    """Return rounded float, or None if v is None / NaN / Inf."""
    if v is None:
        return None
    try:
        f = float(v)
        return round(f, dec) if math.isfinite(f) else None
    except (TypeError, ValueError):
        return None


def _pick(*vals):
    """Return first finite numeric value from info, or None."""
    for v in vals:
        r = _safe(v)
        if r is not None:
            return r
    return None


def _fix_intraday_splits(hist, ticker_obj, period):
    """Fix un-adjusted split prices in intraday data.

    yfinance adjusts daily OHLCV for splits but often does NOT adjust intraday
    (1h/5m) data when a split occurs inside the requested window.  This
    function fetches the daily adjusted closes for the same window and, for
    any trading day where the intraday last close differs from the daily
    adjusted close by more than 5 %, scales all intraday prices for that day
    by the ratio  daily_adj / intraday_last.  That makes the intraday series
    continuous and split-corrected without touching data that is already fine.
    """
    if hist.empty:
        return hist
    try:
        daily = ticker_obj.history(period=period, interval='1d')
        if daily.empty:
            return hist

        daily_map = {}
        for ts, row in daily.iterrows():
            c = float(row['Close'])
            if math.isfinite(c) and c > 0:
                daily_map[ts.date()] = c

        hist = hist.copy()
        idx_dates = hist.index.date
        price_cols = [c for c in ('Open', 'High', 'Low', 'Close') if c in hist.columns]

        for d, daily_close in daily_map.items():
            mask = idx_dates == d
            if not mask.any():
                continue
            last_intra = float(hist.loc[mask, 'Close'].iloc[-1])
            if last_intra <= 0:
                continue
            ratio = daily_close / last_intra
            if 0.95 <= ratio <= 1.05:   # within 5 % — no correction needed
                continue
            for col in price_cols:
                hist.loc[mask, col] = hist.loc[mask, col] * ratio

        return hist
    except Exception:
        return hist     # on any error return original data unchanged


# ── Flask app ─────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = _SECRET_KEY


@app.after_request
def no_cache(response):
    # Prevent browser from caching API responses
    if request.path.startswith('/api/'):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    return response


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/search')
def search_ticker():
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify([])
    try:
        r = req.get(
            'https://query2.finance.yahoo.com/v1/finance/search',
            params={'q': q, 'quotesCount': 7, 'newsCount': 0, 'lang': 'en-US'},
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=5
        )
        quotes = [
            {'symbol': qt['symbol'], 'name': qt.get('longname') or qt.get('shortname', '')}
            for qt in r.json().get('quotes', [])
            if qt.get('symbol') and qt.get('quoteType') != 'NEWS'
        ]
        return jsonify(quotes[:7])
    except Exception:
        return jsonify([])


@app.route('/api/news')
def get_news():
    symbol = request.args.get('symbol', '').strip().upper()
    if not symbol:
        return jsonify([])
    try:
        r = req.get(
            'https://query2.finance.yahoo.com/v1/finance/search',
            params={'q': symbol, 'quotesCount': 0, 'newsCount': 6, 'lang': 'en-US'},
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=5
        )
        news = r.json().get('news', [])
        return jsonify([
            {
                'title':               n.get('title', ''),
                'publisher':           n.get('publisher', ''),
                'link':                n.get('link', ''),
                'providerPublishTime': n.get('providerPublishTime', 0),
            }
            for n in news[:6]
            if n.get('title') and n.get('link')
        ])
    except Exception:
        return jsonify([])


@app.route('/api/stock')
def get_stock():
    symbol = request.args.get('symbol', '').strip().upper()
    period = request.args.get('range', '1mo')

    if not symbol:
        return jsonify({'error': 'Missing symbol parameter'}), 400

    _valid_periods = {'1d', '5d', '1mo', '3mo', '6mo', '1y', '3y', '5y'}
    if period not in _valid_periods:
        return jsonify({'error': f'Invalid range "{period}". Must be one of: {", ".join(sorted(_valid_periods))}'}), 400

    # Serve from cache if fresh
    cached = _cache_get(f'{symbol}|{period}')
    if cached:
        return jsonify(cached)

    # Common name aliases → yfinance tickers
    aliases = {
        # Commodities
        'SILVER':      'SI=F',
        'COPPER':      'HG=F',
        'GOLD':        'GC=F',
        'OIL':         'CL=F',
        'NATGAS':      'NG=F',
        # US indexes
        'SP500':       '^GSPC',
        'SPX':         '^GSPC',
        'DOW':         '^DJI',
        'DJIA':        '^DJI',
        'NASDAQ':      '^IXIC',
        'NDX':         '^NDX',
        'VIX':         '^VIX',
        'RUT':         '^RUT',
        # Japan indexes + stocks
        'NIKKEI':      '^N225',
        'N225':        '^N225',
        'TOPIX':       '^TOPX',
        'TOYOTA':      '7203.T',
        'SONY':        '6758.T',
        'NINTENDO':    '7974.T',
        'SOFTBANK':    '9984.T',
        'HONDA':       '7267.T',
        'PANASONIC':   '6752.T',
        'CANON':       '7751.T',
        'HITACHI':     '6501.T',
        'KEYENCE':     '6861.T',
        'FANUC':       '6954.T',
        'FAST RETAILING': '9983.T',
        'UNIQLO':      '9983.T',
        'RAKUTEN':     '4755.T',
        'DOCOMO':      '9437.T',
        'KDDI':        '9433.T',
        'SHISEIDO':    '4911.T',
        # Hong Kong / China
        'HANGSENG':    '^HSI',
        'HSI':         '^HSI',
        'SSE':         '000001.SS',
        'CSI300':      '000300.SS',
        'ALIBABA':     '9988.HK',
        'TENCENT':     '0700.HK',
        'MEITUAN':     '3690.HK',
        # Korea
        'KOSPI':       '^KS11',
        'SAMSUNG':     '005930.KS',
        'HYUNDAI':     '005380.KS',
        'LG':          '003550.KS',
        'SK HYNIX':    '000660.KS',
        # Australia
        'ASX':         '^AXJO',
        # Europe indexes
        'FTSE':        '^FTSE',
        'DAX':         '^GDAXI',
        'CAC':         '^FCHI',
        'CAC40':       '^FCHI',
        'EUROSTOXX':   '^STOXX50E',
        'AEX':         '^AEX',
        'SMI':         '^SSMI',
        'IBEX':        '^IBEX',
        'MIB':         'FTSEMIB.MI',
        # Europe stocks
        'LVMH':        'MC.PA',
        'NESTLE':      'NESN.SW',
        'NOVARTIS':    'NOVN.SW',
        'ROCHE':       'ROG.SW',
        'ASML':        'ASML.AS',
        'SAP':         'SAP.DE',
        'VOLKSWAGEN':  'VOW3.DE',
        'BMW':         'BMW.DE',
        'MERCEDES':    'MBG.DE',
        'SIEMENS':     'SIE.DE',
        'HSBC':        'HSBA.L',
        'BP':          'BP.L',
        'SHELL':       'SHEL.L',
        'ASTRAZENECA': 'AZN.L',
        'UNILEVER':    'ULVR.L',
        'FERRARI':     'RACE.MI',
    }
    symbol = aliases.get(symbol, symbol)

    interval_map = {
        '1d':  '5m',
        '5d':  '1h',
        '1mo': '1d',
        '3mo': '1d',
        '6mo': '1wk',
        '1y':  '1wk',
        '3y':  '1wk',
        '5y':  '1mo',
    }
    interval = interval_map.get(period, '1d')

    intraday = period in ('1d', '5d')

    def _fetch_hist(sym):
        """Fetch history with up to 2 retries on rate-limit errors."""
        t = yf.Ticker(sym)
        for attempt in range(3):
            try:
                h = t.history(period=period, interval=interval, prepost=False)
                if intraday:
                    h = _fix_intraday_splits(h, t, period)
                return t, h
            except Exception as e:
                msg = str(e).lower()
                if ('429' in msg or 'too many' in msg or 'rate' in msg) and attempt < 2:
                    time.sleep(2 ** attempt)   # 1 s, then 2 s
                else:
                    raise

    try:
        ticker, hist = _fetch_hist(symbol)
        # Auto-retry as crypto (e.g. BTC → BTC-USD)
        if hist.empty and not symbol.endswith('-USD'):
            ticker, hist = _fetch_hist(symbol + '-USD')
            if not hist.empty:
                symbol = symbol + '-USD'
    except Exception as e:
        msg = str(e)
        if '429' in msg or 'Too Many' in msg or 'rate' in msg.lower():
            return jsonify({'error': 'Rate limited by data provider — please wait a moment and try again.'}), 429
        return jsonify({'error': msg}), 500

    # If still no data, try resolving as a company name via search
    if hist.empty:
        try:
            r = req.get(
                'https://query2.finance.yahoo.com/v1/finance/search',
                params={'q': symbol, 'quotesCount': 1, 'newsCount': 0, 'lang': 'en-US'},
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=5
            )
            quotes = r.json().get('quotes', [])
            if quotes and quotes[0].get('symbol'):
                resolved = quotes[0]['symbol']
                ticker = yf.Ticker(resolved)
                hist   = ticker.history(period=period, interval=interval)
                if not hist.empty:
                    symbol = resolved
        except Exception:
            pass

    if hist.empty:
        return jsonify({'error': f'No data found for "{symbol}". Check the symbol.'}), 404

    points = [
        {
            'date': ts.strftime('%Y-%m-%dT%H:%M') if intraday else str(ts.date()),
            'close': round(float(row['Close']), 2)
        }
        for ts, row in hist.iterrows()
        if math.isfinite(float(row['Close'])) and float(row['Close']) > 0
    ]

    # Downsample to keep charts clean for long ranges
    max_pts = {'1d': 80, '5d': 50, '1mo': 60, '3mo': 90, '6mo': 60, '1y': 60, '3y': 80, '5y': 40}
    limit = max_pts.get(period, 100)
    if len(points) > limit:
        step = max(1, len(points) // limit)
        points = points[::step]

    info = {}
    try:
        info = ticker.info
    except Exception:
        pass

    currency     = info.get('currency', 'USD')
    name         = info.get('longName') or info.get('shortName') or symbol
    # Strip trailing futures expiry date e.g. "Copper Sep 24" → "Copper"
    name = re.sub(r'\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{2,4}$', '', name).strip()
    latest_price = (
        info.get('currentPrice') or
        info.get('regularMarketPrice') or
        (points[-1]['close'] if points else None)
    )

    pe       = _pick(info.get('trailingPE'),    info.get('forwardPE'))
    cap      = _safe(info.get('marketCap'),     0)
    eps      = _safe(info.get('trailingEps'))
    target   = _safe(info.get('targetMeanPrice'))
    revenue  = _safe(info.get('totalRevenue'),  0)
    ps       = _safe(info.get('priceToSalesTrailing12Months'))
    wk52high = _safe(info.get('fiftyTwoWeekHigh'))
    wk52low  = _safe(info.get('fiftyTwoWeekLow'))
    peg      = _pick(info.get('pegRatio'),      info.get('trailingPegRatio'))

    # Earnings date
    earnings_date = None
    try:
        cal = ticker.calendar
        if isinstance(cal, dict) and 'Earnings Date' in cal:
            for d in cal['Earnings Date']:
                d2 = d.date() if hasattr(d, 'date') else d
                if d2 >= _dt_date.today():
                    earnings_date = str(d2)
                    break
    except Exception:
        pass
    if not earnings_date:
        try:
            ed = info.get('earningsDate')
            if isinstance(ed, (list, tuple)) and ed:
                ts = ed[0]
                d2 = _dt_datetime.fromtimestamp(ts).date() if isinstance(ts, (int, float)) else ts
                if hasattr(d2, 'date'): d2 = d2.date()
                if d2 >= _dt_date.today():
                    earnings_date = str(d2)
        except Exception:
            pass

    rev_growth = None
    ni_growth  = None
    roic       = None
    try:
        fin = ticker.financials
        if not fin.empty and fin.shape[1] >= 2:
            if 'Total Revenue' in fin.index:
                r = fin.loc['Total Revenue']
                if r.iloc[1] and r.iloc[1] != 0:
                    rev_growth = round((r.iloc[0] - r.iloc[1]) / abs(r.iloc[1]) * 100, 1)
            if 'Net Income' in fin.index:
                n = fin.loc['Net Income']
                if n.iloc[1] and n.iloc[1] != 0:
                    ni_growth = round((n.iloc[0] - n.iloc[1]) / abs(n.iloc[1]) * 100, 1)
            # ROIC = Net Income / (Equity + Long-term Debt)
            try:
                bs = ticker.balance_sheet
                if not bs.empty and 'Net Income' in fin.index:
                    ni_val = fin.loc['Net Income'].iloc[0]
                    equity = None
                    for key in ('Stockholders Equity', 'Total Stockholder Equity', 'Common Stock Equity'):
                        if key in bs.index:
                            equity = bs.loc[key].iloc[0]
                            break
                    debt = 0
                    for key in ('Long Term Debt', 'Long-Term Debt And Capital Lease Obligation'):
                        if key in bs.index:
                            debt = bs.loc[key].iloc[0]
                            break
                    ni_f  = _safe(ni_val,  1)
                    eq_f  = _safe(equity,  1)
                    dbt_f = _safe(debt,    1) or 0.0
                    if ni_f is not None and eq_f and (eq_f + dbt_f) != 0:
                        roic = round(ni_f / (eq_f + dbt_f) * 100, 1)
            except Exception:
                pass
    except Exception:
        pass

    result = {
        'symbol':        symbol,
        'name':          name,
        'currency':      currency,
        'points':        points,
        'latest_price':  _safe(latest_price),
        'pe_ratio':      pe,
        'market_cap':    cap,
        'eps':           eps,
        'target':        target,
        'revenue':       revenue,
        'ps_ratio':      ps,
        'wk52high':      wk52high,
        'wk52low':       wk52low,
        'rev_growth':    _safe(rev_growth, 1),
        'ni_growth':     _safe(ni_growth,  1),
        'peg_ratio':     peg,
        'roic':          _safe(roic,       1),
        'earnings_date': earnings_date,
    }
    _cache_set(f'{symbol}|{period}', result)
    return jsonify(result)


@app.route('/api/watchlists', methods=['GET'])
def get_watchlists():
    owner   = _owner_id()
    new_cid = None
    if not owner:
        new_cid = str(uuid.uuid4())
        owner   = new_cid
    con  = _wl_con()
    rows = _exec(con,
        f'SELECT name, tickers FROM watchlists WHERE client_id = {_PH} ORDER BY updated_at LIMIT 100',
        (owner,)
    ).fetchall()
    con.close()
    lists = [{'name': r[0], 'tickers': json.loads(r[1])} for r in rows]
    resp  = make_response(jsonify(lists))
    if new_cid:
        resp.set_cookie('cid', new_cid, max_age=10 * 365 * 24 * 3600, samesite='Lax', httponly=True)
    return resp


@app.route('/api/watchlists', methods=['POST'])
def save_watchlist():
    owner = _owner_id()
    if not owner:
        return jsonify({'error': 'No session'}), 400
    body    = request.get_json(silent=True) or {}
    name    = (body.get('name') or '').strip()
    raw     = body.get('tickers', [])
    tickers = [t.strip() for t in raw if isinstance(t, str) and t.strip()]
    if not name:
        return jsonify({'error': 'Missing name or tickers'}), 400
    if len(name) > 50:
        return jsonify({'error': 'Watchlist name must be 50 characters or fewer'}), 400
    if not tickers:
        return jsonify({'error': 'Missing name or tickers'}), 400
    con = _wl_con()
    _exec(con,
        f'''INSERT INTO watchlists (client_id, name, tickers, updated_at)
            VALUES ({_PH}, {_PH}, {_PH}, {_NOW})
            ON CONFLICT(client_id, name)
            DO UPDATE SET tickers = EXCLUDED.tickers, updated_at = {_NOW}''',
        (owner, name, json.dumps(tickers))
    )
    con.commit()
    con.close()
    return jsonify({'ok': True})


@app.route('/api/watchlists', methods=['DELETE'])
def delete_watchlist():
    owner = _owner_id()
    name  = request.args.get('name', '').strip()
    if not owner or not name:
        return jsonify({'error': 'Missing session or name'}), 400
    con = _wl_con()
    _exec(con, f'DELETE FROM watchlists WHERE client_id = {_PH} AND name = {_PH}', (owner, name))
    con.commit()
    con.close()
    return jsonify({'ok': True})


# ── Auth routes ───────────────────────────────────────────────────────────────
@app.route('/api/auth/me')
def auth_me():
    return jsonify({'username': session.get('username')})


@app.route('/api/auth/register', methods=['POST'])
def register():
    body     = request.get_json(silent=True) or {}
    username = (body.get('username') or '').strip().lower()
    password = body.get('password', '')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    if len(username) > 30:
        return jsonify({'error': 'Username must be 30 characters or fewer'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    con = _wl_con()
    try:
        _exec(con,
            f'INSERT INTO users (username, password_hash) VALUES ({_PH}, {_PH})',
            (username, generate_password_hash(password, method='pbkdf2:sha256'))
        )
        con.commit()
    except _IntegrityError:
        con.close()
        return jsonify({'error': 'Username already taken'}), 409
    user_id = _exec(con,
        f'SELECT id FROM users WHERE username = {_PH}', (username,)
    ).fetchone()[0]
    _migrate_anon(con, request.cookies.get('cid'), user_id)
    con.close()
    session['user_id']  = user_id
    session['username'] = username
    return jsonify({'username': username})


@app.route('/api/auth/login', methods=['POST'])
def login():
    body     = request.get_json(silent=True) or {}
    username = (body.get('username') or '').strip().lower()
    password = body.get('password', '')
    con = _wl_con()
    row = _exec(con,
        f'SELECT id, password_hash FROM users WHERE username = {_PH}', (username,)
    ).fetchone()
    if not row or not check_password_hash(row[1], password):
        con.close()
        return jsonify({'error': 'Invalid username or password'}), 401
    user_id = row[0]
    _migrate_anon(con, request.cookies.get('cid'), user_id)
    con.close()
    session['user_id']  = user_id
    session['username'] = username
    return jsonify({'username': username})


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'ok': True})


@app.route('/api/auth/forgot', methods=['POST'])
def forgot_password():
    body     = request.get_json(silent=True) or {}
    username = (body.get('username') or '').strip().lower()
    if not username:
        return jsonify({'error': 'Username required'}), 400
    con = _wl_con()
    user = _exec(con,
        f'SELECT id FROM users WHERE username = {_PH}', (username,)
    ).fetchone()
    if not user:
        con.close()
        return jsonify({'error': 'No account found with that username'}), 404
    # Invalidate any existing reset tokens for this user
    _exec(con, f'DELETE FROM password_resets WHERE username = {_PH}', (username,))
    token = secrets.token_urlsafe(32)
    _exec(con,
        f'INSERT INTO password_resets (token, username, expires_at) VALUES ({_PH}, {_PH}, {_NOW_1H})',
        (token, username)
    )
    con.commit()
    con.close()
    reset_url = f"{request.host_url}?reset_token={token}"
    return jsonify({'reset_url': reset_url})


@app.route('/api/auth/reset', methods=['POST'])
def reset_password():
    body     = request.get_json(silent=True) or {}
    token    = (body.get('token') or '').strip()
    password = body.get('password', '')
    if not token or not password:
        return jsonify({'error': 'Token and password required'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    con = _wl_con()
    row = _exec(con,
        f'SELECT username FROM password_resets WHERE token = {_PH} AND expires_at > {_NOW}',
        (token,)
    ).fetchone()
    if not row:
        con.close()
        return jsonify({'error': 'Reset link is invalid or has expired'}), 400
    username = row[0]
    user_row = _exec(con,
        f'SELECT id FROM users WHERE username = {_PH}', (username,)
    ).fetchone()
    _exec(con,
        f'UPDATE users SET password_hash = {_PH} WHERE username = {_PH}',
        (generate_password_hash(password, method='pbkdf2:sha256'), username)
    )
    _exec(con, f'DELETE FROM password_resets WHERE token = {_PH}', (token,))
    con.commit()
    con.close()
    session['user_id']  = user_row[0]
    session['username'] = username
    return jsonify({'username': username})


if __name__ == '__main__':
    print('\n  Stock app running → open http://localhost:8080 in your browser\n')
    app.run(debug=True, port=8080)
