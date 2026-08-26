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
            ('rating', "ALTER TABLE Grievances ADD COLUMN rating INTEGER DEFAULT 0"),
            ('feedback', "ALTER TABLE Grievances ADD COLUMN feedback TEXT DEFAULT ''"),
            ('student_email', "ALTER TABLE Grievances ADD COLUMN student_email TEXT DEFAULT ''"),
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
                last_updated TEXT DEFAULT '',
                returned_at TEXT DEFAULT '',
                student_email TEXT DEFAULT ''
            )
        ''')

        cursor.execute("PRAGMA table_info(LeaveApplications)")
        leave_cols = [row['name'] for row in cursor.fetchall()]
        for col, ddl in [
            ('returned_at', "ALTER TABLE LeaveApplications ADD COLUMN returned_at TEXT DEFAULT ''"),
            ('student_email', "ALTER TABLE LeaveApplications ADD COLUMN student_email TEXT DEFAULT ''"),
        ]:
            if col not in leave_cols:
                cursor.execute(ddl)

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS AuditLog (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                action_type TEXT NOT NULL,
                entity_type TEXT DEFAULT '',
                entity_id TEXT DEFAULT '',
                description TEXT DEFAULT '',
                actor TEXT DEFAULT 'Warden',
                timestamp TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS MessFeedback (
                feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                meal_type TEXT NOT NULL,
                rating INTEGER DEFAULT 0,
                comment TEXT DEFAULT '',
                room_number TEXT DEFAULT '',
                date_posted TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS MessMenu (
                menu_id INTEGER PRIMARY KEY AUTOINCREMENT,
                menu_date TEXT NOT NULL,
                breakfast TEXT DEFAULT '',
                lunch TEXT DEFAULT '',
                dinner TEXT DEFAULT '',
                updated_at TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS VisitorPasses (
                pass_id INTEGER PRIMARY KEY AUTOINCREMENT,
                visitor_name TEXT NOT NULL,
                visitor_id_type TEXT DEFAULT '',
                visitor_id_number TEXT DEFAULT '',
                host_student TEXT NOT NULL,
                host_room TEXT DEFAULT '',
                host_block TEXT DEFAULT 'BH-1',
                purpose TEXT DEFAULT '',
                visit_date TEXT NOT NULL,
                entry_time TEXT DEFAULT '',
                exit_time TEXT DEFAULT '',
                status TEXT DEFAULT 'Registered',
                date_created TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS LostAndFound (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                item_type TEXT NOT NULL DEFAULT 'Lost',
                category TEXT DEFAULT 'Other',
                location TEXT DEFAULT '',
                description TEXT DEFAULT '',
                photo_path TEXT DEFAULT '',
                contact_info TEXT DEFAULT '',
                status TEXT DEFAULT 'Open',
                date_posted TEXT NOT NULL
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

    # Validate real image magic bytes (defends against renamed/spoofed uploads).
    # file_bytes may be a memoryview (Streamlit) — memoryview()[:12] then bytes() is safe.
    header = bytes(memoryview(file_bytes)[:12])
    is_png = header.startswith(b"\x89PNG\r\n\x1a\n")
    is_jpg = header.startswith(b"\xff\xd8\xff")
    is_webp = header[:4] == b"RIFF" and header[8:12] == b"WEBP"
    if not (is_png or is_jpg or is_webp):
        raise DatabaseError("That file does not look like a valid PNG/JPEG/WebP image.")

    ext = ""
    if "." in original_filename:
        ext = original_filename.rsplit(".", 1)[-1].lower()
    if ext not in ("png", "jpg", "jpeg", "webp"):
        ext = "png" if is_png else ("webp" if is_webp else "jpg")

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
def create_grievance(name, room, category, description, block_name="BH-1", priority="Normal", suggestion="", photo_path="", student_email=""):
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
                "student_email": student_email or "",
            }
            resp = supabase.table("Grievances").insert(payload).execute()
            return resp.data[0]["grievance_id"] if resp.data else None
        except Exception as e:
            logger.error("create_grievance (Supabase) failed: %s", e)
            raise DatabaseError("Could not save your complaint. Please try again.") from e

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Grievances (student_name, room_number, category, description, date_submitted, last_updated, block_name, priority, assigned_staff, suggestion, photo_path, student_email)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, '', ?, ?, ?)
        ''', (name, room, category, description, now, now, block_name, priority, suggestion, photo_path or "", student_email or ""))
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
def create_leave_application(name, block, room, phone, parent_phone, reason, destination, from_date, to_date, teacher_name, student_email=""):
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
                "returned_at": "",
                "student_email": student_email or "",
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
                status, warden_remarks, gate_pass_code, date_submitted, last_updated, returned_at, student_email
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending Warden Approval', '', '', ?, ?, '', ?)
        ''', (name, block, room, phone, parent_phone, reason, destination, from_date, to_date, teacher_name, now, now, student_email or ""))
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


def get_leave_by_gate_pass_code(code):
    """Look up an approved leave application by its exact gate pass code
    (used by the gate security verifier). Returns the record or None."""
    code = (code or "").strip()
    if not code:
        return None

    if _sb_ok():
        try:
            resp = supabase.table("LeaveApplications").select("*").eq("gate_pass_code", code).execute()
            return resp.data[0] if resp.data else None
        except Exception as e:
            logger.error("get_leave_by_gate_pass_code (Supabase) failed: %s", e)
            return None

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM LeaveApplications WHERE gate_pass_code = ?", (code,))
        row = cursor.fetchone()
        return dict(row) if row else None


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


# ==========================================
# ⭐ RESOLUTION RATINGS & FEEDBACK
# ==========================================
def submit_grievance_feedback(grievance_id, rating, feedback=""):
    """Save a student's 1–5 star rating and feedback on a resolved grievance."""
    try:
        rating = int(rating)
    except (TypeError, ValueError):
        rating = 0
    rating = max(0, min(5, rating))
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if _sb_ok():
        try:
            # Guard: never overwrite an existing rating.
            existing = get_grievance_by_id(grievance_id)
            if existing and int(existing.get("rating") or 0) > 0:
                return
            supabase.table("Grievances").update({
                "rating": rating,
                "feedback": feedback,
                "last_updated": now,
            }).eq("grievance_id", grievance_id).execute()
            return
        except Exception as e:
            logger.error("submit_grievance_feedback (Supabase) failed: %s", e)
            raise DatabaseError("Could not save your rating. Please try again.") from e

    with get_db() as conn:
        cursor = conn.cursor()
        # Guard at the SQL level: only set when no rating exists yet.
        cursor.execute(
            "UPDATE Grievances SET rating = ?, feedback = ?, last_updated = ? "
            "WHERE grievance_id = ? AND (rating IS NULL OR rating = 0)",
            (rating, feedback, now, grievance_id),
        )
        conn.commit()


# ==========================================
# 📊 ANALYTICS & SLA
# ==========================================
def _parse_dt(value):
    try:
        return datetime.datetime.strptime((value or "").strip(), "%Y-%m-%d %H:%M:%S")
    except (ValueError, AttributeError):
        return None


def get_analytics_summary():
    """Aggregate operational KPIs, distributions, ratings, and SLA aging."""
    rows = get_all_grievances()  # backend-agnostic: all grievances
    now = datetime.datetime.now()

    summary = {
        "total": len(rows),
        "pending": 0, "in_progress": 0, "resolved": 0, "rejected": 0, "emergency": 0,
        "resolution_rate": 0.0,
        "avg_rating": 0.0, "rated_count": 0,
        "by_category": {}, "by_block": {}, "by_priority": {}, "by_status": {},
        "overdue_24_48h": 0, "overdue_48h": 0,
    }

    rating_sum = 0
    for r in rows:
        status = (r.get("status") or "").strip()
        key = status.lower().replace(" ", "_")
        if key in ("pending", "in_progress", "resolved", "rejected"):
            summary[key] += 1
        summary["by_status"][status or "Unknown"] = summary["by_status"].get(status or "Unknown", 0) + 1

        cat = (r.get("category") or "Other").strip()
        summary["by_category"][cat] = summary["by_category"].get(cat, 0) + 1

        blk = (r.get("block_name") or "Unknown").strip()
        summary["by_block"][blk] = summary["by_block"].get(blk, 0) + 1

        pri = (r.get("priority") or "Normal").strip()
        summary["by_priority"][pri] = summary["by_priority"].get(pri, 0) + 1

        if "Emergency" in pri and status != "Resolved":
            summary["emergency"] += 1

        try:
            rt = int(r.get("rating") or 0)
        except (TypeError, ValueError):
            rt = 0
        if rt > 0:
            rating_sum += rt
            summary["rated_count"] += 1

        # SLA aging on still-open tickets
        if status in ("Pending", "In Progress"):
            dt = _parse_dt(r.get("date_submitted"))
            if dt:
                age_h = (now - dt).total_seconds() / 3600.0
                if age_h > 48:
                    summary["overdue_48h"] += 1
                elif age_h > 24:
                    summary["overdue_24_48h"] += 1

    if summary["total"]:
        summary["resolution_rate"] = round(summary["resolved"] * 100.0 / summary["total"], 1)
    if summary["rated_count"]:
        summary["avg_rating"] = round(rating_sum / summary["rated_count"], 2)

    return summary


def detect_cluster_outages(window_hours=48, threshold=2):
    """Flag a real outage only when >= `threshold` DISTINCT rooms in the same
    (block, category) report unresolved complaints within `window_hours`. Counting
    distinct rooms avoids false alarms from one room filing repeat tickets."""
    rows = get_all_grievances()
    now = datetime.datetime.now()
    groups = {}
    for r in rows:
        status = (r.get("status") or "").strip()
        if status in ("Resolved", "Rejected"):
            continue
        dt = _parse_dt(r.get("date_submitted"))
        if not dt or (now - dt).total_seconds() / 3600.0 > window_hours:
            continue
        block = (r.get("block_name") or "Unknown").strip()
        cat = (r.get("category") or "Other").strip()
        groups.setdefault((block, cat), []).append(r)

    alerts = []
    for (block, cat), items in groups.items():
        distinct_rooms = {(it.get("room_number") or "").strip().lower() for it in items}
        distinct_rooms.discard("")
        if len(distinct_rooms) >= threshold:
            alerts.append({
                "block": block,
                "category": cat,
                "count": len(items),
                "room_count": len(distinct_rooms),
                "ticket_ids": [it.get("grievance_id") for it in items],
            })
    alerts.sort(key=lambda a: a["room_count"], reverse=True)
    return alerts


# ==========================================
# 🎒 LOST & FOUND
# ==========================================
def create_lost_found_item(title, item_type, category, location, description, contact_info="", photo_path=""):
    """Create a Lost or Found bulletin entry and return its ID."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if _sb_ok():
        try:
            resp = supabase.table("LostAndFound").insert({
                "title": title,
                "item_type": item_type,
                "category": category,
                "location": location,
                "description": description,
                "photo_path": photo_path or "",
                "contact_info": contact_info,
                "status": "Open",
                "date_posted": now,
            }).execute()
            return resp.data[0]["item_id"] if resp.data else None
        except Exception as e:
            logger.error("create_lost_found_item (Supabase) failed: %s", e)
            raise DatabaseError("Could not post the item. Please try again.") from e

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO LostAndFound (title, item_type, category, location, description, photo_path, contact_info, status, date_posted)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Open', ?)
        ''', (title, item_type, category, location, description, photo_path or "", contact_info, now))
        item_id = cursor.lastrowid
        conn.commit()
    return item_id


