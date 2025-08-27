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
  login: (credentials) => api.post('/token/', credentials),
  refresh: (refreshToken) => api.post('/token/refresh/', { refresh: refreshToken }),
  verify: (token) => api.post('/token/verify/', { token }),
  logout: (refreshToken) => api.post('/token/blacklist/', { refresh: refreshToken }),
};

// Creators API
export const creatorsAPI = {
  getAll: (params) => api.get('/creators/', { params }),
  getById: (id) => api.get(`/creators/${id}/`),
  create: (data) => api.post('/creators/', data),
  update: (id, data) => api.put(`/creators/${id}/`, data),
  delete: (id) => api.delete(`/creators/${id}/`),
  getStats: (id) => api.get(`/creators/${id}/stats/`),
  getProducts: (id) => api.get(`/creators/${id}/products/`),
  getOwnedNFTs: (id) => api.get(`/creators/${id}/owned_nfts/`),
  getTopCreators: () => api.get('/creators/top_creators/'),
};

// Products API
export const productsAPI = {
  getAll: (params) => api.get('/products/', { params }),
  getById: (id) => api.get(`/products/${id}/`),
  create: (data) => api.post('/products/', data),
  update: (id, data) => api.put(`/products/${id}/`, data),
  delete: (id) => api.delete(`/products/${id}/`),
  getNFT: (id) => api.get(`/products/${id}/nft/`),
};

// NFTs API
export const nftsAPI = {
  getAll: (params) => api.get('/nfts/', { params }),
  getById: (id) => api.get(`/nfts/${id}/`),
  create: (data) => api.post('/nfts/', data),
  update: (id, data) => api.put(`/nfts/${id}/`, data),
  delete: (id) => api.delete(`/nfts/${id}/`),
  appendHistory: (id, data) => api.post(`/nfts/${id}/append_history/`, data),
  calculateImpactScore: (id, data) => api.post(`/nfts/${id}/calculate_impact_score/`, data),
  transferOwnership: (id, data) => api.post(`/nfts/${id}/transfer_ownership/`, data),
  isCreator: (id) => api.get(`/nfts/${id}/is_creator/`),
};

// Utilities API
export const utilitiesAPI = {
  getAll: (params) => api.get('/utilities/', { params }),
  getById: (id) => api.get(`/utilities/${id}/`),
  create: (data) => api.post('/utilities/', data),
  update: (id, data) => api.put(`/utilities/${id}/`, data),
  delete: (id) => api.delete(`/utilities/${id}/`),
};

// Ownership API
export const ownershipAPI = {
  getAll: (params) => api.get('/ownerships/', { params }),
  getById: (id) => api.get(`/ownerships/${id}/`),
  create: (data) => api.post('/ownerships/', data),
  update: (id, data) => api.put(`/ownerships/${id}/`, data),
  delete: (id) => api.delete(`/ownerships/${id}/`),
};

// Governance API
export const governanceAPI = {
  getAll: (params) => api.get('/governance-votes/', { params }),
  getById: (id) => api.get(`/governance-votes/${id}/`),
  create: (data) => api.post('/governance-votes/', data),
  update: (id, data) => api.put(`/governance-votes/${id}/`, data),
  delete: (id) => api.delete(`/governance-votes/${id}/`),
};

// Impact Scores API
export const impactScoresAPI = {
  getAll: (params) => api.get('/impact-scores/', { params }),
  getById: (id) => api.get(`/impact-scores/${id}/`),
  create: (data) => api.post('/impact-scores/', data),
  update: (id, data) => api.put(`/impact-scores/${id}/`, data),
  delete: (id) => api.delete(`/impact-scores/${id}/`),
  getTopImpact: () => api.get('/impact-scores/top_impact/'),
};

// Funding Thresholds API
export const fundingThresholdsAPI = {
  getAll: (params) => api.get('/funding-thresholds/', { params }),
  getById: (id) => api.get(`/funding-thresholds/${id}/`),
  create: (data) => api.post('/funding-thresholds/', data),
  update: (id, data) => api.put(`/funding-thresholds/${id}/`, data),
  delete: (id) => api.delete(`/funding-thresholds/${id}/`),
  checkThreshold: (id, data) => api.post(`/funding-thresholds/${id}/check_threshold/`, data),
};

// Marketplace Stats API
export const statsAPI = {
  getOverview: () => api.get('/stats/overview/'),
  getProductTypesDistribution: () => api.get('/stats/product_types_distribution/'),
  getUtilityTypesDistribution: () => api.get('/stats/utility_types_distribution/'),
};

// Marketplace Config API
export const configAPI = {
  getAll: (params) => api.get('/marketplace-configs/', { params }),
  getById: (id) => api.get(`/marketplace-configs/${id}/`),
  create: (data) => api.post('/marketplace-configs/', data),
  update: (id, data) => api.put(`/marketplace-configs/${id}/`, data),
  delete: (id) => api.delete(`/marketplace-configs/${id}/`),
  getConfig: (params) => api.get('/marketplace-configs/get_config/', { params }),
};

export default api;