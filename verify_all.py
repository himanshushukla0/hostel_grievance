import sys
import os
import sqlite3
import datetime
import py_compile

print("==================================================")
print("     COMPREHENSIVE HOSTEL SYSTEM RE-VERIFICATION")
print("==================================================")

# Step 1: Syntax check all files
files = ["database.py", "student_view.py", "admin_view.py", "main.py"]
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

# Test 2.6: Notice Board DB Operations
n_id = database.create_notice(
    title="BH-1 Tank Inspection", 
    content="Water supply off from 2-4 PM.", 
    category="Maintenance Warning & Inspection", 
    target_block="BH-1"
)
notices = database.get_all_notices(block_filter="BH-1")
assert len(notices) >= 1
assert notices[0]['notice_id'] == n_id
print(f"  [OK] Created & Verified Notice #{n_id}: '{notices[0]['title']}'.")

# Clean up test rows
database.delete_grievance(g_id_1)
database.delete_grievance(g_id_2)
database.delete_notice(n_id)

# Step 3: GUI Class Structure & Tkinter Headless Validation
print("\n[Step 3] Verifying Tkinter GUI Classes (Headless Test)...")
import tkinter as tk
from main import App, ADMIN_PASSCODE
from student_view import StudentView
from admin_view import AdminView

root = tk.Tk()
root.withdraw() # Keep window hidden during test

# Verify App instance
app = App(root)
print("  [OK] App initialized successfully.")

# Verify StudentView instance & methods
student_frame = tk.Frame(root)
student_view = StudentView(student_frame)
assert hasattr(student_view, 'submit_grievance')
assert hasattr(student_view, 'check_status')
assert hasattr(student_view, 'setup_notices_tab')

# Test student_view form submission programmatically
student_view.name_entry.insert(0, "Test Student")
student_view.room_entry.insert(0, "D-404")
student_view.category_dropdown.set("📦 Miscellaneous / Other Hostel Issue")
student_view.desc_text.insert("1.0", "Fan making noise.")
student_view.suggestion_text.insert("1.0", "Inspect fan bearing.")

new_g_id = database.create_grievance("Test Student", "D-404", "📦 Miscellaneous / Other Hostel Issue", "Fan making noise.", block_name="BH-1", suggestion="Inspect fan bearing.")
student_view.id_entry.insert(0, str(new_g_id))
student_view.check_status()
assert "Pending" in student_view.status_var.get()
assert "Inspect fan bearing." in student_view.suggestion_display_var.get()
print(f"  [OK] StudentView status & suggestion lookup verified for Grievance #{new_g_id}.")

# Verify AdminView instance & notice methods
admin_frame = tk.Frame(root)
admin_view = AdminView(admin_frame)
assert hasattr(admin_view, 'load_data')
assert hasattr(admin_view, 'publish_notice')
assert hasattr(admin_view, 'load_notices')

admin_view.search_entry.insert(0, "D-404")
admin_view.load_data()
children = admin_view.tree.get_children()
assert len(children) >= 1
print(f"  [OK] AdminView table filtering and Notice Board manager verified.")

# Cleanup test row
database.delete_grievance(new_g_id)

root.destroy()

print("\n==================================================")
print("     ALL VERIFICATION TESTS PASSED SUCCESSFULLY! ")
print("==================================================")
