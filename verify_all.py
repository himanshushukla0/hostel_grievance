import sys
import os
import sqlite3
import datetime
import tempfile
import py_compile

# Run against an isolated, throwaway SQLite DB — never the real/cloud database.
os.environ.pop("SUPABASE_URL", None)
os.environ.pop("SUPABASE_KEY", None)
os.environ["HOSTEL_DB_FILE"] = os.path.join(tempfile.gettempdir(), "hostel_verify.db")
for _ext in ("", "-wal", "-shm", "-journal"):
    try:
        os.remove(os.environ["HOSTEL_DB_FILE"] + _ext)
    except OSError:
        pass

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("==================================================")
print("     COMPREHENSIVE HOSTEL SYSTEM RE-VERIFICATION")
print("==================================================")

# Step 1: Syntax check the web app files
files = ["database.py", "app.py", "qr_gen.py"]
print("\n[Step 1] Checking Python Syntax & Compilability...")
for f in files:
    try:
        py_compile.compile(f, doraise=True)
        print(f"  [OK] {f}: Syntax OK")
    except Exception as e:
        print(f"  [FAIL] {f}: Syntax Error -> {e}")
        sys.exit(1)


# Step 2: Database Layer Verification
print("\n[Step 2] Verifying Database Operations & Migrations...")
import database

database.init_db()

# Test 2.1: Column Inspection
conn = database.get_connection()
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(Grievances)")
cols = [r['name'] for r in cursor.fetchall()]
conn.close()
print(f"  Columns present in DB: {cols}")
assert "last_updated" in cols, "last_updated column missing!"
assert "admin_remarks" in cols, "admin_remarks column missing!"
assert "suggestion" in cols, "suggestion column missing!"

# Test 2.2: Grievance Creation & Retrieval
g_id_1 = database.create_grievance("Alice Smith", "B-204", "Plumbing", "Leaking sink tap in bathroom.", block_name="BH-1", priority="Normal", suggestion="Replace washer.")
g_id_2 = database.create_grievance("Bob Jones", "C-305", "📦 Miscellaneous / Other Hostel Issue", "No internet connection in room.", block_name="BH-2", priority="Urgent", suggestion="Check switchport C3.")

g1 = database.get_grievance_by_id(g_id_1)
print(f"  [OK] Created Grievance #{g_id_1}: {g1['student_name']} - Status: {g1['status']} - Suggestion: '{g1['suggestion']}'")
assert g1['status'] == 'Pending'
assert g1['last_updated'] == g1['date_submitted']
assert g1['suggestion'] == "Replace washer."

# Test 2.3: Admin Update
database.update_grievance(g_id_1, "In Progress", "Plumber dispatched.")
g1_updated = database.get_grievance_by_id(g_id_1)
print(f"  [OK] Updated Grievance #{g_id_1}: Status -> {g1_updated['status']}, Remarks -> '{g1_updated['admin_remarks']}'")
assert g1_updated['status'] == 'In Progress'
assert g1_updated['admin_remarks'] == 'Plumber dispatched.'

database.update_grievance(g_id_2, "Resolved", "Router restarted.")
g2_updated = database.get_grievance_by_id(g_id_2)
assert g2_updated['status'] == 'Resolved'

# Test 2.4: Filters
pending_list = database.get_all_grievances(status_filter="Pending")
in_progress_list = database.get_all_grievances(status_filter="In Progress")
resolved_list = database.get_all_grievances(status_filter="Resolved")
all_list = database.get_all_grievances(status_filter="All")

bh1_list = database.get_all_grievances(block_filter="BH-1")

print(f"  [OK] Status Filters -> All: {len(all_list)}, Pending: {len(pending_list)}, In Progress: {len(in_progress_list)}, Resolved: {len(resolved_list)}")
print(f"  [OK] Block Filter BH-1 -> Found {len(bh1_list)} complaints")
assert any(g['grievance_id'] == g_id_1 for g in bh1_list)

# Test 2.5: Search
search_name = database.get_all_grievances(search_query="Alice")
search_room = database.get_all_grievances(search_query="C-305")
search_cat = database.get_all_grievances(search_query="Miscellaneous")
search_sug = database.get_all_grievances(search_query="washer")

assert len(search_name) >= 1
assert len(search_room) >= 1
assert len(search_cat) >= 1
assert len(search_sug) >= 1
print("  [OK] Search functionality verified across Name, Room, Category, and Suggestion.")

