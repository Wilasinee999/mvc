import re
from datetime import datetime
from model import candidates_db, jobs_db, companies_db, applications_db

class JobFairController:
    def __init__(self, view):
        self.view = view
        self.logged_in_user = None

    def login(self, email):
        candidate = candidates_db.find_one('email', email)
        if candidate:
            self.logged_in_user = candidate
            self.view.show_message(f"Welcome, {candidate['first_name']}!")
            if email == 'admin@admin.com':
                self.view.show_admin_view()
                self.view.update_admin_candidate_list(self.get_all_candidates())
            else:
                self.view.show_candidate_view()
                self.view.update_open_jobs_list(self.get_open_jobs())
            return True
        else:
            self.view.show_message("Invalid email address.", "Error")
            return False

    def logout(self):
        self.logged_in_user = None
        self.view.create_login_view() # แก้ไขให้กลับไปที่หน้า login โดยตรง

    def get_all_candidates(self):
        all_candidates = candidates_db.get_all()
        return sorted(all_candidates, key=lambda c: c['first_name'])

    def get_candidate_details(self, candidate_id):
        candidate = candidates_db.find_one('candidate_id', candidate_id)
        applications = applications_db.find_many('candidate_id', candidate_id)
        
        applied_jobs = []
        for app in applications:
            job = jobs_db.find_one('job_id', app['job_id'])
            company = companies_db.find_one('company_id', job['company_id'])
            applied_jobs.append({
                'job_title': job['job_title'],
                'company_name': company['company_name'],
                'application_date': app['application_date']
            })
        
        applied_jobs_sorted = sorted(applied_jobs, key=lambda j: j['job_title'])
        return candidate, applied_jobs_sorted

    def get_open_jobs(self):
        open_jobs = jobs_db.find_many('status', 'open')
        for job in open_jobs:
            company = companies_db.find_one('company_id', job['company_id'])
            job['company_name'] = company['company_name']
        return sorted(open_jobs, key=lambda j: j['deadline_date'])
    
    def apply_for_job(self, job_id):
        if not self.logged_in_user or self.logged_in_user['email'] == 'admin@admin.com':
            self.view.show_message("You must be logged in as a candidate to apply.", "Error")
            return False
        
        job_details = jobs_db.find_one('job_id', job_id)
        if not job_details:
            self.view.show_message("Job not found.", "Error")
            return False
            
        deadline = datetime.strptime(job_details['deadline_date'], '%Y-%m-%d').date()
        application_date = datetime.now().date()
        if application_date > deadline:
            self.view.show_message("The application deadline has passed.", "Error")
            return False

        existing_app = applications_db.find_many('job_id', job_id)
        for app in existing_app:
            if app['candidate_id'] == self.logged_in_user['candidate_id']:
                 self.view.show_message("You have already applied for this job.", "Info")
                 return False

        new_application = {
            "job_id": job_id,
            "candidate_id": self.logged_in_user['candidate_id'],
            "application_date": application_date.strftime('%Y-%m-%d')
        }
        applications_db.add(new_application)
        self.view.show_message("Application submitted successfully!", "Success")
        self.view.update_open_jobs_list(self.get_open_jobs())
        return True