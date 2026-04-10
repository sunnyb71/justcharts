// ── Quotes ──────────────────────────────────────────────────────────────────
const QUOTES = [
  { text: "The stock market is a device for transferring money from the impatient to the patient.", author: "Warren Buffett" },
  { text: "In investing, what is comfortable is rarely profitable.", author: "Robert Arnott" },
  { text: "The individual investor should act consistently as an investor and not as a speculator.", author: "Benjamin Graham" },
  { text: "Know what you own, and know why you own it.", author: "Peter Lynch" },
  { text: "The four most dangerous words in investing are: 'This time it's different.'", author: "Sir John Templeton" },
  { text: "Price is what you pay. Value is what you get.", author: "Warren Buffett" },
  { text: "The stock market is filled with individuals who know the price of everything, but the value of nothing.", author: "Philip Fisher" },
  { text: "It's not whether you're right or wrong that's important, but how much money you make when you're right.", author: "George Soros" },
  { text: "The time of maximum pessimism is the best time to buy, and the time of maximum optimism is the best time to sell.", author: "Sir John Templeton" },
  { text: "Wide diversification is only required when investors do not understand what they are doing.", author: "Warren Buffett" },
  { text: "An investment in knowledge pays the best interest.", author: "Benjamin Franklin" },
  { text: "The market is a pendulum that forever swings between unsustainable optimism and unjustified pessimism.", author: "Benjamin Graham" },
  { text: "Risk comes from not knowing what you're doing.", author: "Warren Buffett" },
  { text: "The best investment you can make is in yourself.", author: "Warren Buffett" },
  { text: "Behind every stock is a company. Find out what it's doing.", author: "Peter Lynch" },
  { text: "In the short run, the market is a voting machine. In the long run, it is a weighing machine.", author: "Benjamin Graham" },
  { text: "Be fearful when others are greedy and greedy when others are fearful.", author: "Warren Buffett" },
  { text: "The secret to investing is to figure out the value of something and then pay a lot less.", author: "Joel Greenblatt" },
  { text: "Investing should be more like watching paint dry or watching grass grow. If you want excitement, take $800 and go to Las Vegas.", author: "Paul Samuelson" },
  { text: "The big money is not in the buying and the selling, but in the waiting.", author: "Charlie Munger" },
  { text: "It's far better to buy a wonderful company at a fair price than a fair company at a wonderful price.", author: "Warren Buffett" },
  { text: "The most important quality for an investor is temperament, not intellect.", author: "Warren Buffett" },
  { text: "Compound interest is the eighth wonder of the world. He who understands it, earns it; he who doesn't, pays it.", author: "Albert Einstein" },
  { text: "The goal of a successful trader is to make the best trades. Money is secondary.", author: "Alexander Elder" },
  { text: "You get recessions, you have stock market declines. If you don't understand that's going to happen, then you're not ready, you won't do well in the markets.", author: "Peter Lynch" },
  { text: "The intelligent investor is a realist who sells to optimists and buys from pessimists.", author: "Benjamin Graham" },
  { text: "In this business, if you're good, you're right six times out of ten. You're never going to be right nine times out of ten.", author: "Peter Lynch" },
  { text: "Do not save what is left after spending, but spend what is left after saving.", author: "Warren Buffett" },
  { text: "The key to making money in stocks is not to get scared out of them.", author: "Peter Lynch" },
  { text: "I will tell you how to become rich. Close the doors. Be fearful when others are greedy. Be greedy when others are fearful.", author: "Warren Buffett" },
  { text: "The most contrarian thing of all is not to oppose the crowd but to think for yourself.", author: "Peter Thiel" },
  { text: "Every once in a while, the market does something so stupid it takes your breath away.", author: "Jim Cramer" },
  { text: "The market can stay irrational longer than you can stay solvent.", author: "John Maynard Keynes" },
  { text: "I never attempt to make money on the stock market. I buy on the assumption that they could close the market the next day and not reopen it for five years.", author: "Warren Buffett" },
  { text: "Diversification is protection against ignorance. It makes little sense if you know what you are doing.", author: "Warren Buffett" },
  { text: "The best time to plant a tree was 20 years ago. The second best time is now.", author: "Chinese Proverb" },
  { text: "A bull market is when you check your stocks every day. A bear market is when you don't bother.", author: "John Hammerslough" },
  { text: "Investing is the intersection of economics and psychology.", author: "Seth Klarman" },
  { text: "I made my first investment at age eleven. I was wasting my life up until then.", author: "Warren Buffett" },
  { text: "The stock market is the only market where things go on sale and all the customers run out of the store.", author: "Cullen Roche" },
  { text: "Without a saving faith in the future, no investment is possible.", author: "George Gilder" },
  { text: "The best investment you can make is an investment in yourself. The more you learn, the more you earn.", author: "Warren Buffett" },
  { text: "How many millionaires do you know who have become wealthy by investing in savings accounts? I rest my case.", author: "Robert G. Allen" },
  { text: "Financial peace isn't the acquisition of stuff. It's learning to live on less than you make.", author: "Dave Ramsey" },
  { text: "The four most expensive words in the English language are 'This time it's different.'", author: "Sir John Templeton" },
  { text: "October: This is one of the peculiarly dangerous months to speculate in stocks. The others are July, January, September, April, November, May, March, June, December, August, and February.", author: "Mark Twain" },
  { text: "The person that turns over the most rocks wins the game.", author: "Peter Lynch" },
  { text: "An investor without investment objectives is like a traveler without a destination.", author: "Ralph Seger" },
  { text: "The way to build long-term returns is through preservation of capital and home runs.", author: "Stanley Druckenmiller" },
  { text: "Good investing is not necessarily doing good things — it's about doing common things uncommonly well.", author: "Howard Marks" },
  { text: "We don't prognosticate macroeconomic factors. We're trying to find good businesses run by good management teams.", author: "Bill Ackman" },
  { text: "Courage taught me no matter how bad a crisis gets, any sound investment will eventually pay off.", author: "Carlos Slim" },
  { text: "I buy expensive suits. They just look cheap on me.", author: "Warren Buffett" },
  { text: "It's not always easy to do what's not popular, but that's where you make your money.", author: "John Neff" },
  { text: "To be a good investor, you need to be able to handle short-term pain for long-term gain.", author: "Bill Gross" },
  { text: "Investing money is the process of committing resources in a strategic way to accomplish a specific objective.", author: "Alan Gotthardt" },
  { text: "The entrance strategy is actually more important than the exit strategy.", author: "Edward Lampert" },
  { text: "Never invest in a business you cannot understand.", author: "Warren Buffett" },
  { text: "The wisest rule in investment is: when others are selling, buy. When others are buying, sell.", author: "Jonathan Sacks" },
  { text: "You must be a contrarian — buying when there's blood in the streets, even if the blood is your own.", author: "Baron Rothschild" },
];