def get_all_lost_found(item_type_filter=None, status_filter=None, search_query=None):
    """Fetch Lost & Found items with optional type/status filters and text search."""
    if _sb_ok():
        try:
            q = supabase.table("LostAndFound").select("*")
            if item_type_filter and item_type_filter not in ("All", "All Types"):
                q = q.eq("item_type", item_type_filter)
            if status_filter and status_filter not in ("All", "All Statuses"):
                q = q.eq("status", status_filter)
            s = _sanitize_search(search_query)
            if s:
                q = q.or_(
                    f"title.ilike.%{s}%,category.ilike.%{s}%,location.ilike.%{s}%,description.ilike.%{s}%"
                )
            resp = q.order("date_posted", desc=True).execute()
            return resp.data or []
        except Exception as e:
            logger.error("get_all_lost_found (Supabase) failed: %s", e)
            return []

    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM LostAndFound WHERE 1=1"
        params = []
        if item_type_filter and item_type_filter not in ("All", "All Types"):
            query += " AND item_type = ?"
            params.append(item_type_filter)
        if status_filter and status_filter not in ("All", "All Statuses"):
            query += " AND status = ?"
            params.append(status_filter)
        if search_query and search_query.strip():
            sq = f"%{escape_like(search_query.strip())}%"
            query += (" AND (title LIKE ? ESCAPE '\\' OR category LIKE ? ESCAPE '\\'"
                      " OR location LIKE ? ESCAPE '\\' OR description LIKE ? ESCAPE '\\')")
            params.extend([sq, sq, sq, sq])
        query += " ORDER BY date_posted DESC"
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


