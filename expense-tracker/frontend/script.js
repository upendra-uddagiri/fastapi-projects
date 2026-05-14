// ── CONFIG ────────────────────────────────────────────────────────────────
const API = 'http://127.0.0.1:8000';
let editingId = null;

// ── UTILITIES ─────────────────────────────────────────────────────────────

/** Format a number as Indian Rupee */
const fmt = n =>
  '₹' + Number(n).toLocaleString('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });

/** Format an ISO date string to a readable date */
const fmtDate = d =>
  new Date(d).toLocaleDateString('en-IN', {
    day: '2-digit', month: 'short', year: 'numeric'
  });

/** Show a toast notification */
function toast(msg, type = 'success') {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = 'show ' + type;
  clearTimeout(el._t);
  el._t = setTimeout(() => (el.className = ''), 2800);
}

/** Fetch wrapper with JSON headers and error handling */
async function apiFetch(path, opts = {}) {
  const res = await fetch(API + path, {
    headers: { 'Content-Type': 'application/json' },
    ...opts
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

// ── NAVIGATION ────────────────────────────────────────────────────────────

function switchPage(name, btn) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('page-' + name).classList.add('active');
  btn.classList.add('active');

  if (name === 'dashboard')    loadDashboard();
  if (name === 'transactions') loadTransactions();
  if (name === 'summary')      loadSummary();
}

// ── DASHBOARD ─────────────────────────────────────────────────────────────

async function loadDashboard() {
  try {
    const [summary, catSummary, txns] = await Promise.all([
      apiFetch('/transactions/summary'),
      apiFetch('/transactions/category-summary'),
      apiFetch('/transactions')
    ]);

    document.getElementById('dash-income').textContent  = fmt(summary.total_income);
    document.getElementById('dash-expense').textContent = fmt(summary.total_expense);
    document.getElementById('dash-balance').textContent = fmt(summary.balance);

    renderCatChart('dash-cat-chart', catSummary);
    renderRecentTable(txns.slice(-5).reverse());
  } catch (e) {
    toast(e.message, 'error');
  }
}

/** Render a horizontal bar chart into a container element */
function renderCatChart(containerId, data) {
  const el = document.getElementById(containerId);

  if (!data.length) {
    el.innerHTML = '<div class="chart-placeholder">No expense data yet.</div>';
    return;
  }

  const max = Math.max(...data.map(d => d.total));

  el.innerHTML = data
    .map(
      d => `
      <div class="bar-row">
        <div class="bar-row-label">${d.category}</div>
        <div class="bar-track">
          <div class="bar-fill" style="width:${((d.total / max) * 100).toFixed(1)}%"></div>
        </div>
        <div class="bar-val">${fmt(d.total)}</div>
      </div>`
    )
    .join('');
}

/** Render the last-5 transactions table on the dashboard */
function renderRecentTable(txns) {
  const body = document.getElementById('dash-recent-body');

  if (!txns.length) {
    body.innerHTML = `
      <tr>
        <td colspan="5">
          <div class="empty-state">
            <div class="empty-icon">◌</div>No transactions yet
          </div>
        </td>
      </tr>`;
    return;
  }

  body.innerHTML = txns
    .map(
      t => `
      <tr>
        <td>${t.title}</td>
        <td><span class="category-tag">${t.category}</span></td>
        <td><span class="badge ${t.type}">${t.type}</span></td>
        <td class="amount-cell ${t.type}">
          ${t.type === 'income' ? '+' : '-'}${fmt(t.amount)}
        </td>
        <td style="color:var(--muted);font-size:.82rem">${fmtDate(t.date)}</td>
      </tr>`
    )
    .join('');
}

// ── TRANSACTIONS PAGE ─────────────────────────────────────────────────────

async function loadTransactions() {
  const category = document.getElementById('filter-category').value.trim();
  const t_type   = document.getElementById('filter-type').value;
  const sort     = document.getElementById('filter-sort').value;

  const qs = new URLSearchParams();
  if (category) qs.set('category', category);
  if (t_type)   qs.set('t_type', t_type);
  if (sort)     qs.set('sort', sort);

  const body = document.getElementById('transactions-body');
  body.innerHTML =
    '<tr class="loading-row"><td colspan="7"><div class="spinner"></div></td></tr>';

  try {
    const data = await apiFetch('/transactions?' + qs.toString());

    if (!data.length) {
      body.innerHTML = `
        <tr>
          <td colspan="7">
            <div class="empty-state">
              <div class="empty-icon">◌</div>No transactions found
            </div>
          </td>
        </tr>`;
      return;
    }

    body.innerHTML = data
      .map(
        t => `
        <tr>
          <td style="font-weight:500">${t.title}</td>
          <td><span class="category-tag">${t.category}</span></td>
          <td><span class="badge ${t.type}">${t.type}</span></td>
          <td class="amount-cell ${t.type}">
            ${t.type === 'income' ? '+' : '-'}${fmt(t.amount)}
          </td>
          <td style="color:var(--muted);font-size:.82rem">${fmtDate(t.date)}</td>
          <td style="color:var(--muted);font-size:.82rem;max-width:140px;
                     overflow:hidden;text-overflow:ellipsis;white-space:nowrap">
            ${t.description || '—'}
          </td>
          <td>
            <div class="actions-cell">
              <button class="btn btn-edit"   onclick="openEditModal(${t.id})">Edit</button>
              <button class="btn btn-danger" onclick="deleteTransaction(${t.id})">Delete</button>
            </div>
          </td>
        </tr>`
      )
      .join('');
  } catch (e) {
    toast(e.message, 'error');
    body.innerHTML =
      '<tr><td colspan="7" style="text-align:center;color:var(--expense);padding:32px">Failed to load transactions.</td></tr>';
  }
}

function clearFilters() {
  document.getElementById('filter-category').value = '';
  document.getElementById('filter-type').value     = '';
  document.getElementById('filter-sort').value     = '';
  loadTransactions();
}

async function deleteTransaction(id) {
  if (!confirm('Delete this transaction?')) return;
  try {
    await apiFetch('/transactions/' + id, { method: 'DELETE' });
    toast('Transaction deleted', 'success');
    loadTransactions();
    loadDashboard();
  } catch (e) {
    toast(e.message, 'error');
  }
}

// ── SUMMARY PAGE ──────────────────────────────────────────────────────────

async function loadSummary() {
  const month = document.getElementById('summary-month').value;
  const qs    = month ? '?month=' + month : '';

  try {
    const [summary, catSummary] = await Promise.all([
      apiFetch('/transactions/summary' + qs),
      apiFetch('/transactions/category-summary')
    ]);

    document.getElementById('sum-income').textContent  = fmt(summary.total_income);
    document.getElementById('sum-expense').textContent = fmt(summary.total_expense);
    document.getElementById('sum-balance').textContent = fmt(summary.balance);

    renderCatChart('sum-cat-chart', catSummary);
  } catch (e) {
    toast(e.message, 'error');
  }
}

// ── MODAL ─────────────────────────────────────────────────────────────────

function openModal() {
  editingId = null;
  document.getElementById('modal-title').textContent      = 'New Transaction';
  document.getElementById('modal-submit-btn').textContent = 'Save Transaction';
  document.getElementById('f-title').value       = '';
  document.getElementById('f-amount').value      = '';
  document.getElementById('f-type').value        = 'expense';
  document.getElementById('f-category').value    = '';
  document.getElementById('f-date').value        = new Date().toISOString().slice(0, 16);
  document.getElementById('f-description').value = '';
  document.getElementById('modal-overlay').classList.add('open');
}

async function openEditModal(id) {
  try {
    const t = await apiFetch('/transactions/' + id);
    editingId = id;

    document.getElementById('modal-title').textContent      = 'Edit Transaction';
    document.getElementById('modal-submit-btn').textContent = 'Update Transaction';
    document.getElementById('f-title').value       = t.title;
    document.getElementById('f-amount').value      = t.amount;
    document.getElementById('f-type').value        = t.type;
    document.getElementById('f-category').value    = t.category;
    document.getElementById('f-date').value        = t.date.slice(0, 16);
    document.getElementById('f-description').value = t.description || '';

    document.getElementById('modal-overlay').classList.add('open');
  } catch (e) {
    toast(e.message, 'error');
  }
}

function closeModal() {
  document.getElementById('modal-overlay').classList.remove('open');
}

function handleOverlayClick(e) {
  if (e.target === document.getElementById('modal-overlay')) closeModal();
}

async function submitTransaction() {
  const title       = document.getElementById('f-title').value.trim();
  const amount      = parseFloat(document.getElementById('f-amount').value);
  const type        = document.getElementById('f-type').value;
  const category    = document.getElementById('f-category').value.trim();
  const date        = document.getElementById('f-date').value;
  const description = document.getElementById('f-description').value.trim();

  if (!title || isNaN(amount) || !category || !date) {
    toast('Please fill in all required fields', 'error');
    return;
  }

  const payload = {
    title,
    amount,
    type,
    category,
    date: new Date(date).toISOString(),
    description: description || null
  };

  const btn = document.getElementById('modal-submit-btn');
  btn.textContent = 'Saving…';
  btn.disabled    = true;

  try {
    if (editingId) {
      await apiFetch('/transactions/' + editingId, {
        method: 'PUT',
        body: JSON.stringify(payload)
      });
      toast('Transaction updated ✓');
    } else {
      await apiFetch('/transactions', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      toast('Transaction added ✓');
    }

    closeModal();
    loadTransactions();
    loadDashboard();
  } catch (e) {
    toast(e.message, 'error');
  } finally {
    btn.textContent = editingId ? 'Update Transaction' : 'Save Transaction';
    btn.disabled    = false;
  }
}

// ── KEYBOARD SHORTCUTS ────────────────────────────────────────────────────
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
});

// ── INIT ──────────────────────────────────────────────────────────────────
loadDashboard();