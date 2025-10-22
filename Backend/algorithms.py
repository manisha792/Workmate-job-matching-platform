import math

# Linear Search Algorithm
def linear_search_jobs(query, jobs):
    """
    Perform linear search to find jobs matching the query
    Time Complexity: O(n)
    """
    matching_jobs = []
    query = query.lower()
    
    for job in jobs:
        if (query in job['title'].lower() or 
            query in job['description'].lower() or 
            query in job['location'].lower()):
            matching_jobs.append(job)
    
    return matching_jobs

# Sorting Algorithm
def sort_jobs(jobs, key='pay', order='desc'):
    """
    Sort jobs by specified key (pay, location, etc.)
    Time Complexity: O(n log n)
    """
    def get_sort_value(job):
        if key == 'pay':
            return float(job.get('pay', 0))
        elif key == 'location':
            return job.get('location', '')
        else:
            return job.get(key, '')
    
    sorted_jobs = sorted(jobs, key=get_sort_value, reverse=(order == 'desc'))
    return sorted_jobs

# Dijkstra's Algorithm for nearest jobs
def dijkstra_nearest_jobs(student_location, jobs):
    """
    Find nearest jobs using Dijkstra's algorithm (simplified for string locations)
    Time Complexity: O(V + E log V) - simplified implementation
    """
    # Create a simple graph where locations are nodes
    # In a real implementation, you'd have actual coordinates and distances
    locations = set([student_location] + [job['location'] for job in jobs])
    
    # Simplified distance calculation (in real app, use actual coordinates)
    def calculate_distance(loc1, loc2):
        # Simple string similarity as distance proxy
        # In production, use actual geolocation distances
        loc1_clean = loc1.lower().replace(' ', '')
        loc2_clean = loc2.lower().replace(' ', '')
        
        if loc1_clean == loc2_clean:
            return 0
        
        # Calculate Levenshtein distance as proxy
        return levenshtein_distance(loc1_clean, loc2_clean)
    
    # Calculate distances from student location to all job locations
    job_distances = []
    for job in jobs:
        distance = calculate_distance(student_location, job['location'])
        job_distances.append((distance, job))
    
    # Sort by distance (ascending)
    job_distances.sort(key=lambda x: x[0])
    
    return [job for _, job in job_distances]

def levenshtein_distance(s1, s2):
    """
    Calculate Levenshtein distance between two strings
    Used as a proxy for location distance in this simplified implementation
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

# Hungarian Algorithm for fair job assignment
def hungarian_job_assignment(students, jobs):
    """
    Implement Hungarian algorithm for optimal job-student assignment
    Time Complexity: O(n³)
    """
    n = len(students)
    m = len(jobs)
    
    if n == 0 or m == 0:
        return []
    
    # Create cost matrix (students x jobs)
    cost_matrix = []
    for student in students:
        row = []
        for job in jobs:
            # Calculate cost based on location match and student rating
            location_cost = 1 if student['location'] == job['location'] else 10
            rating_cost = (5 - float(student.get('rating', 0))) * 2
            total_cost = location_cost + rating_cost
            row.append(total_cost)
        cost_matrix.append(row)
    
    # Simplified assignment (full Hungarian implementation would be more complex)
    assignments = []
    assigned_jobs = set()
    
    for i, student in enumerate(students):
        if i < m:  # Only assign if there are jobs available
            best_job_idx = -1
            best_cost = float('inf')
            
            for j in range(m):
                if j not in assigned_jobs and cost_matrix[i][j] < best_cost:
                    best_cost = cost_matrix[i][j]
                    best_job_idx = j
            
            if best_job_idx != -1:
                assignments.append({
                    'student_id': student['id'],
                    'job_id': jobs[best_job_idx]['id'],
                    'cost': best_cost
                })
                assigned_jobs.add(best_job_idx)
    
    return assignments