/* ============================================================
   Hostel Care — application logic
   Talks to Supabase directly from the browser. No Python, no
   Streamlit, no server to keep alive.
   ============================================================ */

import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm';

/* ------------------------------------------------------------
   CONFIG — the only block you normally need to edit.
   ------------------------------------------------------------ */
const CONFIG = {
  SUPABASE_URL: 'https://wtfartnzuwdixoniufdz.supabase.co',
  // Publishable ("anon") key. Designed to be public — it is NOT a secret.
  SUPABASE_KEY: 'sb_publishable_7CLKY_ttSdt-aKKYKytvIg_11jrm6qM',

  // 'passcode'      → simple shared passcode, zero setup, DEMO-GRADE ONLY.
  // 'supabase-auth' → real login via Supabase Auth. Use this for anything real.
  //                   See README "Hardening" before switching.
  WARDEN_MODE: 'passcode',

  // Only used when WARDEN_MODE === 'passcode'.
  WARDEN_PASSCODE: 'hostel2026',
};

const sb = createClient(CONFIG.SUPABASE_URL, CONFIG.SUPABASE_KEY);

/* ------------------------------------------------------------
   Reference data (kept identical to the original app so existing
   rows keep rendering correctly)
   ------------------------------------------------------------ */
const OPTIONS = {
  blocksFull: [
    'BH-1 (Boys Hostel 1)', 'BH-2 (Boys Hostel 2)', 'BH-3 (Boys Hostel 3)',
    'GH-1 (Girls Hostel 1)', 'GH-2 (Girls Hostel 2)', 'IH-1 (International Hostel)',
  ],
  blocksShort: ['All Blocks', 'BH-1', 'BH-2', 'BH-3', 'GH-1', 'GH-2', 'IH-1'],
  categories: [
    '⚡ Electrical Repair (Fan, Light, Switch)',
    '🚰 Plumbing & Water (Tap, Leak, Flush)',
    '🧹 Cleaning & Room Sanitation',
    '🍽️ Food & Mess Quality Complaint',
    '📶 Wi-Fi & LAN Internet Connectivity',
    '🚪 Carpentry, Door & Furniture Lock',
    '🏢 General Facility / AC / Water Cooler',
    '📦 Miscellaneous / Other Hostel Issue',
  ],
  priorities: [
    '🟢 Normal (Standard Duty)',
    '🟡 Urgent (Same Day Attention)',
    '🔴 Emergency (Immediate Water/Electrical Hazard)',
  ],
  leaveReasons: [
    '🏡 Home Visit', '🏥 Medical / Emergency', '🎓 Academic Conference / Exam',
    '💼 Personal / Family Event', '🚌 Official College Tour',
  ],
  noticeCategories: [
    '📢 General Notice', '⚡ Power Maintenance', '🚰 Water Supply',
    '🧹 Mess & Sanitation', '🚨 Emergency Alert',
  ],
  durations: [
    '📌 No expiration (permanent)', '⏱️ 1 hour', '⏱️ 12 hours', '⏱️ 24 hours',
    '⏱️ 2 days', '⏱️ 3 days', '⏱️ 7 days',
  ],
};

const DURATION_HOURS = {
  '📌 No expiration (permanent)': 0, '⏱️ 1 hour': 1, '⏱️ 12 hours': 12,
  '⏱️ 24 hours': 24, '⏱️ 2 days': 48, '⏱️ 3 days': 72, '⏱️ 7 days': 168,
};

/* ------------------------------------------------------------
   Small helpers
   ------------------------------------------------------------ */
const $  = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