let quoteIndex = Math.floor(Math.random() * QUOTES.length);

function showQuote() {
  const q = QUOTES[quoteIndex % QUOTES.length];
  const el = document.getElementById('quote-bar');
  el.style.opacity = '0';
  setTimeout(() => {
    el.innerHTML = `"${q.text}" <span class="quote-author">— ${q.author}</span>`;
    el.style.opacity = '1';
  }, 400);
  quoteIndex++;
}

showQuote();
setInterval(showQuote, 3 * 60 * 1000); // rotate every 3 minutes

// ── Colors for up to 50 stocks ─────────────────────────────────────────────
const COLORS = [
  '#6366f1', '#f59e0b', '#10b981', '#ef4444', '#3b82f6',
  '#ec4899', '#14b8a6', '#f97316', '#8b5cf6', '#84cc16',
  '#06b6d4', '#f43f5e', '#a855f7', '#22c55e', '#eab308',
  '#0ea5e9', '#d946ef', '#64748b', '#fb923c', '#4ade80',
  '#7c3aed', '#b45309', '#065f46', '#991b1b', '#1d4ed8',
  '#be185d', '#0f766e', '#c2410c', '#6d28d9', '#4d7c0f',
  '#0e7490', '#be123c', '#7e22ce', '#15803d', '#a16207',
  '#075985', '#a21caf', '#374151', '#ea580c', '#16a34a',
  '#4338ca', '#d97706', '#059669', '#dc2626', '#2563eb',
  '#db2777', '#0d9488', '#ea580c', '#9333ea', '#65a30d',
];

// ── HTML escaping (used wherever server data lands in innerHTML) ─────────────
function escHtml(str) {
  return String(str ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ── App state ──────────────────────────────────────────────────────────────
let currentRange        = '1mo';
let currentView         = 'percent';
let chartInstance       = null;
let individualInstances = [];   // one Chart.js instance per individual chart
let lastStocksData      = null;
let comparisonHidden    = true;
let rankSortOn          = true;
let _compareSeq         = 0;

// ── Ticker row helpers ─────────────────────────────────────────────────────
function addRow() {
  const wrap = document.getElementById('ticker-inputs');
  if (wrap.querySelectorAll('.ticker-row').length >= 50) return;

  const row = document.createElement('div');
  row.className = 'ticker-row';
  row.innerHTML = `
    <input class="ticker-input" type="text" placeholder="AAPL or Apple" maxlength="40" />
    <button class="remove-btn" onclick="removeRow(this)">✕</button>
  `;
  wrap.appendChild(row);
  refreshRemoveButtons();

  const input = row.querySelector('.ticker-input');
  input.focus();

  input.addEventListener('keydown', e => {
    if (e.key === 'Enter' && input.value.trim().length > 0) {
      e.stopPropagation();
      removeDropdown(row);
      compareStocks();
      addRow();
    }
    if (e.key === 'Escape') removeDropdown(row);
  });
  input.addEventListener('input', () => sizeInputToPlaceholder(input));

  sizeInputToPlaceholder(input);
  attachAutocomplete(input, row);

  if (wrap.querySelectorAll('.ticker-row').length >= 50) {
    document.getElementById('add-btn').style.display = 'none';
  }
}

function removeRow(btn) {
  btn.closest('.ticker-row').remove();
  document.getElementById('add-btn').style.display = 'inline-block';
  refreshRemoveButtons();
  saveTickers();
}

function refreshRemoveButtons() {
  const rows = document.querySelectorAll('.ticker-row');
  rows.forEach(row => {
    row.querySelector('.remove-btn').style.display = rows.length > 1 ? 'inline-block' : 'none';
  });
}

// ── Range buttons ──────────────────────────────────────────────────────────
document.querySelectorAll('.range-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.range-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentRange = btn.dataset.range;
    if (lastStocksData) { compareStocks(); updateURL(); }
  });
});

// ── Fetch from our Python backend ─────────────────────────────────────────
async function fetchStock(symbol) {
  const resp = await fetch(`/api/stock?symbol=${encodeURIComponent(symbol)}&range=${currentRange}`);
  let data;
  try { data = await resp.json(); } catch { data = {}; }
  if (!resp.ok) throw new Error(data.error || `Failed to fetch "${symbol}"`);

  return {
    symbol:       data.symbol,
    name:         data.name || data.symbol,
    currency:     data.currency || 'USD',
    points:       data.points.map(p => ({ date: new Date(p.date), close: p.close })),
    latest_price: data.latest_price,
    pe_ratio:   data.pe_ratio,
    market_cap: data.market_cap,
    eps:        data.eps,
    target:     data.target,
    revenue:    data.revenue,
    ps_ratio:   data.ps_ratio,
    wk52high:   data.wk52high,
    wk52low:    data.wk52low,
    rev_growth:     data.rev_growth,
    ni_growth:      data.ni_growth,
    peg_ratio:      data.peg_ratio,
    roic:           data.roic,
    earnings_date:  data.earnings_date,
  };
}

// ── Tick limit based on range ────────────────────────────────────────────────
function tickLimit() {
  const map = { '1d': 8, '5d': 10, '1mo': 8, '3mo': 8, '6mo': 10, '1y': 12, '3y': 12, '5y': 10 };
  return map[currentRange] || 8;
}

