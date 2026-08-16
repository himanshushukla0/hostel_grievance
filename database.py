import os
import sqlite3
import datetime
from contextlib import contextmanager

# ==========================================
# ☁️ SUPABASE CLOUD CONFIGURATION
# ==========================================
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://wtfartnzuwdixoniufdz.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_7CLKY_ttSdt-aKKYKytvIg_11jrm6qM")

supabase = None
USE_SUPABASE = False

try:
    from supabase import create_client, Client
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        USE_SUPABASE = True
except Exception:
    supabase = None
    USE_SUPABASE = False

DB_FILE = 'hostel_care.db'

# ==========================================
# 🗄️ LOCAL SQLITE (fallback only — used automatically
# if Supabase is unreachable or a table is missing)
# ==========================================

def get_connection():
    """Establish and return a connection to the SQLite database with busy timeout."""
    conn = sqlite3.connect(DB_FILE, timeout=15.0)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

@contextmanager
def get_db():
    """Context manager to ensure connections are safely closed even if exceptions occur."""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize local SQLite fallback DB and perform safe schema migrations."""
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("PRAGMA journal_mode=WAL;")
        except Exception:
            pass

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Grievances (
                grievance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                room_number TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                date_submitted TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                admin_remarks TEXT DEFAULT '',
                last_updated TEXT DEFAULT '',
                block_name TEXT DEFAULT 'BH-1',
                priority TEXT DEFAULT 'Normal',
                assigned_staff TEXT DEFAULT '',
                suggestion TEXT DEFAULT '',
                photo_path TEXT DEFAULT ''
            )
        ''')

        cursor.execute("PRAGMA table_info(Grievances)")
        columns = [row['name'] for row in cursor.fetchall()]

        if 'last_updated' not in columns:
            cursor.execute("ALTER TABLE Grievances ADD COLUMN last_updated TEXT DEFAULT ''")
        if 'block_name' not in columns:
            cursor.execute("ALTER TABLE Grievances ADD COLUMN block_name TEXT DEFAULT 'BH-1'")
        if 'priority' not in columns:
            cursor.execute("ALTER TABLE Grievances ADD COLUMN priority TEXT DEFAULT 'Normal'")
        if 'assigned_staff' not in columns:
            cursor.execute("ALTER TABLE Grievances ADD COLUMN assigned_staff TEXT DEFAULT ''")
        if 'suggestion' not in columns:
            cursor.execute("ALTER TABLE Grievances ADD COLUMN suggestion TEXT DEFAULT ''")
        if 'photo_path' not in columns:
            cursor.execute("ALTER TABLE Grievances ADD COLUMN photo_path TEXT DEFAULT ''")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Notices (
                notice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT NOT NULL,
                target_block TEXT DEFAULT 'All Blocks',
                date_posted TEXT NOT NULL,
                posted_by TEXT DEFAULT 'Hostel Warden Office',
                expires_at TEXT DEFAULT ''
            )
        ''')

        cursor.execute("PRAGMA table_info(Notices)")
        notice_cols = [row['name'] for row in cursor.fetchall()]
        if 'expires_at' not in notice_cols:
            cursor.execute("ALTER TABLE Notices ADD COLUMN expires_at TEXT DEFAULT ''")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS LeaveApplications (
                leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                block_name TEXT DEFAULT 'BH-1',
                room_number TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                parent_phone TEXT NOT NULL,
                leave_reason TEXT NOT NULL,
                destination TEXT NOT NULL,
                from_date TEXT NOT NULL,
                to_date TEXT NOT NULL,
                granting_teacher TEXT NOT NULL,
                status TEXT DEFAULT 'Pending Warden Approval',
                warden_remarks TEXT DEFAULT '',
                gate_pass_code TEXT DEFAULT '',
                date_submitted TEXT NOT NULL,
                last_updated TEXT DEFAULT ''
            )
        ''')

        conn.commit()


def escape_like(string):
    """Escape special characters for SQL LIKE pattern matching (SQLite fallback path)."""
    return string.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')


# ==========================================
# 🔧 SUPABASE HELPERS
# ==========================================

def _sb_ok():
    return USE_SUPABASE and supabase is not None


# ==========================================
# 📋 GRIEVANCES
# ==========================================

def create_grievance(name, room, category, description, block_name="BH-1", priority="Normal", suggestion="", photo_path=""):
    """Insert a new grievance. Writes to local SQLite and syncs to Supabase Cloud if available."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Local SQLite generates the ID
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Grievances (student_name, room_number, category, description, date_submitted, last_updated, block_name, priority, assigned_staff, suggestion, photo_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, '', ?, ?)
        ''', (name, room, category, description, now, now, block_name, priority, suggestion, photo_path or ""))
        grievance_id = cursor.lastrowid
        conn.commit()

    # Sync to Supabase Cloud with matching ID
    if _sb_ok():
        try:
            payload = {
                "grievance_id": grievance_id,
                "student_name": name,
                "room_number": room,
                "category": category,
                "description": description,
                "date_submitted": now,
                "status": "Pending",
                "last_updated": now,
                "block_name": block_name,
                "priority": priority,
                "assigned_staff": "",
                "suggestion": suggestion
            }
            if photo_path:
                payload["photo_path"] = photo_path
            supabase.table("Grievances").insert(payload).execute()
        except Exception:
            pass

    return grievance_id


def get_all_grievances(status_filter=None, block_filter=None, search_query=None):
    """Fetch all grievances, reading from Supabase when available, else local SQLite."""
    if _sb_ok():
        try:
            q = supabase.table("Grievances").select("*")
            if status_filter and status_filter not in ("All", "All Statuses"):
                q = q.eq("status", status_filter)
            if block_filter and block_filter not in ("All", "All Blocks"):
                q = q.ilike("block_name", f"{block_filter}%")
            if search_query and search_query.strip():
                s = search_query.strip()
                q = q.or_(
                    f"student_name.ilike.%{s}%,"
                    f"room_number.ilike.%{s}%,"
                    f"category.ilike.%{s}%,"
                    f"block_name.ilike.%{s}%,"
                    f"assigned_staff.ilike.%{s}%,"
                    f"description.ilike.%{s}%,"
                    f"suggestion.ilike.%{s}%"
                )
            q = q.order("date_submitted", desc=True)
            resp = q.execute()
            return resp.data or []
        except Exception:
            pass  # fall through to SQLite

    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM Grievances WHERE 1=1"
        params = []

        if status_filter and status_filter not in ("All", "All Statuses"):
            query += " AND status = ?"
            params.append(status_filter)

        if block_filter and block_filter not in ("All", "All Blocks"):
            query += " AND (block_name = ? OR block_name LIKE ? ESCAPE '\\')"
            params.extend([block_filter, f"{escape_like(block_filter)}%"])

        if search_query:
            escaped_query = escape_like(search_query)
            query += (
                " AND (CAST(grievance_id AS TEXT) LIKE ? ESCAPE '\\'"
                " OR student_name LIKE ? ESCAPE '\\'"
                " OR room_number LIKE ? ESCAPE '\\'"
                " OR category LIKE ? ESCAPE '\\'"
                " OR block_name LIKE ? ESCAPE '\\'"
                " OR assigned_staff LIKE ? ESCAPE '\\'"
                " OR description LIKE ? ESCAPE '\\'"
                " OR suggestion LIKE ? ESCAPE '\\')"
            )
            pattern = f"%{escaped_query}%"
            params.extend([pattern] * 8)

        query += " ORDER BY date_submitted DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_grievance_by_id(grievance_id):
    """Fetch a single grievance by its ID."""
    if _sb_ok():
        try:
            resp = supabase.table("Grievances").select("*").eq("grievance_id", grievance_id).execute()
            if resp.data and len(resp.data) > 0:
                return resp.data[0]
        except Exception:
            pass

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Grievances WHERE grievance_id = ?", (grievance_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_grievance(grievance_id, status, remarks, assigned_staff=""):
    """Update status, remarks, and assigned staff for a grievance (Admin action)."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if _sb_ok():
        try:
            supabase.table("Grievances").update({
                "status": status,
                "admin_remarks": remarks,
                "last_updated": now,
                "assigned_staff": assigned_staff
            }).eq("grievance_id", grievance_id).execute()
        except Exception:
            pass

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Grievances
            SET status = ?, admin_remarks = ?, last_updated = ?, assigned_staff = ?
            WHERE grievance_id = ?
        ''', (status, remarks, now, assigned_staff, grievance_id))
        conn.commit()


