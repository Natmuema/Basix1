import api from './api';

export const productsService = {
  // Get all products with filters
  getAll: async (filters = {}) => {
    const queryParams = new URLSearchParams(filters).toString();
    return api.get(`/products/${queryParams ? `?${queryParams}` : ''}`);
  },

  // Get single product by ID
  getById: async (id) => {
    return api.get(`/products/${id}/`);
  },

  // Create new product
  create: async (productData) => {
    const formData = new FormData();
    
    // Handle file uploads
    Object.keys(productData).forEach(key => {
      if (key === 'image' || key === 'digital_file') {
        if (productData[key]) {
          formData.append(key, productData[key]);
        }
      } else {
        formData.append(key, productData[key]);
      }
    });

    const token = localStorage.getItem('basix_token');
    
    const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000/api'}/products/`, {
      method: 'POST',
      headers: {
        ...(token && { 'Authorization': `Bearer ${token}` })
      },
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to create product');
    }

    return response.json();
  },

  // Update product
  update: async (id, data) => {
    return api.patch(`/products/${id}/`, data);
  },

  // Get NFTs linked to product
  getProductNFTs: async (id) => {
    return api.get(`/products/${id}/nfts/`);
  },

  // Get product statistics
  getStatistics: async () => {
    return api.get('/products/statistics/');
  },

  // Get cultural heritage products
  getCulturalHeritage: async () => {
    return api.get('/products/cultural_heritage/');
  },

  // Get software products
  getSoftwareProducts: async () => {
    return api.get('/products/software_products/');
  }
};

export default productsService;