function formatDate(date) {
  if (currentRange === '1d')
    return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
  if (currentRange === '5d')
    return date.toLocaleDateString('en-US', { weekday: 'short' }) + ' ' +
           date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
  if (['3y', '5y'].includes(currentRange))
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

// ── Build chart datasets ────────────────────────────────────────────────────
function buildDatasets(stocksData) {
  return stocksData.map((stock, i) => {
    const base = stock.points[0].close;

    const data = stock.points.map(p => ({
      x: formatDate(p.date),
      y: currentView === 'percent'
        ? +((p.close - base) / base * 100).toFixed(2)
        : +p.close.toFixed(2),
    }));

    return {
      label:            stock.name || stock.symbol,
      data,
      borderColor:      COLORS[i],
      backgroundColor:  COLORS[i] + '18',
      borderWidth:      2,
      pointRadius:      0,
      pointHoverRadius: 5,
      tension:          0,
      fill:             false,
    };
  });
}

// ── Render chart ────────────────────────────────────────────────────────────
function renderChart(stocksData) {
  const ctx = document.getElementById('chart').getContext('2d');
  if (chartInstance) chartInstance.destroy();

  const yLabel = currentView === 'percent' ? '% change' : 'Price (USD)';

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: { datasets: buildDatasets(stocksData) },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { labels: { color: cssVar('--chart-legend'), font: { size: 13 } } },
        tooltip: {
          callbacks: {
            label: ctx => {
              const v = ctx.parsed.y;
              return currentView === 'percent'
                ? `${ctx.dataset.label}: ${v >= 0 ? '+' : ''}${v}%`
                : `${ctx.dataset.label}: $${v}`;
            },
          },
        },
      },
      scales: {
        x: {
          ticks: { color: cssVar('--chart-tick'), maxTicksLimit: tickLimit(), maxRotation: 0 },
          grid:  { color: cssVar('--chart-grid') },
        },
        y: {
          title: { display: true, text: yLabel, color: cssVar('--chart-tick') },
          ticks: {
            color: cssVar('--chart-tick'),
            callback: v => currentView === 'percent' ? `${v}%` : `$${v}`,
          },
          grid: { color: cssVar('--chart-grid') },
        },
      },
    },
  });
}

// ── Individual stock charts ─────────────────────────────────────────────────
function renderIndividualCharts(stocksData) {
  // Destroy any previously created individual charts
  individualInstances.forEach(c => c.destroy());
  individualInstances = [];

  const wrap = document.getElementById('individual-charts');

  // Relative strength ranking
  const rankMap = {};
  [...stocksData]
    .map((stock, i) => {
      const prices = stock.points.map(p => p.close);
      const latest = stock.latest_price ?? prices[prices.length - 1];
      return { i, pct: (latest - prices[0]) / prices[0] * 100 };
    })
    .sort((a, b) => b.pct - a.pct)
    .forEach((item, rank) => { rankMap[item.i] = rank + 1; });

  wrap.innerHTML = `
    <h2 class="section-title">Individual Charts</h2>
    <div class="individual-grid">
      ${stocksData.map((stock, i) => {
        const d = daysUntil(stock.earnings_date);
        const earningsBadge = d !== null
          ? `<span class="earnings-badge">${d === 0 ? 'Earnings today' : `Earnings in ${d}d`}</span>`
          : '';
        return `
        <div class="individual-card" draggable="${rankSortOn ? 'false' : 'true'}" style="border-top: 3px solid ${COLORS[i]}">
          <div class="flip-card-inner">
            <div class="flip-front-content">
              <div class="card-badges">
                <span class="rank-badge">#${rankMap[i]}</span>
                <div class="card-badges-right">
                  ${earningsBadge}
                  <button class="news-btn" onclick="flipToNews(this, '${stock.symbol}')">News</button>
                  <span class="drag-handle" title="Drag to reorder">⠿</span>
                </div>
              </div>
              <canvas id="chart-individual-${i}"></canvas>
              <div class="individual-meta">
                <div class="meta-row"><span class="meta-label">P/E</span><span class="meta-val">${stock.pe_ratio ?? 'N/A'}</span></div>
                <div class="meta-row"><span class="meta-label">PEG</span><span class="meta-val">${stock.peg_ratio ?? 'N/A'}</span></div>
                <div class="meta-row"><span class="meta-label">P/S</span><span class="meta-val">${stock.ps_ratio ?? 'N/A'}</span></div>
                <div class="meta-row"><span class="meta-label">EPS</span><span class="meta-val">${formatPrice(stock.eps, stock.currency)}</span></div>
                <div class="meta-row"><span class="meta-label">ROIC</span><span class="meta-val ${stock.roic != null ? (stock.roic >= 0 ? 'up' : 'down') : ''}">${stock.roic != null ? stock.roic + '%' : 'N/A'}</span></div>
                <div class="meta-row"><span class="meta-label">Analyst Target</span><span class="meta-val">${formatPrice(stock.target, stock.currency)}</span></div>
                <div class="meta-row"><span class="meta-label">52W High</span><span class="meta-val">${formatPrice(stock.wk52high, stock.currency)}</span></div>
                <div class="meta-row"><span class="meta-label">52W Low</span><span class="meta-val">${formatPrice(stock.wk52low, stock.currency)}</span></div>
                <div class="meta-row"><span class="meta-label">Mkt Cap</span><span class="meta-val">${formatMarketCap(stock.market_cap, stock.currency)}</span></div>
                <div class="meta-row"><span class="meta-label">Revenue</span><span class="meta-val">${formatMarketCap(stock.revenue, stock.currency)}</span></div>
                <div class="meta-row"><span class="meta-label">Rev Growth</span><span class="meta-val ${stock.rev_growth != null ? (stock.rev_growth >= 0 ? 'up' : 'down') : ''}">${stock.rev_growth != null ? (stock.rev_growth >= 0 ? '+' : '') + stock.rev_growth + '%' : 'N/A'}</span></div>
                <div class="meta-row"><span class="meta-label">Net Inc Growth</span><span class="meta-val ${stock.ni_growth != null ? (stock.ni_growth >= 0 ? 'up' : 'down') : ''}">${stock.ni_growth != null ? (stock.ni_growth >= 0 ? '+' : '') + stock.ni_growth + '%' : 'N/A'}</span></div>
              </div>
            </div>
            <div class="flip-back-content" style="display:none">
              <div class="news-header">
                <span class="news-header-symbol">${escHtml(stock.name || stock.symbol)} — Latest News</span>
                <button class="news-back-btn" onclick="flipBack(this)">← Back</button>
              </div>
              <div class="news-list"></div>
            </div>
          </div>
        </div>
      `; }).join('')}
    </div>
  `;

  stocksData.forEach((stock, i) => {
    const labels      = stock.points.map(p => formatDate(p.date));
    const prices      = stock.points.map(p => p.close);
    const first       = prices[0];
    const displayPrice = stock.latest_price ?? prices[prices.length - 1];
    const pct         = ((displayPrice - first) / first * 100).toFixed(2);
    const isUp        = pct >= 0;
    const color  = COLORS[i];

    const ctx = document.getElementById(`chart-individual-${i}`).getContext('2d');

    const instance = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: stock.symbol,
          data: prices,
          borderColor:     color,
          backgroundColor: color + '18',
          borderWidth:     2,
          pointRadius:     0,
          pointHoverRadius: 4,
          tension:         0,
          fill:            true,
        }],
      },
      options: {
        responsive: true,
        aspectRatio: isMobile() ? MOBILE_ASPECT[localStorage.getItem('chartSize') || 'M'] : 2,
        plugins: {
          legend: { display: false },
          title: {
            display: true,
            text: `${stock.name || stock.symbol}   ${formatPrice(displayPrice, stock.currency)}   ${isUp ? '▲' : '▼'} ${Math.abs(pct)}%`,
            color: isUp ? '#16a34a' : '#dc2626',
            font: { size: 14, weight: 'bold' },
            padding: { bottom: 12 },
          },
          tooltip: {
            callbacks: {
              label: ctx => formatPrice(ctx.parsed.y, stock.currency),
            },
          },
        },
        scales: {
          x: {
            ticks: { color: cssVar('--chart-tick'), maxTicksLimit: tickLimit(), maxRotation: 0 },
            grid:  { color: cssVar('--chart-grid') },
          },
          y: {
            ticks: {
              color: cssVar('--chart-tick'),
              callback: v => formatPrice(v, stock.currency),
            },
            grid: { color: cssVar('--chart-grid') },
          },
        },
      },
    });

    individualInstances.push(instance);
  });

  initDragAndDrop();
}

