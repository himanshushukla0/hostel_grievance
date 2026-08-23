import os
import re
import mimetypes
import sqlite3
import logging
import datetime
from contextlib import contextmanager

# ==========================================
# 🪵 LOGGING
# ==========================================
logger = logging.getLogger("hostel_grievance.db")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


class DatabaseError(Exception):
    """Raised when a write to the configured backend fails, so callers can
    surface a real error instead of silently reporting success."""


# ==========================================
# 🔐 CONFIGURATION (env / Streamlit secrets ONLY — never hardcode credentials)
# ==========================================
def _get_secret(key, default=""):
    """Read a config value from environment first, then Streamlit secrets if available."""
    val = os.environ.get(key)
    if val:
        return val
    try:
        import streamlit as st  # optional — only present in the web app
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return default


SUPABASE_URL = _get_secret("SUPABASE_URL")
SUPABASE_KEY = _get_secret("SUPABASE_KEY")
STORAGE_BUCKET = _get_secret("SUPABASE_STORAGE_BUCKET", "grievance-photos")

supabase = None
USE_SUPABASE = False

if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client, Client  # noqa: F401
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        USE_SUPABASE = True
        logger.info("Supabase configured — using cloud database as the single source of truth.")
    except Exception as e:
        supabase = None
        USE_SUPABASE = False
        logger.warning("Supabase client init failed (%s) — falling back to local SQLite.", e)
else:
    logger.info("No Supabase credentials found — using local SQLite database.")


def _sb_ok():
    return USE_SUPABASE and supabase is not None


DB_FILE = os.environ.get("HOSTEL_DB_FILE", "hostel_care.db")


# ==========================================
# 🧼 SEARCH SANITIZATION
# ==========================================
def _sanitize_search(term):
    """Strip characters that have special meaning in the PostgREST filter DSL
    (commas separate conditions, parentheses group them) to prevent filter
    injection / broken queries. Also caps length."""
    if not term:
        return ""
    cleaned = re.sub(r"[,()\r\n]", " ", str(term))
    return cleaned.strip()[:100]


def escape_like(string):
    """Escape special characters for SQL LIKE pattern matching (SQLite path)."""
    return string.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


# ==========================================
# 🗄️ LOCAL SQLITE (used only when Supabase is not configured)
# ==========================================
def get_connection():
    """Establish and return a connection to the SQLite database with busy timeout."""
    conn = sqlite3.connect(DB_FILE, timeout=15.0)
    conn.row_factory = sqlite3.Row
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
    """Initialize the local SQLite schema. No-op when Supabase is the backend."""
    if _sb_ok():
        return

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
        for col, ddl in [
            ('last_updated', "ALTER TABLE Grievances ADD COLUMN last_updated TEXT DEFAULT ''"),
            ('block_name', "ALTER TABLE Grievances ADD COLUMN block_name TEXT DEFAULT 'BH-1'"),
            ('priority', "ALTER TABLE Grievances ADD COLUMN priority TEXT DEFAULT 'Normal'"),
            ('assigned_staff', "ALTER TABLE Grievances ADD COLUMN assigned_staff TEXT DEFAULT ''"),
            ('suggestion', "ALTER TABLE Grievances ADD COLUMN suggestion TEXT DEFAULT ''"),
            ('photo_path', "ALTER TABLE Grievances ADD COLUMN photo_path TEXT DEFAULT ''"),
        ]:
            if col not in columns:
                cursor.execute(ddl)

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


# ==========================================
# 🖼️ PHOTO STORAGE (Supabase Storage when available, local disk in dev)
# ==========================================
def upload_photo(file_bytes, original_filename):
    """Upload a grievance photo and return a persistent reference.

    - With Supabase: uploads to the storage bucket and returns a public URL.
    - Without Supabase (local dev): writes to ./uploads and returns the path.
    Returns "" if nothing could be stored.
    """
    if not file_bytes:
        return ""

    ext = ""
    if "." in original_filename:
        ext = original_filename.rsplit(".", 1)[-1].lower()
    if ext not in ("png", "jpg", "jpeg", "webp"):
        ext = "jpg"

    stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    object_name = f"{stamp}.{ext}"
    content_type = mimetypes.types_map.get(f".{ext}", "image/jpeg")

    if _sb_ok():
        try:
            supabase.storage.from_(STORAGE_BUCKET).upload(
                object_name,
                file_bytes,
                {"content-type": content_type, "upsert": "false"},
            )
            return supabase.storage.from_(STORAGE_BUCKET).get_public_url(object_name)
        except Exception as e:
            logger.error("Supabase Storage upload failed: %s", e)
            raise DatabaseError("Photo upload to cloud storage failed.") from e

    # Local dev fallback
    try:
        os.makedirs("uploads", exist_ok=True)
        path = os.path.join("uploads", object_name)
        with open(path, "wb") as f:
            f.write(file_bytes)
        return path
    except Exception as e:
        logger.error("Local photo save failed: %s", e)
        return ""


