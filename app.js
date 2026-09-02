/**
 * A2Z DSA Tracker & Personal Vault - Main Application Script
 */

(function () {
  'use strict';

  // --- Storage Keys ---
  // v1 (old, integer-id) keys are kept around read-only for migration.
  const STORAGE_KEYS = {
    SCHEMA_VERSION: 'dsa_vault_schema_version',
    SOLVED_V1: 'dsa_vault_solved_ids',
    STARRED_V1: 'dsa_vault_starred_ids',
    NOTES_V1: 'dsa_vault_notes_dict',
    SOLVED: 'dsa_vault_solved_ids',       // now holds an ARRAY OF STRING SLUGS (was int ids)
    STARRED: 'dsa_vault_starred_ids',     // now holds an ARRAY OF STRING SLUGS (was int ids)
    NOTES: 'dsa_vault_notes_dict',        // now keyed by string slug (was int id)
    SOLVE_META: 'dsa_vault_solve_meta',   // NEW: per-id { solvedAt, attempts[], srs } — see solveMeta
    THEME: 'dsa_vault_theme',
    OPEN_STEPS: 'dsa_vault_open_steps',
    GCAL_TIME: 'dsa_vault_gcal_time',
    GCAL_DURATION: 'dsa_vault_gcal_duration'
  };
  const CURRENT_SCHEMA_VERSION = 2;

  // --- App State ---
  const state = {
    solvedIds: new Set(),
    starredIds: new Set(),
    notes: {}, // id -> { notes, code, lang, timeComplexity, spaceComplexity, updatedAt }
    // Per-problem history that rides alongside solvedIds/notes, keyed by the
    // same string id. Kept separate from solvedIds (a plain membership Set)
    // so every existing solvedIds.has()/add()/delete() call site below still
    // works untouched — solveMeta only adds richer data on top.
    //   solveMeta[id] = {
    //     solvedAt: ISOString | null,           // when first marked solved
    //     attempts: [{ ts, seconds, outcome }],  // outcome: 'solved' | 'attempted'
    //     srs: { ease, interval, reps, due }     // spaced-repetition schedule (SM-2-ish)
    //   }
    solveMeta: {},
    theme: 'dark',
    activeFilter: 'all', // 'all' | 'unsolved' | 'solved' | 'neetcode' | 'blind75' | 'starred' | 'notes' | 'due'
    activeDiff: null, // null | 'Easy' | 'Medium' | 'Hard'
    activePatterns: new Set(), // pattern-tag filter, OR semantics
    searchQuery: '',
    searchAutoOpenedSteps: new Set(), // steps expanded BY search, not the user — see applyFilterAndSearch
    openSteps: new Set(['step-1', 'step-2', 'step-3']),
    currentModalProblemId: null,
    gcalTime: '20:00',
    gcalDuration: 120,
    focusedRowId: null, // keyboard-nav cursor (j/k/x/n) — see setupKeyboardNav
    timerStartedAt: null, // Date.now() while the note-modal stopwatch is running, else null
    timerElapsedSeconds: 0
  };

  // --- DOM Elements ---
  const DOM = {
    themeToggleBtn: document.getElementById('themeToggleBtn'),
    themeIcon: document.getElementById('themeIcon'),
    solvedCount: document.getElementById('solvedCount'),
    totalProblemsCount: document.getElementById('totalProblemsCount'),
    progressPercentageText: document.getElementById('progressPercentageText'),
    ringPercentage: document.getElementById('ringPercentage'),
    progressRingCircle: document.getElementById('progressRingCircle'),
    linearProgressBarFill: document.getElementById('linearProgressBarFill'),
    
    easyRatio: document.getElementById('easyRatio'),
    easyBar: document.getElementById('easyBar'),
    mediumRatio: document.getElementById('mediumRatio'),
    mediumBar: document.getElementById('mediumBar'),
    hardRatio: document.getElementById('hardRatio'),
    hardBar: document.getElementById('hardBar'),

    starredCount: document.getElementById('starredCount'),
    savedNotesCount: document.getElementById('savedNotesCount'),

    // Due / Pattern filters
    dueBadge: document.getElementById('dueBadge'),
    patternChipsContainer: document.getElementById('patternChipsContainer'),
    clearPatternsBtn: document.getElementById('clearPatternsBtn'),

    // Insights (streak, heatmap, weak areas)
    streakCount: document.getElementById('streakCount'),
    activityHeatmap: document.getElementById('activityHeatmap'),
    weakAreasList: document.getElementById('weakAreasList'),

    searchInput: document.getElementById('searchInput'),
    clearSearchBtn: document.getElementById('clearSearchBtn'),
    filterChips: document.querySelectorAll('.filter-chip:not(.diff-filter)'),
    diffFilterChips: document.querySelectorAll('.diff-filter'),
    expandAllBtn: document.getElementById('expandAllBtn'),
    randomBtn: document.getElementById('randomBtn'),

    stepsContainer: document.getElementById('stepsContainer'),
    emptyState: document.getElementById('emptyState'),
    resetFiltersBtn: document.getElementById('resetFiltersBtn'),

    // Global Resources Hub Modal
    globalResourcesBtn: document.getElementById('globalResourcesBtn'),
    resourceHubModal: document.getElementById('resourceHubModal'),
    closeResourceHubModalBtn: document.getElementById('closeResourceHubModalBtn'),
    resCatChips: document.querySelectorAll('.res-cat-chip'),
    resCards: document.querySelectorAll('.res-card'),

    // Calendar Modal
    calendarModalBtn: document.getElementById('calendarModalBtn'),
    calendarModal: document.getElementById('calendarModal'),
    closeCalendarModalBtn: document.getElementById('closeCalendarModalBtn'),
    gcalDailyTime: document.getElementById('gcalDailyTime'),
    gcalDuration: document.getElementById('gcalDuration'),
    gcalTargetTime: document.getElementById('gcalTargetTime'),
    scheduleDailyGcalBtn: document.getElementById('scheduleDailyGcalBtn'),
    scheduleTargetGcalBtn: document.getElementById('scheduleTargetGcalBtn'),
    exportIcsBtn: document.getElementById('exportIcsBtn'),
    presetChips: document.querySelectorAll('.preset-chip'),

    // Note Modal
    noteModal: document.getElementById('noteModal'),
    modalDiffBadge: document.getElementById('modalDiffBadge'),
    modalStepName: document.getElementById('modalStepName'),
    modalProblemTitle: document.getElementById('modalProblemTitle'),
    modalTimeComplexity: document.getElementById('modalTimeComplexity'),
    modalSpaceComplexity: document.getElementById('modalSpaceComplexity'),
    modalNotesText: document.getElementById('modalNotesText'),
    modalCodeSnippet: document.getElementById('modalCodeSnippet'),
    modalCodeLang: document.getElementById('modalCodeLang'),
    closeNoteModalBtn: document.getElementById('closeNoteModalBtn'),
    cancelNoteModalBtn: document.getElementById('cancelNoteModalBtn'),
    saveNoteModalBtn: document.getElementById('saveNoteModalBtn'),
    deleteNoteBtn: document.getElementById('deleteNoteBtn'),
    schedRev3dBtn: document.getElementById('schedRev3dBtn'),
    schedRev7dBtn: document.getElementById('schedRev7dBtn'),
    schedRevCustomBtn: document.getElementById('schedRevCustomBtn'),

    // Solve Timer & Attempt Log (inside Note Modal)
    timerDisplay: document.getElementById('timerDisplay'),
    timerStartStopBtn: document.getElementById('timerStartStopBtn'),
    logAttemptBtn: document.getElementById('logAttemptBtn'),
    attemptHistoryRow: document.getElementById('attemptHistoryRow'),

    // Spaced Repetition Review (inside Note Modal)
    srsButtons: document.querySelectorAll('.srs-btn'),
    srsDueLabel: document.getElementById('srsDueLabel'),

    // Backup Modal
    backupModalBtn: document.getElementById('backupModalBtn'),
    backupModal: document.getElementById('backupModal'),
    closeBackupModalBtn: document.getElementById('closeBackupModalBtn'),
    exportDataBtn: document.getElementById('exportDataBtn'),
    importDataBtn: document.getElementById('importDataBtn'),
    importFileInput: document.getElementById('importFileInput'),
    resetAllDataBtn: document.getElementById('resetAllDataBtn'),

    // Toast
    toast: document.getElementById('toastNotification'),
    toastMessage: document.getElementById('toastMessage')
  };

  // --- Flattened Problem Lookup Map ---
  const problemsMap = new Map();
  let allProblemsCount = 0;
  let easyCount = 0;
  let mediumCount = 0;
  let hardCount = 0;
  let allPatterns = []; // distinct prob.patterns values across the whole catalog, sorted

  function initProblemCatalog() {
    problemsMap.clear();
    allProblemsCount = 0;
    easyCount = 0;
    mediumCount = 0;
    hardCount = 0;
    const patternSet = new Set();

    DSA_DATA.forEach(step => {
      step.topics.forEach(topic => {
        topic.problems.forEach(prob => {
          problemsMap.set(prob.id, { ...prob, stepId: step.stepId, stepTitle: step.stepTitle, topicName: topic.subtopic });
          allProblemsCount++;
          if (prob.difficulty === 'Easy') easyCount++;
          else if (prob.difficulty === 'Medium') mediumCount++;
          else if (prob.difficulty === 'Hard') hardCount++;
          (prob.patterns || []).forEach(p => patternSet.add(p));
        });
      });
    });

    allPatterns = Array.from(patternSet).sort();
  }

  // --- Pattern label formatting (shared by chips + weak-areas panel) ---
  function formatPatternLabel(pattern) {
    return pattern.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  }

  // --- LocalStorage Persistence ---
  // Old (pre-rebuild) localStorage held plain integer problem ids. This
  // rebuild moved to stable string slugs (tools/build.py) so a data refresh
  // never renumbers anyone's progress again — but that means anyone who used
  // the tracker before this rebuild has solved/starred/notes keyed by ids
  // that no longer exist. ID_MIGRATION_MAP (id_migration.js) remaps every
  // old int id to its new slug; this runs once, then bumps SCHEMA_VERSION so
  // it never re-runs.
  function migrateLegacyIntIds() {
    const map = (typeof ID_MIGRATION_MAP !== 'undefined') ? ID_MIGRATION_MAP : {};
    const remap = (oldId) => map[String(oldId)] || String(oldId);

    try {
      const rawSolved = localStorage.getItem(STORAGE_KEYS.SOLVED_V1);
      if (rawSolved) {
        const oldIds = JSON.parse(rawSolved);
        if (Array.isArray(oldIds) && oldIds.some(id => typeof id === 'number')) {
          state.solvedIds = new Set(oldIds.map(remap));
          state.solvedIds.forEach(id => {
            state.solveMeta[id] = { solvedAt: null, attempts: [], srs: null };
          });
        }
      }
      const rawStarred = localStorage.getItem(STORAGE_KEYS.STARRED_V1);
      if (rawStarred) {
        const oldIds = JSON.parse(rawStarred);
        if (Array.isArray(oldIds) && oldIds.some(id => typeof id === 'number')) {
          state.starredIds = new Set(oldIds.map(remap));
        }
      }
      const rawNotes = localStorage.getItem(STORAGE_KEYS.NOTES_V1);
      if (rawNotes) {
        const oldNotes = JSON.parse(rawNotes);
        const looksLegacy = Object.keys(oldNotes).some(k => /^\d+$/.test(k));
        if (looksLegacy) {
          const remapped = {};
          Object.keys(oldNotes).forEach(oldId => { remapped[remap(oldId)] = oldNotes[oldId]; });
          state.notes = remapped;
        }
      }
    } catch (e) {
      console.error('Error migrating legacy integer-id progress:', e);
    }

    saveState('solved');
    saveState('starred');
    saveState('notes');
    saveState('solveMeta');
    localStorage.setItem(STORAGE_KEYS.SCHEMA_VERSION, String(CURRENT_SCHEMA_VERSION));
  }

  function loadStoredData() {
    try {
      const schemaVersion = parseInt(localStorage.getItem(STORAGE_KEYS.SCHEMA_VERSION) || '0', 10);

      const savedSolved = localStorage.getItem(STORAGE_KEYS.SOLVED);
      if (savedSolved) state.solvedIds = new Set(JSON.parse(savedSolved));

      const savedStarred = localStorage.getItem(STORAGE_KEYS.STARRED);
      if (savedStarred) state.starredIds = new Set(JSON.parse(savedStarred));

      const savedNotes = localStorage.getItem(STORAGE_KEYS.NOTES);
      if (savedNotes) state.notes = JSON.parse(savedNotes);

      const savedSolveMeta = localStorage.getItem(STORAGE_KEYS.SOLVE_META);
      if (savedSolveMeta) state.solveMeta = JSON.parse(savedSolveMeta);

      if (schemaVersion < CURRENT_SCHEMA_VERSION) {
        migrateLegacyIntIds();
      }

      const savedTheme = localStorage.getItem(STORAGE_KEYS.THEME);
      if (savedTheme) state.theme = savedTheme;

      const savedOpenSteps = localStorage.getItem(STORAGE_KEYS.OPEN_STEPS);
      if (savedOpenSteps) state.openSteps = new Set(JSON.parse(savedOpenSteps));

      const savedGcalTime = localStorage.getItem(STORAGE_KEYS.GCAL_TIME);
      if (savedGcalTime) {
        state.gcalTime = savedGcalTime;
        DOM.gcalDailyTime.value = savedGcalTime;
      }

      const savedGcalDuration = localStorage.getItem(STORAGE_KEYS.GCAL_DURATION);
      if (savedGcalDuration) {
        state.gcalDuration = parseInt(savedGcalDuration, 10);
        DOM.gcalDuration.value = savedGcalDuration;
      }
    } catch (e) {
      console.error('Error loading stored data from LocalStorage:', e);
    }
  }

  function saveState(key) {
    try {
      if (key === 'solved') {
        localStorage.setItem(STORAGE_KEYS.SOLVED, JSON.stringify(Array.from(state.solvedIds)));
      } else if (key === 'starred') {
        localStorage.setItem(STORAGE_KEYS.STARRED, JSON.stringify(Array.from(state.starredIds)));
      } else if (key === 'notes') {
        localStorage.setItem(STORAGE_KEYS.NOTES, JSON.stringify(state.notes));
      } else if (key === 'solveMeta') {
        localStorage.setItem(STORAGE_KEYS.SOLVE_META, JSON.stringify(state.solveMeta));
      } else if (key === 'theme') {
        localStorage.setItem(STORAGE_KEYS.THEME, state.theme);
      } else if (key === 'openSteps') {
        localStorage.setItem(STORAGE_KEYS.OPEN_STEPS, JSON.stringify(Array.from(state.openSteps)));
      } else if (key === 'gcal') {
        localStorage.setItem(STORAGE_KEYS.GCAL_TIME, state.gcalTime);
        localStorage.setItem(STORAGE_KEYS.GCAL_DURATION, state.gcalDuration.toString());
      }
    } catch (e) {
      console.error(`Error saving state for ${key}:`, e);
    }
  }

  // --- Spaced Repetition (simplified SM-2) ---
  // Not a full SM-2 implementation (no sub-day scheduling, no lapses table) —
  // just enough of the idea to space out revision instead of nagging on a
  // fixed +3/+7 day schedule regardless of how well you actually know it.
  const MS_PER_DAY = 24 * 60 * 60 * 1000;

  function todayISODate() {
    return new Date().toISOString().slice(0, 10);
  }

  function defaultSrs() {
    return { ease: 2.5, interval: 0, reps: 0, due: null };
  }

  function ensureSolveMeta(id) {
    if (!state.solveMeta[id]) state.solveMeta[id] = { solvedAt: null, attempts: [], srs: null };
    return state.solveMeta[id];
  }

  // grade: 'again' | 'hard' | 'good' | 'easy'
  function scheduleReview(id, grade) {
    const meta = ensureSolveMeta(id);
    const srs = meta.srs || defaultSrs();

    if (grade === 'again') {
      srs.interval = 1;
      srs.ease = Math.max(1.3, srs.ease - 0.2);
    } else if (grade === 'hard') {
      srs.interval = Math.max(1, Math.round((srs.interval || 1) * 1.2));
      srs.ease = Math.max(1.3, srs.ease - 0.15);
    } else if (grade === 'good') {
      srs.interval = srs.interval === 0 ? 1 : (srs.interval === 1 ? 3 : Math.round(srs.interval * srs.ease));
    } else if (grade === 'easy') {
      srs.interval = srs.interval === 0 ? 3 : Math.round(srs.interval * srs.ease * 1.3);
      srs.ease = srs.ease + 0.15;
    }
    srs.reps = (srs.reps || 0) + 1;
    const dueDate = new Date(Date.now() + srs.interval * MS_PER_DAY);
    srs.due = dueDate.toISOString().slice(0, 10);

    meta.srs = srs;
    saveState('solveMeta');
    return srs;
  }

  function isDueToday(id) {
    const srs = state.solveMeta[id] && state.solveMeta[id].srs;
    if (!srs || !srs.due) return false;
    return srs.due <= todayISODate();
  }

  function dueCountToday() {
    let n = 0;
    state.solvedIds.forEach(id => { if (isDueToday(id)) n++; });
    return n;
  }

  // --- Solve Timer (stopwatch inside the Note Modal) ---
  // timerInterval is deliberately NOT in `state` — it's a live handle, not
  // data, and would break JSON persistence if it ever got saved by mistake.
  let timerInterval = null;

  function formatSeconds(totalSeconds) {
    const s = Math.max(0, Math.floor(totalSeconds || 0));
    const m = Math.floor(s / 60);
    const rem = s % 60;
    return `${String(m).padStart(2, '0')}:${String(rem).padStart(2, '0')}`;
  }

  function currentTimerSeconds() {
    let elapsed = state.timerElapsedSeconds;
    if (state.timerStartedAt) elapsed += Math.floor((Date.now() - state.timerStartedAt) / 1000);
    return elapsed;
  }

  function renderTimerDisplay() {
    if (DOM.timerDisplay) DOM.timerDisplay.textContent = formatSeconds(currentTimerSeconds());
  }

  function setTimerButtonRunning(isRunning) {
    if (!DOM.timerStartStopBtn) return;
    DOM.timerStartStopBtn.innerHTML = isRunning
      ? '<i class="fa-solid fa-pause"></i> Pause'
      : '<i class="fa-solid fa-play"></i> Start';
    DOM.timerStartStopBtn.classList.toggle('timer-running', isRunning);
  }

  function toggleSolveTimer() {
    if (state.timerStartedAt) {
      // Stop: fold the running interval into the accumulated total.
      state.timerElapsedSeconds += Math.floor((Date.now() - state.timerStartedAt) / 1000);
      state.timerStartedAt = null;
      clearInterval(timerInterval);
      timerInterval = null;
      setTimerButtonRunning(false);
    } else {
      state.timerStartedAt = Date.now();
      timerInterval = setInterval(renderTimerDisplay, 1000);
      setTimerButtonRunning(true);
    }
    renderTimerDisplay();
  }

  function resetSolveTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
    state.timerStartedAt = null;
    state.timerElapsedSeconds = 0;
    setTimerButtonRunning(false);
    renderTimerDisplay();
  }

  function stopSolveTimerKeepElapsed() {
    // Used on modal close: stop ticking, but don't reset — resetSolveTimer()
    // runs the next time a (possibly different) problem's modal opens.
    if (state.timerStartedAt) {
      state.timerElapsedSeconds += Math.floor((Date.now() - state.timerStartedAt) / 1000);
      state.timerStartedAt = null;
    }
    clearInterval(timerInterval);
    timerInterval = null;
  }

  // --- Attempt Log ---
  function logAttempt() {
    const pid = state.currentModalProblemId;
    if (!pid) return;
    const meta = ensureSolveMeta(pid);
    meta.attempts.push({ ts: new Date().toISOString(), outcome: 'attempted', seconds: currentTimerSeconds() || null });
    saveState('solveMeta');
    renderAttemptHistory(pid);
    showToast('Attempt logged 🚩', 'fa-flag');
  }

  function renderAttemptHistory(problemId) {
    if (!DOM.attemptHistoryRow) return;
    const meta = state.solveMeta[problemId];
    const attempts = (meta && meta.attempts) || [];
    if (attempts.length === 0) {
      DOM.attemptHistoryRow.innerHTML = '';
      DOM.attemptHistoryRow.style.display = 'none';
      return;
    }
    DOM.attemptHistoryRow.style.display = 'flex';
    const recent = attempts.slice(-6).reverse();
    DOM.attemptHistoryRow.innerHTML = recent.map(a => {
      const dateStr = new Date(a.ts).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
      const timeStr = a.seconds != null ? ` · ${formatSeconds(a.seconds)}` : '';
      const icon = a.outcome === 'solved' ? 'fa-check' : 'fa-flag';
      return `<span class="attempt-pill attempt-${escapeAttr(a.outcome)}" title="${escapeAttr(a.ts)}"><i class="fa-solid ${icon}"></i> ${escapeHTML(dateStr)}${escapeHTML(timeStr)}</span>`;
    }).join('');
  }

  // --- SRS due-label (inside Note Modal) ---
  function updateSrsDueLabel(srs) {
    if (!DOM.srsDueLabel) return;
    DOM.srsDueLabel.textContent = (srs && srs.due) ? `Next review: ${srs.due}` : 'Not scheduled yet — grade it below';
  }

  // --- Weak-Areas Panel (first-attempt success rate, by pattern tag) ---
  function computeWeakAreas() {
    const stats = {}; // pattern -> { attempted, firstAttemptSuccess }
    Object.keys(state.solveMeta).forEach(id => {
      const meta = state.solveMeta[id];
      if (!meta.attempts || meta.attempts.length === 0) return;
      const prob = problemsMap.get(id);
      if (!prob || !prob.patterns || prob.patterns.length === 0) return;
      const firstAttemptSolved = meta.attempts[0].outcome === 'solved';
      prob.patterns.forEach(p => {
        if (!stats[p]) stats[p] = { attempted: 0, firstAttemptSuccess: 0 };
        stats[p].attempted++;
        if (firstAttemptSolved) stats[p].firstAttemptSuccess++;
      });
    });

    return Object.keys(stats)
      .map(p => ({ pattern: p, ...stats[p], rate: stats[p].firstAttemptSuccess / stats[p].attempted }))
      .filter(s => s.attempted >= 2) // need at least a couple data points to mean anything
      .sort((a, b) => a.rate - b.rate)
      .slice(0, 5);
  }

  function renderWeakAreas() {
    if (!DOM.weakAreasList) return;
    const weak = computeWeakAreas();
    if (weak.length === 0) {
      DOM.weakAreasList.innerHTML = '<p class="weak-areas-empty">Log a few attempts (via a problem\'s Note panel) to see this fill in.</p>';
      return;
    }
    DOM.weakAreasList.innerHTML = weak.map(w => `
      <div class="weak-area-row">
        <span class="weak-area-name">${escapeHTML(formatPatternLabel(w.pattern))}</span>
        <div class="weak-area-bar-track"><div class="weak-area-bar-fill" style="width:${Math.round(w.rate * 100)}%;"></div></div>
        <span class="weak-area-pct">${Math.round(w.rate * 100)}%</span>
      </div>
    `).join('');
  }

  // --- Streak & Activity Heatmap ---
  function solvedCountsByDate() {
    const counts = {};
    Object.values(state.solveMeta).forEach(meta => {
      (meta.attempts || []).forEach(a => {
        if (a.outcome === 'solved') {
          const day = a.ts.slice(0, 10);
          counts[day] = (counts[day] || 0) + 1;
        }
      });
    });
    return counts;
  }

  function computeStreak() {
    const counts = solvedCountsByDate();
    const cursor = new Date();
    cursor.setHours(0, 0, 0, 0);
    let cursorKey = cursor.toISOString().slice(0, 10);
    if (!counts[cursorKey]) {
      // No solve yet today — that's fine, don't break the streak until
      // yesterday also comes up empty.
      cursor.setDate(cursor.getDate() - 1);
      cursorKey = cursor.toISOString().slice(0, 10);
      if (!counts[cursorKey]) return 0;
    }
    let streak = 0;
    while (counts[cursorKey]) {
      streak++;
      cursor.setDate(cursor.getDate() - 1);
      cursorKey = cursor.toISOString().slice(0, 10);
    }
    return streak;
  }

  function renderActivityHeatmap() {
    if (!DOM.activityHeatmap) return;
    const counts = solvedCountsByDate();
    const totalDays = 18 * 7;
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const cells = [];
    for (let i = totalDays - 1; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const key = d.toISOString().slice(0, 10);
      const count = counts[key] || 0;
      let level = 0;
      if (count >= 4) level = 4;
      else if (count === 3) level = 3;
      else if (count === 2) level = 2;
      else if (count === 1) level = 1;
      cells.push(`<span class="heat-cell heat-level-${level}" title="${escapeAttr(key)}: ${count} solved"></span>`);
    }
    DOM.activityHeatmap.innerHTML = cells.join('');
  }

  function renderInsights() {
    if (DOM.streakCount) DOM.streakCount.textContent = computeStreak();
    renderActivityHeatmap();
    renderWeakAreas();
  }

  // --- Pattern Filter Chips ---
  function renderPatternChips() {
    if (!DOM.patternChipsContainer) return;
    DOM.patternChipsContainer.innerHTML = '';
    allPatterns.forEach(pattern => {
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'pattern-chip';
      chip.dataset.pattern = pattern;
      chip.textContent = formatPatternLabel(pattern);
      chip.addEventListener('click', () => {
        if (state.activePatterns.has(pattern)) {
          state.activePatterns.delete(pattern);
          chip.classList.remove('active');
        } else {
          state.activePatterns.add(pattern);
          chip.classList.add('active');
        }
        if (DOM.clearPatternsBtn) {
          DOM.clearPatternsBtn.style.display = state.activePatterns.size > 0 ? 'inline-flex' : 'none';
        }
        applyFilterAndSearch();
      });
      DOM.patternChipsContainer.appendChild(chip);
    });
  }

  // --- Theme Management ---
  function applyTheme(theme) {
    state.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    if (theme === 'light') {
      DOM.themeIcon.className = 'fa-solid fa-sun';
      DOM.themeIcon.style.color = '#f59e0b';
    } else {
      DOM.themeIcon.className = 'fa-solid fa-moon';
      DOM.themeIcon.style.color = '';
    }
    saveState('theme');
  }

  // --- Resource Hub Category Filter ---
  function applyResourceCategoryFilter(cat) {
    DOM.resourceHubModal.querySelectorAll('.res-card').forEach(card => {
      card.style.display = card.dataset.cat === cat ? 'flex' : 'none';
    });
  }

  // --- Toast Notifications ---
  let toastTimer = null;
  function showToast(message, iconClass = 'fa-check-circle') {
    clearTimeout(toastTimer);
    DOM.toastMessage.textContent = message;
    DOM.toast.querySelector('.toast-icon').className = `fa-solid ${iconClass} toast-icon`;
    DOM.toast.classList.add('show');
    toastTimer = setTimeout(() => {
      DOM.toast.classList.remove('show');
    }, 2800);
  }

  // --- Analytics & Statistics Updates ---
  function updateDashboardStats() {
    const solvedTotal = state.solvedIds.size;
    DOM.solvedCount.textContent = solvedTotal;
    DOM.totalProblemsCount.textContent = allProblemsCount;

    const percentage = allProblemsCount > 0 ? Math.round((solvedTotal / allProblemsCount) * 100) : 0;
    DOM.progressPercentageText.textContent = `${percentage}% completed`;
    DOM.ringPercentage.textContent = `${percentage}%`;
    DOM.linearProgressBarFill.style.width = `${percentage}%`;

    const circumference = 251.2;
    const strokeDashoffset = circumference - (percentage / 100) * circumference;
    DOM.progressRingCircle.style.strokeDashoffset = strokeDashoffset;

    let easySolved = 0;
    let medSolved = 0;
    let hardSolved = 0;

    state.solvedIds.forEach(id => {
      const prob = problemsMap.get(id);
      if (prob) {
        if (prob.difficulty === 'Easy') easySolved++;
        else if (prob.difficulty === 'Medium') medSolved++;
        else if (prob.difficulty === 'Hard') hardSolved++;
      }
    });

    DOM.easyRatio.textContent = `${easySolved} / ${easyCount}`;
    DOM.easyBar.style.width = easyCount > 0 ? `${(easySolved / easyCount) * 100}%` : '0%';

    DOM.mediumRatio.textContent = `${medSolved} / ${mediumCount}`;
    DOM.mediumBar.style.width = mediumCount > 0 ? `${(medSolved / mediumCount) * 100}%` : '0%';

    DOM.hardRatio.textContent = `${hardSolved} / ${hardCount}`;
    DOM.hardBar.style.width = hardCount > 0 ? `${(hardSolved / hardCount) * 100}%` : '0%';

    DOM.starredCount.textContent = state.starredIds.size;
    DOM.savedNotesCount.textContent = Object.keys(state.notes).length;

    if (DOM.dueBadge) {
      const due = dueCountToday();
      DOM.dueBadge.textContent = due;
      DOM.dueBadge.style.display = due > 0 ? 'inline-flex' : 'none';
    }
  }

  // --- Step Header Progress Bar Update ---
  function updateStepCardProgress(stepCard, stepData) {
    let stepTotal = 0;
    let stepSolved = 0;

    stepData.topics.forEach(topic => {
      topic.problems.forEach(p => {
        stepTotal++;
        if (state.solvedIds.has(p.id)) stepSolved++;
      });
    });

    const ratioElem = stepCard.querySelector('.step-ratio');
    const fillElem = stepCard.querySelector('.step-progress-fill');
    
    if (ratioElem) ratioElem.textContent = `${stepSolved} / ${stepTotal}`;
    if (fillElem) fillElem.style.width = stepTotal > 0 ? `${(stepSolved / stepTotal) * 100}%` : '0%';

    if (stepTotal > 0 && stepSolved === stepTotal) {
      stepCard.classList.add('completed');
    } else {
      stepCard.classList.remove('completed');
    }
  }

  // --- Google Calendar Integration Helpers ---
  function formatGCalDate(date) {
    return date.toISOString().replace(/-|:|\.\d+/g, '');
  }

  function openGoogleCalendarEvent({ title, details, location, startDate, endDate, isDailyRecurring }) {
    const startStr = formatGCalDate(startDate);
    const endStr = formatGCalDate(endDate);

    let url = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${encodeURIComponent(title)}&dates=${startStr}/${endStr}&details=${encodeURIComponent(details)}`;
    if (location) {
      url += `&location=${encodeURIComponent(location)}`;
    }
    if (isDailyRecurring) {
      url += `&recur=RRULE:FREQ=DAILY`;
    }

    window.open(url, '_blank');
  }

  function scheduleDailyDSAStudy() {
    const timeVal = DOM.gcalDailyTime.value || '20:00';
    const durationMinutes = parseInt(DOM.gcalDuration.value || '120', 10);
    const [hours, minutes] = timeVal.split(':').map(Number);

    state.gcalTime = timeVal;
    state.gcalDuration = durationMinutes;
    saveState('gcal');

    const now = new Date();
    const startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hours, minutes, 0);
    // If today's slot has already passed, the first occurrence of a "daily"
    // event should still be in the future — start it tomorrow instead.
    if (startDate.getTime() <= now.getTime()) {
      startDate.setDate(startDate.getDate() + 1);
    }
    const endDate = new Date(startDate.getTime() + durationMinutes * 60 * 1000);

    const solvedCount = state.solvedIds.size;
    const details = `🔥 Daily DSA & Quant Practice Session (${durationMinutes} mins)\n\nOverall Progress: ${solvedCount}/${allProblemsCount} solved.\nOpen your A2Z DSA Vault tracker (double-click LaunchDSAVault, or open index.html).\n\nDaily Goals:\n- Solve 2-3 Problems (Striver & NeetCode 150)\n- Review Quant / Market applications\n- Record time & space complexity notes`;

    openGoogleCalendarEvent({
      title: `💻 Daily DSA Practice (${timeVal})`,
      details: details,
      startDate: startDate,
      endDate: endDate,
      isDailyRecurring: true
    });

    showToast(`Opening Google Calendar: ${timeVal} (${durationMinutes} mins daily)! 📅`, 'fa-calendar-check');
  }

  function scheduleTargetSession() {
    const targetVal = DOM.gcalTargetTime.value;
    let startDate;
    if (targetVal) {
      startDate = new Date(targetVal);
    } else {
      startDate = new Date();
      startDate.setDate(startDate.getDate() + 1);
      startDate.setHours(20, 0, 0, 0);
    }

    const durationMinutes = parseInt(DOM.gcalDuration.value || '120', 10);
    const endDate = new Date(startDate.getTime() + durationMinutes * 60 * 1000);
    const details = `🎯 Targeted DSA Sprint\n\nOpen your A2Z DSA Vault tracker and complete pending Striver & NeetCode problems!`;

    openGoogleCalendarEvent({
      title: '🎯 Target DSA Practice Block',
      details: details,
      startDate: startDate,
      endDate: endDate,
      isDailyRecurring: false
    });

    showToast('Opening Google Calendar for Target Session! 📅', 'fa-calendar-check');
  }

  function scheduleProblemRevisionGcal(daysAhead = 3) {
    const pid = state.currentModalProblemId;
    if (!pid) return;
    const prob = problemsMap.get(pid);
    if (!prob) return;

    const existing = state.notes[pid] || {};
    const [hours, minutes] = (state.gcalTime || '20:00').split(':').map(Number);
    const targetDate = new Date();
    targetDate.setDate(targetDate.getDate() + daysAhead);
    targetDate.setHours(hours, minutes, 0, 0);
    const endDate = new Date(targetDate.getTime() + 45 * 60 * 1000); // 45 mins

    let details = `🔁 Spaced Repetition Revision for: ${prob.title}\nDifficulty: ${prob.difficulty}\nTopic: ${prob.topicName}\n\n`;
    if (prob.link) details += `Problem Link: ${prob.link}\n`;
    if (prob.youtube) details += `Video Tutorial: ${prob.youtube}\n`;
    if (existing.notes) details += `\nYour Personal Intuition Notes:\n${existing.notes}\n`;
    if (existing.timeComplexity) details += `Target Time Complexity: ${existing.timeComplexity}\n`;

    openGoogleCalendarEvent({
      title: `🔁 Revise DSA: ${prob.title} (${prob.difficulty})`,
      details: details,
      location: prob.link || undefined,
      startDate: targetDate,
      endDate: endDate,
      isDailyRecurring: false
    });

    showToast(`Google Calendar reminder created for +${daysAhead} days! 📅`, 'fa-calendar-plus');
  }

  function exportICSFile() {
    const timeVal = DOM.gcalDailyTime.value || '20:00';
    const durationMinutes = parseInt(DOM.gcalDuration.value || '120', 10);
    const [hours, minutes] = timeVal.split(':').map(Number);

    const now = new Date();
    const startDate = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hours, minutes, 0);
    if (startDate.getTime() <= now.getTime()) {
      startDate.setDate(startDate.getDate() + 1);
    }
    const endDate = new Date(startDate.getTime() + durationMinutes * 60 * 1000);

    const icsContent = [
      'BEGIN:VCALENDAR',
      'VERSION:2.0',
      'PRODID:-//A2Z DSA Vault//Study Schedule//EN',
      'CALSCALE:GREGORIAN',
      'BEGIN:VEVENT',
      'SUMMARY:Daily DSA & Quant Practice Session',
      `DESCRIPTION:Daily coding session for Striver A2Z + NeetCode 150 (${durationMinutes} mins). Open your A2Z DSA Vault tracker.`,
      'RRULE:FREQ=DAILY',
      `DTSTART:${formatGCalDate(startDate)}`,
      `DTEND:${formatGCalDate(endDate)}`,
      'STATUS:CONFIRMED',
      'END:VEVENT',
      'END:VCALENDAR'
    ].join('\r\n');

    const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.setAttribute('download', 'DSA_Study_Plan.ics');
    document.body.appendChild(link);
    link.click();
    link.remove();
    showToast('Exported DSA_Study_Plan.ics! 📅', 'fa-file-arrow-down');
  }

  // --- Render Entire Problem Structure with Multi-Source Global Badges & NeetCode Tags ---
  function renderAllSteps() {
    DOM.stepsContainer.innerHTML = '';

    DSA_DATA.forEach(step => {
      const stepCard = document.createElement('div');
      stepCard.className = `step-card ${state.openSteps.has(step.stepId) ? 'open' : ''}`;
      stepCard.id = `card-${step.stepId}`;
      stepCard.dataset.stepId = step.stepId;

      let stepTotal = 0;
      let stepSolved = 0;
      step.topics.forEach(t => t.problems.forEach(p => {
        stepTotal++;
        if (state.solvedIds.has(p.id)) stepSolved++;
      }));

      // Step Header
      const header = document.createElement('div');
      header.className = 'step-header';
      header.innerHTML = `
        <div class="step-info">
          <i class="fa-solid fa-chevron-right step-chevron"></i>
          <div>
            <div class="step-title-text">${escapeHTML(step.stepTitle)}</div>
            <div class="step-desc">${escapeHTML(step.description)}</div>
          </div>
        </div>
        <div class="step-meta">
          <div class="step-progress-wrapper">
            <div class="step-progress-bar">
              <div class="step-progress-fill" style="width: ${stepTotal > 0 ? (stepSolved / stepTotal) * 100 : 0}%;"></div>
            </div>
            <span class="step-ratio">${stepSolved} / ${stepTotal}</span>
          </div>
        </div>
      `;

      header.addEventListener('click', () => {
        const isOpen = stepCard.classList.toggle('open');
        if (isOpen) {
          state.openSteps.add(step.stepId);
        } else {
          state.openSteps.delete(step.stepId);
        }
        saveState('openSteps');
      });

      // Step Content
      const content = document.createElement('div');
      content.className = 'step-content';

      // Step-level resources (citations that were originally stamped onto
      // every problem in the step — lifted here once by tools/build.py
      // instead of repeating the same "source" badge on every row).
      if (step.resources && step.resources.length) {
        const resBar = document.createElement('div');
        resBar.className = 'step-resources-bar';
        resBar.innerHTML = `<span class="step-resources-label"><i class="fa-solid fa-link"></i> Step Resources:</span>` +
          step.resources.map(r => `<a href="${escapeAttr(r.url)}" target="_blank" rel="noopener noreferrer" class="step-resource-link">${escapeHTML(r.source)}</a>`).join('');
        content.appendChild(resBar);
      }

      step.topics.forEach(topic => {
        const subtopicDiv = document.createElement('div');
        subtopicDiv.className = 'subtopic-section';
        subtopicDiv.innerHTML = `<div class="subtopic-title"><i class="fa-regular fa-folder-open"></i> ${escapeHTML(topic.subtopic)}</div>`;

        const problemsList = document.createElement('div');
        problemsList.className = 'problems-list';

        topic.problems.forEach(prob => {
          const isSolved = state.solvedIds.has(prob.id);
          const isStarred = state.starredIds.has(prob.id);
          const hasNote = Boolean(state.notes[prob.id]);
          const isNeetCode = Boolean(prob.isNeetCode);
          const isBlind75 = Boolean(prob.isBlind75);

          const row = document.createElement('div');
          row.className = `problem-row ${isSolved ? 'solved' : ''}`;
          row.id = `prob-row-${prob.id}`;
          row.dataset.probId = prob.id;
          row.dataset.diff = prob.difficulty;
          row.dataset.title = prob.title.toLowerCase();
          row.dataset.topic = topic.subtopic.toLowerCase();
          row.dataset.step = step.stepTitle.toLowerCase();
          row.dataset.stepId = step.stepId;
          row.dataset.isNeetcode = isNeetCode ? 'true' : 'false';
          row.dataset.isBlind75 = isBlind75 ? 'true' : 'false';
          row.dataset.patterns = (prob.patterns || []).join(',');
          row.dataset.due = isDueToday(prob.id) ? 'true' : 'false';

          // Construct Syllabus Tags (NeetCode 150, Blind 75)
          let tagsHtml = '';
          if (isBlind75) {
            tagsHtml += `<span class="blind75-tag" title="Part of the legendary Blind 75 List"><i class="fa-solid fa-fire"></i> Blind 75</span>`;
          } else if (isNeetCode) {
            tagsHtml += `<span class="neetcode-tag" title="Part of NeetCode 150 Curated List"><i class="fa-solid fa-bolt"></i> NeetCode 150</span>`;
          }

          // Construct Multi-Source Badges (TUF, NeetCode, Abdul Bari, MIT, USACO, Article, LeetCode)
          let mediaBadgesHtml = '';
          if (prob.youtube) {
            mediaBadgesHtml += `<a href="${escapeAttr(prob.youtube)}" target="_blank" rel="noopener noreferrer" class="media-badge media-badge-yt" title="Striver Full Whiteboard Lecture"><i class="fa-brands fa-youtube"></i> TUF</a>`;
          }
          if (prob.neetcode) {
            mediaBadgesHtml += `<a href="${escapeAttr(prob.neetcode)}" target="_blank" rel="noopener noreferrer" class="media-badge media-badge-neetcode" title="NeetCode Visual Breakdown"><i class="fa-solid fa-play"></i> NeetCode</a>`;
          }
          if (prob.abdul_bari) {
            mediaBadgesHtml += `<a href="${escapeAttr(prob.abdul_bari)}" target="_blank" rel="noopener noreferrer" class="media-badge media-badge-bari" title="Abdul Bari Algorithm Theory & Proofs"><i class="fa-solid fa-chalkboard-user"></i> Abdul Bari</a>`;
          }
          if (prob.mit) {
            mediaBadgesHtml += `<a href="${escapeAttr(prob.mit)}" target="_blank" rel="noopener noreferrer" class="media-badge media-badge-mit" title="MIT OpenCourseWare Lecture"><i class="fa-solid fa-building-columns"></i> MIT</a>`;
          }
          if (prob.usaco) {
            mediaBadgesHtml += `<a href="${escapeAttr(prob.usaco)}" target="_blank" rel="noopener noreferrer" class="media-badge media-badge-usaco" title="USACO Guide C++ Olympiad Guide"><i class="fa-solid fa-award"></i> USACO</a>`;
          }
          if (prob.article) {
            mediaBadgesHtml += `<a href="${escapeAttr(prob.article)}" target="_blank" rel="noopener noreferrer" class="media-badge media-badge-article" title="Read Editorial Article"><i class="fa-regular fa-newspaper"></i> Article</a>`;
          }
          if (prob.leetcode) {
            mediaBadgesHtml += `<a href="${escapeAttr(prob.leetcode)}" target="_blank" rel="noopener noreferrer" class="media-badge media-badge-lc" title="Practice on LeetCode"><i class="fa-solid fa-code"></i> LeetCode</a>`;
          }

          row.innerHTML = `
            <div class="problem-left">
              <input type="checkbox" class="problem-checkbox" ${isSolved ? 'checked' : ''} title="Mark as solved" aria-label="Mark ${escapeHTML(prob.title)} as solved">
              <button class="star-btn ${isStarred ? 'active' : ''}" title="Bookmark for revision" aria-label="Bookmark ${escapeHTML(prob.title)}">
                <i class="${isStarred ? 'fa-solid' : 'fa-regular'} fa-star"></i>
              </button>
              <a href="${escapeAttr(prob.link)}" target="_blank" rel="noopener noreferrer" class="problem-title-link" title="Open resource">
                ${escapeHTML(prob.title)}
              </a>
              ${tagsHtml}
            </div>
            
            <div class="problem-media-links">
              ${mediaBadgesHtml}
            </div>

            <div class="problem-right">
              <span class="diff-badge ${prob.difficulty}">${prob.difficulty}</span>
              <button class="note-btn ${hasNote ? 'has-note' : ''}" title="Add or view personal solution & notes">
                <i class="fa-solid ${hasNote ? 'fa-file-lines' : 'fa-pen'}"></i>
                <span>${hasNote ? 'Notes' : 'Note'}</span>
              </button>
            </div>
          `;

          // Event: Toggle Solved Checkbox
          const checkbox = row.querySelector('.problem-checkbox');
          checkbox.addEventListener('change', (e) => {
            if (e.target.checked) {
              state.solvedIds.add(prob.id);
              row.classList.add('solved');
              showToast(`Solved: "${prob.title}"! 🎉`, 'fa-check');

              const meta = ensureSolveMeta(prob.id);
              if (!meta.solvedAt) meta.solvedAt = new Date().toISOString();
              meta.attempts.push({ ts: new Date().toISOString(), outcome: 'solved', seconds: null });
              if (!meta.srs) meta.srs = defaultSrs();
              // Kick off the revision schedule as soon as it's solved once —
              // "Good" starting point (due in ~1 day), refined from there by
              // the Again/Hard/Good/Easy buttons in the note modal.
              if (!meta.srs.due) scheduleReview(prob.id, 'good');
              saveState('solveMeta');
            } else {
              state.solvedIds.delete(prob.id);
              row.classList.remove('solved');
            }
            saveState('solved');
            row.dataset.due = isDueToday(prob.id) ? 'true' : 'false';
            updateDashboardStats();
            updateStepCardProgress(stepCard, step);
            applyFilterAndSearch();
            renderInsights();
          });

          // Event: Toggle Star/Revision
          const starBtn = row.querySelector('.star-btn');
          starBtn.addEventListener('click', () => {
            if (state.starredIds.has(prob.id)) {
              state.starredIds.delete(prob.id);
              starBtn.classList.remove('active');
              starBtn.querySelector('i').className = 'fa-regular fa-star';
              showToast('Removed from revision list');
            } else {
              state.starredIds.add(prob.id);
              starBtn.classList.add('active');
              starBtn.querySelector('i').className = 'fa-solid fa-star';
              showToast('Bookmarked for revision ⭐', 'fa-star');
            }
            saveState('starred');
            updateDashboardStats();
            applyFilterAndSearch();
          });

          // Event: Open Note Modal
          const noteBtn = row.querySelector('.note-btn');
          noteBtn.addEventListener('click', () => {
            openNoteModal(prob.id);
          });

          problemsList.appendChild(row);
        });

        subtopicDiv.appendChild(problemsList);
        content.appendChild(subtopicDiv);
      });

      stepCard.appendChild(header);
      stepCard.appendChild(content);
      DOM.stepsContainer.appendChild(stepCard);

      updateStepCardProgress(stepCard, step);
    });
  }

  // --- Note Modal Handling ---
  function openNoteModal(problemId) {
    const prob = problemsMap.get(problemId);
    if (!prob) return;

    state.currentModalProblemId = problemId;
    const existing = state.notes[problemId] || {};

    DOM.modalProblemTitle.textContent = prob.title;
    DOM.modalStepName.textContent = prob.stepTitle.split(':')[0];
    DOM.modalDiffBadge.textContent = prob.difficulty;
    DOM.modalDiffBadge.className = `diff-badge ${prob.difficulty}`;
    
    // Setup modal external links with multi-source coverage
    const linksRow = document.getElementById('modalLinksRow');
    if (linksRow) {
      let linksHtml = '';
      if (prob.leetcode) {
        linksHtml += `<a href="${escapeAttr(prob.leetcode)}" target="_blank" rel="noopener noreferrer" class="link-btn media-badge-lc"><i class="fa-solid fa-code"></i> LeetCode</a>`;
      }
      if (prob.youtube) {
        linksHtml += `<a href="${escapeAttr(prob.youtube)}" target="_blank" rel="noopener noreferrer" class="link-btn media-badge-yt"><i class="fa-brands fa-youtube"></i> Striver / TUF</a>`;
      }
      if (prob.neetcode) {
        linksHtml += `<a href="${escapeAttr(prob.neetcode)}" target="_blank" rel="noopener noreferrer" class="link-btn media-badge-neetcode"><i class="fa-solid fa-play"></i> NeetCode</a>`;
      }
      if (prob.abdul_bari) {
        linksHtml += `<a href="${escapeAttr(prob.abdul_bari)}" target="_blank" rel="noopener noreferrer" class="link-btn media-badge-bari"><i class="fa-solid fa-chalkboard-user"></i> Abdul Bari Theory</a>`;
      }
      if (prob.mit) {
        linksHtml += `<a href="${escapeAttr(prob.mit)}" target="_blank" rel="noopener noreferrer" class="link-btn media-badge-mit"><i class="fa-solid fa-building-columns"></i> MIT OpenCourseWare</a>`;
      }
      if (prob.usaco) {
        linksHtml += `<a href="${escapeAttr(prob.usaco)}" target="_blank" rel="noopener noreferrer" class="link-btn media-badge-usaco"><i class="fa-solid fa-award"></i> USACO Guide</a>`;
      }
      if (prob.article) {
        linksHtml += `<a href="${escapeAttr(prob.article)}" target="_blank" rel="noopener noreferrer" class="link-btn media-badge-article"><i class="fa-regular fa-newspaper"></i> Editorial Article</a>`;
      }
      linksRow.innerHTML = linksHtml;
    }

    DOM.modalTimeComplexity.value = existing.timeComplexity || '';
    DOM.modalSpaceComplexity.value = existing.spaceComplexity || '';
    DOM.modalNotesText.value = existing.notes || '';
    DOM.modalCodeSnippet.value = existing.code || '';
    DOM.modalCodeLang.value = existing.lang || 'cpp';

    if (existing.notes || existing.code || existing.timeComplexity || existing.spaceComplexity) {
      DOM.deleteNoteBtn.style.display = 'inline-flex';
    } else {
      DOM.deleteNoteBtn.style.display = 'none';
    }

    // Solve Timer & Attempt Log / SRS review state, scoped to this problem
    resetSolveTimer();
    renderAttemptHistory(problemId);
    const meta = state.solveMeta[problemId];
    updateSrsDueLabel(meta && meta.srs);

    DOM.noteModal.classList.add('active');
    DOM.noteModal.setAttribute('aria-hidden', 'false');
  }

  function closeNoteModal() {
    DOM.noteModal.classList.remove('active');
    DOM.noteModal.setAttribute('aria-hidden', 'true');
    state.currentModalProblemId = null;
    stopSolveTimerKeepElapsed();
  }

  function saveCurrentNote() {
    const pid = state.currentModalProblemId;
    if (!pid) return;

    const notes = DOM.modalNotesText.value.trim();
    const code = DOM.modalCodeSnippet.value.trim();
    const timeComplexity = DOM.modalTimeComplexity.value.trim();
    const spaceComplexity = DOM.modalSpaceComplexity.value.trim();
    const lang = DOM.modalCodeLang.value;

    if (!notes && !code && !timeComplexity && !spaceComplexity) {
      delete state.notes[pid];
    } else {
      state.notes[pid] = {
        notes,
        code,
        timeComplexity,
        spaceComplexity,
        lang,
        updatedAt: new Date().toISOString()
      };
    }

    saveState('notes');
    updateDashboardStats();
    
    const row = document.getElementById(`prob-row-${pid}`);
    if (row) {
      const noteBtn = row.querySelector('.note-btn');
      const hasNote = Boolean(state.notes[pid]);
      noteBtn.className = `note-btn ${hasNote ? 'has-note' : ''}`;
      noteBtn.querySelector('i').className = `fa-solid ${hasNote ? 'fa-file-lines' : 'fa-pen'}`;
      noteBtn.querySelector('span').textContent = hasNote ? 'Notes' : 'Note';
    }

    showToast('Solution notes saved! 💾', 'fa-floppy-disk');
    closeNoteModal();
    applyFilterAndSearch();
  }

  function deleteCurrentNote() {
    const pid = state.currentModalProblemId;
    if (!pid || !state.notes[pid]) return;

    if (confirm('Are you sure you want to delete your notes for this problem?')) {
      delete state.notes[pid];
      saveState('notes');
      updateDashboardStats();

      const row = document.getElementById(`prob-row-${pid}`);
      if (row) {
        const noteBtn = row.querySelector('.note-btn');
        noteBtn.className = 'note-btn';
        noteBtn.querySelector('i').className = 'fa-solid fa-pen';
        noteBtn.querySelector('span').textContent = 'Note';
      }

      showToast('Note deleted', 'fa-trash');
      closeNoteModal();
      applyFilterAndSearch();
    }
  }

  // --- Search & Filter Logic ---
  function applyFilterAndSearch() {
    const q = state.searchQuery.toLowerCase();
    const filter = state.activeFilter;
    const diff = state.activeDiff;
    const patterns = state.activePatterns; // Set, OR semantics — matches ANY selected pattern

    let visibleProblemCount = 0;

    DSA_DATA.forEach(step => {
      const stepCard = document.getElementById(`card-${step.stepId}`);
      if (!stepCard) return;

      let stepVisibleProblems = 0;

      const subtopics = stepCard.querySelectorAll('.subtopic-section');
      subtopics.forEach(subSec => {
        let subtopicVisibleCount = 0;
        const problemRows = subSec.querySelectorAll('.problem-row');

        problemRows.forEach(row => {
          const pid = row.dataset.probId;
          const isSolved = state.solvedIds.has(pid);
          const isStarred = state.starredIds.has(pid);
          const hasNote = Boolean(state.notes[pid]);
          const isNeetCode = row.dataset.isNeetcode === 'true';
          const isBlind75 = row.dataset.isBlind75 === 'true';
          const pDiff = row.dataset.diff;
          const pTitle = row.dataset.title;
          const pTopic = row.dataset.topic;
          const pStep = row.dataset.step;
          const pPatterns = row.dataset.patterns ? row.dataset.patterns.split(',') : [];

          let matchesFilter = true;
          if (filter === 'unsolved' && isSolved) matchesFilter = false;
          if (filter === 'solved' && !isSolved) matchesFilter = false;
          if (filter === 'starred' && !isStarred) matchesFilter = false;
          if (filter === 'notes' && !hasNote) matchesFilter = false;
          if (filter === 'neetcode' && !isNeetCode) matchesFilter = false;
          if (filter === 'blind75' && !isBlind75) matchesFilter = false;
          if (filter === 'corecs' && row.dataset.stepId !== 'step-22') matchesFilter = false;
          if (filter === 'due' && !(isSolved && isDueToday(pid))) matchesFilter = false;

          let matchesDiff = true;
          if (diff && pDiff !== diff) matchesDiff = false;

          let matchesPatterns = true;
          if (patterns.size > 0) {
            matchesPatterns = pPatterns.some(p => patterns.has(p));
          }

          let matchesSearch = true;
          if (q) {
            matchesSearch = pTitle.includes(q) || pTopic.includes(q) || pStep.includes(q);
          }

          if (matchesFilter && matchesDiff && matchesPatterns && matchesSearch) {
            row.style.display = 'flex';
            subtopicVisibleCount++;
            stepVisibleProblems++;
            visibleProblemCount++;
          } else {
            row.style.display = 'none';
          }
        });

        subSec.style.display = subtopicVisibleCount > 0 ? 'block' : 'none';
      });

      stepCard.style.display = stepVisibleProblems > 0 ? 'block' : 'none';

      // Auto-expand a step while it has search matches, but track that this
      // was search's doing (searchAutoOpenedSteps) rather than the user's,
      // so clearing the search can restore exactly the pre-search open/closed
      // state instead of leaving every matched step permanently expanded.
      if (q) {
        if (stepVisibleProblems > 0) {
          if (!stepCard.classList.contains('open')) {
            stepCard.classList.add('open');
            state.searchAutoOpenedSteps.add(step.stepId);
          }
        }
      } else if (state.searchAutoOpenedSteps.size > 0) {
        if (state.searchAutoOpenedSteps.has(step.stepId) && !state.openSteps.has(step.stepId)) {
          stepCard.classList.remove('open');
        }
        state.searchAutoOpenedSteps.delete(step.stepId);
      }
    });

    DOM.emptyState.style.display = visibleProblemCount === 0 ? 'block' : 'none';
  }

  // --- Random Unsolved Problem Generator ---
  function pickRandomUnsolved() {
    const unsolvedList = [];
    problemsMap.forEach(prob => {
      if (!state.solvedIds.has(prob.id)) {
        unsolvedList.push(prob);
      }
    });

    if (unsolvedList.length === 0) {
      showToast('Incredible! You have solved all problems! 🏆', 'fa-trophy');
      return;
    }

    const randomProb = unsolvedList[Math.floor(Math.random() * unsolvedList.length)];
    
    state.searchQuery = '';
    state.activeFilter = 'all';
    state.activeDiff = null;
    DOM.searchInput.value = '';
    DOM.clearSearchBtn.style.display = 'none';
    DOM.filterChips.forEach(c => c.classList.toggle('active', c.dataset.filter === 'all'));
    DOM.diffFilterChips.forEach(c => c.classList.remove('active'));
    applyFilterAndSearch();

    const targetStep = document.getElementById(`card-${randomProb.stepId}`);
    if (targetStep) {
      targetStep.classList.add('open');
      state.openSteps.add(randomProb.stepId);
      saveState('openSteps');
    }

    const targetRow = document.getElementById(`prob-row-${randomProb.id}`);
    if (targetRow) {
      targetRow.scrollIntoView({ behavior: 'smooth', block: 'center' });
      targetRow.style.boxShadow = '0 0 0 3px #6366f1';
      targetRow.style.transition = 'box-shadow 0.3s ease';
      setTimeout(() => {
        targetRow.style.boxShadow = '';
      }, 2500);
      showToast(`Selected: ${randomProb.title} (${randomProb.difficulty})`, 'fa-shuffle');
    }
  }

  // --- Keyboard Navigation (j/k move cursor, x toggle solved, n open note) ---
  function getVisibleRows() {
    return Array.from(document.querySelectorAll('.problem-row')).filter(r => r.style.display !== 'none');
  }

  function focusRow(row) {
    const prev = document.querySelector('.problem-row.kb-focused');
    if (prev) prev.classList.remove('kb-focused');
    if (row) {
      row.classList.add('kb-focused');
      state.focusedRowId = row.dataset.probId;
      row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  function moveFocus(delta) {
    const rows = getVisibleRows();
    if (rows.length === 0) return;
    let idx = rows.findIndex(r => r.dataset.probId === state.focusedRowId);
    idx = idx === -1 ? (delta > 0 ? 0 : rows.length - 1) : Math.min(rows.length - 1, Math.max(0, idx + delta));
    focusRow(rows[idx]);
  }

  function anyModalOpen() {
    return DOM.noteModal.classList.contains('active') ||
      DOM.backupModal.classList.contains('active') ||
      DOM.calendarModal.classList.contains('active') ||
      DOM.resourceHubModal.classList.contains('active');
  }

  // --- Export & Import Backup (JSON) ---
  function exportData() {
    const backupObj = {
      version: '2.0',
      subject: 'A2Z DSA & Quant Vault',
      exportedAt: new Date().toISOString(),
      solvedIds: Array.from(state.solvedIds),
      starredIds: Array.from(state.starredIds),
      notes: state.notes,
      solveMeta: state.solveMeta
    };

    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(backupObj, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `dsa_vault_backup_${new Date().toISOString().slice(0, 10)}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();

    showToast('Backup JSON exported successfully! 📁', 'fa-download');
  }

  function importData(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (event) {
      try {
        const parsed = JSON.parse(event.target.result);
        if (parsed.solvedIds && Array.isArray(parsed.solvedIds)) {
          state.solvedIds = new Set(parsed.solvedIds);
        }
        if (parsed.starredIds && Array.isArray(parsed.starredIds)) {
          state.starredIds = new Set(parsed.starredIds);
        }
        if (parsed.notes && typeof parsed.notes === 'object') {
          state.notes = parsed.notes;
        }
        // solveMeta (timers/attempts/SRS schedule) only exists in v2.0+
        // backups — older exports simply won't restore review history,
        // which is fine, just don't crash trying to read it.
        if (parsed.solveMeta && typeof parsed.solveMeta === 'object') {
          state.solveMeta = parsed.solveMeta;
        }

        saveState('solved');
        saveState('starred');
        saveState('notes');
        saveState('solveMeta');

        renderAllSteps();
        updateDashboardStats();
        applyFilterAndSearch();
        renderInsights();

        DOM.backupModal.classList.remove('active');
        showToast('Backup imported successfully! 🚀', 'fa-check');
      } catch (err) {
        alert('Invalid JSON backup file format.');
        console.error(err);
      }
    };
    reader.readAsText(file);
    e.target.value = '';
  }

  function resetAllData() {
    if (confirm('CAUTION: This will erase all your solved markers, revision stars, and custom notes from this browser. Do you want to proceed?')) {
      state.solvedIds.clear();
      state.starredIds.clear();
      state.notes = {};
      state.solveMeta = {};

      saveState('solved');
      saveState('starred');
      saveState('notes');
      saveState('solveMeta');

      renderAllSteps();
      updateDashboardStats();
      applyFilterAndSearch();
      renderInsights();
      DOM.backupModal.classList.remove('active');
      showToast('All records have been reset.', 'fa-trash');
    }
  }

  // --- Helper: HTML Escaping ---
  function escapeHTML(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
  // Same escaping covers attribute context too (the quote/amp entities are
  // what matter for breaking out of href="..."); named separately so the
  // call sites read as "this is going in an attribute" for anyone editing.
  const escapeAttr = escapeHTML;

  // --- Setup Event Listeners ---
  function setupEventListeners() {
    // Theme Toggle
    DOM.themeToggleBtn.addEventListener('click', () => {
      const nextTheme = state.theme === 'dark' ? 'light' : 'dark';
      applyTheme(nextTheme);
    });

    // Global Resources Hub Modal Handlers
    DOM.globalResourcesBtn.addEventListener('click', () => {
      DOM.resourceHubModal.classList.add('active');
      DOM.resourceHubModal.setAttribute('aria-hidden', 'false');
    });
    DOM.closeResourceHubModalBtn.addEventListener('click', () => {
      DOM.resourceHubModal.classList.remove('active');
      DOM.resourceHubModal.setAttribute('aria-hidden', 'true');
    });

    // Resource Category Filter Chips inside Hub Modal
    DOM.resCatChips.forEach(chip => {
      chip.addEventListener('click', () => {
        DOM.resCatChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        applyResourceCategoryFilter(chip.dataset.cat);
      });
    });
    // Apply the initially-active category's filter on load — the HTML marks
    // one chip .active by default, but until this ran every card showed
    // regardless of category (the filter only ever fired from a click).
    const initialChip = DOM.resourceHubModal.querySelector('.res-cat-chip.active') || DOM.resCatChips[0];
    if (initialChip) applyResourceCategoryFilter(initialChip.dataset.cat);

    // Calendar Modal
    DOM.calendarModalBtn.addEventListener('click', () => {
      DOM.calendarModal.classList.add('active');
      DOM.calendarModal.setAttribute('aria-hidden', 'false');
    });
    DOM.closeCalendarModalBtn.addEventListener('click', () => {
      DOM.calendarModal.classList.remove('active');
      DOM.calendarModal.setAttribute('aria-hidden', 'true');
    });
    DOM.scheduleDailyGcalBtn.addEventListener('click', scheduleDailyDSAStudy);
    DOM.scheduleTargetGcalBtn.addEventListener('click', scheduleTargetSession);
    DOM.exportIcsBtn.addEventListener('click', exportICSFile);

    // Preset Time Chips
    DOM.presetChips.forEach(chip => {
      chip.addEventListener('click', () => {
        DOM.presetChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        const time = chip.dataset.time;
        DOM.gcalDailyTime.value = time;
        state.gcalTime = time;
        saveState('gcal');
        showToast(`Preset selected: ${time}`, 'fa-clock');
      });
    });

    // Time & Duration Change Listeners
    DOM.gcalDailyTime.addEventListener('change', (e) => {
      state.gcalTime = e.target.value;
      saveState('gcal');
      DOM.presetChips.forEach(c => c.classList.toggle('active', c.dataset.time === e.target.value));
    });

    DOM.gcalDuration.addEventListener('change', (e) => {
      state.gcalDuration = parseInt(e.target.value, 10);
      saveState('gcal');
    });

    // Spaced Revision GCal Buttons inside Note Modal
    DOM.schedRev3dBtn.addEventListener('click', () => scheduleProblemRevisionGcal(3));
    DOM.schedRev7dBtn.addEventListener('click', () => scheduleProblemRevisionGcal(7));
    DOM.schedRevCustomBtn.addEventListener('click', () => scheduleProblemRevisionGcal(1));

    // Search Input
    DOM.searchInput.addEventListener('input', (e) => {
      state.searchQuery = e.target.value;
      DOM.clearSearchBtn.style.display = state.searchQuery ? 'block' : 'none';
      applyFilterAndSearch();
    });

    DOM.clearSearchBtn.addEventListener('click', () => {
      DOM.searchInput.value = '';
      state.searchQuery = '';
      DOM.clearSearchBtn.style.display = 'none';
      applyFilterAndSearch();
    });

    // Filter Chips (All, Unsolved, Solved, NeetCode 150, Blind 75, Starred, Notes)
    DOM.filterChips.forEach(chip => {
      chip.addEventListener('click', () => {
        DOM.filterChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        state.activeFilter = chip.dataset.filter;
        applyFilterAndSearch();
      });
    });

    // Difficulty Filter Chips
    DOM.diffFilterChips.forEach(chip => {
      chip.addEventListener('click', () => {
        const diff = chip.dataset.diff;
        if (state.activeDiff === diff) {
          state.activeDiff = null;
          chip.classList.remove('active');
        } else {
          DOM.diffFilterChips.forEach(c => c.classList.remove('active'));
          chip.classList.add('active');
          state.activeDiff = diff;
        }
        applyFilterAndSearch();
      });
    });

    // Reset Filters from Empty State
    DOM.resetFiltersBtn.addEventListener('click', () => {
      state.searchQuery = '';
      state.activeFilter = 'all';
      state.activeDiff = null;
      DOM.searchInput.value = '';
      DOM.clearSearchBtn.style.display = 'none';
      DOM.filterChips.forEach(c => c.classList.toggle('active', c.dataset.filter === 'all'));
      DOM.diffFilterChips.forEach(c => c.classList.remove('active'));
      applyFilterAndSearch();
    });

    // Expand / Collapse All
    let allExpanded = false;
    DOM.expandAllBtn.addEventListener('click', () => {
      allExpanded = !allExpanded;
      const stepCards = document.querySelectorAll('.step-card');
      stepCards.forEach(card => {
        const sid = card.dataset.stepId;
        if (allExpanded) {
          card.classList.add('open');
          state.openSteps.add(sid);
        } else {
          card.classList.remove('open');
          state.openSteps.delete(sid);
        }
      });
      DOM.expandAllBtn.querySelector('span').textContent = allExpanded ? 'Collapse All' : 'Expand All';
      DOM.expandAllBtn.querySelector('i').className = allExpanded ? 'fa-solid fa-angles-up' : 'fa-solid fa-angles-down';
      saveState('openSteps');
    });

    // Pick Random
    DOM.randomBtn.addEventListener('click', pickRandomUnsolved);

    // Note Modal buttons
    DOM.closeNoteModalBtn.addEventListener('click', closeNoteModal);
    DOM.cancelNoteModalBtn.addEventListener('click', closeNoteModal);
    DOM.saveNoteModalBtn.addEventListener('click', saveCurrentNote);
    DOM.deleteNoteBtn.addEventListener('click', deleteCurrentNote);

    // Solve Timer & Attempt Log
    if (DOM.timerStartStopBtn) DOM.timerStartStopBtn.addEventListener('click', toggleSolveTimer);
    if (DOM.logAttemptBtn) DOM.logAttemptBtn.addEventListener('click', logAttempt);

    // Spaced Repetition Review buttons
    DOM.srsButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const pid = state.currentModalProblemId;
        if (!pid) return;
        const grade = btn.dataset.grade;
        const srs = scheduleReview(pid, grade);
        updateSrsDueLabel(srs);

        const row = document.getElementById(`prob-row-${pid}`);
        if (row) row.dataset.due = isDueToday(pid) ? 'true' : 'false';

        updateDashboardStats();
        applyFilterAndSearch();
        showToast(`Next review: ${srs.due} 🧠`, 'fa-brain');
      });
    });

    // Pattern Filter Chips
    if (DOM.clearPatternsBtn) {
      DOM.clearPatternsBtn.addEventListener('click', () => {
        state.activePatterns.clear();
        if (DOM.patternChipsContainer) {
          DOM.patternChipsContainer.querySelectorAll('.pattern-chip').forEach(c => c.classList.remove('active'));
        }
        DOM.clearPatternsBtn.style.display = 'none';
        applyFilterAndSearch();
      });
    }

    // Backup Modal
    DOM.backupModalBtn.addEventListener('click', () => {
      DOM.backupModal.classList.add('active');
      DOM.backupModal.setAttribute('aria-hidden', 'false');
    });
    DOM.closeBackupModalBtn.addEventListener('click', () => {
      DOM.backupModal.classList.remove('active');
      DOM.backupModal.setAttribute('aria-hidden', 'true');
    });
    DOM.exportDataBtn.addEventListener('click', exportData);
    DOM.importDataBtn.addEventListener('click', () => DOM.importFileInput.click());
    DOM.importFileInput.addEventListener('change', importData);
    DOM.resetAllDataBtn.addEventListener('click', resetAllData);

    // Close Modals on Outside Click
    window.addEventListener('click', (e) => {
      if (e.target === DOM.noteModal) closeNoteModal();
      if (e.target === DOM.backupModal) DOM.backupModal.classList.remove('active');
      if (e.target === DOM.calendarModal) DOM.calendarModal.classList.remove('active');
      if (e.target === DOM.resourceHubModal) DOM.resourceHubModal.classList.remove('active');
    });

    // Keyboard Shortcuts ('/' for search, 'Escape' to close modal, j/k/x/n to
    // navigate & act on the problem list without touching the mouse)
    window.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== DOM.searchInput && !DOM.noteModal.classList.contains('active')) {
        e.preventDefault();
        DOM.searchInput.focus();
      }
      if (e.key === 'Escape') {
        if (DOM.noteModal.classList.contains('active')) closeNoteModal();
        if (DOM.backupModal.classList.contains('active')) DOM.backupModal.classList.remove('active');
        if (DOM.calendarModal.classList.contains('active')) DOM.calendarModal.classList.remove('active');
        if (DOM.resourceHubModal.classList.contains('active')) DOM.resourceHubModal.classList.remove('active');
      }

      const typingInField = ['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName);
      if (typingInField || anyModalOpen()) return;

      if (e.key === 'j' || e.key === 'k') {
        e.preventDefault();
        moveFocus(e.key === 'j' ? 1 : -1);
      } else if (e.key === 'x') {
        const row = document.querySelector('.problem-row.kb-focused');
        if (row) {
          e.preventDefault();
          row.querySelector('.problem-checkbox').click();
        }
      } else if (e.key === 'n') {
        const row = document.querySelector('.problem-row.kb-focused');
        if (row) {
          e.preventDefault();
          openNoteModal(row.dataset.probId);
        }
      }
    });
  }

  // --- PWA: register the service worker ---
  // A no-op on a plain file:// page (browsers refuse SW registration there —
  // see sw.js's header comment) but activates cache-first offline loading
  // for anyone who serves this over http(s) instead.
  function registerServiceWorker() {
    if ('serviceWorker' in navigator && window.location.protocol !== 'file:') {
      navigator.serviceWorker.register('./sw.js').catch(() => {
        // Non-fatal: the app already works fully offline via local files
        // even if this registration fails for some reason.
      });
    }
  }

  // --- Initializer ---
  function init() {
    initProblemCatalog();
    loadStoredData();
    applyTheme(state.theme);
    renderAllSteps();
    renderPatternChips();
    updateDashboardStats();
    renderInsights();
    setupEventListeners();
    registerServiceWorker();
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