// ── Main ────────────────────────────────────────────────────────────────────
async function compareStocks() {
  const seq = ++_compareSeq;

  // Deduplicate input rows with identical values
  const seenValues = new Set();
  [...document.querySelectorAll('.ticker-input')].forEach(el => {
    const val = el.value.trim().toUpperCase();
    if (!val) return;
    if (seenValues.has(val)) {
      el.closest('.ticker-row').remove();
      refreshRemoveButtons();
    } else {
      seenValues.add(val);
    }
  });

  const symbols = [...seenValues];
  if (symbols.length === 0) { showError('Enter at least one stock symbol.'); return; }

  saveTickers();

  setLoading(true);
  hideError();

  try {
    const results = await Promise.allSettled(symbols.map(fetchStock));

    if (seq !== _compareSeq) return; // superseded by a newer request

    const seenSymbols = new Set();
    const stocksData = results
      .filter(r => r.status === 'fulfilled')
      .map(r => r.value)
      .filter(s => { if (seenSymbols.has(s.symbol)) return false; seenSymbols.add(s.symbol); return true; });
    const failed     = results.filter(r => r.status === 'rejected').map(r => r.reason.message);

    if (failed.length > 0) {
      const msgs = failed.map(m =>
        (m.toLowerCase().includes('rate') || m.includes('429'))
          ? 'Data provider is busy — please wait a moment and try again.'
          : m
      );
      showError(msgs[0]);
    } else {
      hideError();
    }

    if (stocksData.length === 0) return;

    lastStocksData = stocksData;
    updateURL();
    document.getElementById('chart-wrap').style.display = comparisonHidden ? 'none' : 'block';
    document.getElementById('toggle-comparison-btn').style.display = 'inline-block';
    const sortBtn = document.getElementById('sort-btn');
    sortBtn.style.display = 'inline-block';
    sortBtn.classList.toggle('active', rankSortOn);
    const displayData = getDisplayData(stocksData);
    renderChart(stocksData);
    renderIndividualCharts(displayData);
    reorderTickerInputsToMatch(displayData);
  } finally {
    if (seq === _compareSeq) setLoading(false);
  }
}

// ── Size input to fit placeholder exactly ────────────────────────────────────
function sizeInputToPlaceholder(input) {
  if (isMobile()) return;
  const hasValue = input.value.trim().length > 0;
  // CSS applies text-transform:uppercase to typed values, so measure the uppercase version
  const text     = hasValue ? input.value.trim().toUpperCase() : input.placeholder;
  const cs       = getComputedStyle(input);
  const ruler    = document.createElement('span');
  // Typed value uses input's own font styles; placeholder uses its overridden styles
  ruler.style.cssText = `
    position:absolute; visibility:hidden; white-space:pre;
    font-family:${cs.fontFamily};
    font-size:${hasValue ? cs.fontSize : '0.72rem'};
    font-weight:${hasValue ? cs.fontWeight : '400'};
    letter-spacing:${cs.letterSpacing};
  `;
  ruler.textContent = text;
  document.body.appendChild(ruler);
  const w = ruler.offsetWidth;
  document.body.removeChild(ruler);
  const pad = parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight);
  input.style.width = (w + pad + 2) + 'px';
}

// ── Autocomplete ─────────────────────────────────────────────────────────────
function removeDropdown(row) {
  const d = row.querySelector('.ticker-dropdown');
  if (d) d.remove();
}