/** Escape user-supplied text before it ever touches innerHTML. */
const esc = (v) => String(v ?? '').replace(/[&<>"']/g, (c) => (
  { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
));

const now = () => new Date().toISOString().slice(0, 19).replace('T', ' ');

/** Storage that degrades to memory if the browser blocks it. */
const store = (() => {
  const mem = {};
  return {
    get(k) { try { return localStorage.getItem(k); } catch { return mem[k] ?? null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch { mem[k] = v; } },
    del(k) { try { localStorage.removeItem(k); } catch { delete mem[k]; } },
  };
})();

function toast(msg, kind = 'ok', title = '') {
  const el = document.createElement('div');
  el.className = `toast ${kind === 'ok' ? '' : kind}`.trim();
  el.innerHTML = (title ? `<b>${esc(title)}</b>` : '') + esc(msg);
  $('#toasts').appendChild(el);
  setTimeout(() => { el.style.opacity = '0'; setTimeout(() => el.remove(), 250); }, 4200);
}

function badgeFor(status) {
  const s = String(status || '');
  if (s === 'Resolved' || s.includes('Approved')) return 'badge-resolved';
  if (s === 'In Progress') return 'badge-progress';
  if (s === 'Rejected') return 'badge-rejected';
  return 'badge-pending';
}

const shortBlock = (b) => (b || '').split(' (')[0];

function setConn(ok) {
  const pill = $('.status-pill');
  if (!pill) return;
  pill.classList.toggle('is-down', !ok);
  $('#connLabel').textContent = ok ? 'Live' : 'Offline';
}

/** Wrap every Supabase call so a network blip shows a toast, not a blank page. */
async function guard(promise, what) {
  const { data, error } = await promise;
  if (error) {
    setConn(false);
    console.error(what, error);
    throw new Error(error.message || `Could not ${what}`);
  }
  setConn(true);
  return data;
}

/* ------------------------------------------------------------
   DATA LAYER — mirrors the old database.py, one function per op
   ------------------------------------------------------------ */
const db = {
  /* ---- grievances ---- */
  async listGrievances({ status, block, search } = {}) {
    let q = sb.from('Grievances').select('*');
    if (status && status !== 'All Statuses') q = q.eq('status', status);
    if (block && block !== 'All Blocks') q = q.ilike('block_name', `${block}%`);
    if (search && search.trim()) {
      const s = search.trim().replace(/[,()]/g, ' ');
      q = q.or(
        `student_name.ilike.%${s}%,room_number.ilike.%${s}%,category.ilike.%${s}%,` +
        `block_name.ilike.%${s}%,assigned_staff.ilike.%${s}%,description.ilike.%${s}%,` +
        `suggestion.ilike.%${s}%`
      );
    }
    return guard(q.order('date_submitted', { ascending: false }), 'load grievances');
  },

  async getGrievance(id) {
    const rows = await guard(
      sb.from('Grievances').select('*').eq('grievance_id', id).limit(1),
      'find that ticket'
    );
    return rows?.[0] ?? null;
  },

  async findGrievances(room, name) {
    return guard(
      sb.from('Grievances').select('*')
        .ilike('room_number', room.trim())
        .ilike('student_name', `%${name.trim()}%`)
        .order('date_submitted', { ascending: false }),
      'search complaints'
    );
  },

  async createGrievance(p) {
    const ts = now();
    // grievance_id is intentionally omitted — Postgres assigns it.
    const rows = await guard(
      sb.from('Grievances').insert({
        student_name: p.student_name,
        room_number: p.room_number,
        category: p.category,
        description: p.description,
        suggestion: p.suggestion || '',
        block_name: p.block_name,
        priority: p.priority,
        status: 'Pending',
        admin_remarks: '',
        assigned_staff: '',
        date_submitted: ts,
        last_updated: ts,
      }).select(),
      'submit the complaint'
    );
    return rows?.[0];
  },

  updateGrievance(id, patch) {
    return guard(
      sb.from('Grievances').update({ ...patch, last_updated: now() }).eq('grievance_id', id),
      'update the ticket'
    );
  },

  deleteGrievance(id) {
    return guard(sb.from('Grievances').delete().eq('grievance_id', id), 'delete the ticket');
  },

  async counts() {
    const rows = await guard(sb.from('Grievances').select('status, priority'), 'load statistics');
    const c = { total: 0, pending: 0, in_progress: 0, resolved: 0, rejected: 0, emergency: 0 };
    for (const r of rows || []) {
      const k = String(r.status || '').toLowerCase().replace(/ /g, '_');
      if (k in c) c[k]++;
      c.total++;
      if (String(r.priority || '').includes('Emergency') && r.status !== 'Resolved') c.emergency++;
    }
    return c;
  },

  /* ---- notices ---- */
  async listNotices(block) {
    await db.purgeExpiredNotices();
    let rows = await guard(
      sb.from('Notices').select('*').order('date_posted', { ascending: false }),
      'load notices'
    );
    rows = rows || [];
    if (block && block !== 'All Blocks') {
      rows = rows.filter((n) => n.target_block === block || n.target_block === 'All Blocks');
    }
    return rows;
  },

  async purgeExpiredNotices() {
    try {
      const rows = await guard(sb.from('Notices').select('notice_id, expires_at'), 'check notices');
      const stamp = now();
      const dead = (rows || []).filter((n) => n.expires_at && n.expires_at <= stamp).map((n) => n.notice_id);
      if (dead.length) await sb.from('Notices').delete().in('notice_id', dead);
    } catch { /* non-fatal: a failed purge must never block the board */ }
  },

  async createNotice(p) {
    let expires_at = '';
    if (p.expiryHours) {
      const d = new Date(Date.now() + p.expiryHours * 3600_000);
      expires_at = d.toISOString().slice(0, 19).replace('T', ' ');
    }
    const rows = await guard(
      sb.from('Notices').insert({
        title: p.title, content: p.content, category: p.category,
        target_block: p.target_block, posted_by: p.posted_by || 'Hostel Warden Office',
        date_posted: now(), expires_at,
      }).select(),
      'publish the notice'
    );
    return rows?.[0];
  },

  deleteNotice(id) {
    return guard(sb.from('Notices').delete().eq('notice_id', id), 'delete the notice');
  },

  /* ---- leave applications ---- */
  async listLeaves({ status, block, search } = {}) {
    let q = sb.from('LeaveApplications').select('*');
    if (status && status !== 'All Statuses') q = q.eq('status', status);
    if (block && block !== 'All Blocks') q = q.ilike('block_name', `${block}%`);
    if (search && search.trim()) {
      const s = search.trim().replace(/[,()]/g, ' ');
      q = q.or(
        `student_name.ilike.%${s}%,room_number.ilike.%${s}%,` +
        `granting_teacher.ilike.%${s}%,destination.ilike.%${s}%`
      );
    }
    return guard(q.order('date_submitted', { ascending: false }), 'load leave applications');
  },

  async getLeave(id) {
    const rows = await guard(
      sb.from('LeaveApplications').select('*').eq('leave_id', id).limit(1),
      'find that application'
    );
    return rows?.[0] ?? null;
  },

  async findLeaves(room, name) {
    return guard(
      sb.from('LeaveApplications').select('*')
        .ilike('room_number', room.trim())
        .ilike('student_name', `%${name.trim()}%`)
        .order('date_submitted', { ascending: false }),
      'search applications'
    );
  },

  async createLeave(p) {
    const ts = now();
    const rows = await guard(
      sb.from('LeaveApplications').insert({
        ...p, status: 'Pending Warden Approval',
        warden_remarks: '', gate_pass_code: '',
        date_submitted: ts, last_updated: ts,
      }).select(),
      'submit the application'
    );
    return rows?.[0];
  },

  updateLeave(id, patch) {
    return guard(
      sb.from('LeaveApplications').update({ ...patch, last_updated: now() }).eq('leave_id', id),
      'update the application'
    );
  },

  deleteLeave(id) {
    return guard(sb.from('LeaveApplications').delete().eq('leave_id', id), 'delete the record');
  },
};

/* ------------------------------------------------------------
   CSV export
   ------------------------------------------------------------ */
function downloadCsv(rows, filename) {
  if (!rows?.length) return toast('Nothing to export yet.', 'warn');
  const cols = Object.keys(rows[0]);
  const cell = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`;
  const csv = [cols.join(','), ...rows.map((r) => cols.map((c) => cell(r[c])).join(','))].join('\n');
  const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8;' }));
  const a = Object.assign(document.createElement('a'), { href: url, download: filename });
  a.click();
  URL.revokeObjectURL(url);
  toast(`Exported ${rows.length} row(s).`);
}

const stamp = () => new Date().toISOString().slice(0, 19).replace(/[-:T]/g, '');

/* ------------------------------------------------------------
   BOOT: fill dropdowns, wire theme + navigation
   ------------------------------------------------------------ */
function fillSelects() {
  $$('[data-fill]').forEach((sel) => {
    const list = OPTIONS[sel.dataset.fill] || [];
    sel.innerHTML = list.map((o) => `<option>${esc(o)}</option>`).join('');
  });
}

function initTheme() {
  const saved = store.get('hc-theme');
  if (saved) document.documentElement.dataset.theme = saved;
  $('#themeToggle').addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    store.set('hc-theme', next);
  });
}

function initNav() {
  $$('.nav-btn').forEach((btn) => btn.addEventListener('click', () => {
    $$('.nav-btn').forEach((b) => { b.classList.remove('is-active'); b.setAttribute('aria-selected', 'false'); });
    btn.classList.add('is-active');
    btn.setAttribute('aria-selected', 'true');
    const student = btn.dataset.view === 'student';
    $('#view-student').hidden = !student;
    $('#view-warden').hidden = student;
  }));

  // student tabs
  $$('[data-tab]').forEach((tab) => tab.addEventListener('click', () => {
    $$('[data-tab]').forEach((t) => t.classList.remove('is-active'));
    tab.classList.add('is-active');
    $$('[data-panel]').forEach((p) => p.classList.toggle('is-active', p.dataset.panel === tab.dataset.tab));
    if (tab.dataset.tab === 'notices') renderNotices();
  }));

  // warden tabs
  $$('[data-wtab]').forEach((tab) => tab.addEventListener('click', () => {
    $$('[data-wtab]').forEach((t) => t.classList.remove('is-active'));
    tab.classList.add('is-active');
    $$('[data-wpanel]').forEach((p) => p.classList.toggle('is-active', p.dataset.wpanel === tab.dataset.wtab));
    if (tab.dataset.wtab === 'roster') loadRoster();
    if (tab.dataset.wtab === 'notices') renderAdminNotices();
  }));

  // segmented controls
  $('#trackMode').addEventListener('click', (e) => {
    const b = e.target.closest('.seg'); if (!b) return;
    $$('#trackMode .seg').forEach((s) => s.classList.remove('is-active'));
    b.classList.add('is-active');
    $('#trackByIdForm').hidden = b.dataset.mode !== 'id';
    $('#trackByRnForm').hidden = b.dataset.mode !== 'rn';
    $('#trackResults').innerHTML = '';
  });

  $('#leaveMode').addEventListener('click', (e) => {
    const b = e.target.closest('.seg'); if (!b) return;
    $$('#leaveMode .seg').forEach((s) => s.classList.remove('is-active'));
    b.classList.add('is-active');
    $('#leaveApplyCard').hidden = b.dataset.mode !== 'apply';
    $('#leaveTrackCard').hidden = b.dataset.mode !== 'track';
    $('#leaveResults').innerHTML = '';
  });
}

/* ------------------------------------------------------------
   STATS + TICKER
   ------------------------------------------------------------ */
async function refreshStats() {
  try {
    const c = await db.counts();
    $$('#statStrip .stat-v').forEach((el) => { el.textContent = c[el.dataset.k] ?? 0; });
    $('#statEmergency').hidden = !c.emergency;
  } catch (e) { console.warn(e); }
}

async function refreshTicker() {
  try {
    const n = (await db.listNotices())[0];
    $('#tickerText').textContent = n
      ? `${n.title} — target ${n.target_block} · Emergency desk Ext 104`
      : 'No active announcements · Warden office Ext 101 · Medical room Ext 108';
  } catch {
    $('#tickerText').textContent = 'Announcements unavailable right now.';
  }
}

/* ------------------------------------------------------------
   STUDENT — submit complaint
   ------------------------------------------------------------ */
function initGrievanceForm() {
  const form = $('#grievanceForm');
  const hint = $('#descHint');

  const validate = () => {
    const d = form.description.value.trim();
    const emergency = form.priority.value.includes('Emergency');
    if (emergency && d.length < 20) {
      hint.textContent = `Emergency reports need at least 20 characters (${d.length}/20) so duty staff know what they are walking into.`;
      hint.classList.add('is-bad');
      return false;
    }
    hint.textContent = emergency ? 'Emergency — on-duty staff are alerted immediately.' : '';
    hint.classList.remove('is-bad');
    return true;
  };
  form.description.addEventListener('input', validate);
  form.priority.addEventListener('change', validate);

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = Object.fromEntries(new FormData(form));
    if (!f.student_name.trim() || !f.room_number.trim() || !f.description.trim()) {
      return toast('Name, room number and description are required.', 'err', 'Incomplete form');
    }
    if (!validate()) return toast('Add more detail to the emergency description.', 'err');

    const btn = form.querySelector('button[type=submit]');
    btn.disabled = true; btn.textContent = 'Submitting…';
    try {
      const row = await db.createGrievance({
        student_name: f.student_name.trim(),
        room_number: f.room_number.trim(),
        category: f.category,
        description: f.description.trim(),
        suggestion: (f.suggestion || '').trim(),
        block_name: shortBlock(f.block_name),
        priority: f.priority,
      });
      const id = row?.grievance_id;
      $('#submitResult').innerHTML = `
        <div class="rec">
          <div class="rec-head">
            <div><div class="rec-id">TICKET #${esc(id)}</div>
            <div class="rec-title">Request logged successfully</div>
            <div class="rec-meta">Save this ticket number — it is the fastest way to track progress.</div></div>
            <span class="badge badge-pending">Pending</span>
          </div>
        </div>`;
      $('#submitResult').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      form.reset(); hint.textContent = '';
      toast(`Ticket #${id} created.`, 'ok', 'Submitted');
      refreshStats();
    } catch (err) {
      toast(err.message, 'err', 'Could not submit');
    } finally {
      btn.disabled = false; btn.textContent = 'Submit complaint';
    }
  });
}

