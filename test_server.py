"""
Tests for stock_comparison/server.py

Covers:
  - Unit tests: _safe, _pick, _migrate_anon
  - Integration tests: auth (register, login, logout, me, forgot, reset)
  - Integration tests: watchlists (GET, POST, DELETE, isolation, migration)
  - Integration tests: stock API (input validation)
"""

import sys
import json
import sqlite3
import tempfile
from pathlib import Path

# ── Patch module-level globals BEFORE importing server ───────────────────────
_tmpdir = Path(tempfile.mkdtemp())

sys.path.insert(0, str(Path(__file__).parent))

import server as _srv

# Redirect DB and secret key to temp locations so tests never touch production data
_srv._WL_DB     = _tmpdir / 'test.db'
_srv._SECRET_KEY = b'test-secret-key-do-not-use-in-prod'
_srv.app.secret_key = _srv._SECRET_KEY

from server import app, _safe, _pick, _migrate_anon, _wl_con

import pytest


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def clean_db():
    """Drop and recreate all tables before every test for full isolation."""
    db = _srv._WL_DB
    if db.exists():
        db.unlink()
    yield
    if db.exists():
        db.unlink()


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


# ── Helpers ───────────────────────────────────────────────────────────────────

def register(client, username='alice', password='secret123'):
    return client.post('/api/auth/register',
                       json={'username': username, 'password': password})

def login(client, username='alice', password='secret123'):
    return client.post('/api/auth/login',
                       json={'username': username, 'password': password})

def logout(client):
    return client.post('/api/auth/logout', json={})

def get_reset_token(client, username='alice', password='secret123'):
    register(client, username, password)
    logout(client)
    r = client.post('/api/auth/forgot', json={'username': username})
    url = r.get_json()['reset_url']
    return url.split('reset_token=')[1]


# ═══════════════════════════════════════════════════════════════════════════════
# UNIT TESTS: _safe
# ═══════════════════════════════════════════════════════════════════════════════

class TestSafe:
    def test_none_returns_none(self):
        assert _safe(None) is None

    def test_nan_returns_none(self):
        assert _safe(float('nan')) is None

    def test_inf_returns_none(self):
        assert _safe(float('inf')) is None

    def test_neg_inf_returns_none(self):
        assert _safe(float('-inf')) is None

    def test_valid_float_rounded(self):
        assert _safe(3.14159) == 3.14

    def test_integer_input(self):
        assert _safe(42) == 42.0

    def test_string_number(self):
        assert _safe('3.14') == 3.14

    def test_invalid_string_returns_none(self):
        assert _safe('not a number') is None

    def test_custom_decimal_places(self):
        assert _safe(3.14159, dec=4) == 3.1416

    def test_zero(self):
        assert _safe(0) == 0.0

    def test_negative_number(self):
        assert _safe(-5.5) == -5.5


# ═══════════════════════════════════════════════════════════════════════════════
# UNIT TESTS: _pick
# ═══════════════════════════════════════════════════════════════════════════════

class TestPick:
    def test_returns_first_valid(self):
        assert _pick(1.0, 2.0, 3.0) == 1.0

    def test_skips_none(self):
        assert _pick(None, 2.0) == 2.0

    def test_all_none_returns_none(self):
        assert _pick(None, None) is None

    def test_skips_nan(self):
        assert _pick(float('nan'), 5.0) == 5.0

    def test_no_args_returns_none(self):
        assert _pick() is None

    def test_skips_inf(self):
        assert _pick(float('inf'), 3.0) == 3.0


# ═══════════════════════════════════════════════════════════════════════════════
# UNIT TESTS: _migrate_anon
# ═══════════════════════════════════════════════════════════════════════════════

