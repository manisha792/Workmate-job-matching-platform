import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { jobService, studentService } from '../services/api';

function StudentDashboard() {
  const { user } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [suggestedJobs, setSuggestedJobs] = useState([]);
  const [studentProfile, setStudentProfile] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('pay');
  const [sortOrder, setSortOrder] = useState('desc');

  useEffect(() => {
    loadJobs();
    loadSuggestedJobs();
    loadStudentProfile();
  }, [user]);

  const loadJobs = async () => {
    try {
      const response = await jobService.getJobs();
      setJobs(response.data);
    } catch (error) {
      console.error('Error loading jobs:', error);
    }
  };

  const loadSuggestedJobs = async () => {
    try {
      const response = await jobService.getSuggestedJobs(user.id);
      setSuggestedJobs(response.data);
    } catch (error) {
      console.error('Error loading suggested jobs:', error);
    }
  };

  const loadStudentProfile = async () => {
    try {
      const response = await studentService.getStudent(user.id);
      setStudentProfile(response.data);
    } catch (error) {
      console.error('Error loading student profile:', error);
    }
  };

  const handleSearch = async () => {
    try {
      const response = await jobService.searchJobs(searchQuery);
      setJobs(response.data);
    } catch (error) {
      console.error('Error searching jobs:', error);
    }
  };

  const handleSort = async () => {
    try {
      const response = await jobService.sortJobs(sortBy, sortOrder);
      setJobs(response.data);
    } catch (error) {
      console.error('Error sorting jobs:', error);
    }
  };

  const handleApply = async (jobId) => {
    try {
      await jobService.applyJob(jobId, user.id);
      alert('Job application submitted successfully!');
      loadJobs();
      loadStudentProfile();
    } catch (error) {
      console.error('Error applying to job:', error);
      alert('Error applying to job. Please try again.');
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Profile Sidebar */}
        <div className="lg:col-span-1">
          {studentProfile && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold mb-4">Your Profile</h2>
              <div className="space-y-3">
                <p><strong>Name:</strong> {studentProfile.name}</p>
                <p><strong>Email:</strong> {studentProfile.email}</p>
                <p><strong>Location:</strong> {studentProfile.location}</p>
                <p><strong>Rating:</strong> ⭐ {studentProfile.rating}/5</p>
                <p><strong>Jobs Completed:</strong> {studentProfile.jobs_completed}</p>
                <p><strong>Bio:</strong> {studentProfile.bio}</p>
              </div>
            </div>
          )}

          {/* Suggested Jobs */}
          <div className="bg-white rounded-lg shadow-md p-6 mt-6">
            <h3 className="text-xl font-bold mb-4">Suggested Jobs</h3>
            <div className="space-y-4">
              {suggestedJobs.map(job => (
                <div key={job.id} className="border rounded-lg p-4">
                  <h4 className="font-semibold">{job.title}</h4>
                  <p className="text-sm text-gray-600">{job.location}</p>
                  <p className="text-green-600 font-bold">${job.pay}/hr</p>
                  <button
                    onClick={() => handleApply(job.id)}
                    className="bg-blue-500 text-white px-3 py-1 rounded text-sm mt-2 hover:bg-blue-600"
                  >
                    Apply
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h1 className="text-3xl font-bold mb-6">Available Jobs</h1>
            
            {/* Search and Sort Controls */}
            <div className="flex flex-col sm:flex-row gap-4 mb-6">
              <div className="flex-1">
                <input
                  type="text"
                  placeholder="Search jobs..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full px-4 py-2 border rounded-lg"
                />
              </div>
              <button
                onClick={handleSearch}
                className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600"
              >
                Search
              </button>
              
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-4 py-2 border rounded-lg"
              >
                <option value="pay">Pay</option>
                <option value="location">Location</option>
              </select>
              
              <select
                value={sortOrder}
                onChange={(e) => setSortOrder(e.target.value)}
                className="px-4 py-2 border rounded-lg"
              >
                <option value="desc">High to Low</option>
                <option value="asc">Low to High</option>
              </select>
              
              <button
                onClick={handleSort}
                className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600"
              >
                Sort
              </button>
            </div>

            {/* Jobs List */}
            <div className="space-y-4">
              {jobs.map(job => (
                <div key={job.id} className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="text-xl font-semibold">{job.title}</h3>
                      <p className="text-gray-600 mt-2">{job.description}</p>
                      <div className="flex items-center gap-4 mt-3">
                        <span className="text-gray-500">📍 {job.location}</span>
                        <span className="text-green-600 font-bold">${job.pay}/hr</span>
                      </div>
                    </div>
                    <button
                      onClick={() => handleApply(job.id)}
                      className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
                    >
                      Apply
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default StudentDashboard;