def delete_grievance(grievance_id):
    """Delete a grievance by ID (Admin action)."""
    if _sb_ok():
        try:
            supabase.table("Grievances").delete().eq("grievance_id", grievance_id).execute()
        except Exception:
            pass

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Grievances WHERE grievance_id = ?", (grievance_id,))
        conn.commit()


def get_grievance_counts():
    """Return dictionary with summary counts of grievances by status and priority."""
    counts = {'total': 0, 'pending': 0, 'in_progress': 0, 'resolved': 0, 'rejected': 0, 'emergency': 0}

    if _sb_ok():
        try:
            resp = supabase.table("Grievances").select("status, priority").execute()
            rows = resp.data or []
            for row in rows:
                st = (row.get('status') or '').lower().replace(" ", "_")
                if st in counts:
                    counts[st] += 1
                counts['total'] += 1
                if row.get('priority') and 'Emergency' in row['priority'] and row.get('status') != 'Resolved':
                    counts['emergency'] += 1
            return counts
        except Exception:
            pass

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) as count FROM Grievances GROUP BY status")
        rows = cursor.fetchall()

        for row in rows:
            if row['status']:
                st = row['status'].lower().replace(" ", "_")
                cnt = row['count']
                if st in counts:
                    counts[st] = cnt
                counts['total'] += cnt

        cursor.execute("SELECT COUNT(*) as count FROM Grievances WHERE priority LIKE '%Emergency%' AND status != 'Resolved'")
        em_row = cursor.fetchone()
        if em_row:
            counts['emergency'] = em_row['count']

        return counts


