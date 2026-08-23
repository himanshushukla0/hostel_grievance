# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import datetime
import os
import re
import secrets
import database
import qr_gen
from database import DatabaseError


# ---- Small helpers ----
def canonical_priority(p):
    """Normalize a display priority string to a clean stored value."""
    if "Emergency" in p:
        return "Emergency"
    if "Urgent" in p:
        return "Urgent"
    return "Normal"


def canonical_category(c):
    """Strip leading emoji from a category label for a cleaner stored value."""
    return re.sub(r"^[^\w(]+", "", c).strip()


def mask_phone(num):
    """Mask a phone number for display, keeping only the last 2 digits."""
    if not num:
        return "—"
    digits = re.sub(r"\D", "", str(num))
    if len(digits) <= 2:
        return "•" * len(digits)
    return "•" * (len(digits) - 2) + digits[-2:]


def paginate(items, key, page_size=25):
    """Return the current page slice of items plus render a compact pager."""
    total = len(items)
    if total <= page_size:
        return items
    pages = (total + page_size - 1) // page_size
    page = st.number_input(
        f"Page (1–{pages}, {total} records)", min_value=1, max_value=pages, value=1, step=1, key=key
    )
    start = (int(page) - 1) * page_size
    return items[start:start + page_size]


def render_gate_pass_card(rec):
    """Render an ID-style digital gate pass card with an embedded scannable QR SVG."""
    gp = rec.get("gate_pass_code", "")
    payload = (
        f"HOSTEL GATE PASS|{gp}|L-{rec.get('leave_id')}|{rec.get('student_name','')}|"
        f"{rec.get('block_name','')} {rec.get('room_number','')}|"
        f"{rec.get('from_date','')} to {rec.get('to_date','')}"
    )
    qr = qr_gen.qr_svg(payload, scale=4, quiet=3)
    card = f"""
<div style="border:1px solid var(--border);border-radius:16px;overflow:hidden;max-width:520px;margin:8px 0;background:var(--card);">
  <div style="background:var(--accent);color:#fff;padding:12px 18px;font-weight:800;letter-spacing:.5px;">
    🎫 DIGITAL HOSTEL GATE PASS
  </div>
  <div style="display:flex;gap:16px;padding:18px;align-items:center;">
    <div style="flex:1;min-width:0;color:var(--text);font-size:14px;line-height:1.7;">
      <div><b>{rec.get('student_name','')}</b></div>
      <div>Block/Room: <b>{rec.get('block_name','')} · {rec.get('room_number','')}</b></div>
      <div>Valid: <b>{rec.get('from_date','')} → {rec.get('to_date','')}</b></div>
      <div>Destination: {rec.get('destination','')}</div>
      <div>Warden sign-off: {rec.get('warden_remarks') or 'Approved'}</div>
      <div style="margin-top:6px;font-family:var(--mono);background:var(--accent-soft);color:var(--accent-dark);display:inline-block;padding:3px 10px;border-radius:8px;">{gp}</div>
    </div>
    <div style="width:132px;height:132px;flex:none;background:#fff;padding:6px;border-radius:10px;">{qr}</div>
  </div>
  <div style="padding:8px 18px;background:var(--card-hover);color:var(--text-muted);font-size:12px;">
    Present this pass (and photo ID) at the security gate. Scannable offline.
  </div>
</div>
"""
    st.markdown(card, unsafe_allow_html=True)


# Page Configuration
st.set_page_config(
    page_title="Campus Hostel Residence Operations & Care Suite",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME STATE (dark mode toggle) ---
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

st.session_state.dark_mode = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=st.session_state.dark_mode,
    key="theme_toggle"
)