def update_lost_found_status(item_id, status):
    """Update a Lost & Found item's status (e.g. 'Claimed / Returned')."""
    if _sb_ok():
        try:
            supabase.table("LostAndFound").update({"status": status}).eq("item_id", item_id).execute()
            return
        except Exception as e:
            logger.error("update_lost_found_status (Supabase) failed: %s", e)
            raise DatabaseError("Could not update the item.") from e

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE LostAndFound SET status = ? WHERE item_id = ?", (status, item_id))
        conn.commit()


def delete_lost_found_item(item_id):
    """Delete a Lost & Found item by ID."""
    if _sb_ok():
        try:
            supabase.table("LostAndFound").delete().eq("item_id", item_id).execute()
            return
        except Exception as e:
            logger.error("delete_lost_found_item (Supabase) failed: %s", e)
            raise DatabaseError("Could not delete the item.") from e

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM LostAndFound WHERE item_id = ?", (item_id,))
        conn.commit()


# ==========================================
# ⏱️ SLA — TARGETED OVERDUE QUERY (A5)
# ==========================================
def get_overdue_grievances(cutoff_hours=24):
    """Return still-open tickets submitted at least `cutoff_hours` ago,
    newest-breach first. Uses a targeted query instead of scanning everything."""
    cutoff = (datetime.datetime.now() - datetime.timedelta(hours=cutoff_hours)).strftime("%Y-%m-%d %H:%M:%S")

    if _sb_ok():
        try:
            resp = (supabase.table("Grievances").select("*")
                    .in_("status", ["Pending", "In Progress"])
                    .lte("date_submitted", cutoff)
                    .order("date_submitted", desc=False).execute())
            return resp.data or []
        except Exception as e:
            logger.error("get_overdue_grievances (Supabase) failed: %s", e)
            return []

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Grievances WHERE status IN ('Pending','In Progress') "
            "AND date_submitted <= ? ORDER BY date_submitted ASC",
            (cutoff,),
        )
        return [dict(row) for row in cursor.fetchall()]


