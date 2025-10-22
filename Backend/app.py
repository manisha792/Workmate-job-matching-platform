from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

# Support running as a module (python -m Backend.app) or as a script (python app.py)
try:
    # When app is part of a package
    from .algorithms import (
        linear_search_jobs,
        sort_jobs,
        dijkstra_nearest_jobs,
        hungarian_job_assignment
    )
except Exception:
    # When running directly from the Backend directory
    from algorithms import (
        linear_search_jobs,
        sort_jobs,
        dijkstra_nearest_jobs,
        hungarian_job_assignment
    )

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000', 'https://your-netlify-site.netlify.app'], 
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

# Data file paths (always resolve relative to this file's directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
JOBS_FILE = os.path.join(DATA_DIR, 'jobs.csv')
STUDENTS_FILE = os.path.join(DATA_DIR, 'students.csv')
PROVIDERS_FILE = os.path.join(DATA_DIR, 'providers.csv')

# Initialize CSV files with headers if they don't exist
def init_csv_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not os.path.exists(JOBS_FILE):
        with open(JOBS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'title', 'description', 'location', 'pay', 'provider_id', 'status', 'assigned_student_id'])
    
    if not os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'email', 'password', 'location', 'bio', 'rating', 'jobs_completed'])
    
    if not os.path.exists(PROVIDERS_FILE):
        with open(PROVIDERS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'email', 'password', 'company'])

