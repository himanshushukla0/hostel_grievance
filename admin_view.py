import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import csv
import database

class AdminView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(self.parent, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Selected grievance state
        self.selected_grievance_id = None
        
        # Track column sort state
        self.sort_reverse = {}
        
        # Create Notebook (Tabs for Admin)
        self.admin_notebook = ttk.Notebook(self.frame)
        self.admin_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Grievance & Dispatch Management
        self.dispatch_tab = ttk.Frame(self.admin_notebook, padding="10")
        self.admin_notebook.add(self.dispatch_tab, text="🛡️ Grievance Dispatch Console")
        self.setup_dispatch_tab()
        
        # Tab 2: Notice Board Management
        self.notice_tab = ttk.Frame(self.admin_notebook, padding="10")
        self.admin_notebook.add(self.notice_tab, text="📢 Notice Board & Circulars")
        self.setup_notice_tab()
        
        # Tab 3: Student Leave & Gate Pass Roster
        self.leave_admin_tab = ttk.Frame(self.admin_notebook, padding="10")
        self.admin_notebook.add(self.leave_admin_tab, text="🌴 Student Leave & Gate Pass Roster")
        self.setup_leave_admin_tab()

    def setup_dispatch_tab(self):
        # 1. Header & Warden KPI Metrics Bar
        self.header_frame = ttk.Frame(self.dispatch_tab)
        self.header_frame.pack(fill=tk.X, pady=(0, 8))
        
        title_label = ttk.Label(self.header_frame, text="Warden Control & Dispatch Operations", font=("Segoe UI", 12, "bold"), foreground="#1e293b")
        title_label.pack(side=tk.LEFT)
        
        # KPI Stats frame
        self.kpi_frame = ttk.Frame(self.header_frame)
        self.kpi_frame.pack(side=tk.RIGHT)
        
        self.lbl_total = ttk.Label(self.kpi_frame, text="Total: 0", font=("Segoe UI", 9, "bold"), padding=(5, 2), background="#e2e8f0", foreground="#334155")
        self.lbl_total.pack(side=tk.LEFT, padx=2)
        
        self.lbl_emergency = ttk.Label(self.kpi_frame, text="🔴 Emergency: 0", font=("Segoe UI", 9, "bold"), padding=(5, 2), background="#fee2e2", foreground="#991b1b")
        self.lbl_emergency.pack(side=tk.LEFT, padx=2)
        
        self.lbl_pending = ttk.Label(self.kpi_frame, text="Pending: 0", font=("Segoe UI", 9, "bold"), padding=(5, 2), background="#ffedd5", foreground="#9a3412")
        self.lbl_pending.pack(side=tk.LEFT, padx=2)
        
        self.lbl_in_prog = ttk.Label(self.kpi_frame, text="In Progress: 0", font=("Segoe UI", 9, "bold"), padding=(5, 2), background="#fef9c3", foreground="#854d0e")
        self.lbl_in_prog.pack(side=tk.LEFT, padx=2)
        
        self.lbl_resolved = ttk.Label(self.kpi_frame, text="Resolved: 0", font=("Segoe UI", 9, "bold"), padding=(5, 2), background="#dcfce7", foreground="#166534")
        self.lbl_resolved.pack(side=tk.LEFT, padx=2)
        
        # 2. Filter & Search Bar
        self.filter_frame = ttk.Frame(self.dispatch_tab)
        self.filter_frame.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(self.filter_frame, text="Block:").pack(side=tk.LEFT, padx=(0, 3))
        self.filter_block_var = tk.StringVar(value="All")
        self.filter_block_combobox = ttk.Combobox(
            self.filter_frame, 
            textvariable=self.filter_block_var, 
            values=["All", "BH-1", "BH-2", "BH-3", "GH-1", "GH-2", "IH-1"], 
            state="readonly", 
            width=10
        )
        self.filter_block_combobox.pack(side=tk.LEFT, padx=(0, 10))
        self.filter_block_combobox.bind("<<ComboboxSelected>>", lambda e: self.load_data())
        
        ttk.Label(self.filter_frame, text="Status:").pack(side=tk.LEFT, padx=(0, 3))
        self.filter_status_var = tk.StringVar(value="All")
        self.filter_status_combobox = ttk.Combobox(
            self.filter_frame, 
            textvariable=self.filter_status_var, 
            values=["All", "Pending", "In Progress", "Resolved"], 
            state="readonly", 
            width=10
        )
        self.filter_status_combobox.pack(side=tk.LEFT, padx=(0, 10))
        self.filter_status_combobox.bind("<<ComboboxSelected>>", lambda e: self.load_data())
        
        ttk.Label(self.filter_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 3))
        self.search_entry = ttk.Entry(self.filter_frame, width=16)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry.bind("<Return>", lambda e: self.load_data())
        
        ttk.Button(self.filter_frame, text="Search", command=self.load_data).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(self.filter_frame, text="Reset", command=self.reset_filters).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(self.filter_frame, text="📥 Export Shift Report", command=self.export_csv).pack(side=tk.RIGHT)
        
        # 3. Data Grid Frame with Scrollbar
        tree_frame = ttk.Frame(self.dispatch_tab)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "block", "room", "name", "category", "priority", "last_updated", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=7)
        
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        for col, col_name in [
            ("id", "ID"), ("block", "Block"), ("room", "Room"), 
            ("name", "Student Name"), ("category", "Category"), 
            ("priority", "Priority"), ("last_updated", "Last Updated"), ("status", "Status")
        ]:
            self.tree.heading(col, text=col_name, command=lambda c=col: self.sort_column(c))
        
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("block", width=65, anchor="center")
        self.tree.column("room", width=60, anchor="center")
        self.tree.column("name", width=125)
        self.tree.column("category", width=130)
        self.tree.column("priority", width=115, anchor="center")
        self.tree.column("last_updated", width=130, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        
        # Row Color Tags
        self.tree.tag_configure("Pending", background="#fff0f0", foreground="#900c3f")
        self.tree.tag_configure("In Progress", background="#fffdf0", foreground="#8a6d3b")
        self.tree.tag_configure("Resolved", background="#f0fff4", foreground="#155724")
        self.tree.tag_configure("Emergency", background="#fee2e2", foreground="#7f1d1d")
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # 4. Warden Management Panel
        self.update_frame = ttk.LabelFrame(self.dispatch_tab, text="Warden Action & Maintenance Dispatch Panel", padding="10")
        self.update_frame.pack(fill=tk.X, pady=8)
        
        ttk.Label(self.update_frame, text="Selected Complaint:").grid(row=0, column=0, sticky="w", pady=3)
        self.selected_id_var = tk.StringVar(value="None (Click a row above)")
        ttk.Label(self.update_frame, textvariable=self.selected_id_var, font=("Segoe UI", 10, "bold"), foreground="#0f172a").grid(row=0, column=1, sticky="w", pady=3)
        
        ttk.Label(self.update_frame, text="Complaint Description:").grid(row=1, column=0, sticky="nw", pady=3)
        self.selected_desc_var = tk.StringVar(value="-")
        ttk.Label(self.update_frame, textvariable=self.selected_desc_var, wraplength=520, justify="left").grid(row=1, column=1, sticky="w", pady=3)
        
        ttk.Label(self.update_frame, text="Student Suggestion:").grid(row=2, column=0, sticky="nw", pady=3)
        self.selected_suggestion_var = tk.StringVar(value="-")
        ttk.Label(self.update_frame, textvariable=self.selected_suggestion_var, wraplength=520, justify="left", foreground="#047857").grid(row=2, column=1, sticky="w", pady=3)

        ttk.Label(self.update_frame, text="Assign Duty Staff:").grid(row=3, column=0, sticky="w", pady=3)
        self.assigned_staff_entry = ttk.Entry(self.update_frame, width=38)
        self.assigned_staff_entry.grid(row=3, column=1, sticky="w", pady=3)
        
        ttk.Label(self.update_frame, text="Update Status:").grid(row=4, column=0, sticky="w", pady=3)
        
        status_subframe = ttk.Frame(self.update_frame)
        status_subframe.grid(row=4, column=1, sticky="w", pady=3)
        
        self.status_var = tk.StringVar()
        status_options = ["Pending", "In Progress", "Resolved"]
        self.status_dropdown = ttk.Combobox(status_subframe, textvariable=self.status_var, values=status_options, state="readonly", width=14)
        self.status_dropdown.pack(side=tk.LEFT, padx=(0, 10))
        
        # Quick action buttons
        self.in_progress_btn = ttk.Button(status_subframe, text="⚡ Mark In Progress", command=lambda: self.quick_set_status("In Progress"), state=tk.DISABLED)
        self.in_progress_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.resolve_btn = ttk.Button(status_subframe, text="✓ Mark Resolved", command=lambda: self.quick_set_status("Resolved"), state=tk.DISABLED)
        self.resolve_btn.pack(side=tk.LEFT)
        
        ttk.Label(self.update_frame, text="Warden Remarks:").grid(row=5, column=0, sticky="nw", pady=3)
        self.remarks_text = tk.Text(self.update_frame, width=50, height=2)
        self.remarks_text.grid(row=5, column=1, sticky="w", pady=3)
        
        btn_bar = ttk.Frame(self.update_frame)
        btn_bar.grid(row=6, column=1, sticky="e", pady=4)
        
        self.delete_btn = ttk.Button(btn_bar, text="🗑 Delete Grievance", command=self.delete_grievance, state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.update_btn = ttk.Button(btn_bar, text="💾 Save Dispatch & Remarks", command=self.update_grievance, state=tk.DISABLED)
        self.update_btn.pack(side=tk.LEFT)
        
        # Initial load
        self.load_data()

    def setup_notice_tab(self):
        # Publish Notice Panel
        pub_frame = ttk.LabelFrame(self.notice_tab, text="📢 Compose & Publish Verified Warden Announcement", padding="12")
        pub_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(pub_frame, text="Notice Title:").grid(row=0, column=0, sticky="w", pady=4)
        self.notice_title_entry = ttk.Entry(pub_frame, width=45)
        self.notice_title_entry.grid(row=0, column=1, sticky="w", pady=4, padx=8)
        
        ttk.Label(pub_frame, text="Category:").grid(row=1, column=0, sticky="w", pady=4)
        self.notice_cat_var = tk.StringVar(value="General Hostel Notice")
        categories = [
            "General Hostel Notice",
            "Maintenance Warning & Inspection",
            "Mess & Food Schedule",
            "Campus Security Advisory",
            "College Circular"
        ]
        self.notice_cat_dropdown = ttk.Combobox(pub_frame, textvariable=self.notice_cat_var, values=categories, state="readonly", width=42)
        self.notice_cat_dropdown.grid(row=1, column=1, sticky="w", pady=4, padx=8)
        
        ttk.Label(pub_frame, text="Target Block:").grid(row=2, column=0, sticky="w", pady=4)
        self.notice_block_var = tk.StringVar(value="All Blocks")
        blocks = ["All Blocks", "BH-1", "BH-2", "BH-3", "GH-1", "GH-2", "IH-1"]
        self.notice_block_dropdown = ttk.Combobox(pub_frame, textvariable=self.notice_block_var, values=blocks, state="readonly", width=42)
        self.notice_block_dropdown.grid(row=2, column=1, sticky="w", pady=4, padx=8)

        ttk.Label(pub_frame, text="Active Duration / Timer:").grid(row=3, column=0, sticky="w", pady=4)
        self.notice_duration_var = tk.StringVar(value="📌 Permanent (No Expiration)")
        durations = [
            "📌 Permanent (No Expiration)",
            "⏱️ 1 Hour",
            "⏱️ 12 Hours",
            "⏱️ 24 Hours (1 Day)",
            "⏱️ 2 Days (48 Hours)",
            "⏱️ 3 Days (72 Hours)",
            "⏱️ 7 Days (1 Week)"
        ]
        self.notice_duration_dropdown = ttk.Combobox(pub_frame, textvariable=self.notice_duration_var, values=durations, state="readonly", width=42)
        self.notice_duration_dropdown.grid(row=3, column=1, sticky="w", pady=4, padx=8)
        
        ttk.Label(pub_frame, text="Announcement Content:").grid(row=4, column=0, sticky="nw", pady=4)
        self.notice_content_text = tk.Text(pub_frame, width=45, height=3)
        self.notice_content_text.grid(row=4, column=1, sticky="w", pady=4, padx=8)
        
        pub_btn = ttk.Button(pub_frame, text="🚀 Publish Notice to Resident Board", command=self.publish_notice, style="Primary.TButton")
        pub_btn.grid(row=5, column=1, sticky="e", pady=8, padx=8)
        
        # Published Notices Table Frame with Scrollbar
        list_frame = ttk.LabelFrame(self.notice_tab, text="Active Published Notices", padding="8")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        notice_tree_frame = ttk.Frame(list_frame)
        notice_tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        columns = ("id", "date", "expires", "category", "block", "title", "posted_by")
        self.notice_tree = ttk.Treeview(notice_tree_frame, columns=columns, show="headings", height=5)
        
        notice_scroll = ttk.Scrollbar(notice_tree_frame, orient="vertical", command=self.notice_tree.yview)
        self.notice_tree.configure(yscrollcommand=notice_scroll.set)

        self.notice_tree.heading("id", text="ID")
        self.notice_tree.heading("date", text="Date Posted")
        self.notice_tree.heading("expires", text="Active Until")
        self.notice_tree.heading("category", text="Category")
        self.notice_tree.heading("block", text="Target Block")
        self.notice_tree.heading("title", text="Title")
        self.notice_tree.heading("posted_by", text="Verified By")
        
        self.notice_tree.column("id", width=40, anchor="center")
        self.notice_tree.column("date", width=120, anchor="center")
        self.notice_tree.column("expires", width=120, anchor="center")
        self.notice_tree.column("category", width=140)
        self.notice_tree.column("block", width=80, anchor="center")
        self.notice_tree.column("title", width=180)
        self.notice_tree.column("posted_by", width=120)
        
        self.notice_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        notice_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action Bar
        act_bar = ttk.Frame(list_frame)
        act_bar.pack(fill=tk.X)
        
        ttk.Button(act_bar, text="🗑 Delete Selected Notice", command=self.delete_notice).pack(side=tk.RIGHT)
        ttk.Button(act_bar, text="🔄 Refresh Notice List", command=self.load_notices).pack(side=tk.LEFT)
        
        self.load_notices()

    def publish_notice(self):
        title = self.notice_title_entry.get().strip()
        category = self.notice_cat_var.get()
        block = self.notice_block_var.get()
        content = self.notice_content_text.get("1.0", tk.END).strip()
        
        if not title or not content:
            messagebox.showerror("Validation Error", "Please provide both a Title and Announcement Content.")
            return
            
        duration_map = {
            "📌 Permanent (No Expiration)": 0,
            "⏱️ 1 Hour": 1,
            "⏱️ 12 Hours": 12,
            "⏱️ 24 Hours (1 Day)": 24,
            "⏱️ 2 Days (48 Hours)": 48,
            "⏱️ 3 Days (72 Hours)": 72,
            "⏱️ 7 Days (1 Week)": 168
        }
        exp_h = duration_map.get(self.notice_duration_var.get(), 0)

        try:
            notice_id = database.create_notice(
                title=title,
                content=content,
                category=category,
                target_block=block,
                posted_by="Warden Office ✔",
                expiry_hours=exp_h
            )
            messagebox.showinfo("Published", f"Notice #{notice_id} published successfully to {block}!")
            
            # Clear form
            self.notice_title_entry.delete(0, tk.END)
            self.notice_content_text.delete("1.0", tk.END)
            self.load_notices()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to publish notice: {e}")

    def load_notices(self):
        for item in self.notice_tree.get_children():
            self.notice_tree.delete(item)
            
        notices = database.get_all_notices()
        for n in notices:
            exp_display = n['expires_at'] if n.get('expires_at') else "Permanent"
            self.notice_tree.insert("", tk.END, values=(
                n['notice_id'],
                n['date_posted'],
                exp_display,
                n['category'],
                n['target_block'],
                n['title'],
                n['posted_by']
            ))

    def delete_notice(self):
        selected = self.notice_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a notice from the table to delete.")
            return

    def setup_leave_admin_tab(self):
        # Header & Filter Bar
        hdr = ttk.Frame(self.leave_admin_tab)
        hdr.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(hdr, text="Student Outstation Leave & Gate Pass Roster", font=("Segoe UI", 12, "bold"), foreground="#1e293b").pack(side=tk.LEFT)
        ttk.Button(hdr, text="🔄 Refresh Leave Roster", command=self.load_leave_data).pack(side=tk.RIGHT)

        # Leave Treeview Table Frame
        tree_frame = ttk.Frame(self.leave_admin_tab)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "block", "room", "name", "teacher", "from", "to", "dest", "status", "pass")
        self.leave_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=6)
        
        l_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.leave_tree.yview)
        self.leave_tree.configure(yscrollcommand=l_scroll.set)

        for col, label in [
            ("id", "ID"), ("block", "Block"), ("room", "Room"), ("name", "Student Name"), 
            ("teacher", "Granting Teacher"), ("from", "From"), ("to", "To"), 
            ("dest", "Destination"), ("status", "Status"), ("pass", "Gate Pass Code")
        ]:
            self.leave_tree.heading(col, text=label)
            
        self.leave_tree.column("id", width=35, anchor="center")
        self.leave_tree.column("block", width=60, anchor="center")
        self.leave_tree.column("room", width=55, anchor="center")
        self.leave_tree.column("name", width=120)
        self.leave_tree.column("teacher", width=130)
        self.leave_tree.column("from", width=85, anchor="center")
        self.leave_tree.column("to", width=85, anchor="center")
        self.leave_tree.column("dest", width=110)
        self.leave_tree.column("status", width=130, anchor="center")
        self.leave_tree.column("pass", width=95, anchor="center")

        self.leave_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        l_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.leave_tree.bind("<<TreeviewSelect>>", self.on_leave_select)

        # Action Panel
        self.l_action_frame = ttk.LabelFrame(self.leave_admin_tab, text="Warden Gate Pass Authorization Panel", padding="10")
        self.l_action_frame.pack(fill=tk.X, pady=8)

        ttk.Label(self.l_action_frame, text="Selected Application:").grid(row=0, column=0, sticky="w", pady=3)
        self.selected_leave_var = tk.StringVar(value="None (Click a row above)")
        ttk.Label(self.l_action_frame, textvariable=self.selected_leave_var, font=("Segoe UI", 10, "bold")).grid(row=0, column=1, sticky="w", pady=3)

        ttk.Label(self.l_action_frame, text="Granting Teacher Sign-off:").grid(row=1, column=0, sticky="w", pady=3)
        self.selected_teacher_var = tk.StringVar(value="-")
        ttk.Label(self.l_action_frame, textvariable=self.selected_teacher_var, font=("Segoe UI", 9, "bold"), foreground="#0369a1").grid(row=1, column=1, sticky="w", pady=3)

        ttk.Label(self.l_action_frame, text="Approval & Gate Pass:").grid(row=2, column=0, sticky="w", pady=3)
        l_act_sub = ttk.Frame(self.l_action_frame)
        l_act_sub.grid(row=2, column=1, sticky="w", pady=3)

        self.l_status_var = tk.StringVar(value="Pending Warden Approval")
        ttk.Combobox(l_act_sub, textvariable=self.l_status_var, values=["Pending Warden Approval", "Approved / Gate Pass Issued", "Rejected"], state="readonly", width=22).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(l_act_sub, text="Pass Code:").pack(side=tk.LEFT, padx=(5, 2))
        self.l_pass_entry = ttk.Entry(l_act_sub, width=15)
        self.l_pass_entry.pack(side=tk.LEFT)

        ttk.Button(self.l_action_frame, text="💾 Save Leave Authorization", command=self.update_leave_authorization).grid(row=3, column=1, sticky="e", pady=5)

        self.selected_leave_id = None
        self.load_leave_data()

    def load_leave_data(self):
        for item in self.leave_tree.get_children():
            self.leave_tree.delete(item)
        leaves = database.get_all_leave_applications()
        for rec in leaves:
            self.leave_tree.insert("", tk.END, values=(
                rec['leave_id'],
                rec.get('block_name', 'BH-1'),
                rec['room_number'],
                rec['student_name'],
                rec['granting_teacher'],
                rec['from_date'],
                rec['to_date'],
                rec['destination'],
                rec['status'],
                rec.get('gate_pass_code', '')
            ))

    def on_leave_select(self, event):
        selected = self.leave_tree.selection()
        if not selected:
            return
        item = self.leave_tree.item(selected[0])
        values = item['values']
        if values:
            try:
                lid = int(values[0])
            except ValueError:
                return
            rec = database.get_leave_application_by_id(lid)
            if rec:
                self.selected_leave_id = lid
                self.selected_leave_var.set(f"#L-{lid}  |  {rec['student_name']} ({rec['block_name']} Room {rec['room_number']})")
                self.selected_teacher_var.set(f"Faculty Approval: {rec['granting_teacher']} | Destination: {rec['destination']}")
                self.l_status_var.set(rec['status'])
                self.l_pass_entry.delete(0, tk.END)
                gp = rec.get('gate_pass_code') or f"GP-2026-X{lid:03d}"
                self.l_pass_entry.insert(0, gp)

    def update_leave_authorization(self):
        if not self.selected_leave_id:
            messagebox.showerror("Error", "No leave application selected.")
            return
        status = self.l_status_var.get()
        pass_code = self.l_pass_entry.get().strip() if "Approved" in status else ""
        try:
            database.update_leave_status(self.selected_leave_id, status, warden_remarks="Warden Authorized", gate_pass_code=pass_code)
            messagebox.showinfo("Updated", f"Leave Application #L-{self.selected_leave_id} status updated to '{status}'.")
            self.load_leave_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update leave application: {e}")

    def delete_notice(self):
        selected = self.notice_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a notice from the table to delete.")
            return
            
        item = self.notice_tree.item(selected[0])
        values = item['values']
        if values:
            try:
                n_id = int(values[0])
            except ValueError:
                return
            confirm = messagebox.askyesno("Confirm Delete", f"Delete Notice #{n_id}?")
            if confirm:
                try:
                    database.delete_notice(n_id)
                    messagebox.showinfo("Deleted", f"Notice #{n_id} deleted.")
                    self.load_notices()
                except Exception as e:
                    messagebox.showerror("Error", f"Could not delete notice: {e}")

    def update_kpi_counters(self):
        counts = database.get_grievance_counts()
        self.lbl_total.config(text=f"Total: {counts['total']}")
        self.lbl_emergency.config(text=f"🔴 Emergency: {counts.get('emergency', 0)}")
        self.lbl_pending.config(text=f"Pending: {counts['pending']}")
        self.lbl_in_prog.config(text=f"In Progress: {counts['in_progress']}")
        self.lbl_resolved.config(text=f"Resolved: {counts['resolved']}")

    def reset_filters(self):
        self.filter_block_var.set("All")
        self.filter_status_var.set("All")
        self.search_entry.delete(0, tk.END)
        self.load_data()

    def load_data(self):
        target_id = self.selected_grievance_id
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        status_filter = self.filter_status_var.get()
        block_filter = self.filter_block_var.get()
        search_query = self.search_entry.get().strip()
        
        grievances = database.get_all_grievances(status_filter=status_filter, block_filter=block_filter, search_query=search_query)
        
        target_item_id = None
        for g in grievances:
            last_up = g.get('last_updated', g['date_submitted'])
            priority = g.get('priority', 'Normal')
            status = g['status']
            
            tag = "Emergency" if "Emergency" in priority and status != "Resolved" else status
            
            item_id = self.tree.insert("", tk.END, values=(
                g['grievance_id'], 
                g.get('block_name', 'BH-1'),
                g['room_number'],
                g['student_name'], 
                g['category'], 
                priority,
                last_up if last_up else g['date_submitted'],
                status
            ), tags=(tag,))
            
            if target_id is not None and g['grievance_id'] == target_id:
                target_item_id = item_id

        self.update_kpi_counters()
        
        if target_item_id:
            self.tree.selection_set(target_item_id)
            self.tree.focus(target_item_id)

    def sort_column(self, col):
        reverse = self.sort_reverse.get(col, False)
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        
        if col == "id":
            items.sort(key=lambda x: int(x[0]), reverse=reverse)
        else:
            items.sort(reverse=reverse)
            
        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)
            
        self.sort_reverse[col] = not reverse

    def clear_selection_panel(self):
        self.selected_grievance_id = None
        self.selected_id_var.set("None (Click a row above)")
        self.selected_desc_var.set("-")
        self.selected_suggestion_var.set("-")
        self.assigned_staff_entry.delete(0, tk.END)
        self.remarks_text.delete("1.0", tk.END)
        self.update_btn.config(state=tk.DISABLED)
        self.in_progress_btn.config(state=tk.DISABLED)
        self.resolve_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            self.clear_selection_panel()
            return
            
        item = self.tree.item(selected[0])
        values = item['values']
        
        if values:
            try:
                g_id = int(values[0])
            except ValueError:
                self.clear_selection_panel()
                return
                
            self.selected_grievance_id = g_id
            self.update_btn.config(state=tk.NORMAL)
            self.in_progress_btn.config(state=tk.NORMAL)
            self.resolve_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
            
            grievance = database.get_grievance_by_id(g_id)
            if grievance:
                block = grievance.get('block_name', 'BH-1')
                room = grievance['room_number']
                student = grievance['student_name']
                self.selected_id_var.set(f"#{g_id}  |  Resident: {student} ({block}, Room {room})")
                
                self.selected_desc_var.set(grievance['description'])
                sug = grievance.get('suggestion', '')
                self.selected_suggestion_var.set(sug if sug else "None provided.")

                self.status_var.set(grievance['status'])
                
                self.assigned_staff_entry.delete(0, tk.END)
                if grievance.get('assigned_staff'):
                    self.assigned_staff_entry.insert(0, grievance['assigned_staff'])
                    
                self.remarks_text.delete("1.0", tk.END)
                if grievance['admin_remarks']:
                    self.remarks_text.insert(tk.END, grievance['admin_remarks'])

    def quick_set_status(self, target_status):
        self.status_var.set(target_status)
        self.update_grievance()

    def update_grievance(self):
        if self.selected_grievance_id is None:
            messagebox.showerror("Error", "No grievance selected. Click a row in the table first.")
            return
            
        g_id = self.selected_grievance_id
        new_status = self.status_var.get()
        new_remarks = self.remarks_text.get("1.0", tk.END).strip()
        assigned_staff = self.assigned_staff_entry.get().strip()
        
        try:
            database.update_grievance(g_id, new_status, new_remarks, assigned_staff=assigned_staff)
            messagebox.showinfo("Warden Dispatch Updated", f"Grievance #{g_id} updated to status '{new_status}'.")
            self.load_data()  # Refresh table & KPIs
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {e}")

    def delete_grievance(self):
        if self.selected_grievance_id is None:
            messagebox.showerror("Error", "No grievance selected.")
            return
            
        g_id = self.selected_grievance_id
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Grievance #{g_id}?\nThis action cannot be undone.")
        if confirm:
            try:
                database.delete_grievance(g_id)
                messagebox.showinfo("Deleted", f"Grievance #{g_id} deleted successfully.")
                self.clear_selection_panel()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete grievance: {e}")

    def export_csv(self):
        status_filter = self.filter_status_var.get()
        block_filter = self.filter_block_var.get()
        search_query = self.search_entry.get().strip()
        grievances = database.get_all_grievances(status_filter=status_filter, block_filter=block_filter, search_query=search_query)
        
        if not grievances:
            messagebox.showwarning("Export Shift Log", "No grievance data available to export.")
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv", 
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Export Warden Shift Log to CSV"
        )
        
        if not filepath:
            return
            
        try:
            with open(filepath, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Grievance ID", "Hostel Block", "Room Number", "Student Name", 
                    "Category", "Priority", "Date Submitted", "Last Updated", 
                    "Status", "Assigned Duty Staff", "Description", "Student Suggestion", "Warden Remarks"
                ])
                for g in grievances:
                    writer.writerow([
                        g['grievance_id'],
                        g.get('block_name', 'BH-1'),
                        g['room_number'],
                        g['student_name'],
                        g['category'],
                        g.get('priority', 'Normal'),
                        g['date_submitted'],
                        g.get('last_updated', g['date_submitted']),
                        g['status'],
                        g.get('assigned_staff', 'Unassigned'),
                        g['description'],
                        g.get('suggestion', ''),
                        g['admin_remarks']
                    ])
            messagebox.showinfo("Success", f"Exported {len(grievances)} warden records to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not write CSV file: {e}")
