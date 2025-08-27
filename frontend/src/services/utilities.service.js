import api from './api';

export const utilitiesService = {
  // Get transactions with filters
  getTransactions: async (filters = {}) => {
    const queryParams = new URLSearchParams(filters).toString();
    return api.get(`/transactions/${queryParams ? `?${queryParams}` : ''}`);
  },

  // Create transaction
  createTransaction: async (transactionData) => {
    return api.post('/transactions/', transactionData);
  },

  // Get impact metrics
  getImpactMetrics: async (filters = {}) => {
    const queryParams = new URLSearchParams(filters).toString();
    return api.get(`/impact-metrics/${queryParams ? `?${queryParams}` : ''}`);
  },

  // Get latest metrics by NFT
  getLatestMetricsByNFT: async (nftId = null) => {
    const endpoint = nftId 
      ? `/impact-metrics/latest_by_nft/?nft_id=${nftId}`
      : '/impact-metrics/latest_by_nft/';
    return api.get(endpoint);
  },

  // Get marketplace statistics
  getMarketplaceStats: async (filters = {}) => {
    const queryParams = new URLSearchParams(filters).toString();
    return api.get(`/marketplace-stats/${queryParams ? `?${queryParams}` : ''}`);
  },

  // Get current marketplace stats
  getCurrentStats: async () => {
    return api.get('/marketplace-stats/current/');
  },

  // Generate marketplace stats for a date
  generateStats: async (date = null) => {
    return api.post('/marketplace-stats/generate/', { date });
  },

  // Calculate impact score for NFT
  calculateImpactScore: async (nftId) => {
    return api.post('/impact-score/', { nft_id: nftId });
  },

  // Check utility access for creator
  checkUtilityAccess: async (creatorId, nftId) => {
    return api.get(`/utility-access/?creator_id=${creatorId}&nft_id=${nftId}`);
  }
};

export default utilitiesService;