def get_grievances_by_room_or_name(search_term):
    """Fetch grievances by room number, student name, or block (for student lookup)."""
    if _sb_ok():
        try:
            s = search_term
            resp = supabase.table("Grievances").select("*").or_(
                f"room_number.ilike.%{s}%,student_name.ilike.%{s}%,block_name.ilike.%{s}%"
            ).order("date_submitted", desc=True).execute()
            return resp.data or []
        except Exception:
            pass

    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT * FROM Grievances
            WHERE room_number LIKE ? ESCAPE '\\' OR student_name LIKE ? ESCAPE '\\' OR block_name LIKE ? ESCAPE '\\' OR CAST(grievance_id AS TEXT) LIKE ? ESCAPE '\\'
            ORDER BY date_submitted DESC
        """
        pattern = f"%{escape_like(search_term)}%"
        cursor.execute(query, (pattern, pattern, pattern, pattern))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_grievances_by_room_and_name(room_number, student_name, block_name=None):
    """Fetch grievances matching BOTH room number AND student name (secure forgot-ID lookup)."""
    if _sb_ok():
        try:
            q = supabase.table("Grievances").select("*").ilike("room_number", room_number.strip()).ilike("student_name", f"%{student_name.strip()}%")
            if block_name and block_name != "All Blocks":
                q = q.eq("block_name", block_name)
            resp = q.order("date_submitted", desc=True).execute()
            return resp.data or []
        except Exception:
            pass

    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT * FROM Grievances
            WHERE LOWER(TRIM(room_number)) = LOWER(TRIM(?))
              AND LOWER(TRIM(student_name)) LIKE LOWER(TRIM(?))
        """
        params = [room_number.strip(), f"%{escape_like(student_name.strip())}%"]
        if block_name and block_name != "All Blocks":
            query += " AND block_name = ?"
            params.append(block_name)
        query += " ORDER BY date_submitted DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


# ==========================================
# 📢 NOTICES
# ==========================================