class TestMigrateAnon:
    def _setup(self):
        con = _wl_con()
        con.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ('bob', 'fakehash')
        )
        con.commit()
        user_id = con.execute("SELECT id FROM users WHERE username='bob'").fetchone()[0]
        return con, user_id

    def test_migrates_lists_to_user(self):
        con, user_id = self._setup()
        con.execute(
            "INSERT INTO watchlists (client_id, name, tickers) VALUES (?, ?, ?)",
            ('anon-cid', 'MyList', '["AAPL"]')
        )
        con.commit()
        _migrate_anon(con, 'anon-cid', user_id)
        row = con.execute(
            "SELECT tickers FROM watchlists WHERE client_id=?", (f'u:{user_id}',)
        ).fetchone()
        con.close()
        assert row is not None
        assert row[0] == '["AAPL"]'

    def test_skips_null_cid(self):
        con, user_id = self._setup()
        # Should not raise
        _migrate_anon(con, None, user_id)
        con.close()

    def test_no_overwrite_on_name_conflict(self):
        con, user_id = self._setup()
        con.execute(
            "INSERT INTO watchlists (client_id, name, tickers) VALUES (?, ?, ?)",
            (f'u:{user_id}', 'MyList', '["MSFT"]')
        )
        con.execute(
            "INSERT INTO watchlists (client_id, name, tickers) VALUES (?, ?, ?)",
            ('anon-cid', 'MyList', '["AAPL"]')
        )
        con.commit()
        _migrate_anon(con, 'anon-cid', user_id)
        row = con.execute(
            "SELECT tickers FROM watchlists WHERE client_id=? AND name='MyList'",
            (f'u:{user_id}',)
        ).fetchone()
        con.close()
        assert row[0] == '["MSFT"]'  # original preserved, not overwritten

    def test_migrates_multiple_lists(self):
        con, user_id = self._setup()
        for name in ('Tech', 'Finance', 'Crypto'):
            con.execute(
                "INSERT INTO watchlists (client_id, name, tickers) VALUES (?, ?, ?)",
                ('anon-cid', name, '["AAPL"]')
            )
        con.commit()
        _migrate_anon(con, 'anon-cid', user_id)
        rows = con.execute(
            "SELECT name FROM watchlists WHERE client_id=?", (f'u:{user_id}',)
        ).fetchall()
        con.close()
        names = [r[0] for r in rows]
        assert set(names) == {'Tech', 'Finance', 'Crypto'}

    def test_empty_cid_skipped(self):
        con, user_id = self._setup()
        _migrate_anon(con, '', user_id)  # empty string cid
        rows = con.execute(
            "SELECT name FROM watchlists WHERE client_id=?", (f'u:{user_id}',)
        ).fetchall()
        con.close()
        assert rows == []


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS: Register
# ═══════════════════════════════════════════════════════════════════════════════

class TestRegister:
    def test_success(self, client):
        r = register(client)
        assert r.status_code == 200
        assert r.get_json()['username'] == 'alice'

    def test_sets_session_on_register(self, client):
        register(client)
        r = client.get('/api/auth/me')
        assert r.get_json()['username'] == 'alice'

    def test_duplicate_username_409(self, client):
        register(client)
        r = register(client, password='different123')
        assert r.status_code == 409
        assert 'taken' in r.get_json()['error'].lower()

    def test_username_too_short(self, client):
        r = register(client, username='ab')
        assert r.status_code == 400

    def test_password_too_short(self, client):
        r = register(client, password='abc')
        assert r.status_code == 400

    def test_missing_username(self, client):
        r = client.post('/api/auth/register', json={'password': 'secret123'})
        assert r.status_code == 400

    def test_missing_password(self, client):
        r = client.post('/api/auth/register', json={'username': 'alice'})
        assert r.status_code == 400

    def test_username_lowercased(self, client):
        r = client.post('/api/auth/register',
                        json={'username': 'ALICE', 'password': 'secret123'})
        assert r.get_json()['username'] == 'alice'

    def test_duplicate_case_insensitive(self, client):
        register(client, username='alice')
        r = register(client, username='ALICE')
        assert r.status_code == 409

    def test_empty_body(self, client):
        r = client.post('/api/auth/register', json={})
        assert r.status_code == 400

    def test_username_too_long(self, client):
        r = client.post('/api/auth/register',
                        json={'username': 'a' * 31, 'password': 'secret123'})
        assert r.status_code == 400
        assert 'error' in r.get_json()


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS: Login
# ═══════════════════════════════════════════════════════════════════════════════

class TestLogin:
    def test_success(self, client):
        register(client)
        logout(client)
        r = login(client)
        assert r.status_code == 200
        assert r.get_json()['username'] == 'alice'

    def test_sets_session(self, client):
        register(client)
        logout(client)
        login(client)
        assert client.get('/api/auth/me').get_json()['username'] == 'alice'

    def test_wrong_password(self, client):
        register(client)
        logout(client)
        r = client.post('/api/auth/login',
                        json={'username': 'alice', 'password': 'wrongpass'})
        assert r.status_code == 401

    def test_nonexistent_user(self, client):
        r = login(client, username='ghost')
        assert r.status_code == 401

    def test_case_insensitive_username(self, client):
        register(client, username='alice')
        logout(client)
        r = client.post('/api/auth/login',
                        json={'username': 'ALICE', 'password': 'secret123'})
        assert r.status_code == 200

    def test_empty_body(self, client):
        r = client.post('/api/auth/login', json={})
        assert r.status_code == 401


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS: Me / Logout
# ═══════════════════════════════════════════════════════════════════════════════

