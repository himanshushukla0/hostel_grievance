# 🏢 Campus Hostel Residence Operations & Care Suite (Web App)

A modern, responsive web application designed for students and hostel wardens to log, track, and manage hostel maintenance grievances and announcements efficiently from any device (smartphones, tablets, PCs).

---

## 🌟 Key Features

### 🎓 Student Resident Web Portal
- **Submit Grievances**: File maintenance or repair requests with details such as Block Name, Room Number, Category (Plumbing, Electrical, Furniture, Internet, etc.), and Priority level.
- **Track Status**: Look up submitted requests by Room Number or Grievance Ticket ID to see real-time status updates and admin remarks.
- **Warden Notices**: View official hostel announcements and broadcast circulars directly on the web portal.

### 🛡️ Warden & Admin Operations Control Center
- **Grievance Dashboard**: Filter, search, and manage pending or resolved grievances by Block, Category, or Status.
- **Action & Dispatch**: Assign staff, update status (`Pending`, `In Progress`, `Resolved`, `Rejected`), and add resolution notes.
- **Announcement Ticker**: Post, update, or remove official warden notices that display on the landing page ticker.
- **Export Shift Reports**: Download filtered grievance datasets directly to CSV.

---

## 🚀 How to Run Locally

### Prerequisites
- **Python 3.8+** installed.
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Run the Web Application
```bash
streamlit run app.py
```
*(The web app will open automatically in your default browser at `http://localhost:8501`)*.

- **Admin Passcode**: The default passcode for the Warden portal is `admin123` *(configurable via `ADMIN_PASSCODE` environment variable)*.

---

## 🌐 How to Deploy Online for FREE (Streamlit Community Cloud)

To make this web portal live for all students and wardens on their mobile phones:

1. Push this repository to **GitHub**:
   ```bash
   git add .
   git commit -m "Add Streamlit web app"
   git push origin main
   ```
2. Go to **[share.streamlit.io](https://share.streamlit.io/)** and sign in with your GitHub account.
3. Click **New App** -> Select your repository `himanshushukla0/hostel_grievance` -> Main file path: `app.py`.
4. Click **Deploy!**
   - You will get a live URL (e.g. `https://hostel-grievance.streamlit.app`) that anyone can open from their mobile phone or laptop browser!

---

## 📁 Repository Structure

```text
hostel_grievance/
├── app.py             # Streamlit Web Application entry point
├── main.py            # Desktop Tkinter app fallback entry point
├── student_view.py     # Student portal Tkinter component
├── admin_view.py       # Warden/Admin Tkinter component
├── database.py         # SQLite database models, connections, and migrations
├── requirements.txt    # Python package dependencies (streamlit, pandas)
├── .gitignore          # Git exclusion rules
└── README.md           # Project documentation
```

---

## 📄 License
This project is open-source and free to modify for educational and hostel administration purposes.