def cleanup_expired_notices():
    """Auto-delete notices whose active timer / expiry timestamp has passed."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if _sb_ok():
        try:
            resp = supabase.table("Notices").select("notice_id, expires_at").execute()
            for n in (resp.data or []):
                exp = n.get("expires_at")
                if exp and exp != "" and exp <= now:
                    supabase.table("Notices").delete().eq("notice_id", n["notice_id"]).execute()
        except Exception:
            pass

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Notices WHERE expires_at != '' AND expires_at <= ?", (now,))
            conn.commit()
    except Exception:
        pass


def create_notice(title, content, category, target_block="All Blocks", posted_by="Hostel Warden Office", expiry_hours=0):
    """Insert a new notice/announcement into local SQLite and sync to Supabase Cloud."""
    now_dt = datetime.datetime.now()
    now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")

    expires_at = ""
    if expiry_hours and float(expiry_hours) != 0:
        exp_dt = now_dt + datetime.timedelta(hours=float(expiry_hours))
        expires_at = exp_dt.strftime("%Y-%m-%d %H:%M:%S")

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Notices (title, content, category, target_block, date_posted, posted_by, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, content, category, target_block, now_str, posted_by, expires_at))
        notice_id = cursor.lastrowid
        conn.commit()

    if _sb_ok():
        try:
            supabase.table("Notices").insert({
                "notice_id": notice_id,
                "title": title,
                "content": content,
                "category": category,
                "target_block": target_block,
                "date_posted": now_str,
                "posted_by": posted_by,
                "expires_at": expires_at
            }).execute()
        except Exception:
            pass

    return notice_id


def get_all_notices(block_filter=None, category_filter=None):
    """Fetch all published active notices, automatically purging expired ones."""
    cleanup_expired_notices()

    if _sb_ok():
        try:
            q = supabase.table("Notices").select("*")
            resp = q.order("date_posted", desc=True).execute()
            notices = resp.data or []
            if block_filter and block_filter != "All Blocks":
                notices = [n for n in notices if n.get("target_block") == block_filter or n.get("target_block") == "All Blocks"]
            if category_filter and category_filter != "All":
                notices = [n for n in notices if n.get("category") == category_filter]
            return notices
        except Exception:
            pass

    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM Notices WHERE 1=1"
        params = []

        if block_filter and block_filter != "All Blocks":
            query += " AND (target_block = ? OR target_block = 'All Blocks')"
            params.append(block_filter)

        if category_filter and category_filter != "All":
            query += " AND category = ?"
            params.append(category_filter)

        query += " ORDER BY date_posted DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def delete_notice(notice_id):
    """Delete a notice by ID."""
    if _sb_ok():
        try:
            supabase.table("Notices").delete().eq("notice_id", notice_id).execute()
        except Exception:
            pass

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Notices WHERE notice_id = ?", (notice_id,))
        conn.commit()


# ==========================================
# 🌴 STUDENT LEAVE & GATE PASS OPERATIONS
# ==========================================

def create_leave_application(name, block, room, phone, parent_phone, reason, destination, from_date, to_date, teacher_name):
    """Insert a new leave application into local SQLite and sync to Supabase Cloud."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO LeaveApplications (
                student_name, block_name, room_number, phone_number, parent_phone,
                leave_reason, destination, from_date, to_date, granting_teacher,
                status, warden_remarks, gate_pass_code, date_submitted, last_updated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending Warden Approval', '', '', ?, ?)
        ''', (name, block, room, phone, parent_phone, reason, destination, from_date, to_date, teacher_name, now, now))
        leave_id = cursor.lastrowid
        conn.commit()

    if _sb_ok():
        try:
            supabase.table("LeaveApplications").insert({
                "leave_id": leave_id,
                "student_name": name,
                "block_name": block,
                "room_number": room,
                "phone_number": phone,
                "parent_phone": parent_phone,
                "leave_reason": reason,
                "destination": destination,
                "from_date": from_date,
                "to_date": to_date,
                "granting_teacher": teacher_name,
                "status": "Pending Warden Approval",
                "warden_remarks": "",
                "gate_pass_code": "",
                "date_submitted": now,
                "last_updated": now
            }).execute()
        except Exception:
            pass

    return leave_id


def get_leave_application_by_id(leave_id):
    """Fetch leave application details by Leave ID."""
    if _sb_ok():
        try:
            resp = supabase.table("LeaveApplications").select("*").eq("leave_id", leave_id).execute()
            if resp.data and len(resp.data) > 0:
                return resp.data[0]
        except Exception:
            pass

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM LeaveApplications WHERE leave_id = ?", (leave_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_leave_applications_by_room_and_name(room_number, student_name):
    """Fetch leave applications matching room number AND student name."""
    if _sb_ok():
        try:
            resp = supabase.table("LeaveApplications").select("*").ilike("room_number", room_number.strip()).ilike("student_name", f"%{student_name.strip()}%").order("date_submitted", desc=True).execute()
            return resp.data or []
        except Exception:
            pass

    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT * FROM LeaveApplications
            WHERE LOWER(TRIM(room_number)) = LOWER(TRIM(?))
              AND LOWER(TRIM(student_name)) LIKE LOWER(TRIM(?))
            ORDER BY date_submitted DESC
        """
        cursor.execute(query, (room_number.strip(), f"%{escape_like(student_name.strip())}%"))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_all_leave_applications(status_filter=None, block_filter=None, search_query=None):
    """Fetch all leave applications with optional status/block filtering and text search."""
    if _sb_ok():
        try:
            q = supabase.table("LeaveApplications").select("*")
            if status_filter and status_filter not in ("All", "All Statuses"):
                q = q.eq("status", status_filter)
            if block_filter and block_filter not in ("All", "All Blocks"):
                q = q.ilike("block_name", f"{block_filter}%")
            if search_query and search_query.strip():
                s = search_query.strip()
                q = q.or_(
                    f"student_name.ilike.%{s}%,"
                    f"room_number.ilike.%{s}%,"
                    f"granting_teacher.ilike.%{s}%,"
                    f"destination.ilike.%{s}%"
                )
            resp = q.order("date_submitted", desc=True).execute()
            return resp.data or []
        except Exception:
            pass

    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM LeaveApplications WHERE 1=1"
        params = []

        if status_filter and status_filter not in ("All", "All Statuses"):
            query += " AND status = ?"
            params.append(status_filter)

        if block_filter and block_filter not in ("All", "All Blocks"):
            query += " AND (block_name = ? OR block_name LIKE ? ESCAPE '\\')"
            params.extend([block_filter, f"{escape_like(block_filter)}%"])

        if search_query and search_query.strip():
            sq = f"%{escape_like(search_query.strip())}%"
            query += " AND (student_name LIKE ? ESCAPE '\\' OR room_number LIKE ? ESCAPE '\\' OR granting_teacher LIKE ? ESCAPE '\\' OR destination LIKE ? ESCAPE '\\' OR CAST(leave_id AS TEXT) LIKE ? ESCAPE '\\')"
            params.extend([sq, sq, sq, sq, sq])

        query += " ORDER BY date_submitted DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def update_leave_status(leave_id, status, warden_remarks="", gate_pass_code=""):
    """Update leave status, warden remarks, and gate pass code."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if _sb_ok():
        try:
            supabase.table("LeaveApplications").update({
                "status": status,
                "warden_remarks": warden_remarks,
                "gate_pass_code": gate_pass_code,
                "last_updated": now
            }).eq("leave_id", leave_id).execute()
        except Exception:
            pass

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE LeaveApplications
            SET status = ?, warden_remarks = ?, gate_pass_code = ?, last_updated = ?
            WHERE leave_id = ?
        ''', (status, warden_remarks, gate_pass_code, now, leave_id))
        conn.commit()


def delete_leave_application(leave_id):
    """Delete a leave application record."""
    if _sb_ok():
        try:
            supabase.table("LeaveApplications").delete().eq("leave_id", leave_id).execute()
        except Exception:
            pass

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM LeaveApplications WHERE leave_id = ?", (leave_id,))
        conn.commit()


# Initialize the local SQLite fallback DB when this module is loaded
init_db()
