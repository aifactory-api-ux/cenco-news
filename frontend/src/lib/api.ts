// src/lib/api.ts
// Axios instance for API calls with token handling
import axios from 'axios';

// Create axios instance with relative URL (no baseURL)
const api = axios.create({
  // No baseURL configuration so all calls use relative paths
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false, // no cookies-based auth
});

// Request interceptor to add Authorization header if token exists
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// Response interceptor to handle errors centrally if needed
api.interceptors.response.use(
  response => response,
  error => {
    // Optional: Could add global error handling/logging here
    return Promise.reject(error);
  }
);

export default api;