class TestMeAndLogout:
    def test_me_unauthenticated(self, client):
        r = client.get('/api/auth/me')
        assert r.status_code == 200
        assert r.get_json()['username'] is None

    def test_me_authenticated(self, client):
        register(client)
        assert client.get('/api/auth/me').get_json()['username'] == 'alice'

    def test_logout_clears_session(self, client):
        register(client)
        logout(client)
        assert client.get('/api/auth/me').get_json()['username'] is None

    def test_logout_idempotent(self, client):
        logout(client)
        assert client.get('/api/auth/me').get_json()['username'] is None


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS: Forgot password
# ═══════════════════════════════════════════════════════════════════════════════

class TestForgotPassword:
    def test_valid_user_returns_reset_url(self, client):
        register(client)
        logout(client)
        r = client.post('/api/auth/forgot', json={'username': 'alice'})
        assert r.status_code == 200
        data = r.get_json()
        assert 'reset_url' in data
        assert 'reset_token=' in data['reset_url']

    def test_invalid_user_returns_404(self, client):
        r = client.post('/api/auth/forgot', json={'username': 'nobody'})
        assert r.status_code == 404

    def test_missing_username(self, client):
        r = client.post('/api/auth/forgot', json={})
        assert r.status_code == 400

    def test_new_request_invalidates_old_token(self, client):
        register(client)
        logout(client)
        token1 = client.post('/api/auth/forgot',
                             json={'username': 'alice'}).get_json()['reset_url'].split('=')[1]
        token2 = client.post('/api/auth/forgot',
                             json={'username': 'alice'}).get_json()['reset_url'].split('=')[1]
        assert token1 != token2
        r = client.post('/api/auth/reset',
                        json={'token': token1, 'password': 'newpass123'})
        assert r.status_code == 400  # old token rejected

    def test_token_is_url_safe(self, client):
        register(client)
        logout(client)
        r = client.post('/api/auth/forgot', json={'username': 'alice'})
        token = r.get_json()['reset_url'].split('reset_token=')[1]
        assert all(c.isalnum() or c in '-_' for c in token)


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS: Reset password
# ═══════════════════════════════════════════════════════════════════════════════

class TestResetPassword:
    def test_valid_reset_succeeds(self, client):
        token = get_reset_token(client)
        r = client.post('/api/auth/reset',
                        json={'token': token, 'password': 'newpass123'})
        assert r.status_code == 200
        assert r.get_json()['username'] == 'alice'

    def test_new_password_works_for_login(self, client):
        token = get_reset_token(client)
        client.post('/api/auth/reset', json={'token': token, 'password': 'newpass123'})
        logout(client)
        assert login(client, password='newpass123').status_code == 200

    def test_old_password_fails_after_reset(self, client):
        token = get_reset_token(client)
        client.post('/api/auth/reset', json={'token': token, 'password': 'newpass123'})
        logout(client)
        assert login(client, password='secret123').status_code == 401

    def test_token_is_single_use(self, client):
        token = get_reset_token(client)
        client.post('/api/auth/reset', json={'token': token, 'password': 'newpass123'})
        r = client.post('/api/auth/reset',
                        json={'token': token, 'password': 'another123'})
        assert r.status_code == 400

    def test_invalid_token(self, client):
        r = client.post('/api/auth/reset',
                        json={'token': 'completely_fake_token', 'password': 'newpass123'})
        assert r.status_code == 400

    def test_password_too_short(self, client):
        token = get_reset_token(client)
        r = client.post('/api/auth/reset', json={'token': token, 'password': 'abc'})
        assert r.status_code == 400

    def test_missing_token(self, client):
        r = client.post('/api/auth/reset', json={'password': 'newpass123'})
        assert r.status_code == 400

    def test_missing_password(self, client):
        token = get_reset_token(client)
        r = client.post('/api/auth/reset', json={'token': token})
        assert r.status_code == 400

    def test_auto_login_after_reset(self, client):
        token = get_reset_token(client)
        client.post('/api/auth/reset', json={'token': token, 'password': 'newpass123'})
        assert client.get('/api/auth/me').get_json()['username'] == 'alice'


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS: Watchlists — anonymous
# ═══════════════════════════════════════════════════════════════════════════════