/* ------------------------------------------------------------
   STUDENT — track complaint
   ------------------------------------------------------------ */
function grievanceCard(g) {
  const alert = String(g.priority || '').includes('Emergency') && g.status !== 'Resolved';
  return `
  <article class="rec ${alert ? 'is-alert' : ''}">
    <div class="rec-head">
      <div>
        <div class="rec-id">TICKET #${esc(g.grievance_id)}</div>
        <div class="rec-title">${esc(g.category)}</div>
        <div class="rec-meta">${esc(g.student_name)} · ${esc(g.block_name)} Room ${esc(g.room_number)} · submitted ${esc(g.date_submitted)}</div>
      </div>
      <span class="badge ${badgeFor(g.status)}">${esc(g.status)}</span>
    </div>
    <div class="rec-body">
      <div class="rec-quote">${esc(g.description)}</div>
      ${g.suggestion ? `<div class="rec-meta" style="margin-top:10px"><b>Suggested fix:</b> ${esc(g.suggestion)}</div>` : ''}
    </div>
    <div class="rec-foot">
      <span><b>Priority</b> ${esc(g.priority || 'Normal')}</span>
      <span><b>Assigned</b> ${esc(g.assigned_staff || 'Not yet assigned')}</span>
      <span><b>Remarks</b> ${esc(g.admin_remarks || 'Awaiting review')}</span>
      <span><b>Updated</b> ${esc(g.last_updated || '—')}</span>
    </div>
  </article>`;
}

