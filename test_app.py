import os
import sys
import tempfile

# Run against an isolated, throwaway SQLite DB — never the real/cloud database.
os.environ.pop("SUPABASE_URL", None)
os.environ.pop("SUPABASE_KEY", None)
os.environ["HOSTEL_DB_FILE"] = os.path.join(tempfile.gettempdir(), "hostel_test.db")
for _ext in ("", "-wal", "-shm", "-journal"):
    try:
        os.remove(os.environ["HOSTEL_DB_FILE"] + _ext)
    except OSError:
        pass

import database  # noqa: E402  (imported after env is set so it picks up the test DB)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("--- Testing Database Migration & Operations ---")
database.init_db()

# Create a test grievance with suggestion
g_id = database.create_grievance(
    name="John Doe", 
    room="A-101", 
    category="📦 Miscellaneous / Other Hostel Issue", 
    description="Desk drawer handle broken.",
    block_name="BH-1",
    priority="Normal",
    suggestion="Please replace the drawer handle or lock."
)
print(f"Created grievance ID: {g_id}")

# Fetch by ID
grievance = database.get_grievance_by_id(g_id)
print(f"Fetched Grievance: {grievance}")

assert grievance['student_name'] == "John Doe"
assert grievance['status'] == "Pending"
assert grievance['block_name'] == "BH-1"
assert grievance['suggestion'] == "Please replace the drawer handle or lock."

# Update grievance as admin
database.update_grievance(g_id, "In Progress", "Carpenter assigned.")

updated_g = database.get_grievance_by_id(g_id)
print(f"Updated Grievance: {updated_g}")
assert updated_g['status'] == "In Progress"
assert updated_g['admin_remarks'] == "Carpenter assigned."
assert updated_g['last_updated'] != ""

# Test Filtering by block
block_grievances = database.get_all_grievances(block_filter="BH-1")
print(f"Filtered 'BH-1' count: {len(block_grievances)}")
assert any(g['grievance_id'] == g_id for g in block_grievances)

# Test Search by suggestion keyword
search_results = database.get_all_grievances(search_query="handle")
print(f"Search results for 'handle': {len(search_results)}")
assert len(search_results) > 0

# Test dual search by Room Number & Student Name (Forgot Ticket ID flow)
room_and_name_results = database.get_grievances_by_room_and_name("A-101", "John Doe")
print(f"Dual room/name search results: {len(room_and_name_results)}")
assert len(room_and_name_results) >= 1
assert any(g['grievance_id'] == g_id for g in room_and_name_results)

# Verify privacy rule: mismatching room or name returns 0 results
assert len(database.get_grievances_by_room_and_name("B-999", "John Doe")) == 0
assert len(database.get_grievances_by_room_and_name("A-101", "Unknown Person")) == 0

# Clean up test entry
database.delete_grievance(g_id)

# Test Notice Timer Creation & Auto Expiration Purge
permanent_notice_id = database.create_notice("Permanent Notice", "Valid indefinitely", "General", "All Blocks", expiry_hours=0)
expired_notice_id = database.create_notice("Expired Test Notice", "Should be auto deleted", "General", "All Blocks", expiry_hours=-1)

active_notices = database.get_all_notices()
assert any(n['notice_id'] == permanent_notice_id for n in active_notices)
assert not any(n['notice_id'] == expired_notice_id for n in active_notices)
print("Notice active duration & auto-cleanup verified.")

database.delete_notice(permanent_notice_id)

# Test Leave Application Creation & Warden Gate Pass Issuance
leave_id = database.create_leave_application(
    name="Test Leave Student",
    block="BH-1",
    room="B-204",
    phone="+91 9876543210",
    parent_phone="+91 9123456789",
    reason="Home Visit",
    destination="New Delhi",
    from_date="2026-08-20",
    to_date="2026-08-22",
    teacher_name="Prof. R.K. Verma"
)
print(f"Created Leave Application ID: {leave_id}")

leave_rec = database.get_leave_application_by_id(leave_id)
assert leave_rec['granting_teacher'] == "Prof. R.K. Verma"
assert leave_rec['status'] == "Pending Warden Approval"

database.update_leave_status(leave_id, "Approved / Gate Pass Issued", warden_remarks="Approved", gate_pass_code="GP-2026-X001")
updated_leave = database.get_leave_application_by_id(leave_id)
assert updated_leave['status'] == "Approved / Gate Pass Issued"
assert updated_leave['gate_pass_code'] == "GP-2026-X001"
print("Leave Application & Gate Pass issuance verified.")

database.delete_leave_application(leave_id)

# ---- NEW FEATURE TESTS ----

# Resolution rating & feedback
rg = database.create_grievance("Rita", "R-1", "Electrical", "Fan dead", block_name="BH-3", priority="Normal")
database.update_grievance(rg, "Resolved", "Fan replaced", "Tech A")
database.submit_grievance_feedback(rg, 5, "Fast fix, thanks!")
rg_rec = database.get_grievance_by_id(rg)
assert rg_rec['rating'] == 5
assert rg_rec['feedback'] == "Fast fix, thanks!"
# rating is clamped to 0..5
database.submit_grievance_feedback(rg, 9, "")
assert database.get_grievance_by_id(rg)['rating'] == 5
print("Resolution rating & feedback verified.")

# Analytics summary
summary = database.get_analytics_summary()
assert summary['total'] >= 1
assert 0.0 <= summary['resolution_rate'] <= 100.0
assert summary['rated_count'] >= 1
assert isinstance(summary['by_category'], dict)
assert 'overdue_24h' in summary and 'overdue_48h' in summary
print(f"Analytics summary verified (total={summary['total']}, resolution_rate={summary['resolution_rate']}%).")

# Cluster outage detection
c1 = database.create_grievance("A", "1", "Plumbing & Water", "Leak", block_name="GH-1", priority="Normal")
c2 = database.create_grievance("B", "2", "Plumbing & Water", "Leak", block_name="GH-1", priority="Normal")
alerts = database.detect_cluster_outages(window_hours=48, threshold=2)
assert any(a['block'] == "GH-1" and a['category'] == "Plumbing & Water" and a['count'] >= 2 for a in alerts)
print("Cluster outage detection verified.")

# Lost & Found CRUD
item = database.create_lost_found_item("Silver watch", "Found", "Electronics", "Gym", "Casio", "B-9")
assert item is not None
assert len(database.get_all_lost_found(item_type_filter="Found")) >= 1
database.update_lost_found_status(item, "Claimed / Returned")
assert len(database.get_all_lost_found(status_filter="Open", item_type_filter="Found")) == 0 or all(
    it['item_id'] != item for it in database.get_all_lost_found(status_filter="Open")
)
database.delete_lost_found_item(item)
print("Lost & Found CRUD verified.")

# Gate pass QR generation (decodes structurally to a non-empty matrix)
import qr_gen
qm = qr_gen.qr_matrix("GP-2026-7X9K2M", "M")
assert len(qm) == 21 and all(len(r) == 21 for r in qm)  # version 1
svg = qr_gen.qr_svg("GP-2026-7X9K2M")
assert svg.startswith("<svg") and svg.endswith("</svg>")
print("Offline QR generation verified.")

# clean up new-feature rows
for gid in (rg, c1, c2):
    database.delete_grievance(gid)

print("--- All Database Verification Tests Passed! ---")