function attachAutocomplete(input, row) {
  let timer;
  input.addEventListener('input', () => {
    clearTimeout(timer);
    const q = input.value.trim();
    if (q.length < 2) { removeDropdown(row); return; }
    timer = setTimeout(async () => {
      try {
        const res  = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
        const list = await res.json();
        removeDropdown(row);
        if (!list.length) return;

        const dropdown = document.createElement('div');
        dropdown.className = 'ticker-dropdown';
        list.forEach(item => {
          const el = document.createElement('div');
          el.className = 'ticker-dropdown-item';
          const sym = document.createElement('strong');
          sym.textContent = item.symbol;
          const nameEl = document.createElement('span');
          nameEl.textContent = item.name;
          el.appendChild(sym);
          el.appendChild(nameEl);
          el.addEventListener('mousedown', e => {
            e.preventDefault();
            const duplicate = [...document.querySelectorAll('.ticker-input')]
              .find(inp => inp !== input && inp.value.trim().toUpperCase() === item.symbol.toUpperCase());
            if (duplicate) {
              removeDropdown(row);
              duplicate.style.outline = '2px solid var(--active-bg)';
              duplicate.scrollIntoView({ block: 'nearest' });
              setTimeout(() => duplicate.style.outline = '', 1400);
              return;
            }
            input.value = item.symbol;
            sizeInputToPlaceholder(input);
            removeDropdown(row);
            saveTickers();
            compareStocks();
          });
          dropdown.appendChild(el);
        });
        row.appendChild(dropdown);
      } catch (_) {}
    }, 280);
  });

  input.addEventListener('blur', () => setTimeout(() => removeDropdown(row), 150));
}

// ── Chart size toggle ─────────────────────────────────────────────────────────
const CHART_SIZES = { S: '240px', M: '380px', L: '520px', XL: '100%' };
// On mobile, size buttons control chart height via Chart.js aspectRatio (lower = taller)
const MOBILE_ASPECT = { S: 3.0, M: 2.0, L: 1.4, XL: 1.0 };

function isMobile() { return window.innerWidth <= 600; }

function setChartSize(size) {
  document.documentElement.style.setProperty('--card-min-width', CHART_SIZES[size]);
  localStorage.setItem('chartSize', size);
  document.querySelectorAll('.size-btn').forEach(b => b.classList.toggle('active', b.dataset.size === size));
  // On mobile re-render so Chart.js picks up the new aspect ratio
  if (isMobile() && lastStocksData) {
    const displayData = getDisplayData(lastStocksData);
    renderIndividualCharts(displayData);
    reorderTickerInputsToMatch(displayData);
  }
}

document.querySelectorAll('.size-btn').forEach(btn => {
  btn.addEventListener('click', () => setChartSize(btn.dataset.size));
});

// ── Drag-and-drop reorder ────────────────────────────────────────────────────
function reorderTickerInputs(fromIdx, toIdx) {
  const wrap = document.getElementById('ticker-inputs');
  const rows = [...wrap.querySelectorAll('.ticker-row')];
  const [moved] = rows.splice(fromIdx, 1);
  rows.splice(toIdx, 0, moved);
  rows.forEach(row => wrap.appendChild(row));
  saveTickers();
}

function initDragAndDrop() {
  const cards = [...document.querySelectorAll('.individual-card')];
  let draggedIdx = null;

  cards.forEach((card, i) => {
    card.addEventListener('dragstart', e => {
      draggedIdx = i;
      setTimeout(() => card.classList.add('dragging'), 0);
      e.dataTransfer.effectAllowed = 'move';
    });

    card.addEventListener('dragend', () => {
      draggedIdx = null;
      document.querySelectorAll('.individual-card').forEach(c => {
        c.classList.remove('dragging', 'drag-over');
      });
    });

    card.addEventListener('dragover', e => {
      e.preventDefault();
      if (draggedIdx !== null && draggedIdx !== i) card.classList.add('drag-over');
    });

    card.addEventListener('dragleave', e => {
      if (!card.contains(e.relatedTarget)) card.classList.remove('drag-over');
    });

    card.addEventListener('drop', e => {
      e.preventDefault();
      card.classList.remove('drag-over');
      if (draggedIdx === null || draggedIdx === i) return;

      const from = draggedIdx;
      const to   = i;
      draggedIdx  = null;

      const [moved] = lastStocksData.splice(from, 1);
      lastStocksData.splice(to, 0, moved);

      reorderTickerInputs(from, to);
      renderIndividualCharts(lastStocksData);
    });
  });
}

// ── Theme toggle ────────────────────────────────────────────────────────────
function toggleTheme() {
  const isDark = document.documentElement.dataset.theme === 'dark';
  document.documentElement.dataset.theme = isDark ? '' : 'dark';
  document.getElementById('theme-btn').textContent = isDark ? 'Dark' : 'Light';
  localStorage.setItem('theme', isDark ? 'light' : 'dark');
  if (lastStocksData) {
    const displayData = getDisplayData(lastStocksData);
    renderChart(lastStocksData);
    renderIndividualCharts(displayData);
    reorderTickerInputsToMatch(displayData);
  }
}

// ── Sync address bar with current tickers + range ───────────────────────────
function updateURL() {
  if (!lastStocksData || !lastStocksData.length) return;
  const symbols = lastStocksData.map(s => s.symbol).join(',');
  const url = `${location.pathname}?tickers=${symbols}&range=${currentRange}`;
  history.replaceState(null, '', url);
}

// ── Share URL ────────────────────────────────────────────────────────────────
function shareURL() {
  const symbols = [...document.querySelectorAll('.ticker-input')]
    .map(el => el.value.trim().toUpperCase()).filter(s => s.length > 0);
  if (symbols.length === 0) return;
  const url = `${location.origin}${location.pathname}?tickers=${symbols.join(',')}&range=${currentRange}`;
  const btn = document.getElementById('share-btn');
  navigator.clipboard.writeText(url).then(() => {
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Share', 2000);
  }).catch(() => {
    prompt('Copy this link to share:', url);
  });
}

// ── Days until earnings ──────────────────────────────────────────────────────
function daysUntil(dateStr) {
  if (!dateStr) return null;
  const now       = new Date();
  const todayUTC  = Date.UTC(now.getFullYear(), now.getMonth(), now.getDate());
  const [y, m, d] = dateStr.split('-').map(Number);
  const targetUTC = Date.UTC(y, m - 1, d);
  const days      = Math.round((targetUTC - todayUTC) / 86400000);
  return days >= 0 ? days : null;
}