function initTracking() {
  $('#trackByIdForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const raw = e.target.ticket.value.trim().replace('#', '');
    const box = $('#trackResults');
    if (!raw) return toast('Enter a ticket ID first.', 'warn');
    if (!/^\d+$/.test(raw)) return toast('Ticket IDs are numeric, e.g. 101.', 'err');
    box.innerHTML = `<div class="empty">Searching…</div>`;
    try {
      const g = await db.getGrievance(Number(raw));
      box.innerHTML = g ? grievanceCard(g)
        : `<div class="empty">No complaint found with ID #${esc(raw)}.</div>`;
    } catch (err) { box.innerHTML = `<div class="empty">${esc(err.message)}</div>`; }
  });

  $('#trackByRnForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const room = e.target.room.value.trim(), name = e.target.name.value.trim();
    const box = $('#trackResults');
    if (!room || !name) return toast('Both room number and student name are required.', 'err');
    box.innerHTML = `<div class="empty">Searching…</div>`;
    try {
      const rows = await db.findGrievances(room, name);
      box.innerHTML = rows.length
        ? rows.map(grievanceCard).join('')
        : `<div class="empty">No complaints match that room and name.</div>`;
    } catch (err) { box.innerHTML = `<div class="empty">${esc(err.message)}</div>`; }
  });
}

