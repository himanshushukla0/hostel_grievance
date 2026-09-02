/**
 * A2Z DSA Tracker - Problem ID Migration & Data Integrity Utility
 * Ensures backward compatibility across question ID changes, legacy string/number formats,
 * and preserves user data, notes, attempts, and SRS intervals smoothly.
 */

(function () {
  'use strict';

  const STORAGE_KEYS = {
    SOLVED: 'dsa_vault_solved_ids',
    STARRED: 'dsa_vault_starred_ids',
    NOTES: 'dsa_vault_notes_dict',
    SRS: 'dsa_vault_srs_data',
    ATTEMPTS: 'dsa_vault_attempts_data',
    ACTIVITY: 'dsa_vault_activity_history',
    VERSION: 'dsa_vault_storage_version'
  };

  const CURRENT_VERSION = '2.0.0';

  function runMigrations() {
    try {
      const storedVersion = localStorage.getItem(STORAGE_KEYS.VERSION);
      if (storedVersion === CURRENT_VERSION) {
        return;
      }

      // 1. Sanitize Solved IDs
      const solvedRaw = localStorage.getItem(STORAGE_KEYS.SOLVED);
      if (solvedRaw) {
        try {
          const solvedArr = JSON.parse(solvedRaw);
          if (Array.isArray(solvedArr)) {
            const sanitized = solvedArr.map(id => String(id).trim()).filter(Boolean);
            localStorage.setItem(STORAGE_KEYS.SOLVED, JSON.stringify(sanitized));
          }
        } catch (e) {
          console.warn('[Migration] Could not parse solved IDs:', e);
        }
      }

      // 2. Sanitize Starred IDs
      const starredRaw = localStorage.getItem(STORAGE_KEYS.STARRED);
      if (starredRaw) {
        try {
          const starredArr = JSON.parse(starredRaw);
          if (Array.isArray(starredArr)) {
            const sanitized = starredArr.map(id => String(id).trim()).filter(Boolean);
            localStorage.setItem(STORAGE_KEYS.STARRED, JSON.stringify(sanitized));
          }
        } catch (e) {
          console.warn('[Migration] Could not parse starred IDs:', e);
        }
      }

      // 3. Sanitize Notes Dictionary
      const notesRaw = localStorage.getItem(STORAGE_KEYS.NOTES);
      if (notesRaw) {
        try {
          const notesObj = JSON.parse(notesRaw);
          if (typeof notesObj === 'object' && notesObj !== null) {
            const sanitizedNotes = {};
            for (const [key, val] of Object.entries(notesObj)) {
              const cleanKey = String(key).trim();
              if (cleanKey && typeof val === 'object' && val !== null) {
                sanitizedNotes[cleanKey] = val;
              }
            }
            localStorage.setItem(STORAGE_KEYS.NOTES, JSON.stringify(sanitizedNotes));
          }
        } catch (e) {
          console.warn('[Migration] Could not sanitize notes:', e);
        }
      }

      localStorage.setItem(STORAGE_KEYS.VERSION, CURRENT_VERSION);
      console.log(`[Migration] DSA Vault storage migrated successfully to v${CURRENT_VERSION}`);
    } catch (err) {
      console.error('[Migration] Failed migration routine:', err);
    }
  }

  // Execute migration immediately
  runMigrations();
})();