def set_grievance_priority(grievance_id, priority):
    """Update only a grievance's priority (used by the escalation engine)."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if _sb_ok():
        try:
            supabase.table("Grievances").update(
                {"priority": priority, "last_updated": now}
            ).eq("grievance_id", grievance_id).execute()
            return
        except Exception as e:
            logger.error("set_grievance_priority (Supabase) failed: %s", e)
            raise DatabaseError("Could not update priority.") from e
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Grievances SET priority = ?, last_updated = ? WHERE grievance_id = ?",
                       (priority, now, grievance_id))
        conn.commit()


# ==========================================
# 📋 AUDIT LOG (B1)
# ==========================================
def log_action(action_type, entity_type="", entity_id="", description="", actor="Warden"):
    """Append an entry to the audit log. Best-effort — never blocks the caller."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "action_type": action_type, "entity_type": entity_type,
        "entity_id": str(entity_id), "description": description,
        "actor": actor, "timestamp": now,
    }
    try:
        if _sb_ok():
            supabase.table("AuditLog").insert(payload).execute()
        else:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO AuditLog (action_type, entity_type, entity_id, description, actor, timestamp) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (action_type, entity_type, str(entity_id), description, actor, now),
                )
                conn.commit()
    except Exception as e:
        logger.error("log_action failed: %s", e)


def get_audit_log(action_filter=None, search_query=None, limit=500):
    """Fetch audit log entries, newest first, with optional action filter and search."""
    if _sb_ok():
        try:
            q = supabase.table("AuditLog").select("*")
            if action_filter and action_filter not in ("All", "All Actions"):
                q = q.eq("action_type", action_filter)
            s = _sanitize_search(search_query)
            if s:
                q = q.or_(f"description.ilike.%{s}%,actor.ilike.%{s}%,entity_type.ilike.%{s}%")
            resp = q.order("timestamp", desc=True).limit(limit).execute()
            return resp.data or []
        except Exception as e:
            logger.error("get_audit_log (Supabase) failed: %s", e)
            return []
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM AuditLog WHERE 1=1"
        params = []
        if action_filter and action_filter not in ("All", "All Actions"):
            query += " AND action_type = ?"
            params.append(action_filter)
        if search_query and search_query.strip():
            sq = f"%{escape_like(search_query.strip())}%"
            query += " AND (description LIKE ? ESCAPE '\\' OR actor LIKE ? ESCAPE '\\' OR entity_type LIKE ? ESCAPE '\\')"
            params.extend([sq, sq, sq])
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]


