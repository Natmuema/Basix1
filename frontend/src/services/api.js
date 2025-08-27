import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
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

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('basix_token');
      localStorage.removeItem('basix_refresh_token');
      localStorage.removeItem('basix_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login/', credentials),
  register: (userData) => api.post('/auth/register/', userData),
  me: () => api.get('/auth/me/'),
  updateProfile: (data) => api.put('/auth/update_profile/', data),
  changePassword: (data) => api.post('/auth/change_password/', data),
  logout: (refreshToken) => api.post('/auth/logout/', { refresh: refreshToken }),
  sendEmailVerification: (email) => api.post('/auth/send_email_verification/', { email }),
  verifyEmail: (token) => api.post('/auth/verify_email/', { token }),
  sendPhoneVerification: (phoneNumber) => api.post('/auth/send_phone_verification/', { phone_number: phoneNumber }),
  verifyPhone: (phoneNumber, code) => api.post('/auth/verify_phone/', { phone_number: phoneNumber, verification_code: code }),
  stats: () => api.get('/auth/stats/'),
  refresh: (refreshToken) => api.post('/token/refresh/', { refresh: refreshToken }),
  verify: (token) => api.post('/token/verify/', { token }),
};

// Users API
export const usersAPI = {
  getAll: (params) => api.get('/users/', { params }),
  getById: (id) => api.get(`/users/${id}/`),
  getProfile: (id) => api.get(`/users/${id}/profile/`),
  getCreators: () => api.get('/users/creators/'),
  getInvestors: () => api.get('/users/investors/'),
};

// Creator Profiles API
export const creatorProfilesAPI = {
  getAll: (params) => api.get('/creator-profiles/', { params }),
  getById: (id) => api.get(`/creator-profiles/${id}/`),
  create: (data) => api.post('/creator-profiles/', data),
  update: (id, data) => api.put(`/creator-profiles/${id}/`, data),
  delete: (id) => api.delete(`/creator-profiles/${id}/`),
  getTopCreators: () => api.get('/creator-profiles/top_creators/'),
};

// Investor Profiles API
export const investorProfilesAPI = {
  getAll: (params) => api.get('/investor-profiles/', { params }),
  getById: (id) => api.get(`/investor-profiles/${id}/`),
  create: (data) => api.post('/investor-profiles/', data),
  update: (id, data) => api.put(`/investor-profiles/${id}/`, data),
  delete: (id) => api.delete(`/investor-profiles/${id}/`),
  getTopInvestors: () => api.get('/investor-profiles/top_investors/'),
};

// JWT Token API
export const tokenAPI = {
  obtain: (credentials) => api.post('/token/', credentials),
  refresh: (refreshToken) => api.post('/token/refresh/', { refresh: refreshToken }),
  verify: (token) => api.post('/token/verify/', { token }),
};

export default api;