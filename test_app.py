import database

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

# Clean up test entry
database.delete_grievance(g_id)

print("--- All Database Verification Tests Passed! ---")