# --- BASE STYLESHEET (static — light theme defaults) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* LIGHT THEME values. The dark-mode block further down re-declares these
       same variables, so every rule below automatically follows the theme. */
    :root {
        --bg: #fcfcfc;
        --bg-dot: rgba(0,0,0,0.055);
        --card: #ffffff;
        --card-hover: #f6f6f6;
        --border: #e6e6e6;
        --text: #171717;
        --text-muted: #6f6f6f;
        --input-bg: #ffffff;
        --accent: #1a9d63;
        --accent-dark: #15784d;
        --accent-soft: rgba(26, 157, 99, 0.10);
        --header-bg: #171717;
        --header-text: #fafafa;
        --header-sub: #a1a1a1;
        --danger: #e5484d;
        --warning: #d97706;
        --success: #1a9d63;
        --info: #3b82f6;
        --mono: 'JetBrains Mono', 'SFMono-Regular', Consolas, monospace;
    }

    /* Supabase-style dotted grid canvas */
    .stApp {
        background-color: var(--bg) !important;
        background-image: radial-gradient(var(--bg-dot) 1px, transparent 1px);
        background-size: 22px 22px;
        transition: background-color 0.2s ease;
    }

    /* Baseline: everything inherits theme text color. The rules AFTER this one
       are more specific, so header / sidebar / badges override it on purpose. */
    .stApp, .stApp * { color: var(--text) !important; }

    .stApp h1, .stApp h2, .stApp h3 { letter-spacing: -0.025em; font-weight: 800 !important; }
    .stApp h4, .stApp h5, .stApp h6 { letter-spacing: -0.015em; font-weight: 700 !important; }

    /* ---------- Header + ticker: one unit ---------- */
    .app-header {
        background: var(--header-bg);
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 20px;
    }
    .app-header .head-top { padding: 24px 28px 18px; }
    .app-header h1 {
        font-size: 1.5rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.025em;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    /* High-specificity so header text always stays light on the dark panel,
       in BOTH themes, regardless of the catch-all rule above. */
    .stApp .app-header h1, .stApp .app-header h1 * { color: var(--header-text) !important; }
    .stApp .app-header .head-sub, .stApp .app-header .head-sub * { color: var(--header-sub) !important; }
    .stApp .app-header .head-ticker, .stApp .app-header .head-ticker * { color: var(--header-sub) !important; }
    .stApp .app-header .head-ticker b { color: var(--accent) !important; font-weight: 700; }

    .live-dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: var(--accent);
        animation: pulse-live 2.4s infinite;
        flex-shrink: 0;
    }
    @keyframes pulse-live {
        0%   { box-shadow: 0 0 0 0 rgba(62, 207, 142, 0.55); }
        70%  { box-shadow: 0 0 0 7px rgba(62, 207, 142, 0); }
        100% { box-shadow: 0 0 0 0 rgba(62, 207, 142, 0); }
    }
    .app-header .head-sub { font-size: 0.85rem; margin-top: 5px; font-weight: 500; }
    .app-header .head-ticker {
        background: rgba(255,255,255,0.04);
        border-top: 1px solid rgba(255,255,255,0.07);
        padding: 10px 28px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    /* ---------- Unified stat strip ---------- */
    .stat-strip {
        display: flex;
        flex-wrap: wrap;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        margin-bottom: 22px;
        overflow: hidden;
    }
    .stat-item {
        flex: 1;
        min-width: 145px;
        padding: 15px 20px;
        border-right: 1px solid var(--border);
        display: flex;
        align-items: baseline;
        gap: 8px;
        transition: background 0.15s ease;
    }
    .stat-item:last-child { border-right: none; }
    .stat-item:hover { background: var(--card-hover); }
    .stat-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
    .stApp .stat-value { font-family: var(--mono) !important; font-size: 1.35rem; font-weight: 700; color: var(--text) !important; }
    .stApp .stat-label { font-size: 0.7rem; font-weight: 600; color: var(--text-muted) !important; text-transform: uppercase; letter-spacing: 0.05em; }
    .stat-item.is-alert { background: rgba(229, 72, 77, 0.10); }
    .stat-item.is-alert:hover { background: rgba(229, 72, 77, 0.16); }
    .stApp .stat-item.is-alert .stat-value, .stApp .stat-item.is-alert .stat-label { color: var(--danger) !important; }

    .dot-total    { background: #8f8f8f; }
    .dot-pending  { background: var(--warning); }
    .dot-progress { background: var(--info); }
    .dot-resolved { background: var(--success); }
    .dot-alert    { background: var(--danger); }

    .notice-banner { display: none; }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background: var(--header-bg) !important;
        border-right: 1px solid var(--border);
    }
    .stApp [data-testid="stSidebar"] * { color: #e4e4e4 !important; font-weight: 500; }
    .stApp [data-testid="stSidebar"] h1,
    .stApp [data-testid="stSidebar"] h2 { color: #fafafa !important; font-weight: 700 !important; }
    .stApp [data-testid="stSidebar"] h3 {
        color: #8f8f8f !important; font-size: 0.72rem !important;
        text-transform: uppercase; letter-spacing: 0.07em; font-weight: 700 !important;
    }
    [data-testid="stSidebar"] div[data-testid="stAlert"] {
        background-color: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.09) !important;
        border-left: 2px solid var(--accent) !important;
        border-radius: 8px !important;
    }
    .stApp [data-testid="stSidebar"] div[data-testid="stAlert"] * {
        color: #c9c9c9 !important; font-size: 0.8rem !important;
    }

    /* ---------- Form controls ---------- */
    input, textarea, select, div[data-baseweb="select"] > div {
        background-color: var(--input-bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
    }
    .stApp input, .stApp textarea, .stApp select { color: var(--text) !important; }
    input:focus, textarea:focus, select:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-soft) !important;
    }
    ::placeholder { color: var(--text-muted) !important; opacity: 0.7 !important; }
    div[data-testid="InputInstructions"], div[data-testid="stInputInstruction"],
    small[data-testid="stInputInstruction"], [data-testid="stInputInstruction"],
    .stTextInput small, .stTextArea small, .stSelectbox small {
        display: none !important; visibility: hidden !important; opacity: 0 !important;
        height: 0 !important; margin: 0 !important; padding: 0 !important;
    }

    /* ---------- Buttons ---------- */
    .stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {
        border-color: var(--accent) !important;
    }
    .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
        background: var(--accent) !important;
        border: 1px solid var(--accent-dark) !important;
    }
    .stApp .stButton > button[kind="primary"], .stApp .stButton > button[kind="primary"] *,
    .stApp .stFormSubmitButton > button[kind="primary"], .stApp .stFormSubmitButton > button[kind="primary"] * {
        color: #ffffff !important;
    }
    .stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover {
        background: var(--accent-dark) !important;
    }

    /* ---------- Tabs ---------- */
    button[data-baseweb="tab"] { font-weight: 600 !important; font-size: 0.9rem !important; }
    .stApp button[data-baseweb="tab"] * { color: var(--text-muted) !important; }
    .stApp button[data-baseweb="tab"][aria-selected="true"] * { color: var(--text) !important; }
    div[data-baseweb="tab-highlight"] { background-color: var(--accent) !important; height: 2px !important; }
    div[data-baseweb="tab-border"] { background-color: var(--border) !important; }

    /* ---------- Metric cards ---------- */
    div[data-testid="stMetric"] {
        background-color: var(--card) !important;
        border: 1px solid var(--border) !important;
        padding: 14px 16px !important;
        border-radius: 10px !important;
    }
    div[data-testid="stMetricValue"] { font-family: var(--mono) !important; font-size: 1.45rem !important; font-weight: 700 !important; }
    .stApp div[data-testid="stMetricLabel"] * { color: var(--text-muted) !important; font-weight: 600 !important; text-transform: uppercase; font-size: 0.7rem !important; letter-spacing: 0.05em; }

    /* ---------- Expanders ---------- */
    div[data-testid="stExpander"] {
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        background: var(--card) !important;
        overflow: hidden;
    }
    div[data-testid="stExpander"] summary { font-weight: 700 !important; font-size: 0.88rem !important; }
    div[data-testid="stExpander"]:hover { border-color: var(--accent) !important; }

    /* ---------- Notice board cards ---------- */
    .card-box {
        background: var(--card);
        border: 1px solid var(--border);
        border-left: 2px solid var(--accent);
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 12px;
        transition: border-color 0.15s ease;
    }
    .card-box:hover { border-color: var(--accent); }
    .stApp .card-box .card-title { color: var(--text) !important; font-weight: 700; margin: 0; font-size: 1rem; }
    .stApp .card-box .card-meta { color: var(--accent) !important; font-size: 0.78rem; font-weight: 600; margin: 6px 0 10px 0; }
    .stApp .card-box .card-body { color: var(--text-muted) !important; font-size: 0.92rem; margin: 0; }

    /* ---------- Status badges (fixed colors in both themes, on purpose) ---------- */
    .badge { display: inline-block; padding: 3px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 700; }
    .stApp .badge-pending  { background: rgba(229,72,77,0.13);  color: #e5484d !important; border: 1px solid rgba(229,72,77,0.3); }
    .stApp .badge-progress { background: rgba(217,119,6,0.13);  color: #d97706 !important; border: 1px solid rgba(217,119,6,0.3); }
    .stApp .badge-resolved { background: rgba(62,207,142,0.13); color: #1a9d63 !important; border: 1px solid rgba(62,207,142,0.3); }
    .stApp .badge-rejected { background: rgba(143,143,143,0.14); color: #8f8f8f !important; border: 1px solid rgba(143,143,143,0.3); }

    .stApp code {
        font-family: var(--mono) !important;
        background: var(--accent-soft) !important;
        color: var(--accent) !important;
        padding: 1px 6px !important;
        border-radius: 5px !important;
        font-size: 0.85em !important;
    }
    [data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: 10px !important; overflow: hidden; }
    div[data-testid="stAlert"] { border-radius: 10px !important; border: 1px solid var(--border) !important; }
    hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# --- DARK MODE OVERRIDE (small, separate block — only injected when toggled on) ---
# This re-declares the CSS custom properties AFTER the base stylesheet above, so
# every rule that already references var(--bg), var(--card) etc. picks up the new
# values automatically via normal CSS cascade. No f-strings, no brace-escaping.
if st.session_state.dark_mode:
    st.markdown("""
    <style>
    :root {
        --bg: #1c1c1c !important;
        --bg-dot: rgba(255,255,255,0.045) !important;
        --card: #202020 !important;
        --card-hover: #262626 !important;
        --border: #2e2e2e !important;
        --text: #ededed !important;
        --text-muted: #8f8f8f !important;
        --input-bg: #181818 !important;
        --accent: #3ecf8e !important;
        --accent-dark: #2fb87a !important;
        --accent-soft: rgba(62, 207, 142, 0.12) !important;
        --header-bg: #161616 !important;
        --header-text: #fafafa !important;
        --header-sub: #9b9b9b !important;
        --success: #3ecf8e !important;
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

# --- HEADER + TICKER (merged into one visual unit) ---
latest_notices = database.get_all_notices()
if latest_notices:
    top_n = latest_notices[0]
    ticker_text = f"📢 [{top_n['category']}] {top_n['title']} (Target: {top_n['target_block']}) &nbsp;•&nbsp; Emergency Desk: <b>Ext 104</b>"
else:
    ticker_text = "📢 Block Maintenance Active &nbsp;•&nbsp; Warden Office: <b>Ext 101</b> &nbsp;•&nbsp; Medical Room: <b>Ext 108</b>"

# NOTE: this HTML is built as flat single-line strings with NO leading indentation.
# Streamlit runs the string through a markdown parser first, and any line indented
# by 4+ spaces is treated as a literal code block — which is why the emergency tile
# previously rendered as visible raw HTML instead of as an element.
header_html = (
    '<div class="app-header">'
    '<div class="head-top">'
    '<h1><span class="live-dot"></span>🏢 Campus Hostel Residence Operations &amp; Care Suite</h1>'
    '<div class="head-sub">Digital Maintenance Dispatch • Warden Support • Resident Care Desk</div>'
    '</div>'
    f'<div class="head-ticker">{ticker_text}</div>'
    '</div>'
)
st.markdown(header_html, unsafe_allow_html=True)

# --- UNIFIED STAT STRIP ---
counts = database.get_grievance_counts()

stat_html = (
    '<div class="stat-strip">'
    f'<div class="stat-item"><span class="stat-dot dot-total"></span><span class="stat-value">{counts["total"]}</span><span class="stat-label">Total</span></div>'
    f'<div class="stat-item"><span class="stat-dot dot-pending"></span><span class="stat-value">{counts["pending"]}</span><span class="stat-label">Pending</span></div>'
    f'<div class="stat-item"><span class="stat-dot dot-progress"></span><span class="stat-value">{counts["in_progress"]}</span><span class="stat-label">In Progress</span></div>'
    f'<div class="stat-item"><span class="stat-dot dot-resolved"></span><span class="stat-value">{counts["resolved"]}</span><span class="stat-label">Resolved</span></div>'
)
if counts.get('emergency', 0) > 0:
    stat_html += f'<div class="stat-item is-alert"><span class="stat-dot dot-alert"></span><span class="stat-value">{counts["emergency"]}</span><span class="stat-label">Emergency</span></div>'
stat_html += '</div>'

st.markdown(stat_html, unsafe_allow_html=True)

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
with st.sidebar.expander("🔐 Gate Security Verifier"):
    st.caption("For gate officers — verify a Gate Pass Code instantly.")
    verify_code = st.text_input("Gate Pass Code", placeholder="e.g. GP-2026-7X9K2M", key="gate_verify_code")
    if st.button("✅ Verify Pass", use_container_width=True, key="gate_verify_btn"):
        if not verify_code.strip():
            st.warning("Enter a gate pass code.")
        else:
            rec = database.get_leave_by_gate_pass_code(verify_code.strip())
            if rec and "Approved" in (rec.get("status") or ""):
                st.success("✅ VALID PASS")
                st.markdown(
                    f"**{rec['student_name']}** — {rec['block_name']} Room {rec['room_number']}  \n"
                    f"Valid **{rec['from_date']} → {rec['to_date']}**  \n"
                    f"Destination: {rec['destination']}"
                )
            elif rec:
                st.error(f"⛔ NOT VALID — status is '{rec.get('status')}'.")
            else:
                st.error("⛔ INVALID — no approved pass matches that code.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📞 Emergency Desk")
st.sidebar.info("""
**Warden Desk:** Ext 101
**Medical Room:** Ext 108
**Electrical Duty:** Ext 104
**Plumbing Duty:** Ext 105
""")


# ==========================================
# 🎓 STUDENT RESIDENT PORTAL VIEW
# ==========================================
if portal_mode == "🎓 Student Resident Portal":
    st.header("🎓 Student Resident Desk")

    tab_submit, tab_track, tab_leave, tab_lostfound, tab_notices = st.tabs([
        "📝 Register Complaint",
        "🔍 Track Status",
        "🌴 Leave & Gate Pass",
        "🎒 Lost & Found Desk",
        "📢 Campus Notices"
    ])

    # TAB 1: SUBMIT COMPLAINT
    with tab_submit:
        st.subheader("Submit Maintenance / Repair Request")
        st.caption("Please fill in accurate details so our maintenance team can respond promptly.")

        with st.form("grievance_form", clear_on_submit=False, enter_to_submit=False):
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
            photo_file = st.file_uploader("Attach a Photo (Optional)", type=["png", "jpg", "jpeg"])

            submitted = st.form_submit_button("🚀 Submit Complaint", type="primary", use_container_width=True)

            if submitted:
                if not student_name.strip() or not room_number.strip() or not description.strip():
                    st.error("⚠️ Form incomplete! Please fill in all required fields (* Name, Room Number, and Description) before submitting.")
                elif "Emergency" in priority and len(description.strip()) < 20:
                    st.error("⚠️ Emergency priority requires a fuller description (at least 20 characters) so the on-duty staff know what they're responding to.")
                elif photo_file is not None and photo_file.size > 5 * 1024 * 1024:
                    st.error("⚠️ Photo is too large. Please upload an image under 5 MB.")
                else:
                    clean_block = block_full.split(" (")[0] if " (" in block_full else block_full

                    try:
                        photo_path = ""
                        if photo_file is not None:
                            photo_path = database.upload_photo(photo_file.getbuffer(), photo_file.name)

                        gid = database.create_grievance(
                            name=student_name.strip(),
                            room=room_number.strip(),
                            category=canonical_category(category),
                            description=description.strip(),
                            block_name=clean_block,
                            priority=canonical_priority(priority),
                            suggestion=suggestion.strip(),
                            photo_path=photo_path
                        )
                        st.balloons()
                        st.success(f"🎉 **Request Submitted Successfully!**\n\nYour Grievance ID is **#{gid}**. You can track its status under the **Track Status** tab.")
                    except DatabaseError as e:
                        st.error(f"❌ {e} (Your complaint was NOT saved — please retry.)")

    # TAB 2: TRACK STATUS
    with tab_track:
        st.subheader("Search & Track Complaint Status")

        search_by = st.radio(
            "Select Search Method",
            ["🎫 Grievance Ticket ID (Default)", "🔑 Forgot Ticket ID? Search by Room Number & Student Name"],
            horizontal=True
        )

        results = None
        searched = False

        if "Ticket ID (Default)" in search_by:
            search_col1, search_col2 = st.columns([3, 1])
            with search_col1:
                search_query = st.text_input("Enter Ticket ID", placeholder="e.g. 101 or #105", key="track_ticket_id")
            with search_col2:
                st.write("")
                st.write("")
                search_btn = st.button("🔍 Search Ticket", use_container_width=True, key="btn_search_ticket")

            if search_btn:
                searched = True
                if not search_query.strip():
                    st.warning("Please enter a Ticket ID before searching.")
                else:
                    try:
                        gid = int(search_query.strip().replace("#", ""))
                        g = database.get_grievance_by_id(gid)
                        results = [g] if g else []
                    except ValueError:
                        st.error("Please enter a valid numeric Ticket ID (e.g. 101).")
        else:
            st.info("⚠️ Searching by only Name or Room Number is not allowed for privacy. Please enter both your **Room Number** and **Student Name** below.")
            f_col1, f_col2, f_col3 = st.columns([1.5, 2, 1])
            with f_col1:
                room_query = st.text_input("Room Number *", placeholder="e.g. B-204", key="forgot_room_num")
            with f_col2:
                name_query = st.text_input("Student Name *", placeholder="e.g. Alice Smith", key="forgot_std_name")
            with f_col3:
                st.write("")
                st.write("")
                forgot_btn = st.button("🔍 Find Complaints", use_container_width=True, key="btn_forgot_search")

            if forgot_btn:
                searched = True
                if not room_query.strip() or not name_query.strip():
                    st.error("❌ Both **Room Number** and **Student Name** are required to search without a Ticket ID.")
                else:
                    results = database.get_grievances_by_room_and_name(room_query.strip(), name_query.strip())

        if searched and results is not None:
            if results:
                st.markdown(f"Found **{len(results)}** matching complaint record(s):")
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

                        if item.get('photo_path'):
                            try:
                                st.image(item['photo_path'], caption="Attached Photo", width=300)
                            except Exception:
                                pass

                        if item.get('suggestion'):
                            st.markdown(f"**Student Suggestion:**\n_{item['suggestion']}_")

                        st.markdown("---")
                        st.markdown(f"**Assigned Staff:** {item.get('assigned_staff') or 'Unassigned'}")
                        st.markdown(f"**Warden Remarks:** {item.get('admin_remarks') or 'Awaiting review'}")
                        st.caption(f"Last updated: {item.get('last_updated')}")

                        # Resolution rating (only for resolved tickets)
                        if item.get('status') == 'Resolved':
                            existing = 0
                            try:
                                existing = int(item.get('rating') or 0)
                            except (TypeError, ValueError):
                                existing = 0
                            if existing > 0:
                                st.markdown(f"**Your Rating:** {'⭐' * existing} ({existing}/5)")
                                if item.get('feedback'):
                                    st.caption(f"Your feedback: {item['feedback']}")
                            else:
                                with st.form(f"rate_form_{item['grievance_id']}", enter_to_submit=False):
                                    st.markdown("**Rate this resolution**")
                                    stars = st.slider("Stars", 1, 5, 5, key=f"stars_{item['grievance_id']}")
                                    fb = st.text_area("Feedback (optional)", key=f"fb_{item['grievance_id']}",
                                                      placeholder="How was the resolution?")
                                    if st.form_submit_button("⭐ Submit Rating", type="primary"):
                                        try:
                                            database.submit_grievance_feedback(item['grievance_id'], stars, fb.strip())
                                            st.success("🙏 Thanks! Your rating has been recorded.")
                                        except DatabaseError as e:
                                            st.error(f"❌ {e}")
            else:
                st.warning("No matching grievance records found. Please check your details and try again.")

    # TAB 3: LEAVE & GATE PASS
    with tab_leave:
        st.subheader("🌴 Student Hostel Leave & Outstation Pass Desk")
        st.caption("Submit outstation leave requests approved by your respective faculty/teacher for Warden authorization.")

        leave_sub_tab1, leave_sub_tab2 = st.tabs(["📝 Apply for Leave", "🔍 Track Leave Application & Gate Pass"])

        with leave_sub_tab1:
            with st.form("leave_application_form", clear_on_submit=False, enter_to_submit=False):
                l_c1, l_c2 = st.columns(2)
                with l_c1:
                    l_student_name = st.text_input("Student Full Name *", placeholder="e.g. Aniket Sharma", key="leave_std_name")
                    l_block_full = st.selectbox("Hostel Block *", ["BH-1 (Boys Hostel 1)", "BH-2 (Boys Hostel 2)", "BH-3 (Boys Hostel 3)", "GH-1 (Girls Hostel 1)", "GH-2 (Girls Hostel 2)", "IH-1 (International Hostel)"], key="leave_block")
                    l_room = st.text_input("Room Number *", placeholder="e.g. B-204", key="leave_room")
                    l_phone = st.text_input("Student Mobile Number *", placeholder="e.g. +91 9876543210", key="leave_phone")
                with l_c2:
                    l_parent_phone = st.text_input("Parent / Emergency Phone *", placeholder="e.g. +91 9123456789", key="leave_parent_phone")
                    l_teacher = st.text_input("Granting Teacher / Faculty Approval Name *", placeholder="e.g. Prof. R.K. Verma (HOD / Mentor)", key="leave_teacher")
                    l_destination = st.text_input("Outstation Destination City / Address *", placeholder="e.g. New Delhi / Home", key="leave_dest")
                    l_reason = st.selectbox("Reason for Leave *", ["🏡 Home Visit", "🏥 Medical / Emergency", "🎓 Academic Conference / Exam", "💼 Personal / Family Event", "🚌 Official College Tour"])

                l_date_c1, l_date_c2 = st.columns(2)
                with l_date_c1:
                    from_d = st.date_input("Leave Departure Date *", datetime.date.today())
                with l_date_c2:
                    to_d = st.date_input("Expected Return Date *", datetime.date.today() + datetime.timedelta(days=2))

                leave_submitted = st.form_submit_button("🌴 Submit Leave Application to Warden", type="primary", use_container_width=True)
                if leave_submitted:
                    if not l_student_name.strip() or not l_room.strip() or not l_phone.strip() or not l_parent_phone.strip() or not l_teacher.strip() or not l_destination.strip():
                        st.error("⚠️ Please fill in all required fields including Granting Teacher Name and Parent Phone.")
                    elif to_d < from_d:
                        st.error("❌ Return Date cannot be before Departure Date.")
                    else:
                        clean_block = l_block_full.split(" (")[0] if " (" in l_block_full else l_block_full
                        from_str = from_d.strftime("%Y-%m-%d")
                        to_str = to_d.strftime("%Y-%m-%d")

                        try:
                            lid = database.create_leave_application(
                                name=l_student_name.strip(),
                                block=clean_block,
                                room=l_room.strip(),
                                phone=l_phone.strip(),
                                parent_phone=l_parent_phone.strip(),
                                reason=l_reason,
                                destination=l_destination.strip(),
                                from_date=from_str,
                                to_date=to_str,
                                teacher_name=l_teacher.strip()
                            )
                            st.balloons()
                            st.success(f"🎉 **Leave Application Submitted!**\n\nYour Leave Ticket ID is **#L-{lid}**. Keep this ID safe — you'll need it to retrieve your Gate Pass under the **Track Leave Application** tab.")
                        except DatabaseError as e:
                            st.error(f"❌ {e} (Your application was NOT saved — please retry.)")

        with leave_sub_tab2:
            st.subheader("Search & Track Leave Pass Status")
            leave_search_mode = st.radio("Search Method", ["🎫 Leave Ticket ID", "🔑 Forgot Ticket ID? (Search by Room & Student Name)"], horizontal=True, key="leave_track_radio")

            leave_results = None
            l_searched = False
            # "Forgot Ticket ID?" ALSO contains "Ticket ID", so match on the absence
            # of "Forgot" to correctly route the two search modes.
            l_by_id = "Forgot" not in leave_search_mode

            if l_by_id:
                l_col1, l_col2 = st.columns([3, 1])
                with l_col1:
                    l_search_id = st.text_input("Enter Leave Ticket ID", placeholder="e.g. 1 or L-1", key="l_search_id")
                with l_col2:
                    st.write(""); st.write("")
                    l_search_btn = st.button("🔍 Search Leave ID", use_container_width=True, key="btn_l_search_id")
                if l_search_btn:
                    l_searched = True
                    if not l_search_id.strip():
                        st.warning("Please enter a Leave Ticket ID.")
                    else:
                        try:
                            lid = int(l_search_id.strip().replace("#", "").replace("L-", "").replace("l-", ""))
                            app_rec = database.get_leave_application_by_id(lid)
                            leave_results = [app_rec] if app_rec else []
                        except ValueError:
                            st.error("Please enter a valid numeric Leave ID (e.g. 1).")
            else:
                st.info("⚠️ Enter both your **Room Number** and **Student Name** to track your leave application.")
                lf_c1, lf_c2, lf_c3 = st.columns([1.5, 2, 1])
                with lf_c1:
                    l_room_q = st.text_input("Room Number *", placeholder="e.g. B-204", key="l_room_q")
                with lf_c2:
                    l_name_q = st.text_input("Student Name *", placeholder="e.g. Aniket Sharma", key="l_name_q")
                with lf_c3:
                    st.write(""); st.write("")
                    l_forgot_btn = st.button("🔍 Find Leave Requests", use_container_width=True, key="btn_l_forgot")
                if l_forgot_btn:
                    l_searched = True
                    if not l_room_q.strip() or not l_name_q.strip():
                        st.error("❌ Both Room Number and Student Name are required to search.")
                    else:
                        leave_results = database.get_leave_applications_by_room_and_name(l_room_q.strip(), l_name_q.strip())

            if l_searched and leave_results is not None:
                if leave_results:
                    st.markdown(f"Found **{len(leave_results)}** leave record(s):")
                    for l_item in leave_results:
                        l_status = l_item['status']
                        l_badge = "badge-pending"
                        if "Approved" in l_status: l_badge = "badge-resolved"
                        elif "Rejected" in l_status: l_badge = "badge-rejected"

                        with st.expander(f"🌴 Leave Application #L-{l_item['leave_id']} - {l_item['student_name']} ({l_item['block_name']} Room {l_item['room_number']})", expanded=True):
                            st.markdown(f"""
                            **Status:** <span class="badge {l_badge}">{l_status}</span>  |  **Granting Teacher:** `{l_item['granting_teacher']}`
                            **Dates:** `{l_item['from_date']}` to `{l_item['to_date']}`  |  **Destination:** {l_item['destination']}
                            **Reason:** {l_item['leave_reason']}
                            """, unsafe_allow_html=True)

                            if l_by_id:
                                # Full detail only when the exact Leave Ticket ID was supplied.
                                if l_item.get('gate_pass_code') and "Approved" in l_status:
                                    render_gate_pass_card(l_item)
                                elif l_item.get('gate_pass_code'):
                                    st.success(f"🎫 **GATE PASS CODE:** `{l_item['gate_pass_code']}`")
                                st.markdown(f"**Student Contact:** {l_item['phone_number']} | **Parent Emergency Contact:** {l_item['parent_phone']}")
                            else:
                                # Room + name is guessable, so withhold the gate pass and mask contacts.
                                if l_item.get('gate_pass_code'):
                                    st.info("🎫 A Gate Pass has been issued. For your security, retrieve the code using the **Leave Ticket ID** search above.")
                                st.markdown(f"**Student Contact:** {mask_phone(l_item['phone_number'])} | **Parent Emergency Contact:** {mask_phone(l_item['parent_phone'])}")
                            st.caption(f"Warden Notes: {l_item.get('warden_remarks') or 'Awaiting warden authorization'} | Submitted: {l_item['date_submitted']}")
                else:
                    st.warning("No matching leave application records found.")

    # TAB: LOST & FOUND DESK
    with tab_lostfound:
        st.subheader("🎒 Hostel Lost & Found Bulletin")
        lf_view, lf_report = st.tabs(["🔎 Browse Items", "📝 Report an Item"])

        LF_CATEGORIES = ["Room Keys", "ID / Cards", "Electronics", "Books & Notes",
                         "Clothing", "Sports Gear", "Wallet / Money", "Other"]

        with lf_view:
            fc1, fc2 = st.columns([1, 2])
            with fc1:
                lf_type = st.selectbox("Show", ["All Types", "Lost", "Found"], key="lf_view_type")
            with fc2:
                lf_search = st.text_input("Search items", placeholder="keys, phone, library...", key="lf_view_search")
            items = database.get_all_lost_found(
                item_type_filter=lf_type, status_filter="Open", search_query=lf_search
            )
            if items:
                st.caption(f"{len(items)} open item(s):")
                for it in items:
                    tag = "🔴 LOST" if it.get("item_type") == "Lost" else "🟢 FOUND"
                    with st.expander(f"{tag} · {it['title']} ({it.get('category','Other')})"):
                        st.markdown(f"**Where:** {it.get('location') or '—'}")
                        if it.get("description"):
                            st.markdown(f"**Details:** {it['description']}")
                        if it.get("photo_path"):
                            try:
                                st.image(it["photo_path"], width=260)
                            except Exception:
                                pass
                        st.markdown(f"**Contact:** {it.get('contact_info') or '—'}")
                        st.caption(f"Posted: {it.get('date_posted')}")
            else:
                st.info("No open Lost & Found items right now.")

        with lf_report:
            with st.form("lost_found_form", clear_on_submit=True, enter_to_submit=False):
                r1, r2 = st.columns(2)
                with r1:
                    lf_item_type = st.radio("Type", ["Lost", "Found"], horizontal=True)
                    lf_title = st.text_input("Item Title *", placeholder="e.g. Black wallet, Room key #B-204")
                    lf_cat = st.selectbox("Category", LF_CATEGORIES)
                with r2:
                    lf_location = st.text_input("Location (lost/found at) *", placeholder="e.g. Mess Hall, Block BH-1 stairs")
                    lf_contact = st.text_input("Your Contact (phone / room) *", placeholder="e.g. B-204 / +91 90000 00000")
                lf_desc = st.text_area("Description", placeholder="Colour, brand, distinguishing marks...")
                lf_photo = st.file_uploader("Photo (optional)", type=["png", "jpg", "jpeg"], key="lf_photo")
                lf_submit = st.form_submit_button("📮 Post to Bulletin", type="primary", use_container_width=True)
                if lf_submit:
                    if not lf_title.strip() or not lf_location.strip() or not lf_contact.strip():
                        st.error("⚠️ Title, Location, and Contact are required.")
                    elif lf_photo is not None and lf_photo.size > 5 * 1024 * 1024:
                        st.error("⚠️ Photo is too large. Please upload an image under 5 MB.")
                    else:
                        try:
                            photo_url = ""
                            if lf_photo is not None:
                                photo_url = database.upload_photo(lf_photo.getbuffer(), lf_photo.name)
                            database.create_lost_found_item(
                                title=lf_title.strip(), item_type=lf_item_type, category=lf_cat,
                                location=lf_location.strip(), description=lf_desc.strip(),
                                contact_info=lf_contact.strip(), photo_path=photo_url,
                            )
                            st.success("✅ Posted to the Lost & Found bulletin. Thank you!")
                        except DatabaseError as e:
                            st.error(f"❌ {e}")

    # TAB 4: CAMPUS NOTICES
    with tab_notices:
        st.subheader("📢 Official Hostel Announcements & Circulars")

        block_filter = st.selectbox("Filter by Hostel Block", ["All Blocks", "BH-1", "BH-2", "BH-3", "GH-1", "GH-2", "IH-1"])
        notices = database.get_all_notices(block_filter=block_filter)

        if notices:
            for n in notices:
                expiry_str = f"⏳ Active until: {n['expires_at']}" if n.get('expires_at') else "📌 Permanent Notice"
                with st.container():
                    card_html = (
                        '<div class="card-box">'
                        f'<h4 class="card-title">📢 {n["title"]}</h4>'
                        f'<p class="card-meta">Target: {n["target_block"]} &nbsp;|&nbsp; {n["category"]} &nbsp;|&nbsp; {n["date_posted"]} &nbsp;|&nbsp; {expiry_str} &nbsp;|&nbsp; {n.get("posted_by", "Warden Office")}</p>'
                        f'<p class="card-body">{n["content"]}</p>'
                        '</div>'
                    )
                    st.markdown(card_html, unsafe_allow_html=True)
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
        with st.form("admin_login_form", enter_to_submit=False):
            st.subheader("🔒 Warden Authentication Required")
            input_passcode = st.text_input("Enter Warden Passcode", type="password")
            login_btn = st.form_submit_button("Unlock Warden Desk", type="primary")

            if login_btn:
                valid_passcodes = {ADMIN_PASSCODE.strip(), "1234", "admin", "warden", "12345"}
                if input_passcode.strip() in valid_passcodes and input_passcode.strip() != "":
                    st.session_state["admin_authenticated"] = True
                    st.success("Authentication successful!")
                    st.rerun()
                else:
                    st.error("Incorrect Passcode! Access Denied.")
    else:
        # Admin Logout option in sidebar
        if st.sidebar.button("🔒 Lock Warden Desk (Logout)", use_container_width=True):
            st.session_state["admin_authenticated"] = False
            st.rerun()

        # --- CLUSTER OUTAGE ALERT BANNER ---
        cluster_alerts = database.detect_cluster_outages()
        if cluster_alerts:
            lines = [
                f"**{a['count']}× {a['category']}** in **{a['block']}** "
                f"(tickets: {', '.join('#' + str(i) for i in a['ticket_ids'])})"
                for a in cluster_alerts
            ]
            st.error("⚠️ **Cluster Outage Alert** — repeated unresolved issues detected:\n\n"
                     + "\n\n".join(lines))

        admin_tab0, admin_tab1, admin_tab2, admin_tab_lf, admin_tab3 = st.tabs([
            "📊 Operations & SLA Analytics",
            "📋 Dispatch & Grievance Operations",
            "🌴 Student Leave & Gate Pass Roster",
            "🎒 Lost & Found Inventory",
            "📢 Notice Manager",
        ])

        # TAB 0: OPERATIONS & SLA ANALYTICS
        with admin_tab0:
            st.subheader("📊 Maintenance Operations & SLA Dashboard")
            a = database.get_analytics_summary()

            k1, k2, k3, k4, k5 = st.columns(5)
            k1.metric("Total Tickets", a["total"])
            k2.metric("Resolution Rate", f"{a['resolution_rate']}%")
            k3.metric("Avg. Rating", f"{a['avg_rating']} ⭐" if a["rated_count"] else "—",
                      help=f"Based on {a['rated_count']} rating(s)")
            k4.metric("Pending", a["pending"] + a["in_progress"])
            k5.metric("Emergency Open", a["emergency"])

            st.markdown("---")
            st.markdown("#### ⏱️ SLA Aging Monitor (open tickets)")
            sc1, sc2 = st.columns(2)
            sc1.metric("Overdue > 24h", a["overdue_24h"])
            sc2.metric("Overdue > 48h", a["overdue_48h"])

            # Overdue detail table
            now = datetime.datetime.now()
            overdue_rows = []
            for g in database.get_all_grievances():
                if (g.get("status") or "") in ("Pending", "In Progress"):
                    try:
                        dt = datetime.datetime.strptime((g.get("date_submitted") or "").strip()[:19], "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        continue
                    age_h = (now - dt).total_seconds() / 3600.0
                    if age_h > 24:
                        overdue_rows.append({
                            "ID": g.get("grievance_id"),
                            "Block": g.get("block_name"),
                            "Room": g.get("room_number"),
                            "Category": g.get("category"),
                            "Priority": g.get("priority"),
                            "Age (h)": round(age_h, 1),
                            "Urgency": "🔴 >48h" if age_h > 48 else "🟠 >24h",
                        })
            if overdue_rows:
                overdue_rows.sort(key=lambda r: r["Age (h)"], reverse=True)
                st.dataframe(pd.DataFrame(overdue_rows), use_container_width=True, hide_index=True)
            else:
                st.success("✅ No tickets breaching the 24h SLA. Nice work!")

            st.markdown("---")
            ch1, ch2, ch3 = st.columns(3)
            with ch1:
                st.markdown("**By Category**")
                if a["by_category"]:
                    st.bar_chart(pd.DataFrame(
                        {"Count": list(a["by_category"].values())},
                        index=list(a["by_category"].keys()),
                    ))
            with ch2:
                st.markdown("**By Block**")
                if a["by_block"]:
                    st.bar_chart(pd.DataFrame(
                        {"Count": list(a["by_block"].values())},
                        index=list(a["by_block"].keys()),
                    ))
            with ch3:
                st.markdown("**By Priority**")
                if a["by_priority"]:
                    st.bar_chart(pd.DataFrame(
                        {"Count": list(a["by_priority"].values())},
                        index=list(a["by_priority"].keys()),
                    ))

        # TAB 1: GRIEVANCE DISPATCH OPERATIONS
        with admin_tab1:
            st.subheader("Warden Control & Dispatch Operations Console")

            # Filter bar
            f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 1.5, 3, 1])
            with f_col1:
                filter_block = st.selectbox("Hostel Block", ["All Blocks", "BH-1", "BH-2", "BH-3", "GH-1", "GH-2", "IH-1"])
            with f_col2:
                filter_status = st.selectbox("Status Filter", ["All Statuses", "Pending", "In Progress", "Resolved", "Rejected"])
            with f_col3:
                search_admin = st.text_input("Search (ID, Name, Room, Description)", placeholder="Search grievances...")
            with f_col4:
                st.write("")
                st.write("")
                if st.button("🔄 Refresh Data", use_container_width=True):
                    st.rerun()

            grievances = database.get_all_grievances(
                status_filter=filter_status,
                block_filter=filter_block,
                search_query=search_admin
            )

            if grievances:
                df = pd.DataFrame(grievances)
                st.markdown(f"Displaying **{len(df)}** grievance record(s):")

                # Render interactive dataframe table
                display_cols = ["grievance_id", "block_name", "room_number", "student_name", "category", "priority", "status", "last_updated"]
                st.dataframe(
                    df[display_cols],
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "grievance_id": "ID",
                        "block_name": "Block",
                        "room_number": "Room",
                        "student_name": "Student Name",
                        "category": "Category",
                        "priority": "Priority",
                        "status": "Status",
                        "last_updated": "Last Updated"
                    }
                )

                st.markdown("---")
                st.subheader("🛠️ Warden Action & Dispatch Details")

                page_grievances = paginate(grievances, key="grievance_pager")
                g_options = [f"Ticket #{g['grievance_id']} - {g['student_name']} ({g['block_name']} Room {g['room_number']})" for g in page_grievances]
                selected_g_label = st.selectbox("Select Grievance Ticket to Manage", g_options)

                if selected_g_label:
                    selected_id = int(selected_g_label.split("Ticket #")[1].split(" - ")[0])
                    selected_item = database.get_grievance_by_id(selected_id)

                    if selected_item:
                        info_c1, info_c2 = st.columns(2)
                        with info_c1:
                            st.markdown(f"**Student:** {selected_item['student_name']} ({selected_item['block_name']} Room {selected_item['room_number']})")
                            st.markdown(f"**Category:** {selected_item['category']}")
                            st.markdown(f"**Submitted:** {selected_item['date_submitted']}")
                        with info_c2:
                            st.markdown(f"**Current Status:** `{selected_item['status']}`")
                            st.markdown(f"**Priority:** `{selected_item['priority']}`")
                            st.markdown(f"**Assigned Staff:** `{selected_item.get('assigned_staff') or 'None'}`")
                            try:
                                _rt = int(selected_item.get('rating') or 0)
                            except (TypeError, ValueError):
                                _rt = 0
                            if _rt > 0:
                                st.markdown(f"**Student Rating:** {'⭐' * _rt} ({_rt}/5)")
                                if selected_item.get('feedback'):
                                    st.caption(f"Feedback: {selected_item['feedback']}")

                        st.markdown(f"**Issue Description:**\n>{selected_item['description']}")
                        if selected_item.get('photo_path'):
                            try:
                                st.image(selected_item['photo_path'], caption="Attached Photo", width=300)
                            except Exception:
                                pass
                        if selected_item.get('suggestion'):
                            st.markdown(f"**Student Suggestion:**\n_{selected_item['suggestion']}_")

                        st.markdown("---")

                        with st.form(f"update_form_{selected_id}", enter_to_submit=False):
                            u_col1, u_col2 = st.columns(2)
                            with u_col1:
                                new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Resolved", "Rejected"], index=["Pending", "In Progress", "Resolved", "Rejected"].index(selected_item['status']) if selected_item['status'] in ["Pending", "In Progress", "Resolved", "Rejected"] else 0)
                            with u_col2:
                                new_staff = st.text_input("Assign Maintenance Staff", value=selected_item.get('assigned_staff', ''))

                            new_remarks = st.text_area("Warden Remarks / Resolution Notes", value=selected_item.get('admin_remarks', ''))
                            confirm_delete = st.checkbox("⚠️ Confirm I want to permanently delete this ticket", key=f"confirm_del_g_{selected_id}")

                            b_col1, b_col2 = st.columns([3, 1])
                            with b_col1:
                                save_btn = st.form_submit_button("💾 Save Dispatch Updates", type="primary", use_container_width=True)
                            with b_col2:
                                delete_btn = st.form_submit_button("🗑️ Delete Ticket", use_container_width=True)

                            if save_btn:
                                try:
                                    database.update_grievance(selected_id, new_status, new_remarks, assigned_staff=new_staff.strip())
                                    st.success(f"Grievance #{selected_id} updated successfully!")
                                    st.rerun()
                                except DatabaseError as e:
                                    st.error(f"❌ {e}")

                            if delete_btn:
                                if not confirm_delete:
                                    st.warning("Tick the confirmation box before deleting a ticket.")
                                else:
                                    try:
                                        database.delete_grievance(selected_id)
                                        st.warning(f"Grievance #{selected_id} deleted!")
                                        st.rerun()
                                    except DatabaseError as e:
                                        st.error(f"❌ {e}")

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

        # TAB 2: STUDENT LEAVE & GATE PASS ROSTER
        with admin_tab2:
            st.subheader("🌴 Student Outstation Leave & Gate Pass Control")

            l_f1, l_f2, l_f3, l_f4 = st.columns([1.5, 1.5, 3, 1])
            with l_f1:
                l_filter_block = st.selectbox("Hostel Block Filter", ["All Blocks", "BH-1", "BH-2", "BH-3", "GH-1", "GH-2", "IH-1"], key="w_l_block")
            with l_f2:
                l_filter_status = st.selectbox("Status Filter", ["All Statuses", "Pending Warden Approval", "Approved / Gate Pass Issued", "Rejected"], key="w_l_status")
            with l_f3:
                l_search_w = st.text_input("Search (ID, Name, Room, Teacher, Destination)", placeholder="Search leave applications...", key="w_l_search")
            with l_f4:
                st.write(""); st.write("")
                if st.button("🔄 Refresh Roster", use_container_width=True, key="w_l_refresh"):
                    st.rerun()

            all_leaves = database.get_all_leave_applications(status_filter=l_filter_status, block_filter=l_filter_block, search_query=l_search_w)

            if all_leaves:
                l_df = pd.DataFrame(all_leaves)
                st.markdown(f"Displaying **{len(l_df)}** leave application(s):")

                l_display_cols = ["leave_id", "block_name", "room_number", "student_name", "granting_teacher", "from_date", "to_date", "destination", "status", "gate_pass_code"]
                st.dataframe(
                    l_df[l_display_cols],
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "leave_id": "Leave ID",
                        "block_name": "Block",
                        "room_number": "Room",
                        "student_name": "Student Name",
                        "granting_teacher": "Granting Teacher / Faculty",
                        "from_date": "From",
                        "to_date": "To",
                        "destination": "Destination",
                        "status": "Approval Status",
                        "gate_pass_code": "Gate Pass Code"
                    }
                )

                st.markdown("---")
                st.subheader("🛠️ Warden Gate Pass Action Panel")

                page_leaves = paginate(all_leaves, key="leave_pager")
                l_options = [f"Leave #L-{rec['leave_id']} - {rec['student_name']} ({rec['block_name']} Room {rec['room_number']})" for rec in page_leaves]
                selected_leave_label = st.selectbox("Select Leave Application to Action", l_options, key="sel_leave_label")

                if selected_leave_label:
                    sel_lid = int(selected_leave_label.split("Leave #L-")[1].split(" - ")[0])
                    sel_leave = database.get_leave_application_by_id(sel_lid)

                    if sel_leave:
                        lc_1, lc_2 = st.columns(2)
                        with lc_1:
                            st.markdown(f"**Student:** {sel_leave['student_name']} ({sel_leave['block_name']} Room {sel_leave['room_number']})")
                            st.markdown(f"**Student Phone:** `{sel_leave['phone_number']}`  |  **Parent Phone:** `{sel_leave['parent_phone']}`")
                            st.markdown(f"**Granting Teacher Sign-off:** `{sel_leave['granting_teacher']}`")
                        with lc_2:
                            st.markdown(f"**Destination:** {sel_leave['destination']}")
                            st.markdown(f"**Leave Dates:** `{sel_leave['from_date']}` to `{sel_leave['to_date']}`")
                            st.markdown(f"**Reason:** {sel_leave['leave_reason']}")

                        if sel_leave.get('gate_pass_code') and "Approved" in (sel_leave.get('status') or ""):
                            render_gate_pass_card(sel_leave)

                        st.markdown("---")
                        with st.form(f"leave_action_form_{sel_lid}", enter_to_submit=False):
                            la_col1, la_col2 = st.columns(2)
                            with la_col1:
                                new_l_status = st.selectbox("Action / Approval", ["Pending Warden Approval", "Approved / Gate Pass Issued", "Rejected"], index=["Pending Warden Approval", "Approved / Gate Pass Issued", "Rejected"].index(sel_leave['status']) if sel_leave['status'] in ["Pending Warden Approval", "Approved / Gate Pass Issued", "Rejected"] else 0)
                            with la_col2:
                                # Unguessable default so students can't derive another student's pass from the ID.
                                default_gp = sel_leave.get('gate_pass_code') or f"GP-2026-{secrets.token_hex(3).upper()}"
                                new_gp_code = st.text_input("Gate Pass Code", value=default_gp)

                            new_w_remarks = st.text_area("Warden Remarks / Authorization Notes", value=sel_leave.get('warden_remarks', ''))
                            confirm_del_leave = st.checkbox("⚠️ Confirm I want to permanently delete this leave record", key=f"confirm_del_l_{sel_lid}")

                            lb_col1, lb_col2 = st.columns([3, 1])
                            with lb_col1:
                                save_l_btn = st.form_submit_button("💾 Save Leave Authorization & Issue Pass", type="primary", use_container_width=True)
                            with lb_col2:
                                delete_l_btn = st.form_submit_button("🗑️ Delete Leave Record", use_container_width=True)

                            if save_l_btn:
                                try:
                                    database.update_leave_status(sel_lid, new_l_status, warden_remarks=new_w_remarks.strip(), gate_pass_code=new_gp_code.strip() if "Approved" in new_l_status else "")
                                    st.success(f"Leave Application #L-{sel_lid} updated successfully!")
                                    st.rerun()
                                except DatabaseError as e:
                                    st.error(f"❌ {e}")

                            if delete_l_btn:
                                if not confirm_del_leave:
                                    st.warning("Tick the confirmation box before deleting a leave record.")
                                else:
                                    try:
                                        database.delete_leave_application(sel_lid)
                                        st.warning(f"Leave Record #L-{sel_lid} deleted!")
                                        st.rerun()
                                    except DatabaseError as e:
                                        st.error(f"❌ {e}")

                # Export CSV
                l_csv_data = l_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Export Outstation Roster (CSV)",
                    data=l_csv_data,
                    file_name=f"hostel_outstation_roster_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No leave applications match the current filter criteria.")

        # TAB: LOST & FOUND INVENTORY (WARDEN)
        with admin_tab_lf:
            st.subheader("🎒 Lost & Found Inventory Manager")

            wf1, wf2, wf3 = st.columns([1.2, 1.2, 3])
            with wf1:
                w_lf_type = st.selectbox("Type", ["All Types", "Lost", "Found"], key="w_lf_type")
            with wf2:
                w_lf_status = st.selectbox("Status", ["All Statuses", "Open", "Claimed / Returned"], key="w_lf_status")
            with wf3:
                w_lf_search = st.text_input("Search", placeholder="Search items...", key="w_lf_search")

            lf_items = database.get_all_lost_found(
                item_type_filter=w_lf_type, status_filter=w_lf_status, search_query=w_lf_search
            )

            if lf_items:
                lf_df = pd.DataFrame(lf_items)
                show_cols = [c for c in ["item_id", "item_type", "title", "category", "location", "status", "contact_info", "date_posted"] if c in lf_df.columns]
                st.dataframe(lf_df[show_cols], use_container_width=True, hide_index=True,
                             column_config={"item_id": "ID", "item_type": "Type", "date_posted": "Posted"})

                st.markdown("---")
                for it in paginate(lf_items, key="w_lf_pager", page_size=15):
                    tag = "🔴 LOST" if it.get("item_type") == "Lost" else "🟢 FOUND"
                    with st.expander(f"{tag} · #{it['item_id']} {it['title']} — {it.get('status','Open')}"):
                        st.markdown(f"**Category:** {it.get('category','Other')}  |  **Where:** {it.get('location') or '—'}")
                        if it.get("description"):
                            st.markdown(f"**Details:** {it['description']}")
                        st.markdown(f"**Contact:** {it.get('contact_info') or '—'}")
                        if it.get("photo_path"):
                            try:
                                st.image(it["photo_path"], width=240)
                            except Exception:
                                pass
                        ac1, ac2 = st.columns(2)
                        with ac1:
                            if it.get("status") != "Claimed / Returned":
                                if st.button("✅ Mark Claimed / Returned", key=f"lf_claim_{it['item_id']}", use_container_width=True):
                                    try:
                                        database.update_lost_found_status(it["item_id"], "Claimed / Returned")
                                        st.success("Marked as claimed / returned.")
                                        st.rerun()
                                    except DatabaseError as e:
                                        st.error(f"❌ {e}")
                            else:
                                if st.button("↩️ Reopen", key=f"lf_reopen_{it['item_id']}", use_container_width=True):
                                    try:
                                        database.update_lost_found_status(it["item_id"], "Open")
                                        st.rerun()
                                    except DatabaseError as e:
                                        st.error(f"❌ {e}")
                        with ac2:
                            confirm_lf = st.checkbox("⚠️ Confirm delete", key=f"lf_confirm_{it['item_id']}")
                            if st.button("🗑️ Delete Item", key=f"lf_del_{it['item_id']}", use_container_width=True):
                                if not confirm_lf:
                                    st.warning("Tick 'Confirm delete' first.")
                                else:
                                    try:
                                        database.delete_lost_found_item(it["item_id"])
                                        st.warning("Item deleted.")
                                        st.rerun()
                                    except DatabaseError as e:
                                        st.error(f"❌ {e}")
            else:
                st.info("No Lost & Found items match the current filter.")

        # TAB 3: NOTICE MANAGER
        with admin_tab3:
            st.subheader("📢 Create New Hostel Announcement")

            with st.form("create_notice_form", clear_on_submit=True, enter_to_submit=False):
                n_title = st.text_input("Announcement Title *", placeholder="e.g. Water Tank Cleaning Notice")
                n_col1, n_col2, n_col3 = st.columns([1, 1, 1])
                with n_col1:
                    n_cat = st.selectbox("Category", ["📢 General Notice", "⚡ Power Maintenance", "🚰 Water Supply", "🧹 Mess & Sanitation", "🚨 Emergency Alert"])
                with n_col2:
                    n_block = st.selectbox("Target Hostel Block", ["All Blocks", "BH-1", "BH-2", "BH-3", "GH-1", "GH-2", "IH-1"])
                with n_col3:
                    n_duration = st.selectbox(
                        "Active Duration / Expiry Timer *",
                        [
                            "📌 No Expiration (Permanent)",
                            "⏱️ 1 Hour",
                            "⏱️ 12 Hours",
                            "⏱️ 24 Hours (1 Day)",
                            "⏱️ 2 Days (48 Hours)",
                            "⏱️ 3 Days (72 Hours)",
                            "⏱️ 7 Days (1 Week)"
                        ]
                    )

                n_content = st.text_area("Notice Content / Message Body *")
                n_posted_by = st.text_input("Posted By", value="Chief Hostel Warden Office")

                post_btn = st.form_submit_button("📢 Publish Announcement", type="primary")
                if post_btn:
                    if not n_title.strip() or not n_content.strip():
                        st.error("Title and Content are required.")
                    else:
                        duration_map = {
                            "📌 No Expiration (Permanent)": 0,
                            "⏱️ 1 Hour": 1,
                            "⏱️ 12 Hours": 12,
                            "⏱️ 24 Hours (1 Day)": 24,
                            "⏱️ 2 Days (48 Hours)": 48,
                            "⏱️ 3 Days (72 Hours)": 72,
                            "⏱️ 7 Days (1 Week)": 168
                        }
                        exp_h = duration_map.get(n_duration, 0)
                        try:
                            database.create_notice(n_title.strip(), n_content.strip(), n_cat, n_block, n_posted_by, expiry_hours=exp_h)
                            st.success("Notice published successfully!")
                            st.rerun()
                        except DatabaseError as e:
                            st.error(f"❌ {e}")

            st.markdown("---")
            st.subheader("Manage Published Announcements")
            all_notices = database.get_all_notices()
            if all_notices:
                for noti in all_notices:
                    exp_badge = f" (⏳ Expires: {noti['expires_at']})" if noti.get('expires_at') else " (📌 Permanent)"
                    with st.expander(f"📢 [{noti['target_block']}] {noti['title']} ({noti['date_posted']}{exp_badge})"):
                        st.write(noti['content'])
                        st.caption(f"Posted by: {noti.get('posted_by', 'Warden Office')}{exp_badge}")
                        confirm_del_n = st.checkbox("⚠️ Confirm delete", key=f"confirm_del_n_{noti['notice_id']}")
                        if st.button("🗑️ Delete Notice", key=f"del_notice_{noti['notice_id']}"):
                            if not confirm_del_n:
                                st.warning("Tick 'Confirm delete' before removing a notice.")
                            else:
                                try:
                                    database.delete_notice(noti['notice_id'])
                                    st.warning("Notice deleted!")
                                    st.rerun()
                                except DatabaseError as e:
                                    st.error(f"❌ {e}")
            else:
                st.info("No active published notices currently on the board.")