// ── CSS variable reader (for chart colors) ───────────────────────────────────
function cssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

// ── Card flip: show news ─────────────────────────────────────────────────────
function formatTimeAgo(ts) {
  if (!ts) return '';
  const mins = Math.floor((Date.now() / 1000 - ts) / 60);
  if (mins < 60)   return mins + 'm ago';
  if (mins < 1440) return Math.floor(mins / 60) + 'h ago';
  return Math.floor(mins / 1440) + 'd ago';
}

function flipAnimate(inner, onMidpoint) {
  inner.style.transition = 'transform 0.22s ease-in';
  inner.style.transform  = 'rotateY(90deg)';
  setTimeout(() => {
    onMidpoint();
    inner.style.transform  = 'rotateY(-90deg)';
    inner.style.transition = '';
    requestAnimationFrame(() => requestAnimationFrame(() => {
      inner.style.transition = 'transform 0.22s ease-out';
      inner.style.transform  = 'rotateY(0deg)';
    }));
  }, 220);
}

async function flipToNews(btn, symbol) {
  const card  = btn.closest('.individual-card');
  const inner = card.querySelector('.flip-card-inner');
  const front = inner.querySelector('.flip-front-content');
  const back  = inner.querySelector('.flip-back-content');
  card.setAttribute('draggable', 'false');

  flipAnimate(inner, () => {
    front.style.display = 'none';
    back.style.display  = 'block';
    back.querySelector('.news-list').innerHTML = '<span class="news-loading">Loading…</span>';
  });

  try {
    const res   = await fetch(`/api/news?symbol=${encodeURIComponent(symbol)}`);
    const items = res.ok ? await res.json() : [];
    const list  = back.querySelector('.news-list');
    list.innerHTML = items.length
      ? items.map(n => `
          <a class="news-item" href="${escHtml(n.link)}" target="_blank" rel="noopener noreferrer">
            <div class="news-title">${escHtml(n.title)}</div>
            <div class="news-meta">${escHtml(n.publisher)} · ${formatTimeAgo(n.providerPublishTime)}</div>
          </a>`).join('')
      : '<span class="news-empty">No recent news found.</span>';
  } catch {
    back.querySelector('.news-list').innerHTML = '<span class="news-empty">Could not load news.</span>';
  }
}

function flipBack(btn) {
  const card  = btn.closest('.individual-card');
  const inner = card.querySelector('.flip-card-inner');
  const front = inner.querySelector('.flip-front-content');
  const back  = inner.querySelector('.flip-back-content');
  card.setAttribute('draggable', rankSortOn ? 'false' : 'true');

  flipAnimate(inner, () => {
    back.style.display  = 'none';
    front.style.display = '';
  });
}

// ── Sort by rank toggle ──────────────────────────────────────────────────────
function getDisplayData(data) {
  if (!rankSortOn || !data) return data;
  return [...data].sort((a, b) => {
    const pct = s => {
      const prices = s.points.map(p => p.close);
      return ((s.latest_price ?? prices[prices.length - 1]) - prices[0]) / prices[0];
    };
    return pct(b) - pct(a);
  });
}

function reorderTickerInputsToMatch(stocks) {
  const wrap = document.getElementById('ticker-inputs');
  const rows = [...wrap.querySelectorAll('.ticker-row')];
  const symbolToRow = {};
  rows.forEach(row => {
    const val = row.querySelector('.ticker-input').value.trim().toUpperCase();
    symbolToRow[val] = row;
  });
  stocks.forEach(stock => {
    const row = symbolToRow[stock.symbol];
    if (row) wrap.appendChild(row);
  });
}

function sortByRank() {
  rankSortOn = !rankSortOn;
  const btn = document.getElementById('sort-btn');
  btn.classList.toggle('active', rankSortOn);
  if (lastStocksData) {
    const displayData = getDisplayData(lastStocksData);
    renderIndividualCharts(displayData);
    reorderTickerInputsToMatch(displayData);
  }
}

// ── Toggle comparison chart ─────────────────────────────────────────────────
function toggleComparison() {
  comparisonHidden = !comparisonHidden;
  document.getElementById('chart-wrap').style.display = comparisonHidden ? 'none' : 'block';
  document.getElementById('toggle-comparison-btn').textContent = comparisonHidden ? 'Show Comparison' : 'Hide Comparison';
}

// ── Currency helpers ─────────────────────────────────────────────────────────
const CURRENCY_SYMBOLS = {
  USD: '$', EUR: '€', GBP: '£', JPY: '¥', CNY: '¥', HKD: 'HK$',
  KRW: '₩', AUD: 'A$', CHF: 'Fr ', CAD: 'C$', SEK: 'kr ', NOK: 'kr ',
  DKK: 'kr ', SGD: 'S$', INR: '₹', MXN: 'MX$', BRL: 'R$', TWD: 'NT$',
};
const ZERO_DECIMAL_CURRENCIES = new Set(['JPY', 'KRW', 'HUF', 'CLP', 'IDR', 'VND']);

function formatPrice(val, currency = 'USD') {
  if (val == null) return 'N/A';
  const sym = CURRENCY_SYMBOLS[currency] || (currency + ' ');
  const dec = ZERO_DECIMAL_CURRENCIES.has(currency) ? 0 : 2;
  return sym + val.toFixed(dec);
}

// ── Format market cap ────────────────────────────────────────────────────────
function formatMarketCap(val, currency = 'USD') {
  if (val == null) return 'N/A';
  const sym = CURRENCY_SYMBOLS[currency] || (currency + ' ');
  if (val >= 1e12) return sym + (val / 1e12).toFixed(2) + 'T';
  if (val >= 1e9)  return sym + (val / 1e9).toFixed(2)  + 'B';
  if (val >= 1e6)  return sym + (val / 1e6).toFixed(2)  + 'M';
  return sym + val.toLocaleString();
}

