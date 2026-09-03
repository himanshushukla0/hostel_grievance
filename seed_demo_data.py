"""
Seed realistic demo data into hostel_care.db for exploring the Streamlit application.
"""
import os
import sys
import datetime

# Ensure we use the local SQLite DB
os.environ.pop("SUPABASE_URL", None)
os.environ.pop("SUPABASE_KEY", None)
os.environ["HOSTEL_DB_FILE"] = "hostel_care.db"

import database

def seed():
    print("Initializing Database...")
    database.init_db()
    now = datetime.datetime.now()

    print("Populating Notices...")
    notices = [
        ("🚨 Water Supply Interruption", "Annual overhead tank cleaning scheduled for BH-1 and BH-2 on Saturday from 9:00 AM to 2:00 PM. Please store sufficient water.", "Maintenance", "All Blocks", "Hostel Chief Warden"),
        ("🏆 Inter-Hostel Badminton & Table Tennis Tournament", "Registrations open at the sports office. Matches commence this Friday evening at the indoor complex.", "Sports & Events", "All Blocks", "Sports Secretary"),
        ("🍲 Special Festive Dinner & Mess Schedule", "Special South & North Indian thali served this Sunday night. Dinner timings extended to 10:00 PM.", "Mess & Food", "All Blocks", "Mess Committee"),
        ("⚡ High-Speed Wi-Fi Router Upgrades in GH-1", "New optical fibre APs are being installed on 2nd and 3rd floors of GH-1 today between 11 AM - 4 PM.", "Internet & Wi-Fi", "GH-1", "IT Support Desk")
    ]
    for title, content, cat, blk, by in notices:
        database.create_notice(title, content, cat, blk, by)

    print("Populating Grievances...")
    grievances = [
        # Cluster in BH-1 (Plumbing) to trigger cluster outage KPI
        ("Aarav Sharma", "BH-1", "102", "🚰 Plumbing & Water Supply", "Shower head is leaking continuously and pressure is low.", "Urgent", "Needs washer and head replacement.", "In Progress", "Ramesh (Plumber)", "Parts ordered, visiting today."),
        ("Rohan Verma", "BH-1", "104", "🚰 Plumbing & Water Supply", "No hot water in geyser and tap leaking near washbasin.", "Urgent", "Inspect heating coil.", "In Progress", "Ramesh (Plumber)", "Heating element inspected."),
        ("Vikram Singh", "BH-1", "108", "🚰 Plumbing & Water Supply", "Main pipeline joint dripping onto bathroom floor.", "Emergency", "Tighten pipe union or seal with tape.", "Pending", "", ""),
        
        # Electrical & Appliances
        ("Ananya Iyer", "GH-1", "204", "⚡ Electrical & Appliances", "Ceiling fan making squeaking noise at speed 4 and regulator stiff.", "Normal", "Lubricate fan bearing.", "Resolved", "Suresh (Electrician)", "Replaced capacitor and regulator switch.", 5, "Fixed very fast within 3 hours. Excellent!"),
        ("Priya Nair", "GH-1", "305", "⚡ Electrical & Appliances", "Study table power socket spark when plugging laptop adapter.", "Urgent", "Replace socket module with 16A anchor switch.", "In Progress", "Suresh (Electrician)", "Inspected, replacing socket board."),
        
        # Furniture & Carpentry
        ("Devansh Patel", "BH-2", "312", "🪑 Furniture & Carpentry", "Study table drawer slider stuck and chair backrest loose.", "Normal", "Realign telescopic rails.", "Resolved", "Mahesh (Carpenter)", "Fixed rails and tightened chair screws.", 4, "Drawer works smoothly now, thank you."),
        ("Kavya Reddy", "GH-2", "115", "🪑 Furniture & Carpentry", "Wardrobe door latch broken, unable to lock personal locker.", "Urgent", "Install new brass latch.", "Pending", "", ""),

        # Internet & Wi-Fi
        ("Sneha Gupta", "GH-1", "210", "🌐 Internet & Wi-Fi", "Wi-Fi access point showing 'Connected, no internet' since morning.", "Normal", "Reboot Floor 2 Access Point.", "Resolved", "Amit (Network)", "Rebooted Switch 2B and DHCP lease cleared.", 5, "Internet speed is back to 100 Mbps!"),
        ("Rahul Mehta", "BH-2", "201", "🌐 Internet & Wi-Fi", "Ethernet port in room loose, cable disconnects when moved.", "Normal", "Crimp new RJ45 keystone jack.", "Pending", "", ""),

        # Cleanliness & Hygiene
        ("Aditya Roy", "BH-1", "215", "🧹 Cleanliness & Hygiene", "Corridor dustbin overflowed and floor needs mopping.", "Normal", "Daily morning cleaning schedule.", "Resolved", "Sunil (Sanitation)", "Cleaned and sanitized.", 5, "Good job."),
        ("Tanvi Deshmukh", "GH-2", "402", "🧹 Cleanliness & Hygiene", "Common washroom mirror stained and drainage slow.", "Normal", "Apply drain unclogger liquid.", "In Progress", "Sunil (Sanitation)", "Drain cleared, sanitization in progress.")
    ]

    for item in grievances:
        name, blk, room, cat, desc, prio, sugg, status, staff, remarks = item[:10]
        gid = database.create_grievance(name, room, cat, desc, blk, prio, sugg, photo_path="", student_email=f"{name.lower().replace(' ', '.')}@campus.edu")
        if status != "Pending" or staff or remarks:
            database.update_grievance(gid, status, remarks, staff)
        if len(item) > 10:
            rating, feedback = item[10], item[11]
            database.submit_grievance_feedback(gid, rating, feedback)

    print("Populating Leave Applications & Gate Passes...")
    leaves = [
        ("Aarav Sharma", "BH-1", "102", "9876543210", "9876500001", "Attending sister's wedding in Jaipur", "Jaipur, Rajasthan", 
         (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d"), (now + datetime.timedelta(days=5)).strftime("%Y-%m-%d"), 
         "Prof. K. Sharma", "Approved / Gate Pass Issued", "Approved. Return before 8 PM on closing date.", "GP-BH1-8842", "aarav.sharma@campus.edu"),
        
        ("Kavya Reddy", "GH-2", "115", "9812345678", "9812300002", "National Hackathon Finalist Presentation", "Bangalore, Karnataka", 
         (now + datetime.timedelta(days=2)).strftime("%Y-%m-%d"), (now + datetime.timedelta(days=6)).strftime("%Y-%m-%d"), 
         "Dr. V. Rao", "Approved / Gate Pass Issued", "Official institute representation approved.", "GP-GH2-3391", "kavya.reddy@campus.edu"),
        
        ("Devansh Patel", "BH-2", "312", "9723456789", "9723400003", "Medical checkup and dentist appointment", "Ahmedabad, Gujarat", 
         (now + datetime.timedelta(days=3)).strftime("%Y-%m-%d"), (now + datetime.timedelta(days=5)).strftime("%Y-%m-%d"), 
         "Prof. M. Gupta", "Pending Warden Approval", "", "", "devansh.patel@campus.edu"),
        
        ("Rohan Verma", "BH-1", "104", "9934567890", "9934500004", "Weekend home visit", "Delhi NCR", 
         (now - datetime.timedelta(days=4)).strftime("%Y-%m-%d"), (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d"), 
         "Prof. A. Bansal", "Approved / Gate Pass Issued", "Returned safely.", "GP-BH1-1104", "rohan.verma@campus.edu")
    ]

    for name, blk, room, ph, pph, rsn, dest, f_dt, t_dt, tch, st, rem, code, eml in leaves:
        lid = database.create_leave_application(name, blk, room, ph, pph, rsn, dest, f_dt, t_dt, tch, eml)
        if "Approved" in st:
            database.update_leave_status(lid, "Approved / Gate Pass Issued", rem, code)
            if "Returned" in rem:
                database.mark_student_returned(lid)

    print("Populating Lost & Found...")
    lost_found_items = [
        ("Blue Hydro Flask Water Bottle", "Lost", "Personal Belongings", "Hostel Gymnasium / 1st floor water cooler", "Blue 1L stainless steel bottle with GitHub and Linux stickers.", "9876543210"),
        ("Scientific Calculator Casio fx-991EX", "Found", "Electronics", "Study Hall 3, 2nd floor BH-2", "Found on corner table near power plug after evening study session.", "Ext 102 (Care Desk)"),
        ("Boat Wireless Earbuds (Black Case)", "Lost", "Electronics", "Central Mess Dining Hall near handwash", "Black charging case with right earbud inside, Left missing.", "9812345678"),
        ("Student ID Card (CSE Dept)", "Found", "Documents & Cards", "Main Gate Turnstile area", "Belongs to 3rd year student. Handed over to Security Guard Desk.", "Security Gate 1")
    ]
    for title, itype, cat, loc, desc, contact in lost_found_items:
        database.create_lost_found_item(title, itype, cat, loc, desc, contact)

    print("Populating Mess Menu & Feedback...")
    today_str = now.strftime("%Y-%m-%d")
    tomorrow_str = (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    database.set_mess_menu(today_str, 
        breakfast="Masala Dosa, Sambhar, Coconut Chutney, Boiled Eggs, Tea/Coffee", 
        lunch="Paneer Butter Masala, Dal Tadka, Jeera Rice, Phulka Roti, Cucumber Salad, Curd", 
        dinner="Aloo Gobi, Rajma Masala, Steamed Basmati Rice, Chapatis, Gulab Jamun")
    
    database.set_mess_menu(tomorrow_str, 
        breakfast="Poha with Sev & Peanuts, Sprouts, Bread-Butter-Jam, Milk/Tea", 
        lunch="Chole Bhature, Pulao, Boondi Raita, Onion Pickle", 
        dinner="Mix Veg Korma, Dal Makhani, Tawa Roti, Rice, Fruit Custard")

    mess_feedbacks = [
        ("Breakfast", 5, "Masala Dosa was crisp and sambhar had great flavour!", "BH-1 - 102"),
        ("Lunch", 4, "Paneer sabzi was rich and fresh, curd was cold and nice.", "GH-1 - 204"),
        ("Dinner", 4, "Gulab jamun was great! Rajma was nicely cooked.", "BH-2 - 312"),
        ("Breakfast", 3, "Tea was a bit sweet today, please reduce sugar in one container.", "GH-2 - 115")
    ]
    for meal, rt, com, rm in mess_feedbacks:
        database.create_mess_feedback(meal, rt, com, rm)

    print("Populating Visitor Passes...")
    visitors = [
        ("Rajesh Sharma", "Aadhaar Card", "XXXX-XXXX-4912", "Aarav Sharma", "102", "BH-1", "Father visiting to deliver luggage and study material", today_str),
        ("Sunita Reddy", "Driving License", "DL-042019-XXXX", "Kavya Reddy", "115", "GH-2", "Parent visiting for weekend", today_str),
        ("Dr. Ashok Bansal", "College Faculty ID", "FAC-9912", "Devansh Patel", "312", "BH-2", "Academic project mentorship discussion", today_str)
    ]
    for vname, idt, idnum, hstud, hroom, hblk, purp, vdate in visitors:
        vp = database.create_visitor_pass(vname, idt, idnum, hstud, hroom, hblk, purp, vdate)
        database.update_visitor_status(vp, "Checked In")

    print("Populating Audit Log History...")
    database.log_action("TICKET_RESOLVED", "Grievance", "4", "Resolved electrical fan issue in GH-1 Room 204", "Warden - Mr. Joshi")
    database.log_action("GATE_PASS_ISSUED", "LeaveApplication", "1", "Issued Gate Pass GP-BH1-8842 for Aarav Sharma", "Chief Warden Office")
    database.log_action("NOTICE_PUBLISHED", "Notice", "1", "Published water tank cleaning notice for BH-1/BH-2", "Chief Warden Office")

    print("\n[OK] Demo Dataset Successfully Seeded into hostel_care.db!")

if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    seed()