# ==========================================
# ⬆️ PRIORITY ESCALATION ENGINE (B2)
# ==========================================
def auto_escalate_priorities():
    """Escalate stale open tickets: Normal->Urgent after 24h, Urgent->Emergency after 48h.
    Returns the list of escalations performed (each logged to the audit trail)."""
    rows = get_all_grievances()
    now = datetime.datetime.now()
    escalations = []
    for r in rows:
        status = (r.get("status") or "").strip()
        if status not in ("Pending", "In Progress"):
            continue
        dt = _parse_dt(r.get("date_submitted"))
        if not dt:
            continue
        age_h = (now - dt).total_seconds() / 3600.0
        pri = r.get("priority") or "Normal"
        tier = 3 if "Emergency" in pri else (2 if "Urgent" in pri else 1)
        new_pri = None
        if tier == 1 and age_h > 24:
            new_pri = "Urgent"
        elif tier == 2 and age_h > 48:
            new_pri = "Emergency"
        if new_pri:
            gid = r.get("grievance_id")
            try:
                set_grievance_priority(gid, new_pri)
                log_action("AUTO_ESCALATE", "Grievance", gid,
                           f"Priority auto-escalated to {new_pri} after {int(age_h)}h open", actor="System")
                escalations.append({"grievance_id": gid, "new_priority": new_pri, "age_h": round(age_h, 1)})
            except DatabaseError:
                pass
    return escalations


# ==========================================
# 👷 STAFF PERFORMANCE (B3)
# ==========================================
def get_staff_performance():
    """Per-staff resolution stats: tickets resolved, avg rating, avg resolution hours."""
    rows = get_all_grievances()
    stats = {}
    for r in rows:
        if (r.get("status") or "").strip() != "Resolved":
            continue
        staff = (r.get("assigned_staff") or "").strip()
        if not staff:
            continue
        s = stats.setdefault(staff, {"staff": staff, "resolved": 0, "rating_sum": 0, "rated": 0, "hours_sum": 0.0, "timed": 0})
        s["resolved"] += 1
        try:
            rt = int(r.get("rating") or 0)
        except (TypeError, ValueError):
            rt = 0
        if rt > 0:
            s["rating_sum"] += rt
            s["rated"] += 1
        d1, d2 = _parse_dt(r.get("date_submitted")), _parse_dt(r.get("last_updated"))
        if d1 and d2 and d2 >= d1:
            s["hours_sum"] += (d2 - d1).total_seconds() / 3600.0
            s["timed"] += 1
    out = []
    for s in stats.values():
        out.append({
            "staff": s["staff"],
            "resolved": s["resolved"],
            "avg_rating": round(s["rating_sum"] / s["rated"], 2) if s["rated"] else 0.0,
            "avg_resolution_h": round(s["hours_sum"] / s["timed"], 1) if s["timed"] else 0.0,
        })
    out.sort(key=lambda x: x["resolved"], reverse=True)
    return out


# ==========================================
# 📈 MONTHLY TRENDS (B4)
# ==========================================
def get_monthly_trends():
    """Group grievances by YYYY-MM: volume and resolution rate. Chronological."""
    rows = get_all_grievances()
    buckets = {}
    for r in rows:
        dt = _parse_dt(r.get("date_submitted"))
        if not dt:
            continue
        key = dt.strftime("%Y-%m")
        b = buckets.setdefault(key, {"month": key, "volume": 0, "resolved": 0})
        b["volume"] += 1
        if (r.get("status") or "").strip() == "Resolved":
            b["resolved"] += 1
    out = []
    for key in sorted(buckets.keys()):
        b = buckets[key]
        b["resolution_rate"] = round(b["resolved"] * 100.0 / b["volume"], 1) if b["volume"] else 0.0
        out.append(b)
    return out


