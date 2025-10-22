import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { jobService } from '../services/api';

function ProviderDashboard() {
  const { user } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [showJobForm, setShowJobForm] = useState(false);
  const [newJob, setNewJob] = useState({
    title: '',
    description: '',
    location: '',
    pay: ''
  });

  useEffect(() => {
    loadProviderJobs();
  }, [user]);

  const loadProviderJobs = async () => {
    try {
      const response = await jobService.getProviderJobs(user.id);
      setJobs(response.data);
    } catch (error) {
      console.error('Error loading provider jobs:', error);
    }
  };

  const handleCreateJob = async (e) => {
    e.preventDefault();
    try {
      await jobService.createJob({
        ...newJob,
        provider_id: user.id
      });
      setNewJob({ title: '', description: '', location: '', pay: '' });
      setShowJobForm(false);
      loadProviderJobs();
      alert('Job created successfully!');
    } catch (error) {
      console.error('Error creating job:', error);
      alert('Error creating job. Please try again.');
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Provider Dashboard</h1>
          <button
            onClick={() => setShowJobForm(true)}
            className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Post New Job
          </button>
        </div>

        {/* Job Creation Form */}
        {showJobForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
              <h2 className="text-2xl font-bold mb-4">Post New Job</h2>
              <form onSubmit={handleCreateJob} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Job Title</label>
                  <input
                    type="text"
                    required
                    value={newJob.title}
                    onChange={(e) => setNewJob({...newJob, title: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Description</label>
                  <textarea
                    required
                    value={newJob.description}
                    onChange={(e) => setNewJob({...newJob, description: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg"
                    rows="3"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Location</label>
                  <input
                    type="text"
                    required
                    value={newJob.location}
                    onChange={(e) => setNewJob({...newJob, location: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Pay ($/hr)</label>
                  <input
                    type="number"
                    required
                    value={newJob.pay}
                    onChange={(e) => setNewJob({...newJob, pay: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg"
                  />
                </div>
                <div className="flex gap-4">
                  <button
                    type="submit"
                    className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600"
                  >
                    Create Job
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowJobForm(false)}
                    className="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Posted Jobs */}
        <div>
          <h2 className="text-2xl font-bold mb-4">Your Posted Jobs</h2>
          {jobs.length === 0 ? (
            <p className="text-gray-500">No jobs posted yet.</p>
          ) : (
            <div className="space-y-4">
              {jobs.map(job => (
                <div key={job.id} className="border rounded-lg p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="text-xl font-semibold">{job.title}</h3>
                      <p className="text-gray-600 mt-2">{job.description}</p>
                      <div className="flex items-center gap-4 mt-3">
                        <span className="text-gray-500">📍 {job.location}</span>
                        <span className="text-green-600 font-bold">${job.pay}/hr</span>
                        <span className={`px-3 py-1 rounded-full text-sm ${
                          job.status === 'available' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
                        }`}>
                          {job.status}
                        </span>
                      </div>
                      {job.assigned_student_id && (
                        <p className="text-sm text-gray-500 mt-2">
                          Assigned to student: {job.assigned_student_id}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProviderDashboard;