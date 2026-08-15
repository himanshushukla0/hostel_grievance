import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database

class StudentView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(self.parent, padding="15")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Submit Grievance
        self.submit_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.submit_tab, text="📝 Register Complaint / Maintenance")
        self.setup_submit_tab()
        
        # Tab 2: Track Status
        self.track_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.track_tab, text="🔍 Track Complaint Status")
        self.setup_track_tab()
        
        # Tab 3: Campus Notices & Circulars
        self.notices_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.notices_tab, text="📢 Campus & Hostel Notices")
        self.setup_notices_tab()

    def setup_notices_tab(self):
        # Top Header / Notice Board Title
        hdr = ttk.Frame(self.notices_tab)
        hdr.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(hdr, text="📢 Official Hostel & College Circular Board", font=("Segoe UI", 12, "bold"), foreground="#0f172a").pack(side=tk.LEFT)
        
        # Filter dropdown
        filter_frame = ttk.Frame(hdr)
        filter_frame.pack(side=tk.RIGHT)
        
        ttk.Label(filter_frame, text="Filter Block:").pack(side=tk.LEFT, padx=(0, 4))
        self.student_notice_block_var = tk.StringVar(value="All Blocks")
        block_combo = ttk.Combobox(
            filter_frame, 
            textvariable=self.student_notice_block_var, 
            values=["All Blocks", "BH-1", "BH-2", "BH-3", "GH-1", "GH-2", "IH-1"], 
            state="readonly", 
            width=12
        )

        block_combo.pack(side=tk.LEFT)
        block_combo.bind("<<ComboboxSelected>>", lambda e: self.load_student_notices())
        
        # Notices Treeview Table Frame with Scrollbar
        notice_tree_frame = ttk.Frame(self.notices_tab)
        notice_tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        columns = ("id", "date", "category", "block", "title")
        self.student_notice_tree = ttk.Treeview(notice_tree_frame, columns=columns, show="headings", height=5)
        
        notice_scroll = ttk.Scrollbar(notice_tree_frame, orient="vertical", command=self.student_notice_tree.yview)
        self.student_notice_tree.configure(yscrollcommand=notice_scroll.set)
        
        self.student_notice_tree.heading("id", text="ID")
        self.student_notice_tree.heading("date", text="Date Posted")
        self.student_notice_tree.heading("category", text="Category")
        self.student_notice_tree.heading("block", text="Target Block")
        self.student_notice_tree.heading("title", text="Notice Title")
        
        self.student_notice_tree.column("id", width=35, anchor="center")
        self.student_notice_tree.column("date", width=130, anchor="center")
        self.student_notice_tree.column("category", width=160)
        self.student_notice_tree.column("block", width=90, anchor="center")
        self.student_notice_tree.column("title", width=300)
        
        self.student_notice_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        notice_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.student_notice_tree.bind("<<TreeviewSelect>>", self.on_student_notice_select)
        
        # Notice Detail Panel
        self.notice_detail_frame = ttk.LabelFrame(self.notices_tab, text="Announcement Details", padding="12")
        self.notice_detail_frame.pack(fill=tk.BOTH, expand=True)
        
        self.notice_title_var = tk.StringVar(value="Select a notice from the table above to view details.")
        self.notice_meta_var = tk.StringVar(value="")
        self.notice_body_var = tk.StringVar(value="")
        
        ttk.Label(self.notice_detail_frame, textvariable=self.notice_title_var, font=("Segoe UI", 11, "bold"), foreground="#1e293b").pack(anchor="w", pady=(0, 4))
        ttk.Label(self.notice_detail_frame, textvariable=self.notice_meta_var, font=("Segoe UI", 9, "bold"), foreground="#0369a1").pack(anchor="w", pady=(0, 8))
        ttk.Label(self.notice_detail_frame, textvariable=self.notice_body_var, wraplength=600, justify="left", font=("Segoe UI", 10)).pack(anchor="w")

        self.load_student_notices()

    def load_student_notices(self):
        for item in self.student_notice_tree.get_children():
            self.student_notice_tree.delete(item)
            
        block_filter = self.student_notice_block_var.get()
        notices = database.get_all_notices(block_filter=block_filter)
        
        for n in notices:
            self.student_notice_tree.insert("", tk.END, values=(
                n['notice_id'],
                n['date_posted'],
                n['category'],
                n['target_block'],
                n['title']
            ))
            
        if notices:
            children = self.student_notice_tree.get_children()
            if children:
                first_child = children[0]
                self.student_notice_tree.selection_set(first_child)
                self.student_notice_tree.focus(first_child)
                self.display_notice_details(notices[0])
        else:
            self.notice_title_var.set("No notices published yet.")
            self.notice_meta_var.set("")
            self.notice_body_var.set("")

    def on_student_notice_select(self, event):
        selected = self.student_notice_tree.selection()
        if not selected:
            return
        item = self.student_notice_tree.item(selected[0])
        values = item['values']
        if values:
            try:
                n_id = int(values[0])
            except ValueError:
                return
            notices = database.get_all_notices()
            target = next((n for n in notices if n['notice_id'] == n_id), None)
            if target:
                self.display_notice_details(target)

    def display_notice_details(self, notice):
        self.notice_title_var.set(f"📢 {notice['title']}")
        posted_by = notice.get('posted_by', 'Warden Office')
        self.notice_meta_var.set(
            f"✔ Verified by: {posted_by}  |  Category: {notice['category']}  |  Target: {notice['target_block']}  |  Date: {notice['date_posted']}"
        )
        self.notice_body_var.set(notice['content'])


    def setup_submit_tab(self):
        # Form Container
        form_frame = ttk.LabelFrame(self.submit_tab, text="Resident Maintenance Request Form", padding="15")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Student Name
        ttk.Label(form_frame, text="Student Full Name:").grid(row=0, column=0, sticky="w", pady=4)
        self.name_entry = ttk.Entry(form_frame, width=42)
        self.name_entry.grid(row=0, column=1, sticky="w", pady=4, padx=10)
        
        # Hostel Block
        ttk.Label(form_frame, text="Hostel Block:").grid(row=1, column=0, sticky="w", pady=4)
        self.block_var = tk.StringVar(value="BH-1 (Boys Hostel 1)")
        blocks = [
            "BH-1 (Boys Hostel 1)",
            "BH-2 (Boys Hostel 2)",
            "BH-3 (Boys Hostel 3)",
            "GH-1 (Girls Hostel 1)",
            "GH-2 (Girls Hostel 2)",
            "IH-1 (International / PG Hostel)"
        ]
        self.block_dropdown = ttk.Combobox(form_frame, textvariable=self.block_var, values=blocks, state="readonly", width=39)
        self.block_dropdown.grid(row=1, column=1, sticky="w", pady=4, padx=10)
        
        # Room Number
        ttk.Label(form_frame, text="Room / Bed Number:").grid(row=2, column=0, sticky="w", pady=4)
        self.room_entry = ttk.Entry(form_frame, width=42)
        self.room_entry.grid(row=2, column=1, sticky="w", pady=4, padx=10)
        
        # Category with Icons (including Miscellaneous)
        ttk.Label(form_frame, text="Maintenance Category:").grid(row=3, column=0, sticky="w", pady=4)
        self.category_var = tk.StringVar()
        categories = [
            "⚡ Electrical Repair (Fan, Light, Switch)",
            "🚰 Plumbing & Water (Tap, Leak, Flush)",
            "🧹 Cleaning & Room Sanitation",
            "🍽️ Food & Mess Quality Complaint",
            "📶 Wi-Fi & LAN Internet Connectivity",
            "🚪 Carpentry, Door & Furniture Lock",
            "🏢 General Facility / AC / Water Cooler",
            "📦 Miscellaneous / Other Hostel Issue"
        ]
        self.category_dropdown = ttk.Combobox(form_frame, textvariable=self.category_var, values=categories, state="readonly", width=39)
        self.category_dropdown.grid(row=3, column=1, sticky="w", pady=4, padx=10)
        
        # Priority Level
        ttk.Label(form_frame, text="Priority Level:").grid(row=4, column=0, sticky="w", pady=4)
        self.priority_var = tk.StringVar(value="🟢 Normal (Standard Duty)")
        priorities = [
            "🟢 Normal (Standard Duty)",
            "🟡 Urgent (Same Day Attention)",
            "🔴 Emergency (Immediate Water/Electrical Hazard)"
        ]
        self.priority_dropdown = ttk.Combobox(form_frame, textvariable=self.priority_var, values=priorities, state="readonly", width=39)
        self.priority_dropdown.grid(row=4, column=1, sticky="w", pady=4, padx=10)
        
        # Description
        ttk.Label(form_frame, text="Issue Description:").grid(row=5, column=0, sticky="nw", pady=4)
        self.desc_text = tk.Text(form_frame, width=42, height=3)
        self.desc_text.grid(row=5, column=1, sticky="w", pady=4, padx=10)
        
        # Student Suggestion / Solution
        ttk.Label(form_frame, text="Suggestion / Solution:").grid(row=6, column=0, sticky="nw", pady=4)
        self.suggestion_text = tk.Text(form_frame, width=42, height=3)
        self.suggestion_text.grid(row=6, column=1, sticky="w", pady=4, padx=10)
        
        # Submit Button
        submit_btn = ttk.Button(form_frame, text="🚀 Submit Maintenance Request", command=self.submit_grievance, style="Primary.TButton")
        submit_btn.grid(row=7, column=1, pady=10, sticky="e", padx=10)

    def submit_grievance(self):
        name = self.name_entry.get().strip()
        block_full = self.block_var.get()
        # Parse clean block code e.g. "BH-1" from "BH-1 (Boys Hostel 1)"
        block = block_full.split(" (")[0] if " (" in block_full else block_full
        room = self.room_entry.get().strip()
        category = self.category_var.get()
        priority = self.priority_var.get()
        description = self.desc_text.get("1.0", tk.END).strip()
        suggestion = self.suggestion_text.get("1.0", tk.END).strip()
        
        if not name or not room or not category or not description:
            messagebox.showerror("Validation Error", "Please fill in all required fields (Name, Room, Category, Description).")
            return
            
        try:
            grievance_id = database.create_grievance(
                name=name,
                room=room,
                category=category,
                description=description,
                block_name=block,
                priority=priority,
                suggestion=suggestion
            )
            
            # Copy to clipboard automatically
            try:
                self.parent.clipboard_clear()
                self.parent.clipboard_append(str(grievance_id))
                copied_text = "\n(Grievance ID copied to clipboard!)"
            except Exception:
                copied_text = ""
                
            messagebox.showinfo(
                "Request Submitted", 
                f"Your request has been logged successfully!\n\n"
                f"🎫 Grievance ID: #{grievance_id}\n"
                f"🏢 Block: {block} | Room: {room}\n"
                f"⚡ Priority: {priority}{copied_text}\n\n"
                f"Redirecting to Track Status..."
            )
            
            # Clear form fields
            self.name_entry.delete(0, tk.END)
            self.room_entry.delete(0, tk.END)
            self.category_dropdown.set('')
            self.desc_text.delete("1.0", tk.END)
            self.suggestion_text.delete("1.0", tk.END)
            
            # Switch to track tab & auto-search
            self.search_mode_var.set("Grievance ID")
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, str(grievance_id))
            self.notebook.select(self.track_tab)
            self.check_status()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit request: {e}")

    def setup_track_tab(self):
        search_frame = ttk.Frame(self.track_tab)
        search_frame.pack(fill=tk.X, pady=(0, 8))
        
        ttk.Label(search_frame, text="Search By:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_mode_var = tk.StringVar(value="Grievance ID")
        search_combobox = ttk.Combobox(
            search_frame, 
            textvariable=self.search_mode_var, 
            values=["Grievance ID", "Room Number / Name"], 
            state="readonly", 
            width=18
        )
        search_combobox.pack(side=tk.LEFT, padx=(0, 10))
        
        self.id_entry = ttk.Entry(search_frame, width=22)
        self.id_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.id_entry.bind("<Return>", lambda event: self.check_status())
        
        check_btn = ttk.Button(search_frame, text="Search", command=self.check_status)
        check_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.copy_btn = ttk.Button(search_frame, text="📋 Copy ID", command=self.copy_current_id, state=tk.DISABLED)
        self.copy_btn.pack(side=tk.LEFT)
        
        # Results List Table Frame with Scrollbar
        self.results_frame = ttk.LabelFrame(self.track_tab, text="Matching Complaints for Room / Resident", padding="8")
        
        tree_subframe = ttk.Frame(self.results_frame)
        tree_subframe.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "block", "room", "category", "priority", "status")
        self.results_tree = ttk.Treeview(tree_subframe, columns=columns, show="headings", height=4)
        
        results_scroll = ttk.Scrollbar(tree_subframe, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=results_scroll.set)

        self.results_tree.heading("id", text="ID")
        self.results_tree.heading("block", text="Block")
        self.results_tree.heading("room", text="Room")
        self.results_tree.heading("category", text="Category")
        self.results_tree.heading("priority", text="Priority")
        self.results_tree.heading("status", text="Status")
        
        self.results_tree.column("id", width=40, anchor="center")
        self.results_tree.column("block", width=70, anchor="center")
        self.results_tree.column("room", width=60, anchor="center")
        self.results_tree.column("category", width=140)
        self.results_tree.column("priority", width=110, anchor="center")
        self.results_tree.column("status", width=95, anchor="center")
        
        self.results_tree.tag_configure("Pending", background="#fff0f0", foreground="#900c3f")
        self.results_tree.tag_configure("In Progress", background="#fffdf0", foreground="#8a6d3b")
        self.results_tree.tag_configure("Resolved", background="#f0fff4", foreground="#155724")
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_tree.bind("<<TreeviewSelect>>", self.on_list_select)
        
        # Details display panel
        self.result_frame = ttk.LabelFrame(self.track_tab, text="Detailed Complaint Status & Warden Remarks", padding="12")
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Detail variables
        self.current_grievance_id = None
        self.status_var = tk.StringVar(value="Status: N/A")
        self.details_var = tk.StringVar(value="Enter a Grievance ID or Room Number above to track status.")
        self.desc_display_var = tk.StringVar(value="")
        self.suggestion_display_var = tk.StringVar(value="")
        self.staff_var = tk.StringVar(value="")
        self.remarks_var = tk.StringVar(value="")
        
        # Status header with color badge
        self.status_label = ttk.Label(self.result_frame, textvariable=self.status_var, font=("Arial", 12, "bold"))
        self.status_label.pack(anchor="w", pady=(0, 5))
        
        # Student info summary
        ttk.Label(self.result_frame, textvariable=self.details_var, font=("Arial", 9)).pack(anchor="w", pady=(0, 6))
        
        # Assigned Staff
        ttk.Label(self.result_frame, textvariable=self.staff_var, font=("Arial", 9, "bold"), foreground="#0369a1").pack(anchor="w", pady=(0, 6))
        
        # Description
        ttk.Label(self.result_frame, text="Submitted Complaint Description:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(4, 0))
        ttk.Label(self.result_frame, textvariable=self.desc_display_var, wraplength=560, justify="left").pack(anchor="w", pady=(0, 6))
        
        # Student Suggestion
        ttk.Label(self.result_frame, text="Student Suggestion / Requested Action:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(4, 0))
        ttk.Label(self.result_frame, textvariable=self.suggestion_display_var, wraplength=560, justify="left", foreground="#047857").pack(anchor="w", pady=(0, 6))

        # Admin Remarks
        ttk.Label(self.result_frame, text="Warden / Maintenance Remarks:", font=("Arial", 9, "bold")).pack(anchor="w", pady=(4, 0))
        ttk.Label(self.result_frame, textvariable=self.remarks_var, wraplength=560, justify="left", foreground="#1e40af").pack(anchor="w", pady=(0, 5))

    def copy_current_id(self):
        if self.current_grievance_id:
            try:
                self.parent.clipboard_clear()
                self.parent.clipboard_append(str(self.current_grievance_id))
                messagebox.showinfo("Copied", f"Grievance ID #{self.current_grievance_id} copied to clipboard!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not copy: {e}")

    def clear_status_display(self):
        self.current_grievance_id = None
        self.copy_btn.config(state=tk.DISABLED)
        self.status_var.set("Status: N/A")
        self.status_label.config(foreground="black")
        self.details_var.set("Enter a Grievance ID or Room Number above to track status.")
        self.desc_display_var.set("")
        self.suggestion_display_var.set("")
        self.staff_var.set("")
        self.remarks_var.set("")
        self.results_frame.pack_forget()

    def update_status_display(self, grievance):
        self.current_grievance_id = grievance['grievance_id']
        self.copy_btn.config(state=tk.NORMAL)
        
        status = grievance['status']
        
        # Color badge
        if status == "Pending":
            badge = "🔴 Pending"
            self.status_label.config(foreground="#b71c1c")
        elif status == "In Progress":
            badge = "🟡 In Progress"
            self.status_label.config(foreground="#e65100")
        elif status == "Resolved":
            badge = "🟢 Resolved"
            self.status_label.config(foreground="#1b5e20")
        else:
            badge = status
            self.status_label.config(foreground="black")
            
        self.status_var.set(f"Status: {badge}")
        
        block = grievance.get('block_name', 'BH-1')
        priority = grievance.get('priority', 'Normal')
        last_up = grievance.get('last_updated', '')
        up_str = f" | Last Updated: {last_up}" if last_up else ""
        
        summary = (f"ID: #{grievance['grievance_id']}  |  Resident: {grievance['student_name']} ({block}, Room {grievance['room_number']})\n"
                   f"Category: {grievance['category']}  |  Priority: {priority}  |  Submitted: {grievance['date_submitted']}{up_str}")
        self.details_var.set(summary)
        
        staff = grievance.get('assigned_staff', '')
        if staff:
            self.staff_var.set(f"🛠 Assigned Duty Officer / Staff: {staff}")
        else:
            self.staff_var.set("🛠 Assigned Duty Officer / Staff: Pending Warden Assignment")
            
        self.desc_display_var.set(grievance['description'])
        
        sug = grievance.get('suggestion', '')
        self.suggestion_display_var.set(sug if sug else "None provided.")

        remarks = grievance['admin_remarks'] if grievance['admin_remarks'] else "No remarks from Warden Office yet."
        self.remarks_var.set(remarks)

    def on_list_select(self, event):
        selected = self.results_tree.selection()
        if not selected:
            return
        item = self.results_tree.item(selected[0])
        values = item['values']
        if values:
            try:
                g_id = int(values[0])
            except ValueError:
                return
            grievance = database.get_grievance_by_id(g_id)
            if grievance:
                self.update_status_display(grievance)

    def check_status(self):
        raw_search = self.id_entry.get().strip()
        search_mode = self.search_mode_var.get()
        
        if not raw_search:
            messagebox.showerror("Input Error", f"Please enter a {search_mode}.")
            self.clear_status_display()
            return

        if search_mode == "Grievance ID":
            try:
                g_id = int(raw_search)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid numeric Grievance ID.")
                self.clear_status_display()
                return
                
            grievance = database.get_grievance_by_id(g_id)
            if grievance:
                self.results_frame.pack_forget()
                self.update_status_display(grievance)
            else:
                messagebox.showerror("Not Found", f"No complaint found with ID #{g_id}.")
                self.clear_status_display()
                
        else:  # Room / Name Search
            grievances = database.get_grievances_by_room_or_name(raw_search)
            if not grievances:
                messagebox.showerror("Not Found", f"No complaints found matching '{raw_search}'.")
                self.clear_status_display()
                return
                
            # Show results list table
            self.results_frame.pack(fill=tk.X, before=self.result_frame, pady=(0, 5))
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
                
            for g in grievances:
                self.results_tree.insert("", tk.END, values=(
                    g['grievance_id'],
                    g.get('block_name', 'BH-1'),
                    g['room_number'],
                    g['category'],
                    g.get('priority', 'Normal'),
                    g['status']
                ), tags=(g['status'],))
                
            # Select first result by default
            children = self.results_tree.get_children()
            if children:
                first_child = children[0]
                self.results_tree.selection_set(first_child)
                self.results_tree.focus(first_child)
                self.update_status_display(grievances[0])