# ==========================================
# 🔁 RETURN CHECK-IN & LEAVE QUOTA (B5, B6)
# ==========================================
def mark_student_returned(leave_id):
    """Record a student's return from leave (timestamps returned_at)."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if _sb_ok():
        try:
            supabase.table("LeaveApplications").update(
                {"returned_at": now, "last_updated": now}
            ).eq("leave_id", leave_id).execute()
            return now
        except Exception as e:
            logger.error("mark_student_returned (Supabase) failed: %s", e)
            raise DatabaseError("Could not record the return.") from e
    with get_db() as conn:
        conn.execute("UPDATE LeaveApplications SET returned_at = ?, last_updated = ? WHERE leave_id = ?",
                     (now, now, leave_id))
        conn.commit()
    return now


def get_leave_days_used(room_number, student_name):
    """Sum days of approved leave for this student in the current calendar year."""
    apps = get_leave_applications_by_room_and_name(room_number, student_name)
    year = datetime.datetime.now().year
    total = 0
    for a in apps:
        if "Approved" not in (a.get("status") or ""):
            continue
        try:
            fd = datetime.datetime.strptime(a["from_date"], "%Y-%m-%d").date()
            td = datetime.datetime.strptime(a["to_date"], "%Y-%m-%d").date()
        except (ValueError, KeyError, TypeError):
            continue
        if fd.year == year or td.year == year:
            total += max(0, (td - fd).days) + 1
    return total


# ==========================================
# 🎒 LOST & FOUND — AUTO-EXPIRY (B7)
# ==========================================
def cleanup_old_lost_found(days=30):
    """Archive Open Lost & Found items older than `days`."""
    cutoff = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    if _sb_ok():
        try:
            resp = supabase.table("LostAndFound").select("item_id, status, date_posted").eq("status", "Open").execute()
            for it in (resp.data or []):
                if (it.get("date_posted") or "") <= cutoff:
                    supabase.table("LostAndFound").update({"status": "Archived"}).eq("item_id", it["item_id"]).execute()
        except Exception as e:
            logger.error("cleanup_old_lost_found (Supabase) failed: %s", e)
        return
    try:
        with get_db() as conn:
            conn.execute("UPDATE LostAndFound SET status='Archived' WHERE status='Open' AND date_posted <= ?", (cutoff,))
            conn.commit()
    except Exception as e:
        logger.error("cleanup_old_lost_found (SQLite) failed: %s", e)


# ==========================================
# 🍽️ MESS FEEDBACK & MENU (B9)
# ==========================================
def create_mess_feedback(meal_type, rating, comment="", room_number=""):
    """Record a mess/food rating (1-5) for a meal."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        rating = max(1, min(5, int(rating)))
    except (TypeError, ValueError):
        rating = 3
    if _sb_ok():
        try:
            resp = supabase.table("MessFeedback").insert({
                "meal_type": meal_type, "rating": rating, "comment": comment,
                "room_number": room_number, "date_posted": now,
            }).execute()
            return resp.data[0]["feedback_id"] if resp.data else None
        except Exception as e:
            logger.error("create_mess_feedback (Supabase) failed: %s", e)
            raise DatabaseError("Could not submit mess feedback.") from e
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO MessFeedback (meal_type, rating, comment, room_number, date_posted) VALUES (?, ?, ?, ?, ?)",
                    (meal_type, rating, comment, room_number, now))
        fid = cur.lastrowid
        conn.commit()
    return fid


def get_mess_feedback(limit=500):
    """Fetch mess feedback, newest first."""
    if _sb_ok():
        try:
            resp = supabase.table("MessFeedback").select("*").order("date_posted", desc=True).limit(limit).execute()
            return resp.data or []
        except Exception as e:
            logger.error("get_mess_feedback (Supabase) failed: %s", e)
            return []
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM MessFeedback ORDER BY date_posted DESC LIMIT ?", (limit,))
        return [dict(r) for r in cur.fetchall()]


_STOPWORDS = {"the", "and", "was", "were", "for", "with", "this", "that", "very", "too",
              "not", "but", "had", "has", "are", "you", "your", "have", "is", "it",
              "of", "to", "a", "in", "on", "at", "my", "me", "we", "so", "no"}