/* ------------------------------------------------------------
   STUDENT — leave & gate pass
   ------------------------------------------------------------ */
function leaveCard(l) {
  return `
  <article class="rec">
    <div class="rec-head">
      <div>
        <div class="rec-id">LEAVE #L-${esc(l.leave_id)}</div>
        <div class="rec-title">${esc(l.student_name)} · ${esc(l.destination)}</div>
        <div class="rec-meta">${esc(l.block_name)} Room ${esc(l.room_number)} · ${esc(l.from_date)} → ${esc(l.to_date)}</div>
      </div>
      <span class="badge ${badgeFor(l.status)}">${esc(l.status)}</span>
    </div>
    ${l.gate_pass_code ? `
      <div class="gatepass">
        <div class="code">${esc(l.gate_pass_code)}</div>
        <small>Show this code to the security officer at the gate on departure.</small>
      </div>` : ''}
    <div class="rec-foot">
      <span><b>Faculty</b> ${esc(l.granting_teacher)}</span>
      <span><b>Reason</b> ${esc(l.leave_reason)}</span>
      <span><b>Warden notes</b> ${esc(l.warden_remarks || 'Awaiting authorisation')}</span>
    </div>
  </article>`;
}

function initLeave() {
  const form = $('#leaveForm');
  const today = new Date().toISOString().slice(0, 10);
  const plus2 = new Date(Date.now() + 2 * 86400_000).toISOString().slice(0, 10);
  form.from_date.value = today; form.to_date.value = plus2;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = Object.fromEntries(new FormData(form));
    const required = ['student_name', 'room_number', 'phone_number', 'parent_phone', 'granting_teacher', 'destination'];
    if (required.some((k) => !String(f[k] || '').trim())) {
      return toast('Fill in every required field, including faculty name and parent phone.', 'err', 'Incomplete form');
    }
    if (f.to_date < f.from_date) return toast('Return date cannot be before departure date.', 'err');

    const btn = form.querySelector('button[type=submit]');
    btn.disabled = true; btn.textContent = 'Submitting…';
    try {
      const row = await db.createLeave({
        student_name: f.student_name.trim(),
        block_name: shortBlock(f.block_name),
        room_number: f.room_number.trim(),
        phone_number: f.phone_number.trim(),
        parent_phone: f.parent_phone.trim(),
        leave_reason: f.leave_reason,
        destination: f.destination.trim(),
        from_date: f.from_date,
        to_date: f.to_date,
        granting_teacher: f.granting_teacher.trim(),
      });
      toast(`Application #L-${row?.leave_id} submitted.`, 'ok', 'Sent to warden');
      $('#leaveResults').innerHTML = leaveCard(row);
      form.reset(); form.from_date.value = today; form.to_date.value = plus2;
    } catch (err) {
      toast(err.message, 'err', 'Could not submit');
    } finally {
      btn.disabled = false; btn.textContent = 'Submit to warden';
    }
  });

  $('#leaveTrackForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const lid = e.target.lid.value.trim().replace(/[#]|L-/gi, '');
    const room = e.target.room.value.trim(), name = e.target.name.value.trim();
    const box = $('#leaveResults');
    box.innerHTML = `<div class="empty">Searching…</div>`;
    try {
      let rows = [];
      if (lid) {
        if (!/^\d+$/.test(lid)) { box.innerHTML = ''; return toast('Leave IDs are numeric, e.g. 1.', 'err'); }
        const r = await db.getLeave(Number(lid));
        rows = r ? [r] : [];
      } else if (room && name) {
        rows = await db.findLeaves(room, name);
      } else {
        box.innerHTML = '';
        return toast('Enter a leave ID, or both room number and name.', 'warn');
      }
      box.innerHTML = rows.length ? rows.map(leaveCard).join('')
        : `<div class="empty">No leave applications found.</div>`;
    } catch (err) { box.innerHTML = `<div class="empty">${esc(err.message)}</div>`; }
  });
}

/* ------------------------------------------------------------
   STUDENT — notice board
   ------------------------------------------------------------ */
function noticeCard(n, admin = false) {
  const expiry = n.expires_at ? `Active until ${esc(n.expires_at)}` : 'Permanent notice';
  return `
  <article class="rec">
    <div class="rec-head">
      <div>
        <div class="rec-id">${esc(n.category)}</div>
        <div class="rec-title">${esc(n.title)}</div>
        <div class="rec-meta">${esc(n.target_block)} · posted ${esc(n.date_posted)} · ${expiry}</div>
      </div>
      ${admin ? `<button class="btn btn-sm btn-danger" data-del-notice="${esc(n.notice_id)}">Delete</button>` : ''}
    </div>
    <div class="rec-body">${esc(n.content)}</div>
    <div class="rec-foot"><span><b>Posted by</b> ${esc(n.posted_by || 'Warden Office')}</span></div>
  </article>`;
}

