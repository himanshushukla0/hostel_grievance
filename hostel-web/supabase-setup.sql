-- ============================================================================
--  Hostel Care — Supabase preparation
--  Run in: Supabase dashboard → SQL Editor → New query → Run
--  Safe to run more than once.
-- ============================================================================


-- ─────────────────────────────────────────────────────────────────────────────
--  STEP 1 — REQUIRED.  Fix the ID sequences.
--
--  Why this matters: the old Streamlit app let SQLite pick each ID and then
--  pushed that exact number into Postgres. Because the IDs were supplied
--  explicitly, Postgres never advanced its own identity counter — it still
--  thinks the next ID is 1.
--
--  The new website (correctly) lets Postgres assign IDs. Without this fix the
--  very first complaint submitted would try to reuse an ID that already exists
--  and fail with "duplicate key value violates unique constraint".
--
--  These three statements move each counter past the highest existing row.
-- ─────────────────────────────────────────────────────────────────────────────

SELECT setval(
  pg_get_serial_sequence('"Grievances"', 'grievance_id'),
  COALESCE((SELECT MAX(grievance_id) FROM "Grievances"), 0) + 1,
  false
);

SELECT setval(
  pg_get_serial_sequence('"Notices"', 'notice_id'),
  COALESCE((SELECT MAX(notice_id) FROM "Notices"), 0) + 1,
  false
);

SELECT setval(
  pg_get_serial_sequence('"LeaveApplications"', 'leave_id'),
  COALESCE((SELECT MAX(leave_id) FROM "LeaveApplications"), 0) + 1,
  false
);


-- ─────────────────────────────────────────────────────────────────────────────
--  STEP 2 — Confirm the fix worked.
--  next_id should be greater than max_id for all three tables.
-- ─────────────────────────────────────────────────────────────────────────────

SELECT 'Grievances' AS table_name,
       (SELECT MAX(grievance_id) FROM "Grievances") AS max_id,
       nextval(pg_get_serial_sequence('"Grievances"', 'grievance_id')) AS next_id
UNION ALL
SELECT 'Notices',
       (SELECT MAX(notice_id) FROM "Notices"),
       nextval(pg_get_serial_sequence('"Notices"', 'notice_id'))
UNION ALL
SELECT 'LeaveApplications',
       (SELECT MAX(leave_id) FROM "LeaveApplications"),
       nextval(pg_get_serial_sequence('"LeaveApplications"', 'leave_id'));

-- NOTE: the check above *consumes* one ID per table (that is what nextval does).
-- Harmless — it just means your next ticket number skips by one. Re-run STEP 1
-- afterwards if you want the numbering tight.



-- ============================================================================
--  STEP 3 — OPTIONAL BUT STRONGLY RECOMMENDED: lock the database down.
--
--  Read this before running it.
--
--  Right now RLS is OFF, which means the publishable key shipped in the
--  browser can read, edit and DELETE every row. That was already true of the
--  Streamlit version, but a browser app makes it easier to notice: anyone can
--  open devtools and issue delete calls. The warden passcode lives in
--  JavaScript, so it stops casual visitors, not anyone determined.
--
--  For a class demo that is usually acceptable. For a portal real students
--  actually use, do this instead:
--
--    1. Supabase dashboard → Authentication → Users → "Add user".
--       Create one account for the warden (email + password).
--    2. In app.js set:   WARDEN_MODE: 'supabase-auth'
--    3. Run everything below.
--
--  Result: anybody may file a complaint or a leave request and read notices,
--  but only a signed-in warden can change status, issue gate passes, publish
--  notices, or delete anything.
-- ============================================================================

-- --- Grievances -------------------------------------------------------------
-- ALTER TABLE "Grievances" ENABLE ROW LEVEL SECURITY;
--
-- CREATE POLICY "anyone can file a complaint"
--   ON "Grievances" FOR INSERT TO anon, authenticated WITH CHECK (true);
--
-- CREATE POLICY "anyone can read complaints"
--   ON "Grievances" FOR SELECT TO anon, authenticated USING (true);
--
-- CREATE POLICY "only warden can edit"
--   ON "Grievances" FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
--
-- CREATE POLICY "only warden can delete"
--   ON "Grievances" FOR DELETE TO authenticated USING (true);


-- --- LeaveApplications -------------------------------------------------------
-- ALTER TABLE "LeaveApplications" ENABLE ROW LEVEL SECURITY;
--
-- CREATE POLICY "anyone can apply"
--   ON "LeaveApplications" FOR INSERT TO anon, authenticated WITH CHECK (true);
--
-- CREATE POLICY "anyone can read applications"
--   ON "LeaveApplications" FOR SELECT TO anon, authenticated USING (true);
--
-- CREATE POLICY "only warden can authorise"
--   ON "LeaveApplications" FOR UPDATE TO authenticated USING (true) WITH CHECK (true);
--
-- CREATE POLICY "only warden can delete applications"
--   ON "LeaveApplications" FOR DELETE TO authenticated USING (true);


-- --- Notices ----------------------------------------------------------------
-- ALTER TABLE "Notices" ENABLE ROW LEVEL SECURITY;
--
-- CREATE POLICY "anyone can read notices"
--   ON "Notices" FOR SELECT TO anon, authenticated USING (true);
--
-- CREATE POLICY "only warden can publish"
--   ON "Notices" FOR INSERT TO authenticated WITH CHECK (true);
--
-- CREATE POLICY "only warden can remove notices"
--   ON "Notices" FOR DELETE TO authenticated USING (true);

-- Heads-up: with RLS on, expired-notice auto-cleanup also needs a signed-in
-- warden, so notices will only be purged while a warden has the desk open.
-- To purge them server-side instead, use a Supabase scheduled function.