// ── UI helpers ─────────────────────────────────────────────────────────────
function setLoading(on) {
  document.getElementById('loading-msg').style.display = on ? 'block' : 'none';
  document.getElementById('show-btn').disabled = on;
}
function showError(msg) {
  const el = document.getElementById('error-msg');
  el.textContent = msg;
  el.style.display = 'block';
}
function hideError() {
  document.getElementById('error-msg').style.display = 'none';
}

// ── Persist tickers to localStorage ────────────────────────────────────────
function saveTickers() {
  const symbols = [...document.querySelectorAll('.ticker-input')].map(el => el.value.trim());
  try { localStorage.setItem('savedTickers', JSON.stringify(symbols)); } catch { /* storage full or blocked */ }
}

function loadTickers() {
  // URL params take priority over localStorage
  const params   = new URLSearchParams(location.search);
  const urlTickers = params.get('tickers');
  const urlRange   = params.get('range');

  if (urlRange && document.querySelector(`[data-range="${urlRange}"]`)) {
    currentRange = urlRange;
    document.querySelectorAll('.range-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`[data-range="${urlRange}"]`).classList.add('active');
  }

  let savedFromStorage = [];
  if (!urlTickers) {
    try { savedFromStorage = JSON.parse(localStorage.getItem('savedTickers') || '[]'); } catch { savedFromStorage = []; }
  }
  const saved = (urlTickers ? urlTickers.split(',') : savedFromStorage).filter(s => s.length > 0);

  if (saved.length === 0) { addRow(); return; }
  saved.forEach(symbol => {
    addRow();
    const inputs = document.querySelectorAll('.ticker-input');
    const input  = inputs[inputs.length - 1];
    input.value  = symbol;
    sizeInputToPlaceholder(input);
  });
  saveTickers();
  compareStocks();
}

// ── Apply saved theme + chart size on load ───────────────────────────────────
(function () {
  const theme = localStorage.getItem('theme') || 'light';
  if (theme === 'dark') {
    document.documentElement.dataset.theme = 'dark';
    document.getElementById('theme-btn').textContent = 'Light';
  }
  const size = localStorage.getItem('chartSize') || 'M';
  setChartSize(size);
})();

document.addEventListener('keydown', e => { if (e.key === 'Enter') compareStocks(); });
document.getElementById('ticker-inputs').addEventListener('input', saveTickers);
document.getElementById('ticker-inputs').addEventListener('click', saveTickers);
window.addEventListener('beforeunload', saveTickers);
loadTickers();

// ── Named watchlists (server-backed) ────────────────────────────────────────
let _watchlistsCache = [];

function renderWatchlistPills() {
  const container = document.getElementById('watchlist-pills');
  container.innerHTML = '';
  _watchlistsCache.forEach(wl => {
    const pill = document.createElement('div');
    pill.className = 'watchlist-pill';

    const nameSpan = document.createElement('span');
    nameSpan.textContent = wl.name;
    nameSpan.addEventListener('click', () => loadWatchlist(wl.name));

    const delBtn = document.createElement('button');
    delBtn.className = 'watchlist-del';
    delBtn.textContent = '✕';
    delBtn.title = 'Delete watchlist';
    delBtn.addEventListener('click', () => deleteWatchlist(wl.name));

    pill.appendChild(nameSpan);
    pill.appendChild(delBtn);
    container.appendChild(pill);
  });
}

async function fetchWatchlists() {
  try {
    const res = await fetch('/api/watchlists');
    if (!res.ok) return;
    _watchlistsCache = await res.json();
    renderWatchlistPills();
  } catch {
    // server unavailable — silently skip
  }
}

function saveWatchlistPrompt() {
  const inp = document.getElementById('watchlist-name-input');
  const btn = document.getElementById('watchlist-save-btn');
  if (inp.style.display === 'none') {
    inp.style.display = 'inline-block';
    inp.value = '';
    inp.focus();
    btn.textContent = '✓';
  } else {
    confirmSaveWatchlist();
  }
}

async function confirmSaveWatchlist() {
  const inp = document.getElementById('watchlist-name-input');
  const name = inp.value.trim();
  if (!name) { inp.focus(); return; }
  const tickers = [...document.querySelectorAll('.ticker-input')]
    .map(el => el.value.trim()).filter(s => s.length > 0);
  if (tickers.length === 0) return;
  inp.style.display = 'none';
  document.getElementById('watchlist-save-btn').textContent = '+ Save';
  try {
    const res = await fetch('/api/watchlists', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, tickers }),
    });
    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      showError(data.error || 'Failed to save watchlist.');
      return;
    }
    // Update cache locally so UI reflects change immediately
    _watchlistsCache = _watchlistsCache.filter(w => w.name !== name);
    _watchlistsCache.push({ name, tickers });
    renderWatchlistPills();
  } catch {
    showError('Network error — could not save watchlist.');
  }
}

function loadWatchlist(name) {
  const wl = _watchlistsCache.find(w => w.name === name);
  if (!wl) return;
  document.getElementById('ticker-inputs').innerHTML = '';
  document.getElementById('add-btn').style.display = 'inline-block';
  wl.tickers.forEach(symbol => {
    addRow();
    const inputs = document.querySelectorAll('.ticker-input');
    const input  = inputs[inputs.length - 1];
    input.value  = symbol;
    sizeInputToPlaceholder(input);
  });
  saveTickers();
  compareStocks();
}

async function deleteWatchlist(name) {
  if (!confirm(`Delete watchlist "${name}"?`)) return;
  try {
    await fetch(`/api/watchlists?name=${encodeURIComponent(name)}`, { method: 'DELETE' });
    _watchlistsCache = _watchlistsCache.filter(w => w.name !== name);
    renderWatchlistPills();
  } catch (e) {
    // ignore network errors
  }
}

document.getElementById('watchlist-save-btn').addEventListener('click', saveWatchlistPrompt);
document.getElementById('watchlist-name-input').addEventListener('keydown', e => {
  if (e.key === 'Enter') confirmSaveWatchlist();
  if (e.key === 'Escape') {
    e.target.style.display = 'none';
    document.getElementById('watchlist-save-btn').textContent = '+ Save';
  }
});

