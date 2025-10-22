#!/usr/bin/env python3
"""
Test script for all algorithms in the Job Matching Platform
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from algorithms import (
    linear_search_jobs,
    sort_jobs,
    dijkstra_nearest_jobs,
    hungarian_job_assignment
)

def test_linear_search():
    """Test linear search algorithm"""
    print("Testing Linear Search Algorithm...")
    
    jobs = [
        {'id': '1', 'title': 'Web Developer', 'description': 'Frontend development', 'location': 'New York'},
        {'id': '2', 'title': 'Data Entry', 'description': 'Remote data entry work', 'location': 'Brooklyn'},
        {'id': '3', 'title': 'Graphic Designer', 'description': 'Create marketing materials', 'location': 'Manhattan'}
    ]
    
    # Test search by title
    results = linear_search_jobs('developer', jobs)
    print(f"Search for 'developer': {len(results)} results")
    assert len(results) == 1
    assert results[0]['title'] == 'Web Developer'
    
    # Test search by location
    results = linear_search_jobs('manhattan', jobs)
    print(f"Search for 'manhattan': {len(results)} results")
    assert len(results) == 1
    assert results[0]['location'] == 'Manhattan'
    
    print("Linear Search Algorithm: PASSED\n")

def test_sorting():
    """Test sorting algorithm"""
    print("Testing Sorting Algorithm...")
    
    jobs = [
        {'id': '1', 'title': 'Job A', 'pay': '20', 'location': 'New York'},
        {'id': '2', 'title': 'Job B', 'pay': '30', 'location': 'Brooklyn'},
        {'id': '3', 'title': 'Job C', 'pay': '15', 'location': 'Manhattan'}
    ]
    
    # Test sorting by pay (descending)
    sorted_jobs = sort_jobs(jobs, 'pay', 'desc')
    print(f"Sorted by pay (desc): {[job['pay'] for job in sorted_jobs]}")
    assert sorted_jobs[0]['pay'] == '30'
    assert sorted_jobs[1]['pay'] == '20'
    assert sorted_jobs[2]['pay'] == '15'
    
    # Test sorting by pay (ascending)
    sorted_jobs = sort_jobs(jobs, 'pay', 'asc')
    print(f"Sorted by pay (asc): {[job['pay'] for job in sorted_jobs]}")
    assert sorted_jobs[0]['pay'] == '15'
    assert sorted_jobs[1]['pay'] == '20'
    assert sorted_jobs[2]['pay'] == '30'
    
    print("Sorting Algorithm: PASSED\n")

def test_dijkstra():
    """Test Dijkstra's algorithm for nearest jobs"""
    print("Testing Dijkstra's Algorithm...")
    
    jobs = [
        {'id': '1', 'title': 'Job A', 'location': 'New York'},
        {'id': '2', 'title': 'Job B', 'location': 'Brooklyn'},
        {'id': '3', 'title': 'Job C', 'location': 'Manhattan'},
        {'id': '4', 'title': 'Job D', 'location': 'New York'}  # Same as student location
    ]
    
    student_location = 'New York'
    nearest_jobs = dijkstra_nearest_jobs(student_location, jobs)
    
    print(f"Student location: {student_location}")
    print(f"Nearest jobs: {[job['title'] for job in nearest_jobs]}")
    
    # Jobs in the same location should be first
    assert nearest_jobs[0]['location'] == 'New York'
    assert nearest_jobs[1]['location'] == 'New York'
    
    print("Dijkstra's Algorithm: PASSED\n")

def test_hungarian():
    """Test Hungarian algorithm for job assignment"""
    print("Testing Hungarian Algorithm...")
    
    students = [
        {'id': '1', 'location': 'New York', 'rating': '4.5'},
        {'id': '2', 'location': 'Brooklyn', 'rating': '4.2'},
        {'id': '3', 'location': 'Manhattan', 'rating': '4.8'}
    ]
    
    jobs = [
        {'id': '1', 'location': 'New York'},
        {'id': '2', 'location': 'Brooklyn'},
        {'id': '3', 'location': 'Manhattan'}
    ]
    
    assignments = hungarian_job_assignment(students, jobs)
    
    print(f"Assignments: {assignments}")
    assert len(assignments) == 3
    
    # Check that each student gets assigned to a job
    assigned_students = {assignment['student_id'] for assignment in assignments}
    assigned_jobs = {assignment['job_id'] for assignment in assignments}
    
    assert len(assigned_students) == 3
    assert len(assigned_jobs) == 3
    
    print("Hungarian Algorithm: PASSED\n")

def main():
    """Run all algorithm tests"""
    print("Testing Job Matching Platform Algorithms\n")
    print("=" * 50)
    
    try:
        test_linear_search()
        test_sorting()
        test_dijkstra()
        test_hungarian()
        
        print("All algorithms are working correctly!")
        print("=" * 50)
        
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
