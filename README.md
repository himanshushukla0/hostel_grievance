# 🏢 Campus Hostel Residence Operations & Care Suite

A responsive Streamlit web app for students and hostel wardens to log, track, and manage
hostel maintenance grievances, outstation leave / gate passes, and announcements — from any
device (phone, tablet, or PC).

> **Desktop app note:** the Tkinter desktop version was moved to its own repository so this
> repo stays a single, focused Streamlit codebase. The two no longer drift apart.

---

## 🌟 Features

**🎓 Student portal**
- **Submit grievances** — block, room, category, priority, description, optional photo,
  optional email for updates; a duplicate-ticket nudge if you already have one open.
- **Track status** — by Ticket ID, or by Room + Name if the ID is lost.
- **Rate resolutions** — leave a 1–5 star rating and feedback once a ticket is resolved.
- **Leave & digital gate pass** — apply for outstation leave (max 30 days, with a yearly
  quota note) and, once approved, get an ID-style gate pass card with a **scannable QR code**
  (generated offline, no dependencies).
- **Lost & Found desk** — browse and report items with photo/contact; get **match
  suggestions** against opposing lost/found posts.
- **Mess feedback** — rate each meal, read today's menu, see the community average.
- **Visitor pass** — pre-register a guest and track the pass status.
- **Notices** — read warden announcements, filtered by block.

**🛡️ Warden / admin desk**
- **Operations & SLA analytics** — resolution rate, average rating, pending/emergency KPIs;
  category/block/priority charts; **month-over-month trends**; **staff performance**; and an
  **SLA aging monitor** (24–48h warning band vs >48h breached).
- **Priority auto-escalation** — stale open tickets bump Normal→Urgent (>24h) and
  Urgent→Emergency (>48h) on dashboard load, each logged.
