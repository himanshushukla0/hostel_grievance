import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import database
from student_view import StudentView
from admin_view import AdminView

ADMIN_PASSCODE = os.environ.get("ADMIN_PASSCODE", "1234")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Hostel Care & Warden Operations Portal")
        self.root.geometry("880x720")
        self.root.minsize(840, 680)
        
        # Configure global custom TTK styles
        self.configure_styles()
        
        # Main container
        self.container = ttk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        self.show_landing_page()
        
    def configure_styles(self):
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
            
        # Custom styling colors
        style.configure(".", font=("Segoe UI", 10))
        style.configure("TFrame", background="#f8fafc")
        style.configure("Header.TFrame", background="#1e293b")
        style.configure("HeaderTitle.TLabel", background="#1e293b", foreground="#ffffff", font=("Segoe UI", 16, "bold"))
        style.configure("HeaderSubtitle.TLabel", background="#1e293b", foreground="#94a3b8", font=("Segoe UI", 9))
        
        # Notice ticker bar
        style.configure("Notice.TFrame", background="#fef3c7")
        style.configure("Notice.TLabel", background="#fef3c7", foreground="#92400e", font=("Segoe UI", 9, "bold"))
        
        # Portal cards
        style.configure("Card.TFrame", background="#ffffff", relief="solid", borderwidth=1)
        style.configure("CardTitle.TLabel", background="#ffffff", foreground="#0f172a", font=("Segoe UI", 13, "bold"))
        style.configure("CardDesc.TLabel", background="#ffffff", foreground="#475569", font=("Segoe UI", 9))
        
        # Primary Action Buttons
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=6)

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_landing_page(self):
        self.clear_container()
        
        # 1. Top Hostel Branding Header
        header_frame = ttk.Frame(self.container, style="Header.TFrame", padding="15")
        header_frame.pack(fill=tk.X)
        
        ttk.Label(header_frame, text="🏢 Campus Hostel Residence Operations & Care Suite", style="HeaderTitle.TLabel").pack(anchor="w")
        ttk.Label(header_frame, text="Digital Maintenance Dispatch  •  Warden Support  •  Resident Care Desk", style="HeaderSubtitle.TLabel").pack(anchor="w", pady=(2, 0))
        
        # 2. Dynamic Warden Notice Board Ticker
        notice_frame = ttk.Frame(self.container, style="Notice.TFrame", padding="8")
        notice_frame.pack(fill=tk.X)
        
        latest_notices = database.get_all_notices()
        if latest_notices:
            top_n = latest_notices[0]
            ticker_text = f"📢 WARDEN ANNOUNCEMENT: [{top_n['category']}] {top_n['title']} (Target: {top_n['target_block']}) • Emergency Desk: Ext 104"
        else:
            ticker_text = "📢 WARDEN ANNOUNCEMENT: Block Maintenance Active • Warden Office: Ext 101 • Medical Room: Ext 108"
            
        ttk.Label(
            notice_frame, 
            text=ticker_text, 
            style="Notice.TLabel"
        ).pack(anchor="center")

        
        # 3. Main Portal Selection Container
        content_frame = ttk.Frame(self.container, padding="30")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(content_frame, text="Select Portal to Access System", font=("Segoe UI", 14, "bold"), foreground="#1e293b").pack(pady=(0, 20))
        
        cards_frame = ttk.Frame(content_frame)
        cards_frame.pack(expand=True)
        
        # Card 1: Student Portal
        student_card = ttk.Frame(cards_frame, style="Card.TFrame", padding="20")
        student_card.pack(side=tk.LEFT, padx=15, ipady=10)
        
        ttk.Label(student_card, text="🎓 Student Resident Portal", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 5))
        ttk.Label(student_card, text="Submit room repair requests, track maintenance\nstatus by room number or ID, and get warden updates.", style="CardDesc.TLabel").pack(anchor="w", pady=(0, 15))
        
        student_btn = ttk.Button(student_card, text="Enter Student Portal ➔", command=self.show_student_view, style="Primary.TButton", width=24)
        student_btn.pack(anchor="w")
        
        # Card 2: Warden & Admin Portal
        admin_card = ttk.Frame(cards_frame, style="Card.TFrame", padding="20")
        admin_card.pack(side=tk.LEFT, padx=15, ipady=10)
        
        ttk.Label(admin_card, text="🛡️ Warden & Admin Control Center", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 5))
        ttk.Label(admin_card, text="Manage block grievances, assign maintenance staff,\nfilter urgent repairs, and export daily shift logs.", style="CardDesc.TLabel").pack(anchor="w", pady=(0, 15))
        
        admin_btn = ttk.Button(admin_card, text="Access Warden Desk ➔", command=self.prompt_admin_login, style="Primary.TButton", width=24)
        admin_btn.pack(anchor="w")
        
        # 4. Campus Emergency & Support Desk Footer
        footer_frame = ttk.Frame(self.container, padding="10")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        contact_info = "📞 Emergency Contacts:  Warden Desk: Ext 101  |  Medical Room: Ext 108  |  Electrical Duty: Ext 104  |  Plumbing Duty: Ext 105"
        ttk.Label(footer_frame, text=contact_info, font=("Segoe UI", 9), foreground="#64748b").pack(anchor="center")

    def prompt_admin_login(self):
        passcode = simpledialog.askstring("Warden Authentication", "Enter Warden / Admin Passcode (Default: admin123):", show="*")
        if passcode is None:
            return  # User canceled
        if passcode.strip() == ADMIN_PASSCODE:
            self.show_admin_view()
        else:
            messagebox.showerror("Access Denied", "Incorrect Warden Passcode.")

    def show_student_view(self):
        self.clear_container()
        
        # Add a back button & navigation header
        top_frame = ttk.Frame(self.container, padding="8", style="Header.TFrame")
        top_frame.pack(fill=tk.X)
        
        ttk.Button(top_frame, text="← Back to Main Menu", command=self.show_landing_page).pack(side=tk.LEFT, padx=5)
        ttk.Label(top_frame, text="🎓 Student Resident Maintenance Portal", style="HeaderTitle.TLabel", font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT, padx=15)
        
        StudentView(self.container)

    def show_admin_view(self):
        self.clear_container()
        
        # Add a back button & navigation header
        top_frame = ttk.Frame(self.container, padding="8", style="Header.TFrame")
        top_frame.pack(fill=tk.X)
        
        ttk.Button(top_frame, text="← Back to Main Menu", command=self.show_landing_page).pack(side=tk.LEFT, padx=5)
        ttk.Label(top_frame, text="🛡️ Warden & Hostel Administration Control Center", style="HeaderTitle.TLabel", font=("Segoe UI", 12, "bold")).pack(side=tk.LEFT, padx=15)
        
        AdminView(self.container)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
