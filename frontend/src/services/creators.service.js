import api from './api';

export const creatorsService = {
  // Get all creators with pagination
  getAll: async (page = 1, pageSize = 20) => {
    return api.get(`/creators/?page=${page}&page_size=${pageSize}`);
  },

  // Get single creator by ID
  getById: async (id) => {
    return api.get(`/creators/${id}/`);
  },

  // Create new creator profile
  create: async (creatorData) => {
    return api.post('/creators/', creatorData);
  },

  // Update creator profile
  update: async (id, data) => {
    return api.patch(`/creators/${id}/`, data);
  },

  // Get creator's NFTs
  getCreatorNFTs: async (id) => {
    return api.get(`/creators/${id}/nfts/`);
  },

  // Get NFTs created by creator (primary ownership)
  getCreatedNFTs: async (id) => {
    return api.get(`/creators/${id}/created_nfts/`);
  },

  // Update creator reputation
  updateReputation: async (id, actionType, value = 1) => {
    return api.post(`/creators/${id}/update_reputation/`, {
      action_type: actionType,
      value
    });
  },

  // Get top creators by reputation
  getTopCreators: async (limit = 10) => {
    return api.get(`/creators/top_creators/?limit=${limit}`);
  },

  // Get verified creators only
  getVerified: async () => {
    return api.get('/creators/verified/');
  }
};

export default creatorsService;