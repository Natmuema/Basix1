import axios from 'axios';

// Base API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('basix_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const errorMessage = error.response.data?.detail || 
                          error.response.data?.message || 
                          'An error occurred';
      
      // Handle 401 unauthorized
      if (error.response.status === 401) {
        localStorage.removeItem('basix_token');
        window.location.href = '/login';
      }
      
      throw new Error(errorMessage);
    } else if (error.request) {
      // Request was made but no response
      throw new Error('Network error. Please check your connection.');
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred');
    }
  }
);

export const api = {
  get: (endpoint) => axiosInstance.get(endpoint).then(res => res.data),
  post: (endpoint, data) => axiosInstance.post(endpoint, data).then(res => res.data),
  put: (endpoint, data) => axiosInstance.put(endpoint, data).then(res => res.data),
  patch: (endpoint, data) => axiosInstance.patch(endpoint, data).then(res => res.data),
  delete: (endpoint) => axiosInstance.delete(endpoint).then(res => res.data),
};

export default api;