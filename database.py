import sqlite3
import datetime
from contextlib import contextmanager

DB_FILE = 'hostel_care.db'

def get_connection():
    """Establish and return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
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
    """Initialize database and perform safe schema migrations."""
    with get_db() as conn:
        cursor = conn.cursor()
        
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
                suggestion TEXT DEFAULT ''
            )
        ''')
        
        # Safe migrations for existing DB instances
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
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Notices (
                notice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT NOT NULL,
                target_block TEXT DEFAULT 'All Blocks',
                date_posted TEXT NOT NULL,
                posted_by TEXT DEFAULT 'Hostel Warden Office'
            )
        ''')
        
        conn.commit()


def create_grievance(name, room, category, description, block_name="BH-1", priority="Normal", suggestion=""):
    """Insert a new grievance into the database and return its ID."""
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO Grievances (student_name, room_number, category, description, date_submitted, last_updated, block_name, priority, assigned_staff, suggestion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, '', ?)
        ''', (name, room, category, description, now, now, block_name, priority, suggestion))
        
        grievance_id = cursor.lastrowid
        conn.commit()
        return grievance_id

def escape_like(string):
    """Escape special characters for SQL LIKE pattern matching."""
    return string.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')

def get_all_grievances(status_filter=None, block_filter=None, search_query=None):
    """Fetch all grievances with optional status/block filtering and text searching."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        query = "SELECT * FROM Grievances WHERE 1=1"
        params = []
        
        if status_filter and status_filter != "All":
            query += " AND status = ?"
            params.append(status_filter)
            
        if block_filter and block_filter != "All":
            query += " AND block_name = ?"
            params.append(block_filter)
            
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
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Grievances WHERE grievance_id = ?", (grievance_id,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

def update_grievance(grievance_id, status, remarks, assigned_staff=""):
    """Update status, remarks, and assigned staff for a grievance (Admin action)."""
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            UPDATE Grievances 
            SET status = ?, admin_remarks = ?, last_updated = ?, assigned_staff = ? 
            WHERE grievance_id = ?
        ''', (status, remarks, now, assigned_staff, grievance_id))
        conn.commit()

def delete_grievance(grievance_id):
    """Delete a grievance by ID (Admin action)."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Grievances WHERE grievance_id = ?", (grievance_id,))
        conn.commit()

def get_grievance_counts():
    """Return dictionary with summary counts of grievances by status and priority."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status, COUNT(*) as count FROM Grievances GROUP BY status")
        rows = cursor.fetchall()
        
        counts = {'total': 0, 'pending': 0, 'in_progress': 0, 'resolved': 0, 'emergency': 0}
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

def create_notice(title, content, category, target_block="All Blocks", posted_by="Hostel Warden Office"):
    """Insert a new notice/announcement into database."""
    with get_db() as conn:
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO Notices (title, content, category, target_block, date_posted, posted_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, content, category, target_block, now, posted_by))
        notice_id = cursor.lastrowid
        conn.commit()
        return notice_id

def get_all_notices(block_filter=None, category_filter=None):
    """Fetch all published notices with optional block/category filtering."""
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
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Notices WHERE notice_id = ?", (notice_id,))
        conn.commit()

# Initialize the database file when this module is loaded
init_db()