class TestWatchlistsAnonymous:
    def test_get_returns_empty_list(self, client):
        r = client.get('/api/watchlists')
        assert r.status_code == 200
        assert r.get_json() == []

    def test_get_sets_cid_cookie(self, client):
        r = client.get('/api/watchlists')
        set_cookies = r.headers.getlist('Set-Cookie')
        assert any('cid=' in h for h in set_cookies)

    def test_post_without_any_session_returns_400(self, client):
        # No prior GET (no cid), no auth session
        r = client.post('/api/watchlists',
                        json={'name': 'Test', 'tickers': ['AAPL']})
        assert r.status_code == 400

    def test_save_and_retrieve(self, client):
        client.get('/api/watchlists')  # establish cid
        client.post('/api/watchlists', json={'name': 'Tech', 'tickers': ['AAPL', 'GOOGL']})
        r = client.get('/api/watchlists')
        data = r.get_json()
        assert len(data) == 1
        assert data[0]['name'] == 'Tech'
        assert data[0]['tickers'] == ['AAPL', 'GOOGL']

    def test_upsert_replaces_existing(self, client):
        client.get('/api/watchlists')
        client.post('/api/watchlists', json={'name': 'Tech', 'tickers': ['AAPL']})
        client.post('/api/watchlists', json={'name': 'Tech', 'tickers': ['MSFT', 'GOOGL']})
        data = client.get('/api/watchlists').get_json()
        assert len(data) == 1
        assert data[0]['tickers'] == ['MSFT', 'GOOGL']

    def test_multiple_watchlists(self, client):
        client.get('/api/watchlists')
        client.post('/api/watchlists', json={'name': 'Tech',    'tickers': ['AAPL']})
        client.post('/api/watchlists', json={'name': 'Finance', 'tickers': ['JPM']})
        data = client.get('/api/watchlists').get_json()
        assert len(data) == 2

    def test_delete_watchlist(self, client):
        client.get('/api/watchlists')
        client.post('/api/watchlists', json={'name': 'Tech', 'tickers': ['AAPL']})
        client.delete('/api/watchlists?name=Tech')
        assert client.get('/api/watchlists').get_json() == []

    def test_delete_nonexistent_is_ok(self, client):
        client.get('/api/watchlists')
        r = client.delete('/api/watchlists?name=DoesNotExist')
        assert r.status_code == 200

    def test_delete_missing_name_400(self, client):
        client.get('/api/watchlists')
        r = client.delete('/api/watchlists')
        assert r.status_code == 400

    def test_save_missing_name_400(self, client):
        client.get('/api/watchlists')
        r = client.post('/api/watchlists', json={'tickers': ['AAPL']})
        assert r.status_code == 400

    def test_save_empty_tickers_400(self, client):
        client.get('/api/watchlists')
        r = client.post('/api/watchlists', json={'name': 'Test', 'tickers': []})
        assert r.status_code == 400

    def test_save_whitespace_only_tickers_filtered_to_400(self, client):
        client.get('/api/watchlists')
        r = client.post('/api/watchlists', json={'name': 'Test', 'tickers': ['', '   ']})
        assert r.status_code == 400

    def test_save_name_too_long(self, client):
        client.get('/api/watchlists')
        r = client.post('/api/watchlists',
                        json={'name': 'N' * 51, 'tickers': ['AAPL']})
        assert r.status_code == 400
        assert 'error' in r.get_json()

    def test_save_mixed_valid_invalid_tickers(self, client):
        client.get('/api/watchlists')
        r = client.post('/api/watchlists',
                        json={'name': 'Test', 'tickers': ['', '  ', 'AAPL', '  MSFT  ']})
        assert r.status_code == 200
        data = client.get('/api/watchlists').get_json()
        assert data[0]['tickers'] == ['AAPL', 'MSFT']


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS: Watchlists — authenticated
# ═══════════════════════════════════════════════════════════════════════════════

