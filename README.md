# 🏢 Campus Hostel Residence Operations & Care Suite

A desktop application designed for students and hostel wardens to log, track, and manage hostel maintenance grievances and announcements efficiently.

---

## 🌟 Key Features

### 🎓 Student Resident Portal
- **Submit Grievances**: File maintenance or repair requests with details such as Block Name, Room Number, Category (Plumbing, Electrical, Furniture, Internet, etc.), and Priority level.
- **Track Status**: Look up submitted requests by Room Number or Grievance ID to see real-time updates and admin remarks.
- **Warden Notices**: View official hostel announcements and broadcast notices directly on the portal.

### 🛡️ Warden & Admin Operations Desk
- **Grievance Dashboard**: Filter, search, and manage pending or resolved grievances by Block, Category, or Status.
- **Action & Dispatch**: Assign staff, update status (`Pending`, `In Progress`, `Resolved`, `Rejected`), and add resolution notes.
- **Announcement Ticker**: Post, update, or remove official warden notices that display on the landing page ticker.

---

## 📁 Repository Structure

```text
hostel_grievance/
├── main.py            # Application entry point & theme setup
├── student_view.py     # Student portal interface & workflows
├── admin_view.py       # Warden/Admin dashboard & management
├── database.py         # SQLite database models, connections, and migrations
├── verify_all.py       # Verification script for DB and UI components
├── requirements.txt    # Dependency documentation
├── .gitignore          # Git exclusion rules
└── README.md           # Project documentation
```

---

## 🚀 How to Run the Source Code

### Prerequisites
- **Python 3.8+** installed on your system.
- *Tkinter* (included by default with Python on Windows and macOS. On Linux/Ubuntu, install via `sudo apt install python3-tk`).

### Step-by-Step Instructions

1. **Clone or Download the Repository**:
   ```bash
   git clone <YOUR-GITHUB-REPO-URL>
   cd hostel_grievance
   ```

2. **Run the Application**:
   ```bash
   python main.py
   ```
   *(The database `hostel_care.db` will be automatically initialized on first run).*

3. **Admin Passcode**:
   - The default passcode for the Warden / Admin portal is: `admin123` *(configured in `main.py`)*.

---

## 🛠️ How to Contribute & Make Changes

We welcome contributions! Feel free to modify the codebase:
- **UI Customizations**: Modify `configure_styles()` in [`main.py`](main.py) or component layouts in [`student_view.py`](student_view.py) and [`admin_view.py`](admin_view.py).
- **Database Schema**: Add new fields or tables inside [`database.py`](database.py).
- **Submitting Changes**: Create a new branch, commit your improvements, and open a Pull Request (PR).

---

## 📄 License
This project is open-source and free to modify for educational and hostel administration purposes.