- **Cluster outage alerts** — fires only when the same issue hits **≥2 distinct rooms** in a
  block within 48h (repeat tickets from one room don't false-trigger).
- **Return check-in** — the gate verifier marks students returned; the roster flags overdue returns.
- **Lost & Found inventory**, **Mess feedback + menu manager**, **Visitor log**, and a full
  **Audit trail** (filter/search/export) of every admin action.
- **Gate security verifier** — validate a gate pass code or a visitor by name/ID from the sidebar.
- Assign staff, update status, add notes, issue passes; post/expire/delete notices.
- Export grievances, leave roster (phones masked), visitor log, and audit log to CSV.

**✉️ Email notifications (optional)** — when SMTP is configured, students who leave an email
get notified on grievance status changes and leave decisions. Unconfigured, it's a silent no-op.

### 🎫 Offline QR gate pass

`qr_gen.py` is a dependency-free QR encoder (byte mode, Reed-Solomon ECC, mask optimization)
that renders a scannable QR as inline SVG. It needs no `qrcode`/`pillow` package and no network,
so passes render anywhere — including Streamlit Community Cloud.

---

## 🗄️ Data model — one source of truth

The app uses **one** backend at a time, chosen automatically at startup:

- **Supabase configured** (`SUPABASE_URL` + `SUPABASE_KEY` present) → all reads and writes go
  to Supabase. Postgres generates the row IDs, so there are no ID collisions.
- **Not configured** → a local SQLite file (`hostel_care.db`) is used instead. Handy for local
  development, but note that on Streamlit Community Cloud the disk is **ephemeral**, so use
  Supabase for anything that must persist.

There is no dual-write anymore: the previous "write to SQLite *and* Supabase with the same ID"
scheme caused silent duplicate-key failures whenever the ephemeral SQLite file reset.

---

## 🚀 Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Without any credentials it runs on local SQLite. To use Supabase, add credentials (below).

---

## 🔐 Configuration (credentials & passcode)

Credentials are read from **environment variables** or **Streamlit secrets** — never hardcoded.

Copy the template and fill it in (this file is git-ignored):

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

```toml
SUPABASE_URL = "https://your-project-ref.supabase.co"
SUPABASE_KEY = "your-publishable-anon-key"
SUPABASE_STORAGE_BUCKET = "grievance-photos"
ADMIN_PASSCODE = "a-strong-passcode"

# Optional — email notifications (leave blank to disable)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = "587"
SMTP_USER = "you@gmail.com"
SMTP_PASSWORD = "your-16-char-app-password"
SMTP_FROM = "you@gmail.com"
```

On **Streamlit Community Cloud**, paste the same lines into *App → Settings → Secrets*.

> **Gmail note:** use a **Google App Password** (Google Account → Security → 2-Step
> Verification → App passwords), not your normal password. Any other SMTP server works too —
> just set the five `SMTP_*` values. If they're absent, email is skipped silently.

> ⚠️ **If you previously committed a Supabase key** (older versions of this repo did), rotate it
> in the Supabase dashboard — it is in your git history and should be considered exposed.

---

## ☁️ Supabase setup

**1. Tables** — create three tables whose primary keys auto-generate
(`identity`/`serial`). Minimal SQL:

```sql
create table if not exists "Grievances" (
  grievance_id  bigint generated always as identity primary key,
  student_name  text, room_number text, category text, description text,
  date_submitted text, status text default 'Pending', admin_remarks text default '',
  last_updated  text default '', block_name text default 'BH-1', priority text default 'Normal',
  assigned_staff text default '', suggestion text default '', photo_path text default '',
  rating integer default 0, feedback text default '', student_email text default ''
);

create table if not exists "Notices" (
  notice_id   bigint generated always as identity primary key,
  title text, content text, category text, target_block text default 'All Blocks',
  date_posted text, posted_by text default 'Hostel Warden Office', expires_at text default ''
);

create table if not exists "LeaveApplications" (
  leave_id    bigint generated always as identity primary key,
  student_name text, block_name text default 'BH-1', room_number text,
  phone_number text, parent_phone text, leave_reason text, destination text,
  from_date text, to_date text, granting_teacher text,
  status text default 'Pending Warden Approval', warden_remarks text default '',
  gate_pass_code text default '', date_submitted text, last_updated text default '',
  returned_at text default '', student_email text default ''
);

create table if not exists "LostAndFound" (
  item_id     bigint generated always as identity primary key,
  title text, item_type text default 'Lost', category text default 'Other',
  location text default '', description text default '', photo_path text default '',
  contact_info text default '', status text default 'Open', date_posted text
);

create table if not exists "AuditLog" (
  log_id     bigint generated always as identity primary key,
  action_type text, entity_type text default '', entity_id text default '',
  description text default '', actor text default 'Warden', timestamp text
);

create table if not exists "MessFeedback" (
  feedback_id bigint generated always as identity primary key,
  meal_type text, rating integer default 0, comment text default '',
  room_number text default '', date_posted text
);

create table if not exists "MessMenu" (
  menu_id    bigint generated always as identity primary key,
  menu_date text, breakfast text default '', lunch text default '',
  dinner text default '', updated_at text
);

create table if not exists "VisitorPasses" (
  pass_id    bigint generated always as identity primary key,
  visitor_name text, visitor_id_type text default '', visitor_id_number text default '',
  host_student text, host_room text default '', host_block text default 'BH-1',
  purpose text default '', visit_date text, entry_time text default '',
  exit_time text default '', status text default 'Registered', date_created text
);
```

> **Upgrading an existing Supabase project?** Add the new columns and tables:
> ```sql
> alter table "Grievances" add column if not exists rating integer default 0;
> alter table "Grievances" add column if not exists feedback text default '';
> alter table "Grievances" add column if not exists student_email text default '';
> alter table "LeaveApplications" add column if not exists returned_at text default '';
> alter table "LeaveApplications" add column if not exists student_email text default '';
> ```
> then create the `LostAndFound`, `AuditLog`, `MessFeedback`, `MessMenu`, and `VisitorPasses`
> tables above. (SQLite runs all of these migrations automatically.)

**2. Row Level Security** — decide your policy deliberately. With the publishable/anon key and
**RLS disabled**, anyone with the key can read/write every row. Enable RLS and add policies that
match how you deploy.

**3. Storage** — create a **public** bucket named `grievance-photos` (or set
`SUPABASE_STORAGE_BUCKET`). Uploaded photos are stored there and referenced by public URL, so
they persist across restarts and devices.

---

## 🧪 Tests

```bash
python test_app.py     # focused DB operations
python verify_all.py   # broader system verification
```

Both run against an **isolated temporary SQLite file** and never touch your real or cloud data.

---

## 🔒 Security notes (read before real deployment)

- **Warden login accepts several built-in demo passcodes** (in addition to `ADMIN_PASSCODE`).
  This is intentionally left in for demos. **Before any real deployment, remove the extra
  passcodes** in `app.py` so only your configured `ADMIN_PASSCODE` works — otherwise the warden
  desk is effectively open.
- The passcode is a single shared secret with no per-user accounts or rate limiting. Fine for a
  class project; add proper auth for production.
- Student lookups have no login, so student-facing views **always mask phone numbers**, and the
  **Room + Name** search withholds the gate-pass code (retrieve the pass via the exact **Leave
  Ticket ID** instead). CSV exports of the leave roster are masked too.
- All database-sourced text rendered as HTML is **HTML-escaped** (XSS-safe), and photo uploads
  are validated by **magic bytes** (a renamed non-image is rejected), not just file extension.

---

## 📁 Repository structure

```text
hostel_grievance/
├── app.py                        # Streamlit web app (entry point)
├── database.py                   # Backend layer: Supabase (primary) or SQLite (fallback)
├── qr_gen.py                     # Dependency-free offline QR code generator
├── test_app.py                   # DB tests (isolated temp DB)
├── verify_all.py                 # Broader verification (isolated temp DB)
├── requirements.txt              # Python dependencies
├── .streamlit/
│   ├── config.toml               # Theme / server config
│   └── secrets.toml.example      # Copy to secrets.toml and fill in
└── README.md
```

---

## 📄 License
Open-source and free to modify for educational and hostel administration purposes.