async function renderNotices() {
  const box = $('#noticeList');
  box.innerHTML = `<div class="empty">Loading…</div>`;
  try {
    const rows = await db.listNotices($('#noticeBlockFilter').value);
    box.innerHTML = rows.length ? rows.map((n) => noticeCard(n)).join('')
      : `<div class="empty">No announcements published for this block.</div>`;
  } catch (err) { box.innerHTML = `<div class="empty">${esc(err.message)}</div>`; }
}

/* ------------------------------------------------------------
   WARDEN — auth
   ------------------------------------------------------------ */
function initWardenAuth() {
  const usingAuth = CONFIG.WARDEN_MODE === 'supabase-auth';
  $('#emailField').hidden = !usingAuth;
  $('#pwLabel').textContent = usingAuth ? 'Password' : 'Passcode';
  $('#loginHint').textContent = usingAuth
    ? 'Restricted area — sign in with your warden account.'
    : 'Restricted area — enter the shared warden passcode.';

  const openConsole = () => {
    $('#wardenLogin').hidden = true;
    $('#wardenConsole').hidden = false;
    loadDispatch();
  };

  if (usingAuth) {
    sb.auth.getSession().then(({ data }) => { if (data?.session) openConsole(); });
  } else if (store.get('hc-warden') === '1') {
    openConsole();
  }

  $('#wardenLoginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = Object.fromEntries(new FormData(e.target));
    if (usingAuth) {
      const { error } = await sb.auth.signInWithPassword({
        email: (f.email || '').trim(), password: f.password || '',
      });
      if (error) return toast(error.message, 'err', 'Sign-in failed');
      toast('Signed in.', 'ok');
      openConsole();
    } else {
      if ((f.password || '').trim() !== CONFIG.WARDEN_PASSCODE) {
        return toast('Incorrect passcode.', 'err', 'Access denied');
      }
      store.set('hc-warden', '1');
      openConsole();
    }
    e.target.reset();
  });

  $('#wardenLogout').addEventListener('click', async () => {
    if (usingAuth) await sb.auth.signOut();
    store.del('hc-warden');
    $('#wardenConsole').hidden = true;
    $('#wardenLogin').hidden = false;
    toast('Warden desk locked.');
  });
}

/* ------------------------------------------------------------
   WARDEN — dispatch console
   ------------------------------------------------------------ */
let grievCache = [];

async function loadDispatch() {
  const wrap = $('#grievTableWrap');
  wrap.innerHTML = `<div class="empty">Loading tickets…</div>`;
  try {
    grievCache = await db.listGrievances({
      status: $('#fStatus').value, block: $('#fBlock').value, search: $('#fSearch').value,
    });
    if (!grievCache.length) {
      wrap.innerHTML = `<div class="empty">No tickets match these filters.</div>`;
      $('#grievEditor').innerHTML = '';
      return;
    }
    wrap.innerHTML = `
      <div class="table-count">${grievCache.length} ticket(s) — click a row to manage</div>
      <table><thead><tr>
        <th>ID</th><th>Block</th><th>Room</th><th>Student</th>
        <th>Category</th><th>Priority</th><th>Status</th><th>Updated</th>
      </tr></thead><tbody>
      ${grievCache.map((g) => `
        <tr data-gid="${esc(g.grievance_id)}">
          <td class="num">#${esc(g.grievance_id)}</td>
          <td>${esc(g.block_name)}</td>
          <td>${esc(g.room_number)}</td>
          <td>${esc(g.student_name)}</td>
          <td>${esc(g.category)}</td>
          <td>${esc(g.priority || 'Normal')}</td>
          <td><span class="badge ${badgeFor(g.status)}">${esc(g.status)}</span></td>
          <td class="num">${esc((g.last_updated || '').slice(0, 16))}</td>
        </tr>`).join('')}
      </tbody></table>`;

    $$('#grievTableWrap tr[data-gid]').forEach((tr) => tr.addEventListener('click', () => {
      $$('#grievTableWrap tr').forEach((r) => r.classList.remove('is-selected'));
      tr.classList.add('is-selected');
      openGrievanceEditor(Number(tr.dataset.gid));
    }));
    refreshStats();
  } catch (err) { wrap.innerHTML = `<div class="empty">${esc(err.message)}</div>`; }
}