init_csv_files()
# Root and health routes for quick checks
@app.route('/', methods=['GET'])
def root():
    return jsonify({'status': 'ok', 'service': 'workmate-backend'}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200


# Helper functions for CSV operations
def read_csv(file_path):
    with open(file_path, 'r') as f:
        return list(csv.DictReader(f))

def write_csv(file_path, data):
    with open(file_path, 'w', newline='') as f:
        if data:
            # Clean the data to remove None values
            cleaned_data = []
            for row in data:
                cleaned_row = {k: v for k, v in row.items() if v is not None}
                cleaned_data.append(cleaned_row)
            
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(cleaned_data)

def append_csv(file_path, row):
    with open(file_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        writer.writerow(row)

# Authentication routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    user_type = data.get('type', '').lower().strip()
    email = data.get('email')
    
    if user_type == 'student':
        users = read_csv(STUDENTS_FILE)
        if any(u['email'] == email for u in users):
            return jsonify({'error': 'Email already exists'}), 400
        
        new_student = {
            'id': str(len(users) + 1),
            'name': data.get('name'),
            'email': email,
            'password': data.get('password'),
            'location': data.get('location'),
            'bio': data.get('bio', ''),
            'rating': '0',
            'jobs_completed': '0'
        }
        append_csv(STUDENTS_FILE, new_student)
        return jsonify({'message': 'Student registered successfully', 'user': new_student})
    
    elif user_type == 'provider':
        providers = read_csv(PROVIDERS_FILE)
        if any(p['email'] == email for p in providers):
            return jsonify({'error': 'Email already exists'}), 400
        
        new_provider = {
            'id': str(len(providers) + 1),
            'name': data.get('name'),
            'email': email,
            'password': data.get('password'),
            'company': data.get('company')
        }
        append_csv(PROVIDERS_FILE, new_provider)
        return jsonify({'message': 'Provider registered successfully', 'user': new_provider})
    
    return jsonify({'error': 'Invalid user type'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user_type = data.get('type')
    email = data.get('email')
    password = data.get('password')
    
    if user_type == 'student':
        students = read_csv(STUDENTS_FILE)
        student = next((s for s in students if s['email'] == email and s['password'] == password), None)
        if student:
            return jsonify({'message': 'Login successful', 'user': student})
    
    elif user_type == 'provider':
        providers = read_csv(PROVIDERS_FILE)
        provider = next((p for p in providers if p['email'] == email and p['password'] == password), None)
        if provider:
            return jsonify({'message': 'Login successful', 'user': provider})
    
    return jsonify({'error': 'Invalid credentials'}), 401

# Job routes
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = read_csv(JOBS_FILE)
    # Filter only available jobs
    available_jobs = [job for job in jobs if job['status'] == 'available']
    return jsonify(available_jobs)

@app.route('/api/jobs/provider/<provider_id>', methods=['GET'])
def get_provider_jobs(provider_id):
    jobs = read_csv(JOBS_FILE)
    provider_jobs = [job for job in jobs if job['provider_id'] == provider_id]
    return jsonify(provider_jobs)

@app.route('/api/jobs', methods=['POST'])
def create_job():
    data = request.json
    jobs = read_csv(JOBS_FILE)
    
    new_job = {
        'id': str(len(jobs) + 1),
        'title': data.get('title'),
        'description': data.get('description'),
        'location': data.get('location'),
        'pay': data.get('pay'),
        'provider_id': data.get('provider_id'),
        'status': 'available',
        'assigned_student_id': ''
    }
    
    append_csv(JOBS_FILE, new_job)
    return jsonify({'message': 'Job created successfully', 'job': new_job})

@app.route('/api/jobs/<job_id>/apply', methods=['POST'])
def apply_job(job_id):
    data = request.json
    student_id = data.get('student_id')
    
    jobs = read_csv(JOBS_FILE)
    for job in jobs:
        if job['id'] == job_id:
            job['status'] = 'applied'
            job['assigned_student_id'] = student_id
            break
    
    write_csv(JOBS_FILE, jobs)
    
    # Update student's jobs completed
    students = read_csv(STUDENTS_FILE)
    for student in students:
        if student['id'] == student_id:
            student['jobs_completed'] = str(int(student.get('jobs_completed', 0)) + 1)
            break
    
    write_csv(STUDENTS_FILE, students)
    
    return jsonify({'message': 'Job applied successfully'})

# Algorithm routes
@app.route('/api/jobs/suggested/<student_id>', methods=['GET'])
def get_suggested_jobs(student_id):
    students = read_csv(STUDENTS_FILE)
    jobs = read_csv(JOBS_FILE)
    
    student = next((s for s in students if s['id'] == student_id), None)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    available_jobs = [job for job in jobs if job['status'] == 'available']
    
    # Use Dijkstra's algorithm to find nearest jobs
    suggested_jobs = dijkstra_nearest_jobs(student['location'], available_jobs)
    return jsonify(suggested_jobs[:5])  # Return top 5 suggested jobs

@app.route('/api/jobs/search', methods=['GET'])
def search_jobs():
    query = request.args.get('q', '')
    jobs = read_csv(JOBS_FILE)
    available_jobs = [job for job in jobs if job['status'] == 'available']
    
    # Use linear search to find jobs matching query
    matching_jobs = linear_search_jobs(query, available_jobs)
    return jsonify(matching_jobs)

@app.route('/api/jobs/sort', methods=['GET'])
def sort_jobs_route():
    sort_by = request.args.get('by', 'pay')
    order = request.args.get('order', 'desc')
    
    jobs = read_csv(JOBS_FILE)
    available_jobs = [job for job in jobs if job['status'] == 'available']
    
    sorted_jobs = sort_jobs(available_jobs, sort_by, order)
    return jsonify(sorted_jobs)

# Student routes
@app.route('/api/students/<student_id>', methods=['GET'])
def get_student(student_id):
    students = read_csv(STUDENTS_FILE)
    student = next((s for s in students if s['id'] == student_id), None)
    
    if student:
        # Get student's job history
        jobs = read_csv(JOBS_FILE)
        student_jobs = [job for job in jobs if job['assigned_student_id'] == student_id]
        student['job_history'] = student_jobs
        return jsonify(student)
    
    return jsonify({'error': 'Student not found'}), 404

@app.route('/api/students/<student_id>/rate', methods=['POST'])
def rate_student(student_id):
    data = request.json
    rating = float(data.get('rating', 0))
    
    if rating < 1 or rating > 5:
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    students = read_csv(STUDENTS_FILE)
    for student in students:
        if student['id'] == student_id:
            # Update rating (simple average for now)
            current_rating = float(student.get('rating', 0))
            jobs_completed = int(student.get('jobs_completed', 0))
            
            if jobs_completed > 0:
                new_rating = (current_rating * jobs_completed + rating) / (jobs_completed + 1)
            else:
                new_rating = rating
            
            student['rating'] = str(round(new_rating, 2))
            break
    
    write_csv(STUDENTS_FILE, students)
    return jsonify({'message': 'Student rated successfully'})

# Provider routes
@app.route('/api/providers/<provider_id>', methods=['GET'])
def get_provider(provider_id):
    providers = read_csv(PROVIDERS_FILE)
    provider = next((p for p in providers if p['id'] == provider_id), None)
    
    if provider:
        # Get provider's jobs
        jobs = read_csv(JOBS_FILE)
        provider_jobs = [job for job in jobs if job['provider_id'] == provider_id]
        provider['jobs'] = provider_jobs
        return jsonify(provider)
    
    return jsonify({'error': 'Provider not found'}), 404

# Job management routes
@app.route('/api/jobs/<job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.json
    jobs = read_csv(JOBS_FILE)
    
    for job in jobs:
        if job['id'] == job_id:
            job.update(data)
            break
    
    write_csv(JOBS_FILE, jobs)
    return jsonify({'message': 'Job updated successfully'})

@app.route('/api/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    jobs = read_csv(JOBS_FILE)
    jobs = [job for job in jobs if job['id'] != job_id]
    
    write_csv(JOBS_FILE, jobs)
    return jsonify({'message': 'Job deleted successfully'})

# Hungarian algorithm route for optimal assignment
@app.route('/api/assignments/optimal', methods=['POST'])
def optimal_assignment():
    data = request.json
    student_ids = data.get('student_ids', [])
    job_ids = data.get('job_ids', [])
    
    students = read_csv(STUDENTS_FILE)
    jobs = read_csv(JOBS_FILE)
    
    selected_students = [s for s in students if s['id'] in student_ids]
    selected_jobs = [j for j in jobs if j['id'] in job_ids and j['status'] == 'available']
    
    assignments = hungarian_job_assignment(selected_students, selected_jobs)
    
    # Update job assignments
    for assignment in assignments:
        for job in jobs:
            if job['id'] == assignment['job_id']:
                job['assigned_student_id'] = assignment['student_id']
                job['status'] = 'assigned'
                break
    
    write_csv(JOBS_FILE, jobs)
    
    return jsonify({'message': 'Optimal assignments completed', 'assignments': assignments})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)