def get_mess_analytics():
    """Per-meal averages/counts, overall average, and top complaint keywords."""
    rows = get_mess_feedback(limit=2000)
    by_meal = {}
    overall_sum = 0
    kw = {}
    for r in rows:
        meal = (r.get("meal_type") or "Other").strip()
        try:
            rt = int(r.get("rating") or 0)
        except (TypeError, ValueError):
            rt = 0
        m = by_meal.setdefault(meal, {"meal": meal, "count": 0, "sum": 0})
        m["count"] += 1
        m["sum"] += rt
        overall_sum += rt
        # keyword mining from low-rating comments (complaints)
        if rt <= 2 and r.get("comment"):
            for w in re.findall(r"[a-zA-Z]{3,}", r["comment"].lower()):
                if w not in _STOPWORDS:
                    kw[w] = kw.get(w, 0) + 1
    meals = []
    for m in by_meal.values():
        m["avg"] = round(m["sum"] / m["count"], 2) if m["count"] else 0.0
        meals.append(m)
    meals.sort(key=lambda x: x["meal"])
    top_keywords = sorted(kw.items(), key=lambda x: x[1], reverse=True)[:10]
    total = len(rows)
    return {
        "total": total,
        "overall_avg": round(overall_sum / total, 2) if total else 0.0,
        "by_meal": meals,
        "top_complaint_keywords": top_keywords,
    }


def set_mess_menu(menu_date, breakfast, lunch, dinner):
    """Create or update the mess menu for a given date (YYYY-MM-DD)."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if _sb_ok():
        try:
            existing = supabase.table("MessMenu").select("menu_id").eq("menu_date", menu_date).execute()
            data = {"menu_date": menu_date, "breakfast": breakfast, "lunch": lunch, "dinner": dinner, "updated_at": now}
            if existing.data:
                supabase.table("MessMenu").update(data).eq("menu_id", existing.data[0]["menu_id"]).execute()
            else:
                supabase.table("MessMenu").insert(data).execute()
            return
        except Exception as e:
            logger.error("set_mess_menu (Supabase) failed: %s", e)
            raise DatabaseError("Could not save the menu.") from e
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT menu_id FROM MessMenu WHERE menu_date = ?", (menu_date,))
        row = cur.fetchone()
        if row:
            cur.execute("UPDATE MessMenu SET breakfast=?, lunch=?, dinner=?, updated_at=? WHERE menu_id=?",
                        (breakfast, lunch, dinner, now, row["menu_id"]))
        else:
            cur.execute("INSERT INTO MessMenu (menu_date, breakfast, lunch, dinner, updated_at) VALUES (?, ?, ?, ?, ?)",
                        (menu_date, breakfast, lunch, dinner, now))
        conn.commit()


def get_mess_menu(menu_date):
    """Return the menu dict for a date, or None."""
    if _sb_ok():
        try:
            resp = supabase.table("MessMenu").select("*").eq("menu_date", menu_date).execute()
            return resp.data[0] if resp.data else None
        except Exception as e:
            logger.error("get_mess_menu (Supabase) failed: %s", e)
            return None
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM MessMenu WHERE menu_date = ?", (menu_date,))
        row = cur.fetchone()
        return dict(row) if row else None


# ==========================================
# 👤 VISITOR PASSES (B10)
# ==========================================
def create_visitor_pass(visitor_name, visitor_id_type, visitor_id_number, host_student,
                        host_room, host_block, purpose, visit_date):
    """Register a visitor pass and return its ID."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if _sb_ok():
        try:
            resp = supabase.table("VisitorPasses").insert({
                "visitor_name": visitor_name, "visitor_id_type": visitor_id_type,
                "visitor_id_number": visitor_id_number, "host_student": host_student,
                "host_room": host_room, "host_block": host_block, "purpose": purpose,
                "visit_date": visit_date, "entry_time": "", "exit_time": "",
                "status": "Registered", "date_created": now,
            }).execute()
            return resp.data[0]["pass_id"] if resp.data else None
        except Exception as e:
            logger.error("create_visitor_pass (Supabase) failed: %s", e)
            raise DatabaseError("Could not register the visitor pass.") from e
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('''INSERT INTO VisitorPasses
            (visitor_name, visitor_id_type, visitor_id_number, host_student, host_room, host_block,
             purpose, visit_date, entry_time, exit_time, status, date_created)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, '', '', 'Registered', ?)''',
            (visitor_name, visitor_id_type, visitor_id_number, host_student, host_room, host_block,
             purpose, visit_date, now))
        pid = cur.lastrowid
        conn.commit()
    return pid


def get_visitor_pass_by_id(pass_id):
    """Fetch a visitor pass by its ID."""
    if _sb_ok():
        try:
            resp = supabase.table("VisitorPasses").select("*").eq("pass_id", pass_id).execute()
            return resp.data[0] if resp.data else None
        except Exception as e:
            logger.error("get_visitor_pass_by_id (Supabase) failed: %s", e)
            return None
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM VisitorPasses WHERE pass_id = ?", (pass_id,))
        row = cur.fetchone()
        return dict(row) if row else None