function openGrievanceEditor(id) {
  const g = grievCache.find((x) => x.grievance_id === id);
  if (!g) return;
  const statuses = ['Pending', 'In Progress', 'Resolved', 'Rejected'];
  $('#grievEditor').innerHTML = `
    <div class="card">
      <div class="card-head">
        <h2>Ticket #${esc(g.grievance_id)} — ${esc(g.student_name)}</h2>
        <p>${esc(g.block_name)} Room ${esc(g.room_number)} · ${esc(g.category)} · ${esc(g.priority || 'Normal')}</p>
      </div>
      <div class="rec-quote">${esc(g.description)}</div>
      ${g.suggestion ? `<p class="rec-meta" style="margin-top:10px"><b>Student suggestion:</b> ${esc(g.suggestion)}</p>` : ''}
      <form class="form" id="grievEditForm" style="margin-top:16px">
        <div class="grid-2">
          <label class="field"><span class="label">Status</span>
            <select name="status">${statuses.map((s) => `<option ${s === g.status ? 'selected' : ''}>${s}</option>`).join('')}</select>
          </label>
          <label class="field"><span class="label">Assigned staff</span>
            <input name="assigned_staff" value="${esc(g.assigned_staff || '')}" placeholder="e.g. Ramesh (electrician)" />
          </label>
        </div>
        <label class="field"><span class="label">Warden remarks</span>
          <textarea name="admin_remarks" rows="3">${esc(g.admin_remarks || '')}</textarea>
        </label>
        <div class="form-foot">
          <button class="btn btn-primary" type="submit">Save changes</button>
          <button class="btn btn-danger" type="button" id="delGriev">Delete ticket</button>
        </div>
      </form>
    </div>`;

  $('#grievEditForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = Object.fromEntries(new FormData(e.target));
    try {
      await db.updateGrievance(id, {
        status: f.status,
        assigned_staff: f.assigned_staff.trim(),
        admin_remarks: f.admin_remarks.trim(),
      });
      toast(`Ticket #${id} updated.`, 'ok', 'Saved');
      loadDispatch();
    } catch (err) { toast(err.message, 'err'); }
  });

  $('#delGriev').addEventListener('click', async () => {
    if (!confirm(`Delete ticket #${id}? This cannot be undone.`)) return;
    try {
      await db.deleteGrievance(id);
      toast(`Ticket #${id} deleted.`, 'warn');
      $('#grievEditor').innerHTML = '';
      loadDispatch();
    } catch (err) { toast(err.message, 'err'); }
  });

  $('#grievEditor').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* ------------------------------------------------------------
   WARDEN — leave roster
   ------------------------------------------------------------ */
let leaveCache = [];

async function loadRoster() {
  const wrap = $('#leaveTableWrap');
  wrap.innerHTML = `<div class="empty">Loading roster…</div>`;
  try {
    leaveCache = await db.listLeaves({
      status: $('#lStatus').value, block: $('#lBlock').value, search: $('#lSearch').value,
    });
    if (!leaveCache.length) {
      wrap.innerHTML = `<div class="empty">No leave applications match these filters.</div>`;
      $('#leaveEditor').innerHTML = '';
      return;
    }
    wrap.innerHTML = `
      <div class="table-count">${leaveCache.length} application(s) — click a row to action</div>
      <table><thead><tr>
        <th>ID</th><th>Block</th><th>Room</th><th>Student</th><th>Faculty</th>
        <th>From</th><th>To</th><th>Destination</th><th>Status</th><th>Pass</th>
      </tr></thead><tbody>
      ${leaveCache.map((l) => `
        <tr data-lid="${esc(l.leave_id)}">
          <td class="num">L-${esc(l.leave_id)}</td>
          <td>${esc(l.block_name)}</td>
          <td>${esc(l.room_number)}</td>
          <td>${esc(l.student_name)}</td>
          <td>${esc(l.granting_teacher)}</td>
          <td class="num">${esc(l.from_date)}</td>
          <td class="num">${esc(l.to_date)}</td>
          <td>${esc(l.destination)}</td>
          <td><span class="badge ${badgeFor(l.status)}">${esc(l.status)}</span></td>
          <td class="num">${esc(l.gate_pass_code || '—')}</td>
        </tr>`).join('')}
      </tbody></table>`;

    $$('#leaveTableWrap tr[data-lid]').forEach((tr) => tr.addEventListener('click', () => {
      $$('#leaveTableWrap tr').forEach((r) => r.classList.remove('is-selected'));
      tr.classList.add('is-selected');
      openLeaveEditor(Number(tr.dataset.lid));
    }));
  } catch (err) { wrap.innerHTML = `<div class="empty">${esc(err.message)}</div>`; }
}

