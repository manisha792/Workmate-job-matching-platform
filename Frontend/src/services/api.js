import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const authService = {
  login: (email, password, type) => 
    api.post('/login', { email, password, type }),
  
  register: (userData) => 
    api.post('/register', userData),
};

export const jobService = {
  getJobs: () => api.get('/jobs'),
  getProviderJobs: (providerId) => api.get(`/jobs/provider/${providerId}`),
  createJob: (jobData) => api.post('/jobs', jobData),
  updateJob: (jobId, jobData) => api.put(`/jobs/${jobId}`, jobData),
  deleteJob: (jobId) => api.delete(`/jobs/${jobId}`),
  applyJob: (jobId, studentId) => api.post(`/jobs/${jobId}/apply`, { student_id: studentId }),
  getSuggestedJobs: (studentId) => api.get(`/jobs/suggested/${studentId}`),
  searchJobs: (query) => api.get(`/jobs/search?q=${query}`),
  sortJobs: (sortBy, order) => api.get(`/jobs/sort?by=${sortBy}&order=${order}`),
};

export const studentService = {
  getStudent: (studentId) => api.get(`/students/${studentId}`),
  rateStudent: (studentId, rating) => api.post(`/students/${studentId}/rate`, { rating }),
};

export const providerService = {
  getProvider: (providerId) => api.get(`/providers/${providerId}`),
};

export const assignmentService = {
  getOptimalAssignment: (studentIds, jobIds) => 
    api.post('/assignments/optimal', { student_ids: studentIds, job_ids: jobIds }),
};

export default api;