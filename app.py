# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import datetime
import os
import database

# Page Configuration
st.set_page_config(
    page_title="Campus Hostel Residence Operations & Care Suite",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling for Premium UI
st.markdown("""
<style>
    /* Main Theme Overrides */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Header Container */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: #ffffff;
        padding: 24px 30px;
        border-radius: 12px;
        margin-bottom: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    .main-header p {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 4px;
        margin-bottom: 0;
    }

    /* Warden Ticker Banner */
    .notice-banner {
        background-color: #fef3c7;
        border-left: 5px solid #d97706;
        color: #92400e;
        padding: 12px 18px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 24px;
    }

    /* Metric Cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
    }
    .metric-label {
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
    }

    /* Status Badges */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 700;
    }
    .badge-pending { background-color: #ffedd5; color: #c2410c; }
    .badge-progress { background-color: #fef9c3; color: #854d0e; }
    .badge-resolved { background-color: #dcfce7; color: #15803d; }
    .badge-rejected { background-color: #fee2e2; color: #b91c1c; }
    .badge-emergency { background-color: #991b1b; color: #ffffff; }

    /* Text contrast & Visibility overrides */
    h1, h2, h3, h4, h5, h6 {
        color: #0f172a !important;
    }
    .stMarkdown, .stText, p, label {
        color: #1e293b !important;
    }
    .main-header h1 {
        color: #ffffff !important;
    }
    .main-header p {
        color: #94a3b8 !important;
    }
</style>
""", unsafe_allow_html=True)

# Admin passcode configuration (safely handles Streamlit Secrets or environment with fallback '1234')
def get_admin_passcode():
    try:
        if hasattr(st, "secrets") and "ADMIN_PASSCODE" in st.secrets:
            return str(st.secrets["ADMIN_PASSCODE"])
    except Exception:
        pass
    return str(os.environ.get("ADMIN_PASSCODE", "1234"))

ADMIN_PASSCODE = get_admin_passcode()

# Initialize database on app startup
database.init_db()

# --- HEADER SECTION ---
st.markdown("""
<div class="main-header">
    <h1>🏢 Campus Hostel Residence Operations & Care Suite</h1>
    <p>Digital Maintenance Dispatch • Warden Support • Resident Care Desk</p>
</div>
""", unsafe_allow_html=True)

# Announcement Ticker
latest_notices = database.get_all_notices()
if latest_notices:
    top_n = latest_notices[0]
    ticker_text = f"📢 WARDEN ANNOUNCEMENT: [{top_n['category']}] {top_n['title']} (Target: {top_n['target_block']}) • Emergency Desk: Ext 104"
else:
    ticker_text = "📢 WARDEN ANNOUNCEMENT: Block Maintenance Active • Warden Office: Ext 101 • Medical Room: Ext 108"

st.markdown(f'<div class="notice-banner">{ticker_text}</div>', unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
try:
    st.sidebar.image("https://img.icons8.com/isometric/100/building.png", width=70)
except Exception:
    st.sidebar.markdown("# 🏢")

st.sidebar.title("Hostel Portal Desk")

portal_mode = st.sidebar.radio(
    "Select Portal View",
    ["🎓 Student Resident Portal", "🛡️ Warden & Admin Desk"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📞 Emergency Desk")
st.sidebar.info("""
**Warden Desk:** Ext 101  
**Medical Room:** Ext 108  
**Electrical Duty:** Ext 104  
**Plumbing Duty:** Ext 105
""")

# Quick Stats Widget in Sidebar
counts = database.get_grievance_counts()
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Live System Overview")
st.sidebar.caption(f"**Total Grievances:** {counts['total']}")
st.sidebar.caption(f"**Pending Requests:** {counts['pending']}")
st.sidebar.caption(f"**In Progress:** {counts['in_progress']}")
st.sidebar.caption(f"**Resolved:** {counts['resolved']}")

if counts.get('emergency', 0) > 0:
    st.sidebar.error(f"🚨 **Active Emergencies:** {counts['emergency']}")


# ==========================================
# 🎓 STUDENT RESIDENT PORTAL VIEW
# ==========================================
if portal_mode == "🎓 Student Resident Portal":
    st.header("🎓 Student Resident Desk")
    
    tab_submit, tab_track, tab_notices = st.tabs([
        "📝 Register Complaint", 
        "🔍 Track Status", 
        "📢 Campus Notices"
    ])
    
    # TAB 1: SUBMIT COMPLAINT
    with tab_submit:
        st.subheader("Submit Maintenance / Repair Request")
        st.caption("Please fill in accurate details so our maintenance team can respond promptly.")
        
        with st.form("grievance_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                student_name = st.text_input("Student Full Name *", placeholder="e.g. Rahul Sharma")
                
                block_options = [
                    "BH-1 (Boys Hostel 1)",
                    "BH-2 (Boys Hostel 2)",
                    "BH-3 (Boys Hostel 3)",
                    "GH-1 (Girls Hostel 1)",
                    "GH-2 (Girls Hostel 2)",
                    "IH-1 (International Hostel)"
                ]
                block_full = st.selectbox("Hostel Block *", block_options)
                
                room_number = st.text_input("Room / Bed Number *", placeholder="e.g. B-204")
            
            with col2:
                categories = [
                    "⚡ Electrical Repair (Fan, Light, Switch)",
                    "🚰 Plumbing & Water (Tap, Leak, Flush)",
                    "🧹 Cleaning & Room Sanitation",
                    "🍽️ Food & Mess Quality Complaint",
                    "📶 Wi-Fi & LAN Internet Connectivity",
                    "🚪 Carpentry, Door & Furniture Lock",
                    "🏢 General Facility / AC / Water Cooler",
                    "📦 Miscellaneous / Other Hostel Issue"
                ]
                category = st.selectbox("Maintenance Category *", categories)
                
                priorities = [
                    "🟢 Normal (Standard Duty)",
                    "🟡 Urgent (Same Day Attention)",
                    "🔴 Emergency (Immediate Water/Electrical Hazard)"
                ]
                priority = st.selectbox("Priority Level *", priorities)
            
            description = st.text_area("Issue Description *", placeholder="Describe the problem in detail (location, behavior, urgency)...")
            suggestion = st.text_area("Suggestion / Recommended Solution (Optional)", placeholder="Any suggestions for maintenance team?")
            
            submitted = st.form_submit_button("🚀 Submit Complaint", type="primary", use_container_width=True)
            
            if submitted:
                if not student_name.strip() or not room_number.strip() or not description.strip():
                    st.error("⚠️ Please fill in all required fields (Name, Room Number, and Description).")
                else:
                    clean_block = block_full.split(" (")[0] if " (" in block_full else block_full
                    gid = database.create_grievance(
                        name=student_name.strip(),
                        room=room_number.strip(),
                        category=category,
                        description=description.strip(),
                        block_name=clean_block,
                        priority=priority,
                        suggestion=suggestion.strip()
                    )
                    st.balloons()
                    st.success(f"🎉 **Request Submitted Successfully!**\n\nYour Grievance ID is **#{gid}**. You can track its status under the **Track Status** tab.")

    # TAB 2: TRACK STATUS
    with tab_track:
        st.subheader("Search & Track Complaint Status")
        
        search_col1, search_col2 = st.columns([1, 3])
        with search_col1:
            search_by = st.radio("Search By", ["Grievance Ticket ID", "Room Number / Student Name"])
        
        with search_col2:
            search_query = st.text_input("Enter Ticket ID or Room/Name to Search", placeholder="e.g. 101 or B-204...")
            search_btn = st.button("🔍 Search Database", use_container_width=True)
        
        if search_query or search_btn:
            results = []
            if "Ticket ID" in search_by:
                try:
                    gid = int(search_query.strip().replace("#", ""))
                    g = database.get_grievance_by_id(gid)
                    if g:
                        results = [g]
                except ValueError:
                    st.error("Please enter a valid numeric Ticket ID.")
            else:
                results = database.get_grievance_by_room_or_name(search_query.strip())
            
            if results:
                st.markdown(f"Found **{len(results)}** record(s):")
                for item in results:
                    st_val = item['status']
                    badge_class = "badge-pending"
                    if st_val == "In Progress": badge_class = "badge-progress"
                    elif st_val == "Resolved": badge_class = "badge-resolved"
                    elif st_val == "Rejected": badge_class = "badge-rejected"
                    
                    with st.expander(f"🎫 Ticket #{item['grievance_id']} - {item['category']} ({item['block_name']} Room {item['room_number']})", expanded=True):
                        st.markdown(f"""
                        **Student Name:** {item['student_name']}  |  **Submitted:** {item['date_submitted']}  
                        **Status:** <span class="badge {badge_class}">{st_val}</span>  |  **Priority:** {item['priority']}  
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"**Issue Description:**\n>{item['description']}")
                        
                        if item.get('suggestion'):
                            st.markdown(f"**Student Suggestion:**\n_{item['suggestion']}_")
                            
                        st.markdown("---")
                        st.markdown(f"**Assigned Staff:** {item.get('assigned_staff') or 'Unassigned'}")
                        st.markdown(f"**Warden Remarks:** {item.get('admin_remarks') or 'Awaiting review'}")
                        st.caption(f"Last updated: {item.get('last_updated')}")
            else:
                st.warning("No matching grievance records found. Please check your search term.")

    # TAB 3: CAMPUS NOTICES
    with tab_notices:
        st.subheader("📢 Official Hostel Announcements & Circulars")
        
        block_filter = st.selectbox("Filter by Hostel Block", ["All Blocks", "BH-1", "BH-2", "BH-3", "GH-1", "GH-2", "IH-1"])
        notices = database.get_all_notices(block_filter=block_filter)
        
        if notices:
            for n in notices:
                with st.container():
                    st.markdown(f"""
                    <div class="card-box">
                        <h4 style="margin:0; color:#0f172a;">📢 {n['title']}</h4>
                        <p style="color:#0284c7; font-size:0.85rem; font-weight:600; margin: 4px 0 10px 0;">
                            Target: {n['target_block']} | Category: {n['category']} | Date: {n['date_posted']} | Posted by: {n.get('posted_by', 'Warden Office')}
                        </p>
                        <p style="color:#334155; font-size:0.95rem; margin:0;">{n['content']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No active announcements published for this block.")


# ==========================================
# 🛡️ WARDEN & ADMIN DESK VIEW
# ==========================================
else:
    st.header("🛡️ Warden Administration & Dispatch Operations")
    
    # Password authentication state
    if "admin_authenticated" not in st.session_state:
        st.session_state["admin_authenticated"] = False
        
    if not st.session_state["admin_authenticated"]:
        with st.form("admin_login_form"):
            st.subheader("🔒 Warden Authentication Required")
            input_passcode = st.text_input("Enter Warden Passcode", type="password")
            login_btn = st.form_submit_button("Unlock Warden Desk", type="primary")
            
            if login_btn:
                valid_passcodes = {"1234", "admin123", ADMIN_PASSCODE.strip(), "MySecretWardenPass123"}
                if input_passcode.strip() in valid_passcodes:
                    st.session_state["admin_authenticated"] = True
                    st.success("Authentication successful!")
                    st.rerun()
                else:
                    st.error("Incorrect Passcode. Access denied.")
    else:
        if st.sidebar.button("🔒 Lock Warden Desk"):
            st.session_state["admin_authenticated"] = False
            st.rerun()
            
        admin_tab1, admin_tab2 = st.tabs(["🛡️ Grievance Dispatch Console", "📢 Notice Board Manager"])
        
        # TAB 1: DISPATCH CONSOLE
        with admin_tab1:
            # KPI Metrics Row
            counts = database.get_grievance_counts()
            m1, m2, m3, m4, m5, m6 = st.columns(6)
            
            m1.metric("Total", counts['total'])
            m2.metric("Emergency 🚨", counts.get('emergency', 0))
            m3.metric("Pending 🟧", counts['pending'])
            m4.metric("In Progress 🟨", counts['in_progress'])
            m5.metric("Resolved 🟩", counts['resolved'])
            m6.metric("Rejected 🟥", counts.get('rejected', 0))
            
            st.markdown("---")
            
            # Filter bar
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                filter_block = st.selectbox("Filter Block", ["All", "BH-1", "BH-2", "BH-3", "GH-1", "GH-2", "IH-1"])
            with f_col2:
                filter_status = st.selectbox("Filter Status", ["All", "Pending", "In Progress", "Resolved", "Rejected"])
            with f_col3:
                search_term = st.text_input("Search (ID, Name, Room, Staff)", placeholder="Search grievances...")
                
            grievances = database.get_all_grievances(status_filter=filter_status, block_filter=filter_block, search_query=search_term)
            
            if grievances:
                df = pd.DataFrame(grievances)
                st.subheader(f"Grievances List ({len(df)})")
                
                # Format table
                display_cols = ["grievance_id", "date_submitted", "block_name", "room_number", "student_name", "category", "priority", "status", "assigned_staff", "admin_remarks"]
                st.dataframe(df[display_cols], use_container_width=True)
                
                st.markdown("### ⚡ Dispatch & Action Controls")
                selected_id = st.selectbox("Select Grievance ID to Action", df['grievance_id'].tolist())
                
                if selected_id:
                    selected_item = database.get_grievance_by_id(selected_id)
                    if selected_item:
                        st.info(f"Selected Ticket **#{selected_id}** by {selected_item['student_name']} (Room {selected_item['room_number']}, {selected_item['block_name']})")
                        st.caption(f"**Issue Description:** {selected_item['description']}")
                        
                        with st.form("action_form"):
                            act_col1, act_col2 = st.columns(2)
                            with act_col1:
                                new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Resolved", "Rejected"], index=["Pending", "In Progress", "Resolved", "Rejected"].index(selected_item['status']) if selected_item['status'] in ["Pending", "In Progress", "Resolved", "Rejected"] else 0)
                                new_staff = st.text_input("Assign Staff / Technician", value=selected_item.get('assigned_staff', ''))
                            with act_col2:
                                new_remarks = st.text_area("Warden Remarks / Resolution Notes", value=selected_item.get('admin_remarks', ''))
                                
                            upd_col1, upd_col2 = st.columns([1, 1])
                            with upd_col1:
                                update_btn = st.form_submit_button("💾 Update Status & Dispatch Staff", type="primary", use_container_width=True)
                            with upd_col2:
                                delete_btn = st.form_submit_button("🗑️ Delete Grievance Record", use_container_width=True)
                                
                            if update_btn:
                                database.update_grievance(selected_id, new_status, new_remarks, new_staff)
                                st.success(f"Grievance #{selected_id} updated successfully!")
                                st.rerun()
                                
                            if delete_btn:
                                database.delete_grievance(selected_id)
                                st.warning(f"Grievance #{selected_id} deleted!")
                                st.rerun()

                # Export CSV
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Export Shift Report (CSV)",
                    data=csv_data,
                    file_name=f"hostel_grievance_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No grievances match the current filter criteria.")

        # TAB 2: NOTICE MANAGER
        with admin_tab2:
            st.subheader("📢 Create New Hostel Announcement")
            
            with st.form("create_notice_form", clear_on_submit=True):
                n_title = st.text_input("Announcement Title *", placeholder="e.g. Water Tank Cleaning Notice")
                n_col1, n_col2 = st.columns(2)
                with n_col1:
                    n_cat = st.selectbox("Category", ["📢 General Notice", "⚡ Power Maintenance", "🚰 Water Supply", "🧹 Mess & Sanitation", "🚨 Emergency Alert"])
                with n_col2:
                    n_block = st.selectbox("Target Hostel Block", ["All Blocks", "BH-1", "BH-2", "BH-3", "GH-1", "GH-2", "IH-1"])
                n_content = st.text_area("Notice Content / Message Body *")
                n_posted_by = st.text_input("Posted By", value="Chief Hostel Warden Office")
                
                post_btn = st.form_submit_button("📢 Publish Announcement", type="primary")
                if post_btn:
                    if not n_title.strip() or not n_content.strip():
                        st.error("Title and Content are required.")
                    else:
                        database.create_notice(n_title.strip(), n_content.strip(), n_cat, n_block, n_posted_by)
                        st.success("Notice published successfully!")
                        st.rerun()
                        
            st.markdown("---")
            st.subheader("Manage Published Announcements")
            all_notices = database.get_all_notices()
            if all_notices:
                for noti in all_notices:
                    with st.expander(f"📢 [{noti['target_block']}] {noti['title']} ({noti['date_posted']})"):
                        st.write(noti['content'])
                        if st.button("Delete Notice", key=f"del_notice_{noti['notice_id']}"):
                            database.delete_notice(noti['notice_id'])
                            st.warning("Notice deleted!")
                            st.rerun()