function openLeaveEditor(id) {
  const l = leaveCache.find((x) => x.leave_id === id);
  if (!l) return;
  const statuses = ['Pending Warden Approval', 'Approved / Gate Pass Issued', 'Rejected'];
  const defaultPass = l.gate_pass_code || `GP-${new Date().getFullYear()}-X${String(id).padStart(3, '0')}`;
  $('#leaveEditor').innerHTML = `
    <div class="card">
      <div class="card-head">
        <h2>Application #L-${esc(id)} — ${esc(l.student_name)}</h2>
        <p>${esc(l.block_name)} Room ${esc(l.room_number)} · ${esc(l.from_date)} → ${esc(l.to_date)} · ${esc(l.destination)}</p>
      </div>
      <div class="rec-foot" style="margin-top:0;border-top:0;padding-top:0">
        <span><b>Student</b> ${esc(l.phone_number)}</span>
        <span><b>Parent</b> ${esc(l.parent_phone)}</span>
        <span><b>Faculty sign-off</b> ${esc(l.granting_teacher)}</span>
        <span><b>Reason</b> ${esc(l.leave_reason)}</span>
      </div>
      <form class="form" id="leaveEditForm" style="margin-top:16px">
        <div class="grid-2">
          <label class="field"><span class="label">Decision</span>
            <select name="status">${statuses.map((s) => `<option ${s === l.status ? 'selected' : ''}>${s}</option>`).join('')}</select>
          </label>
          <label class="field"><span class="label">Gate pass code</span>
            <input name="gate_pass_code" value="${esc(defaultPass)}" />
          </label>
        </div>
        <label class="field"><span class="label">Warden remarks</span>
          <textarea name="warden_remarks" rows="2">${esc(l.warden_remarks || '')}</textarea>
        </label>
        <div class="form-foot">
          <button class="btn btn-primary" type="submit">Save authorisation</button>
          <button class="btn btn-danger" type="button" id="delLeave">Delete record</button>
        </div>
      </form>
    </div>`;

  $('#leaveEditForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = Object.fromEntries(new FormData(e.target));
    try {
      await db.updateLeave(id, {
        status: f.status,
        warden_remarks: f.warden_remarks.trim(),
        // A pass code only means anything once the leave is actually approved.
        gate_pass_code: f.status.includes('Approved') ? f.gate_pass_code.trim() : '',
      });
      toast(`Application #L-${id} updated.`, 'ok', 'Saved');
      loadRoster();
    } catch (err) { toast(err.message, 'err'); }
  });

  $('#delLeave').addEventListener('click', async () => {
    if (!confirm(`Delete leave record #L-${id}?`)) return;
    try {
      await db.deleteLeave(id);
      toast(`Record #L-${id} deleted.`, 'warn');
      $('#leaveEditor').innerHTML = '';
      loadRoster();
    } catch (err) { toast(err.message, 'err'); }
  });

  $('#leaveEditor').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* ------------------------------------------------------------
   WARDEN — notice manager
   ------------------------------------------------------------ */
async function renderAdminNotices() {
  const box = $('#noticeAdminList');
  box.innerHTML = `<div class="empty">Loading…</div>`;
  try {
    const rows = await db.listNotices();
    box.innerHTML = rows.length ? rows.map((n) => noticeCard(n, true)).join('')
      : `<div class="empty">Nothing published yet.</div>`;
    $$('#noticeAdminList [data-del-notice]').forEach((btn) => btn.addEventListener('click', async () => {
      const id = Number(btn.dataset.delNotice);
      if (!confirm('Delete this notice?')) return;
      try {
        await db.deleteNotice(id);
        toast('Notice deleted.', 'warn');
        renderAdminNotices(); refreshTicker();
      } catch (err) { toast(err.message, 'err'); }
    }));
  } catch (err) { box.innerHTML = `<div class="empty">${esc(err.message)}</div>`; }
}

function initNoticeForm() {
  $('#noticeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = Object.fromEntries(new FormData(e.target));
    if (!f.title.trim() || !f.content.trim()) return toast('Title and message are required.', 'err');
    try {
      await db.createNotice({
        title: f.title.trim(),
        content: f.content.trim(),
        category: f.category,
        target_block: f.target_block,
        posted_by: f.posted_by.trim() || 'Hostel Warden Office',
        expiryHours: DURATION_HOURS[f.expiry] ?? 0,
      });
      toast('Announcement published.', 'ok');
      e.target.reset();
      fillSelects();
      renderAdminNotices(); refreshTicker();
    } catch (err) { toast(err.message, 'err'); }
  });
}

/* ------------------------------------------------------------
   INIT
   ------------------------------------------------------------ */
function initWardenFilters() {
  ['#fBlock', '#fStatus'].forEach((s) => $(s).addEventListener('change', loadDispatch));
  $('#fRefresh').addEventListener('click', loadDispatch);
  let t; $('#fSearch').addEventListener('input', () => { clearTimeout(t); t = setTimeout(loadDispatch, 350); });

  ['#lBlock', '#lStatus'].forEach((s) => $(s).addEventListener('change', loadRoster));
  $('#lRefresh').addEventListener('click', loadRoster);
  let t2; $('#lSearch').addEventListener('input', () => { clearTimeout(t2); t2 = setTimeout(loadRoster, 350); });

  $('#exportGrievances').addEventListener('click', () => downloadCsv(grievCache, `grievances_${stamp()}.csv`));
  $('#exportLeaves').addEventListener('click', () => downloadCsv(leaveCache, `leave_roster_${stamp()}.csv`));
}

function init() {
  fillSelects();
  initTheme();
  initNav();
  initGrievanceForm();
  initTracking();
  initLeave();
  initNoticeForm();
  initWardenAuth();
  initWardenFilters();

  $('#noticeBlockFilter').addEventListener('change', renderNotices);
  $('#brandHome').addEventListener('click', (e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); });

  refreshStats();
  refreshTicker();
  renderNotices();
  setInterval(refreshStats, 60_000);
}

init();
