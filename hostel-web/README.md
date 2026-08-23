# Hostel Care — Campus Residence Operations

A self-contained web portal for hostel maintenance complaints, outstation leave
and gate passes, and warden announcements.

No Python. No Streamlit. No server to keep awake. Three static files talk to
Supabase directly from the browser, so it loads instantly and hosts free
anywhere.

```
index.html          markup
styles.css          design system (dark + light, one token set)
app.js              data layer + all UI logic
supabase-setup.sql  one required migration, plus optional hardening
```

---

## 1. Prepare the database (do this first)

Open Supabase → **SQL Editor** → **New query**, paste **`supabase-setup.sql`**,
and run **Step 1**.

This is not optional. The old Streamlit app generated IDs in SQLite and pushed
them into Postgres explicitly, so Postgres never advanced its own counter. The
new site lets Postgres assign IDs — without the fix, the first complaint someone
files collides with an existing row and fails. Step 2 in the file verifies it.

Your existing tables and data are reused as-is. Nothing is dropped.

---

## 2. Run it locally

Because it uses ES modules, open it through a local server, not by
double-clicking the file:

```bash
cd hostel-care
python3 -m http.server 5173
# then open http://localhost:5173
```

Warden desk passcode (default): **`hostel2026`** — change it in `app.js`.

---

## 3. Put it online

Pick whichever you prefer. All are free and all give HTTPS.

**Vercel** (fastest)
```bash
npm i -g vercel
vercel
```
Accept the defaults. No build step, no framework — it is a static site.

**Netlify** — drag the folder onto <https://app.netlify.com/drop>. Done.

**GitHub Pages**
```bash
git init && git add . && git commit -m "Hostel Care web portal"
git branch -M main
git remote add origin https://github.com/<you>/hostel-care.git
git push -u origin main
```
Then Settings → Pages → Source: `main` / root.

### Custom domain
All three let you attach one under project settings. A `.com` runs about
₹800–1000/year; students can usually get a free `.me` through the
[GitHub Student Developer Pack](https://education.github.com/pack).

---

## 4. Configure

Everything adjustable lives in the `CONFIG` block at the top of `app.js`:

```js
const CONFIG = {
  SUPABASE_URL:    'https://wtfartnzuwdixoniufdz.supabase.co',
  SUPABASE_KEY:    'sb_publishable_...',   // publishable key — public by design
  WARDEN_MODE:     'passcode',             // or 'supabase-auth'
  WARDEN_PASSCODE: 'hostel2026',
};
```

The publishable key is *meant* to be visible in browser code — that is what it
is for. It is not a leak.

---

## 5. Security — please read

As shipped, the warden passcode is checked in JavaScript and RLS is off on your
tables. That means a determined visitor can open devtools and modify or delete
records. This was already true of the Streamlit version; it is just more visible
now.

Fine for a demo or an evaluation. **Not** fine for a portal real students rely
on. To fix it properly:

1. Supabase → Authentication → Users → **Add user** (warden's email + password)
2. In `app.js`: `WARDEN_MODE: 'supabase-auth'`
3. Run **Step 3** in `supabase-setup.sql`

Then anyone can file complaints and read notices, but only a signed-in warden can
change status, issue gate passes, publish notices, or delete anything — enforced
by the database itself, not by the browser.

---

## Features

**Student**
- File a maintenance request (block, room, category, priority, description, suggested fix)
- Emergency priority requires a fuller description before it will submit
- Track by ticket ID, or by room + name together if the ID is lost (both required, for privacy)
- Apply for outstation leave; track approval and collect the gate pass code
- Read warden announcements, filtered by block

**Warden**
- Dispatch console: filter by block/status, live search, click any row to action it
- Update status, assign staff, leave remarks, delete tickets
- Leave roster: approve/reject, issue gate pass codes
- Publish announcements with an expiry timer (auto-removed once elapsed)
- Export either table to CSV

**Both**
- Dark and light themes, remembered between visits
- Responsive down to phone width
- Live counters across the top

---

## Known gaps

- **Photo attachments** are not implemented. The old app wrote files to the
  Streamlit server's disk, which does not exist here. The proper replacement is
  Supabase Storage — create a public bucket, upload with
  `sb.storage.from('photos').upload(...)`, and store the returned URL in the
  existing `photo_path` column.
- **Expired notices** are purged when someone loads the notice board, not on a
  schedule. Good enough in practice; a Supabase scheduled function would make it
  exact.

---

## What happened to the old files

`app.py`, `database.py`, `main.py`, `student_view.py`, `admin_view.py` and
`requirements.txt` are no longer used. Keep them in git history if you want to
show the project's progression — the Tkinter desktop version and the Streamlit
version are both reasonable things to point at in a viva.
