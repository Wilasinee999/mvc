import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class JobFairView:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Fair System")
        self.controller = None
        self.create_login_view()

    def set_controller(self, controller):
        self.controller = controller

    def show_message(self, message, message_type="Info"):
        if message_type == "Error":
            messagebox.showerror("Error", message)
        else:
            messagebox.showinfo("Info", message)

    def clear_frames(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_view(self):
        self.clear_frames()
        self.login_frame = tk.Frame(self.root, padx=30, pady=30)
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Job Fair System", font=("Arial", 20, "bold")).pack(pady=10)
        tk.Label(self.login_frame, text="Please enter your email to log in.", font=("Arial", 12)).pack()
        
        email_label = tk.Label(self.login_frame, text="Email:")
        email_label.pack(pady=(15, 0))
        self.email_entry = tk.Entry(self.login_frame, width=40, font=("Arial", 12))
        self.email_entry.pack(pady=5)
        
        login_button = tk.Button(self.login_frame, text="Login", command=self.handle_login, font=("Arial", 12, "bold"))
        login_button.pack(pady=10)
        
    def handle_login(self):
        email = self.email_entry.get()
        if self.controller:
            self.controller.login(email)

    def show_admin_view(self):
        
        self.clear_frames()
        self.admin_frame = tk.Frame(self.root, padx=15, pady=15)
        self.admin_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = tk.Frame(self.admin_frame)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="Admin Dashboard: All Candidates", font=("Arial", 16, "bold")).pack(side=tk.LEFT, pady=5)
        tk.Button(header_frame, text="Logout", command=self.controller.logout, font=("Arial", 10)).pack(side=tk.RIGHT)
        
        self.candidate_listbox = tk.Listbox(self.admin_frame, width=70, height=20, font=("Arial", 11))
        self.candidate_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        self.candidate_listbox.bind('<<ListboxSelect>>', self.handle_candidate_select)

        
        self.update_admin_candidate_list(self.controller.get_all_candidates())

    def update_admin_candidate_list(self, candidates):
        self.candidate_listbox.delete(0, tk.END)
        self.candidates_data = candidates
        for candidate in candidates:
            self.candidate_listbox.insert(tk.END, f"  {candidate['first_name']} {candidate['last_name']} ({candidate['email']})")

    def handle_candidate_select(self, event):
        selected_index = self.candidate_listbox.curselection()
        if selected_index:
            candidate_id = self.candidates_data[selected_index[0]]['candidate_id']
            self.show_candidate_details_view(candidate_id)

    def show_candidate_details_view(self, candidate_id):

        self.clear_frames()
        details_frame = tk.Frame(self.root, padx=15, pady=15)
        details_frame.pack(fill=tk.BOTH, expand=True)

        tk.Button(details_frame, text="< Back to Admin Dashboard", command=self.show_admin_view, font=("Arial", 10)).pack(anchor=tk.NW, pady=(0, 10))
        
        candidate, applied_jobs = self.controller.get_candidate_details(candidate_id)
        
        tk.Label(details_frame, text=f"Candidate Profile: {candidate['first_name']} {candidate['last_name']}", font=("Arial", 16, "bold")).pack(pady=5)
        tk.Label(details_frame, text=f"Email: {candidate['email']}", font=("Arial", 12)).pack(anchor=tk.W, pady=(5, 10))

        tk.Label(details_frame, text="Applied Jobs:", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=(10, 5))
        job_listbox = tk.Listbox(details_frame, width=80, height=15, font=("Arial", 11))
        job_listbox.pack(fill=tk.BOTH, expand=True)
        
        if applied_jobs:
            for job in applied_jobs:
                job_listbox.insert(tk.END, f"  - {job['job_title']} at {job['company_name']} (Applied: {job['application_date']})")
        else:
            job_listbox.insert(tk.END, "  - No applications submitted yet.")

    def show_candidate_view(self):
       
        self.clear_frames()
        self.candidate_frame = tk.Frame(self.root, padx=15, pady=15)
        self.candidate_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = tk.Frame(self.candidate_frame)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="Open Job Positions", font=("Arial", 16, "bold")).pack(side=tk.LEFT, pady=5)
        tk.Button(header_frame, text="Logout", command=self.controller.logout, font=("Arial", 10)).pack(side=tk.RIGHT)

        self.job_listbox = tk.Listbox(self.candidate_frame, width=80, height=20, font=("Arial", 11))
        self.job_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        self.job_listbox.bind('<<ListboxSelect>>', self.handle_job_select)

        self.update_open_jobs_list(self.controller.get_open_jobs())

    def update_open_jobs_list(self, jobs):
        self.job_listbox.delete(0, tk.END)
        self.jobs_data = jobs
        if jobs:
            for job in jobs:
                self.job_listbox.insert(tk.END, f"  {job['job_title']} at {job['company_name']} (Deadline: {job['deadline_date']})")
        else:
            self.job_listbox.insert(tk.END, "  - No open positions available at this time.")

    def handle_job_select(self, event):
        selected_index = self.job_listbox.curselection()
        if selected_index:
            job = self.jobs_data[selected_index[0]]
            confirm = messagebox.askyesno("Confirm Application", f"Do you want to apply for '{job['job_title']}'?")
            if confirm:
                self.controller.apply_for_job(job['job_id'])