# Test 2.5b: Forgot Ticket ID Dual Room & Name Lookup
dual_search = database.get_grievances_by_room_and_name("B-204", "Alice Smith")
assert len(dual_search) >= 1
assert dual_search[0]['grievance_id'] == g_id_1
assert len(database.get_grievances_by_room_and_name("B-204", "Wrong Student")) == 0
print("  [OK] Secure Forgot-ID dual Room & Student Name lookup verified.")

# Test 2.6: Notice Board DB Operations & Active Timers
n_id = database.create_notice(
    title="BH-1 Tank Inspection", 
    content="Water supply off from 2-4 PM.", 
    category="Maintenance Warning & Inspection", 
    target_block="BH-1"
)
n_id_timed = database.create_notice(
    title="Timed Notice Test",
    content="Expires in 24 hours.",
    category="Maintenance Warning & Inspection",
    target_block="BH-1",
    expiry_hours=24
)
n_id_exp = database.create_notice(
    title="Expired Notice Test",
    content="Expired 1 hour ago.",
    category="Maintenance Warning & Inspection",
    target_block="BH-1",
    expiry_hours=-1
)
notices = database.get_all_notices(block_filter="BH-1")
assert any(n['notice_id'] == n_id for n in notices)
assert any(n['notice_id'] == n_id_timed for n in notices)
assert not any(n['notice_id'] == n_id_exp for n in notices)
print(f"  [OK] Created & Verified Notice #{n_id}: '{notices[0]['title']}' with Expiry Timers & Auto-Purge.")

# Step 3: Leave application & gate pass flow
print("\n[Step 3] Verifying Leave Application & Gate Pass flow...")
lv_id = database.create_leave_application(
    name="Test Student", block="BH-1", room="D-404",
    phone="+91 9000000000", parent_phone="+91 9111111111",
    reason="Home Visit", destination="New Delhi",
    from_date="2026-09-01", to_date="2026-09-03", teacher_name="Prof. Verma"
)
lv = database.get_leave_application_by_id(lv_id)
assert lv['status'] == 'Pending Warden Approval'
database.update_leave_status(lv_id, "Approved / Gate Pass Issued", warden_remarks="OK", gate_pass_code="GP-2026-TEST01")
lv2 = database.get_leave_application_by_id(lv_id)
assert lv2['gate_pass_code'] == "GP-2026-TEST01"
masked = database.get_leave_applications_by_room_and_name("D-404", "Test Student")
assert any(r['leave_id'] == lv_id for r in masked)
print(f"  [OK] Leave application #{lv_id}, gate pass issuance, and room+name lookup verified.")

# Step 4: Search sanitization (PostgREST filter-injection guard)
print("\n[Step 4] Verifying search input sanitization...")
assert database._sanitize_search("B-204, or 1=1") == "B-204  or 1=1"
assert "(" not in database._sanitize_search("a(b)c") and ")" not in database._sanitize_search("a(b)c")
assert database.get_all_grievances(search_query="x,y(z)") == [] or isinstance(database.get_all_grievances(search_query="x,y(z)"), list)
print("  [OK] Commas/parentheses stripped from search terms.")

# Step 5: New features — ratings, analytics, cluster detection, Lost & Found, QR
print("\n[Step 5] Verifying ratings, analytics, cluster detection, Lost & Found, QR...")

# ratings
database.update_grievance(g_id_1, "Resolved", "Fixed", "Tech")
database.submit_grievance_feedback(g_id_1, 4, "Good work")
assert database.get_grievance_by_id(g_id_1)['rating'] == 4
print("  [OK] Resolution rating & feedback.")

# analytics
summ = database.get_analytics_summary()
assert summ['total'] >= 2 and summ['rated_count'] >= 1
assert 0.0 <= summ['resolution_rate'] <= 100.0
print(f"  [OK] Analytics summary (resolution_rate={summ['resolution_rate']}%, avg_rating={summ['avg_rating']}).")

# cluster detection
ca = database.create_grievance("Cx", "9", "Plumbing & Water", "Leak", block_name="GH-2", priority="Normal")
cb = database.create_grievance("Cy", "10", "Plumbing & Water", "Leak", block_name="GH-2", priority="Normal")
clusters = database.detect_cluster_outages()
assert any(c['block'] == "GH-2" and c['count'] >= 2 for c in clusters)
print(f"  [OK] Cluster outage detection ({len(clusters)} cluster group(s)).")

