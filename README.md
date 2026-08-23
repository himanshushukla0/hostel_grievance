# 🏢 Campus Hostel Residence Operations & Care Suite

A responsive Streamlit web app for students and hostel wardens to log, track, and manage
hostel maintenance grievances, outstation leave / gate passes, and announcements — from any
device (phone, tablet, or PC).

> **Desktop app note:** the Tkinter desktop version was moved to its own repository so this
> repo stays a single, focused Streamlit codebase. The two no longer drift apart.

---

## 🌟 Features

**🎓 Student portal**
- **Submit grievances** — block, room, category, priority, description, optional photo.
- **Track status** — by Ticket ID, or by Room + Name if the ID is lost.
- **Rate resolutions** — leave a 1–5 star rating and feedback once a ticket is resolved.
- **Leave & digital gate pass** — apply for outstation leave and, once approved, get an
  ID-style gate pass card with a **scannable QR code** (generated offline, no dependencies).
- **Lost & Found desk** — browse and report lost/found items with photo and contact.
- **Notices** — read warden announcements, filtered by block.

**🛡️ Warden / admin desk**
- **Operations & SLA analytics** — resolution rate, average rating, pending/emergency KPIs,
  category/block/priority charts, and an **SLA aging monitor** for tickets overdue >24h / >48h.
- **Cluster outage alerts** — a banner warns when ≥2 unresolved complaints of the same
  category hit one block within 48h (e.g. *"3× Plumbing in BH-1"*).
- Filter, search, and paginate grievances and leave applications; see student ratings.
- Assign staff, update status, add resolution notes, issue gate passes.
- **Lost & Found inventory** — verify claims, mark items returned, remove entries.
- **Gate security verifier** — a sidebar tool for gate officers to validate any pass code.
- Post, expire, and delete announcements.
- Export filtered datasets to CSV.

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
```

On **Streamlit Community Cloud**, paste the same lines into *App → Settings → Secrets*.

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
  rating integer default 0, feedback text default ''
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
  gate_pass_code text default '', date_submitted text, last_updated text default ''
);

create table if not exists "LostAndFound" (
  item_id     bigint generated always as identity primary key,
  title text, item_type text default 'Lost', category text default 'Other',
  location text default '', description text default '', photo_path text default '',
  contact_info text default '', status text default 'Open', date_posted text
);
```

> **Upgrading an existing Supabase project?** Add the two new grievance columns:
> `alter table "Grievances" add column if not exists rating integer default 0;`
> `alter table "Grievances" add column if not exists feedback text default '';`
> then create the `LostAndFound` table above. (SQLite runs these migrations automatically.)

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
- Student lookups have no login, so the **Room + Name** search deliberately masks phone numbers
  and withholds the gate-pass code (retrieve the pass via the exact **Leave Ticket ID** instead).

---

## 📁 Repository structure

```text
hostel_grievance/
├── app.py                        # Streamlit web app (entry point)
├── database.py                   # Backend layer: Supabase (primary) or SQLite (fallback)
├── qr_gen.py                     # Dependency-free offline QR code generator
├── requirements.txt              # Python dependencies
├── test_app.py                   # Isolated DB tests
├── verify_all.py                 # Broader verification script
├── .streamlit/
│   ├── config.toml               # Theme / server config
│   └── secrets.toml.example      # Copy to secrets.toml and fill in
└── README.md
```

---

## 📄 License
Open-source and free to modify for educational and hostel administration purposes.