class TestWatchlistsAuthenticated:
    def test_save_and_retrieve_while_logged_in(self, client):
        register(client)
        client.post('/api/watchlists', json={'name': 'Portfolio', 'tickers': ['AAPL', 'TSLA']})
        data = client.get('/api/watchlists').get_json()
        assert len(data) == 1
        assert data[0]['name'] == 'Portfolio'

    def test_logout_hides_user_watchlists(self, client):
        register(client)
        client.post('/api/watchlists', json={'name': 'Private', 'tickers': ['AAPL']})
        logout(client)
        # After logout, new anon session has no lists
        data = client.get('/api/watchlists').get_json()
        assert all(w['name'] != 'Private' for w in data)

    def test_different_users_are_isolated(self, client):
        register(client, 'alice')
        client.post('/api/watchlists', json={'name': 'AliceList', 'tickers': ['AAPL']})
        logout(client)
        register(client, 'bob', 'bobpass123')
        names = [w['name'] for w in client.get('/api/watchlists').get_json()]
        assert 'AliceList' not in names

    def test_delete_only_affects_own_lists(self, client):
        register(client, 'alice')
        client.post('/api/watchlists', json={'name': 'AliceList', 'tickers': ['AAPL']})
        logout(client)
        register(client, 'bob', 'bobpass123')
        # Bob tries to delete Alice's list
        client.delete('/api/watchlists?name=AliceList')
        logout(client)
        login(client, 'alice')
        names = [w['name'] for w in client.get('/api/watchlists').get_json()]
        assert 'AliceList' in names  # Alice's list is untouched


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS: Watchlist migration
# ═══════════════════════════════════════════════════════════════════════════════

class TestWatchlistMigration:
    def test_anon_lists_migrate_on_register(self, client):
        client.get('/api/watchlists')  # get cid
        client.post('/api/watchlists', json={'name': 'Saved', 'tickers': ['AAPL']})
        register(client)  # registers and migrates
        names = [w['name'] for w in client.get('/api/watchlists').get_json()]
        assert 'Saved' in names

    def test_anon_lists_migrate_on_login(self, client):
        register(client)
        logout(client)
        client.get('/api/watchlists')  # new cid
        client.post('/api/watchlists', json={'name': 'AnonList', 'tickers': ['MSFT']})
        login(client)  # login migrates
        names = [w['name'] for w in client.get('/api/watchlists').get_json()]
        assert 'AnonList' in names

    def test_migration_skips_name_conflicts(self, client):
        # Alice has 'Conflict' = MSFT
        register(client)
        client.post('/api/watchlists', json={'name': 'Conflict', 'tickers': ['MSFT']})
        logout(client)
        # New anon session also has 'Conflict' = GOOGL
        client.get('/api/watchlists')
        client.post('/api/watchlists', json={'name': 'Conflict', 'tickers': ['GOOGL']})
        # Login: anon 'Conflict' should NOT overwrite Alice's
        login(client)
        wls = client.get('/api/watchlists').get_json()
        conflict = next(w for w in wls if w['name'] == 'Conflict')
        assert conflict['tickers'] == ['MSFT']  # Alice's original preserved

    def test_non_conflicting_anon_lists_are_merged(self, client):
        register(client)
        client.post('/api/watchlists', json={'name': 'UserList', 'tickers': ['AAPL']})
        logout(client)
        client.get('/api/watchlists')
        client.post('/api/watchlists', json={'name': 'AnonList', 'tickers': ['TSLA']})
        login(client)
        names = [w['name'] for w in client.get('/api/watchlists').get_json()]
        assert 'UserList' in names
        assert 'AnonList' in names


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION TESTS: Stock API (input validation only — no live network calls)
# ═══════════════════════════════════════════════════════════════════════════════

class TestStockAPI:
    def test_missing_symbol_returns_400(self, client):
        r = client.get('/api/stock')
        assert r.status_code == 400
        assert 'error' in r.get_json()

    def test_empty_symbol_returns_400(self, client):
        r = client.get('/api/stock?symbol=')
        assert r.status_code == 400

    def test_whitespace_symbol_returns_400(self, client):
        r = client.get('/api/stock?symbol=   ')
        assert r.status_code == 400

    def test_invalid_period_returns_400(self, client):
        r = client.get('/api/stock?symbol=AAPL&range=invalid')
        assert r.status_code == 400
        assert 'error' in r.get_json()

    def test_search_empty_query_returns_empty_list(self, client):
        r = client.get('/api/search?q=')
        assert r.status_code == 200
        assert r.get_json() == []

    def test_search_single_char_returns_empty_list(self, client):
        r = client.get('/api/search?q=A')
        assert r.status_code == 200
        assert r.get_json() == []