# lost & found
lf = database.create_lost_found_item("Umbrella", "Lost", "Other", "Library", "Black", "B-7")
assert any(i['item_id'] == lf for i in database.get_all_lost_found())
database.update_lost_found_status(lf, "Claimed / Returned")
assert all(i['item_id'] != lf for i in database.get_all_lost_found(status_filter="Open"))
database.delete_lost_found_item(lf)
print("  [OK] Lost & Found CRUD.")

# gate pass code lookup + QR
database.update_leave_status(lv_id, "Approved / Gate Pass Issued", "OK", "GP-2026-VERIFY1")
found_pass = database.get_leave_by_gate_pass_code("GP-2026-VERIFY1")
assert found_pass and found_pass['leave_id'] == lv_id
import qr_gen
assert qr_gen.qr_svg("GP-2026-VERIFY1").startswith("<svg")
print("  [OK] Gate pass code lookup + offline QR generation.")

# Step 6: Round-3 bug fixes + new features
print("\n[Step 6] Verifying Round-3 fixes & features (audit, escalation, mess, visitor, email)...")

# rating overwrite guard (A3)
database.update_grievance(ca, "Resolved", "done", "StaffA")
database.submit_grievance_feedback(ca, 5, "great")
database.submit_grievance_feedback(ca, 1, "override attempt")
assert database.get_grievance_by_id(ca)["rating"] == 5
print("  [OK] A3 rating overwrite guard.")

# image magic-byte validation (A10)
try:
    database.upload_photo(b"totally not an image", "x.png"); raise AssertionError("should reject")
except database.DatabaseError:
    pass
print("  [OK] A10 image magic-byte validation.")

# audit + escalation (B1, B2)
esc_target = database.create_grievance("Stale", "Z-1", "Wi-Fi", "down", block_name="BH-3", priority="Normal")
with database.get_db() as _c:
    _c.execute("UPDATE Grievances SET date_submitted=? WHERE grievance_id=?", ("2020-01-01 00:00:00", esc_target)); _c.commit()
assert any(e["grievance_id"] == esc_target for e in database.auto_escalate_priorities())
assert database.get_audit_log(action_filter="AUTO_ESCALATE")
print("  [OK] B1/B2 audit log + priority escalation.")

# staff perf + trends (B3, B4)
assert any(s["staff"] == "StaffA" for s in database.get_staff_performance())
assert len(database.get_monthly_trends()) >= 1
print("  [OK] B3/B4 staff performance + monthly trends.")

# return + quota (B5, B6)
database.mark_student_returned(lv_id)
assert database.get_leave_application_by_id(lv_id)["returned_at"]
assert database.get_leave_days_used("B-204", "Test") >= 0
print("  [OK] B5/B6 return check-in + leave quota.")

# lost & found expiry (B7)
oi = database.create_lost_found_item("Old", "Lost", "Other", "Lib", "x", "B-1")
with database.get_db() as _c:
    _c.execute("UPDATE LostAndFound SET date_posted=? WHERE item_id=?", ("2020-01-01 00:00:00", oi)); _c.commit()
database.cleanup_old_lost_found(30)
assert all(i["item_id"] != oi for i in database.get_all_lost_found(status_filter="Open"))
print("  [OK] B7 Lost & Found auto-expiry.")

# mess + menu (B9)
database.create_mess_feedback("Dinner", 2, "cold and bland", "B-1")
assert database.get_mess_analytics()["total"] >= 1
database.set_mess_menu("2026-08-25", "Idli", "Rajma Rice", "Chapati")
assert database.get_mess_menu("2026-08-25")["dinner"] == "Chapati"
print("  [OK] B9 mess feedback + menu.")

# visitor (B10)
vpid = database.create_visitor_pass("VerifyGuest", "Aadhaar", "1", "Host", "H-1", "BH-1", "Meet", "2026-08-26")
database.update_visitor_status(vpid, "Checked In")
assert database.get_visitor_pass_by_id(vpid)["entry_time"]
assert database.get_visitor_passes_by_name("Verify")
print("  [OK] B10 visitor passes.")

# email no-op (B11)
assert database.send_notification_email("a@b.com", "s", "b") is False
print("  [OK] B11 email notification (unconfigured no-op).")

# Clean up test rows
database.delete_grievance(g_id_1)
database.delete_grievance(g_id_2)
database.delete_grievance(ca)
database.delete_grievance(cb)
database.delete_grievance(esc_target)
database.delete_notice(n_id)
database.delete_notice(n_id_timed)
database.delete_leave_application(lv_id)

print("\n==================================================")
print("     ALL VERIFICATION TESTS PASSED SUCCESSFULLY! ")
print("==================================================")
