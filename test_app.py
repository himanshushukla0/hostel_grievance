import sys
import database

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

print("--- All Database Verification Tests Passed! ---")