# ==========================================
# 📋 GRIEVANCES
# ==========================================
def create_grievance(name, room, category, description, block_name="BH-1", priority="Normal", suggestion="", photo_path=""):
    """Insert a new grievance into the configured backend and return its ID."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if _sb_ok():
        try:
            payload = {
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
                "suggestion": suggestion,
                "photo_path": photo_path or "",
            }
            resp = supabase.table("Grievances").insert(payload).execute()
            return resp.data[0]["grievance_id"] if resp.data else None
        except Exception as e:
            logger.error("create_grievance (Supabase) failed: %s", e)
            raise DatabaseError("Could not save your complaint. Please try again.") from e

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Grievances (student_name, room_number, category, description, date_submitted, last_updated, block_name, priority, assigned_staff, suggestion, photo_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, '', ?, ?)
        ''', (name, room, category, description, now, now, block_name, priority, suggestion, photo_path or ""))
        grievance_id = cursor.lastrowid
        conn.commit()
    return grievance_id


def get_all_grievances(status_filter=None, block_filter=None, search_query=None):
    """Fetch all grievances from the configured backend."""
    if _sb_ok():
        try:
            q = supabase.table("Grievances").select("*")
            if status_filter and status_filter not in ("All", "All Statuses"):
                q = q.eq("status", status_filter)
            if block_filter and block_filter not in ("All", "All Blocks"):
                q = q.ilike("block_name", f"{block_filter}%")
            s = _sanitize_search(search_query)
            if s:
                q = q.or_(
                    f"student_name.ilike.%{s}%,"
                    f"room_number.ilike.%{s}%,"
                    f"category.ilike.%{s}%,"
                    f"block_name.ilike.%{s}%,"
                    f"assigned_staff.ilike.%{s}%,"
                    f"description.ilike.%{s}%,"
                    f"suggestion.ilike.%{s}%"
                )
            resp = q.order("date_submitted", desc=True).execute()
            return resp.data or []
        except Exception as e:
            logger.error("get_all_grievances (Supabase) failed: %s", e)
            return []

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
        return [dict(row) for row in cursor.fetchall()]


def get_grievance_by_id(grievance_id):
    """Fetch a single grievance by its ID."""
    if _sb_ok():
        try:
            resp = supabase.table("Grievances").select("*").eq("grievance_id", grievance_id).execute()
            return resp.data[0] if resp.data else None
        except Exception as e:
            logger.error("get_grievance_by_id (Supabase) failed: %s", e)
            return None

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
                "assigned_staff": assigned_staff,
            }).eq("grievance_id", grievance_id).execute()
            return
        except Exception as e:
            logger.error("update_grievance (Supabase) failed: %s", e)
            raise DatabaseError("Could not update the grievance.") from e

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
            return
        except Exception as e:
            logger.error("delete_grievance (Supabase) failed: %s", e)
            raise DatabaseError("Could not delete the grievance.") from e

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
            for row in (resp.data or []):
                st = (row.get('status') or '').lower().replace(" ", "_")
                if st in counts:
                    counts[st] += 1
                counts['total'] += 1
                if row.get('priority') and 'Emergency' in row['priority'] and row.get('status') != 'Resolved':
                    counts['emergency'] += 1
            return counts
        except Exception as e:
            logger.error("get_grievance_counts (Supabase) failed: %s", e)
            return counts

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) as count FROM Grievances GROUP BY status")
        for row in cursor.fetchall():
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
    """Fetch grievances by room number, student name, or block (kept for compatibility)."""
    if _sb_ok():
        try:
            s = _sanitize_search(search_term)
            resp = supabase.table("Grievances").select("*").or_(
                f"room_number.ilike.%{s}%,student_name.ilike.%{s}%,block_name.ilike.%{s}%"
            ).order("date_submitted", desc=True).execute()
            return resp.data or []
        except Exception as e:
            logger.error("get_grievances_by_room_or_name (Supabase) failed: %s", e)
            return []

    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT * FROM Grievances
            WHERE room_number LIKE ? ESCAPE '\\' OR student_name LIKE ? ESCAPE '\\' OR block_name LIKE ? ESCAPE '\\' OR CAST(grievance_id AS TEXT) LIKE ? ESCAPE '\\'
            ORDER BY date_submitted DESC
        """
        pattern = f"%{escape_like(search_term)}%"
        cursor.execute(query, (pattern, pattern, pattern, pattern))
        return [dict(row) for row in cursor.fetchall()]