fetchWatchlists();

// ── Auth ─────────────────────────────────────────────────────────────────────
let _currentUser = null;
let _authTab     = 'login';
let _resetToken  = null;

async function fetchMe() {
  try {
    const res  = await fetch('/api/auth/me');
    const data = await res.json();
    _currentUser = data.username || null;
    updateAuthBtn();
  } catch (e) { /* ignore */ }
}

function updateAuthBtn() {
  const btn = document.getElementById('auth-btn');
  btn.textContent = _currentUser || 'Login';
}

function openAuthModal() {
  if (_currentUser) {
    logoutUser();
    return;
  }
  document.getElementById('auth-modal-overlay').style.display = 'flex';
  document.getElementById('auth-username').value = '';
  document.getElementById('auth-password').value = '';
  document.getElementById('auth-error').style.display = 'none';
  switchTab('login');
  setTimeout(() => document.getElementById('auth-username').focus(), 50);
}

function closeAuthModal(e) {
  if (!e || e.target === document.getElementById('auth-modal-overlay')) {
    document.getElementById('auth-modal-overlay').style.display = 'none';
    _resetToken = null;
  }
}

function switchTab(tab) {
  _authTab = tab;
  const isAuth   = tab === 'login' || tab === 'register';
  const isForgot = tab === 'forgot';
  const isReset  = tab === 'reset';

  document.getElementById('auth-tabs').style.display    = isAuth   ? 'flex'  : 'none';
  document.getElementById('auth-view').style.display    = isAuth   ? 'block' : 'none';
  document.getElementById('forgot-view').style.display  = isForgot ? 'block' : 'none';
  document.getElementById('reset-view').style.display   = isReset  ? 'block' : 'none';

  if (isAuth) {
    document.getElementById('tab-login').classList.toggle('active', tab === 'login');
    document.getElementById('tab-register').classList.toggle('active', tab === 'register');
    document.getElementById('auth-submit-btn').textContent = tab === 'login' ? 'Log in' : 'Register';
    document.getElementById('auth-error').style.display = 'none';
    document.getElementById('forgot-link-btn').style.display = tab === 'login' ? 'block' : 'none';
    document.getElementById('auth-password').setAttribute(
      'autocomplete', tab === 'login' ? 'current-password' : 'new-password'
    );
  }
  if (isForgot) {
    document.getElementById('forgot-username').value = '';
    document.getElementById('forgot-error').style.display = 'none';
    document.getElementById('forgot-result').style.display = 'none';
    setTimeout(() => document.getElementById('forgot-username').focus(), 50);
  }
  if (isReset) {
    document.getElementById('reset-password').value = '';
    document.getElementById('reset-error').style.display = 'none';
    setTimeout(() => document.getElementById('reset-password').focus(), 50);
  }
}

async function submitAuth() {
  const username = document.getElementById('auth-username').value.trim();
  const password = document.getElementById('auth-password').value;
  const errEl    = document.getElementById('auth-error');
  const btn      = document.getElementById('auth-submit-btn');
  if (!username || !password) {
    errEl.textContent = 'Please fill in both fields.';
    errEl.style.display = 'block';
    return;
  }
  btn.disabled = true;
  try {
    const endpoint = _authTab === 'login' ? '/api/auth/login' : '/api/auth/register';
    const res  = await fetch(endpoint, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    const data = await res.json();
    if (!res.ok) { errEl.textContent = data.error || 'Something went wrong.'; errEl.style.display = 'block'; return; }
    _currentUser = data.username;
    updateAuthBtn();
    closeAuthModal();
    fetchWatchlists();
  } catch (e) {
    errEl.textContent = 'Network error.';
    errEl.style.display = 'block';
  } finally { btn.disabled = false; }
}

async function submitForgot() {
  const username = document.getElementById('forgot-username').value.trim();
  const errEl    = document.getElementById('forgot-error');
  const result   = document.getElementById('forgot-result');
  if (!username) { errEl.textContent = 'Please enter your username.'; errEl.style.display = 'block'; return; }
  errEl.style.display = 'none';
  result.style.display = 'none';
  try {
    const res  = await fetch('/api/auth/forgot', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username }),
    });
    const data = await res.json();
    if (!res.ok) { errEl.textContent = data.error || 'Something went wrong.'; errEl.style.display = 'block'; return; }
    const link = document.getElementById('forgot-reset-link');
    link.textContent = data.reset_url;
    link.href = data.reset_url;
    result.style.display = 'block';
  } catch (e) {
    errEl.textContent = 'Network error.';
    errEl.style.display = 'block';
  }
}

async function submitReset() {
  const password = document.getElementById('reset-password').value;
  const errEl    = document.getElementById('reset-error');
  if (!password) { errEl.textContent = 'Please enter a new password.'; errEl.style.display = 'block'; return; }
  try {
    const res  = await fetch('/api/auth/reset', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: _resetToken, password }),
    });
    const data = await res.json();
    if (!res.ok) { errEl.textContent = data.error || 'Something went wrong.'; errEl.style.display = 'block'; return; }
    _currentUser = data.username;
    updateAuthBtn();
    _resetToken = null;
    closeAuthModal();
    fetchWatchlists();
  } catch (e) {
    errEl.textContent = 'Network error.';
    errEl.style.display = 'block';
  }
}

async function logoutUser() {
  await fetch('/api/auth/logout', { method: 'POST' });
  _currentUser = null;
  updateAuthBtn();
  fetchWatchlists();
}

document.getElementById('auth-modal-overlay').addEventListener('keydown', e => {
  if (e.key === 'Escape') closeAuthModal();
  if (e.key === 'Enter') {
    if (_authTab === 'forgot') submitForgot();
    else if (_authTab === 'reset') submitReset();
    else submitAuth();
  }
});

// Open reset modal if URL contains a reset token
(function () {
  const token = new URLSearchParams(location.search).get('reset_token');
  if (token) {
    _resetToken = token;
    history.replaceState(null, '', location.pathname);
    document.getElementById('auth-modal-overlay').style.display = 'flex';
    switchTab('reset');
  }
})();

fetchMe();