def get_visitor_passes_by_name(visitor_name):
    """Look up visitor passes by (partial) visitor name — for the gate verifier."""
    if _sb_ok():
        try:
            s = _sanitize_search(visitor_name)
            resp = supabase.table("VisitorPasses").select("*").ilike("visitor_name", f"%{s}%").order("visit_date", desc=True).execute()
            return resp.data or []
        except Exception as e:
            logger.error("get_visitor_passes_by_name (Supabase) failed: %s", e)
            return []
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM VisitorPasses WHERE visitor_name LIKE ? ESCAPE '\\' ORDER BY visit_date DESC",
                    (f"%{escape_like(visitor_name.strip())}%",))
        return [dict(r) for r in cur.fetchall()]


def get_all_visitor_passes(status_filter=None, block_filter=None, search_query=None):
    """Fetch all visitor passes with optional filters."""
    if _sb_ok():
        try:
            q = supabase.table("VisitorPasses").select("*")
            if status_filter and status_filter not in ("All", "All Statuses"):
                q = q.eq("status", status_filter)
            if block_filter and block_filter not in ("All", "All Blocks"):
                q = q.eq("host_block", block_filter)
            s = _sanitize_search(search_query)
            if s:
                q = q.or_(f"visitor_name.ilike.%{s}%,host_student.ilike.%{s}%,host_room.ilike.%{s}%,purpose.ilike.%{s}%")
            resp = q.order("date_created", desc=True).execute()
            return resp.data or []
        except Exception as e:
            logger.error("get_all_visitor_passes (Supabase) failed: %s", e)
            return []
    with get_db() as conn:
        cur = conn.cursor()
        query = "SELECT * FROM VisitorPasses WHERE 1=1"
        params = []
        if status_filter and status_filter not in ("All", "All Statuses"):
            query += " AND status = ?"
            params.append(status_filter)
        if block_filter and block_filter not in ("All", "All Blocks"):
            query += " AND host_block = ?"
            params.append(block_filter)
        if search_query and search_query.strip():
            sq = f"%{escape_like(search_query.strip())}%"
            query += (" AND (visitor_name LIKE ? ESCAPE '\\' OR host_student LIKE ? ESCAPE '\\'"
                      " OR host_room LIKE ? ESCAPE '\\' OR purpose LIKE ? ESCAPE '\\')")
            params.extend([sq, sq, sq, sq])
        query += " ORDER BY date_created DESC"
        cur.execute(query, params)
        return [dict(r) for r in cur.fetchall()]


def update_visitor_status(pass_id, status):
    """Update a visitor pass status; stamps entry/exit time on check-in/out."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updates = {"status": status}
    if status == "Checked In":
        updates["entry_time"] = now
    elif status == "Checked Out":
        updates["exit_time"] = now
    if _sb_ok():
        try:
            supabase.table("VisitorPasses").update(updates).eq("pass_id", pass_id).execute()
            return
        except Exception as e:
            logger.error("update_visitor_status (Supabase) failed: %s", e)
            raise DatabaseError("Could not update the visitor pass.") from e
    with get_db() as conn:
        sets = ", ".join(f"{k} = ?" for k in updates)
        conn.execute(f"UPDATE VisitorPasses SET {sets} WHERE pass_id = ?", (*updates.values(), pass_id))
        conn.commit()


# ==========================================
# ✉️ EMAIL NOTIFICATIONS (B11) — SMTP, best-effort no-op if unconfigured
# ==========================================
def send_notification_email(to_email, subject, body):
    """Send a plain-text email via SMTP using env/secrets. Returns True if sent.
    Silent no-op (returns False) when SMTP is not configured or `to_email` is blank."""
    to_email = (to_email or "").strip()
    if not to_email:
        return False
    host = _get_secret("SMTP_HOST")
    user = _get_secret("SMTP_USER")
    password = _get_secret("SMTP_PASSWORD")
    if not (host and user and password):
        return False  # not configured — silently skip
    port = int(_get_secret("SMTP_PORT", "587") or "587")
    sender = _get_secret("SMTP_FROM", user)
    try:
        import smtplib
        from email.mime.text import MIMEText
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = to_email
        with smtplib.SMTP(host, port, timeout=10) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(sender, [to_email], msg.as_string())
        return True
    except Exception as e:
        logger.error("send_notification_email failed: %s", e)
        return False
