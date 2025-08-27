import api from './api';

export const nftsService = {
  // Get all NFTs with filters
  getAll: async (filters = {}) => {
    const queryParams = new URLSearchParams(filters).toString();
    return api.get(`/nfts/${queryParams ? `?${queryParams}` : ''}`);
  },

  // Get single NFT by ID
  getById: async (id) => {
    return api.get(`/nfts/${id}/`);
  },

  // Create new NFT
  create: async (nftData) => {
    return api.post('/nfts/', nftData);
  },

  // Update NFT
  update: async (id, data) => {
    return api.patch(`/nfts/${id}/`, data);
  },

  // Contribute funding to NFT
  contributeFunding: async (id, amount) => {
    return api.post(`/nfts/${id}/contribute_funding/`, { amount });
  },

  // Append to NFT history
  appendHistory: async (id, action, details = {}) => {
    return api.post(`/nfts/${id}/append_history/`, { action, details });
  },

  // Get ownership distribution
  getOwnershipDistribution: async (id) => {
    return api.get(`/nfts/${id}/ownership_distribution/`);
  },

  // Add or update ownership
  addOwnership: async (id, creatorId, percentage, transferRule = '', decayRule = '') => {
    return api.post(`/nfts/${id}/add_ownership/`, {
      creator_id: creatorId,
      percentage,
      transfer_rule: transferRule,
      decay_rule: decayRule
    });
  },

  // Add utility to NFT
  addUtility: async (id, utilityType, description = '', ownershipRequirement = 0, condition = '') => {
    return api.post(`/nfts/${id}/add_utility/`, {
      utility_type: utilityType,
      description,
      ownership_requirement: ownershipRequirement,
      condition
    });
  },

  // Get accessible utilities for a creator
  getAccessibleUtilities: async (nftId, creatorId) => {
    return api.get(`/nfts/${nftId}/accessible_utilities/?creator_id=${creatorId}`);
  },

  // Add governance vote
  addGovernanceVote: async (id, creatorId, weight, isReputationWeighted = true) => {
    return api.post(`/nfts/${id}/add_governance_vote/`, {
      creator_id: creatorId,
      weight,
      is_reputation_weighted: isReputationWeighted
    });
  },

  // Record impact metrics
  recordMetrics: async (id) => {
    return api.post(`/nfts/${id}/record_metrics/`);
  },

  // Get top funded NFTs
  getTopFunded: async (limit = 10) => {
    return api.get(`/nfts/top_funded/?limit=${limit}`);
  },

  // Get high impact NFTs
  getHighImpact: async (minScore = 80) => {
    return api.get(`/nfts/high_impact/?min_score=${minScore}`);
  }
};

export default nftsService;