def get_grievances_by_room_and_name(room_number, student_name, block_name=None):
    """Fetch grievances matching BOTH room number AND student name (secure forgot-ID lookup)."""
    if _sb_ok():
        try:
            room = _sanitize_search(room_number)
            name = _sanitize_search(student_name)
            q = supabase.table("Grievances").select("*").ilike("room_number", room.strip()).ilike("student_name", f"%{name.strip()}%")
            if block_name and block_name != "All Blocks":
                q = q.eq("block_name", block_name)
            resp = q.order("date_submitted", desc=True).execute()
            return resp.data or []
        except Exception as e:
            logger.error("get_grievances_by_room_and_name (Supabase) failed: %s", e)
            return []

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
        return [dict(row) for row in cursor.fetchall()]


# ==========================================
# 📢 NOTICES
# ==========================================
def cleanup_expired_notices():
    """Auto-delete notices whose expiry timestamp has passed."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if _sb_ok():
        try:
            resp = supabase.table("Notices").select("notice_id, expires_at").execute()
            for n in (resp.data or []):
                exp = n.get("expires_at")
                if exp and exp != "" and exp <= now:
                    supabase.table("Notices").delete().eq("notice_id", n["notice_id"]).execute()
        except Exception as e:
            logger.error("cleanup_expired_notices (Supabase) failed: %s", e)
        return

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Notices WHERE expires_at != '' AND expires_at <= ?", (now,))
            conn.commit()
    except Exception as e:
        logger.error("cleanup_expired_notices (SQLite) failed: %s", e)


def create_notice(title, content, category, target_block="All Blocks", posted_by="Hostel Warden Office", expiry_hours=0):
    """Insert a new notice/announcement and return its ID."""
    now_dt = datetime.datetime.now()
    now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")

    expires_at = ""
    if expiry_hours and float(expiry_hours) != 0:
        exp_dt = now_dt + datetime.timedelta(hours=float(expiry_hours))
        expires_at = exp_dt.strftime("%Y-%m-%d %H:%M:%S")

    if _sb_ok():
        try:
            resp = supabase.table("Notices").insert({
                "title": title,
                "content": content,
                "category": category,
                "target_block": target_block,
                "date_posted": now_str,
                "posted_by": posted_by,
                "expires_at": expires_at,
            }).execute()
            return resp.data[0]["notice_id"] if resp.data else None
        except Exception as e:
            logger.error("create_notice (Supabase) failed: %s", e)
            raise DatabaseError("Could not publish the notice.") from e

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Notices (title, content, category, target_block, date_posted, posted_by, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, content, category, target_block, now_str, posted_by, expires_at))
        notice_id = cursor.lastrowid
        conn.commit()
    return notice_id


def get_all_notices(block_filter=None, category_filter=None):
    """Fetch all published active notices, automatically purging expired ones."""
    cleanup_expired_notices()

    if _sb_ok():
        try:
            resp = supabase.table("Notices").select("*").order("date_posted", desc=True).execute()
            notices = resp.data or []
            if block_filter and block_filter != "All Blocks":
                notices = [n for n in notices if n.get("target_block") == block_filter or n.get("target_block") == "All Blocks"]
            if category_filter and category_filter != "All":
                notices = [n for n in notices if n.get("category") == category_filter]
            return notices
        except Exception as e:
            logger.error("get_all_notices (Supabase) failed: %s", e)
            return []

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
        return [dict(row) for row in cursor.fetchall()]


def delete_notice(notice_id):
    """Delete a notice by ID."""
    if _sb_ok():
        try:
            supabase.table("Notices").delete().eq("notice_id", notice_id).execute()
            return
        except Exception as e:
            logger.error("delete_notice (Supabase) failed: %s", e)
            raise DatabaseError("Could not delete the notice.") from e

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Notices WHERE notice_id = ?", (notice_id,))
        conn.commit()


# ==========================================
# 🌴 STUDENT LEAVE & GATE PASS OPERATIONS
# ==========================================
def create_leave_application(name, block, room, phone, parent_phone, reason, destination, from_date, to_date, teacher_name):
    """Insert a new leave application and return its ID."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if _sb_ok():
        try:
            resp = supabase.table("LeaveApplications").insert({
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
                "last_updated": now,
            }).execute()
            return resp.data[0]["leave_id"] if resp.data else None
        except Exception as e:
            logger.error("create_leave_application (Supabase) failed: %s", e)
            raise DatabaseError("Could not submit your leave application.") from e

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
    return leave_id


def get_leave_application_by_id(leave_id):
    """Fetch leave application details by Leave ID."""
    if _sb_ok():
        try:
            resp = supabase.table("LeaveApplications").select("*").eq("leave_id", leave_id).execute()
            return resp.data[0] if resp.data else None
        except Exception as e:
            logger.error("get_leave_application_by_id (Supabase) failed: %s", e)
            return None

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM LeaveApplications WHERE leave_id = ?", (leave_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_leave_applications_by_room_and_name(room_number, student_name):
    """Fetch leave applications matching room number AND student name."""
    if _sb_ok():
        try:
            room = _sanitize_search(room_number)
            name = _sanitize_search(student_name)
            resp = supabase.table("LeaveApplications").select("*").ilike("room_number", room.strip()).ilike("student_name", f"%{name.strip()}%").order("date_submitted", desc=True).execute()
            return resp.data or []
        except Exception as e:
            logger.error("get_leave_applications_by_room_and_name (Supabase) failed: %s", e)
            return []

    with get_db() as conn:
        cursor = conn.cursor()
        query = """
            SELECT * FROM LeaveApplications
            WHERE LOWER(TRIM(room_number)) = LOWER(TRIM(?))
              AND LOWER(TRIM(student_name)) LIKE LOWER(TRIM(?))
            ORDER BY date_submitted DESC
        """
        cursor.execute(query, (room_number.strip(), f"%{escape_like(student_name.strip())}%"))
        return [dict(row) for row in cursor.fetchall()]


def get_all_leave_applications(status_filter=None, block_filter=None, search_query=None):
    """Fetch all leave applications with optional status/block filtering and text search."""
    if _sb_ok():
        try:
            q = supabase.table("LeaveApplications").select("*")
            if status_filter and status_filter not in ("All", "All Statuses"):
                q = q.eq("status", status_filter)
            if block_filter and block_filter not in ("All", "All Blocks"):
                q = q.ilike("block_name", f"{block_filter}%")
            s = _sanitize_search(search_query)
            if s:
                q = q.or_(
                    f"student_name.ilike.%{s}%,"
                    f"room_number.ilike.%{s}%,"
                    f"granting_teacher.ilike.%{s}%,"
                    f"destination.ilike.%{s}%"
                )
            resp = q.order("date_submitted", desc=True).execute()
            return resp.data or []
        except Exception as e:
            logger.error("get_all_leave_applications (Supabase) failed: %s", e)
            return []

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
        return [dict(row) for row in cursor.fetchall()]


def update_leave_status(leave_id, status, warden_remarks="", gate_pass_code=""):
    """Update leave status, warden remarks, and gate pass code."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if _sb_ok():
        try:
            supabase.table("LeaveApplications").update({
                "status": status,
                "warden_remarks": warden_remarks,
                "gate_pass_code": gate_pass_code,
                "last_updated": now,
            }).eq("leave_id", leave_id).execute()
            return
        except Exception as e:
            logger.error("update_leave_status (Supabase) failed: %s", e)
            raise DatabaseError("Could not update the leave application.") from e

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
            return
        except Exception as e:
            logger.error("delete_leave_application (Supabase) failed: %s", e)
            raise DatabaseError("Could not delete the leave application.") from e

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM LeaveApplications WHERE leave_id = ?", (leave_id,))
        conn.commit()


# Initialize the local SQLite schema on import (no-op when Supabase is configured)
init_db()
