# Frontend Integration Guide

This guide shows how to integrate the Django marketplace backend with your React frontend.

## API Service Setup

Create an API service to handle all backend communication:

```javascript
// services/api.js
const API_BASE_URL = 'http://localhost:8000/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('token');
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem('token', token);
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };
    
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    
    return headers;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: this.getHeaders(),
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Creators
  async getCreators(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/creators/${queryString ? `?${queryString}` : ''}`);
  }

  async getCreator(id) {
    return this.request(`/creators/${id}/`);
  }

  async createCreator(data) {
    return this.request('/creators/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async updateCreator(id, data) {
    return this.request(`/creators/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // Products
  async getProducts(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/products/${queryString ? `?${queryString}` : ''}`);
  }

  async getProduct(id) {
    return this.request(`/products/${id}/`);
  }

  async createProduct(data) {
    return this.request('/products/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // NFTs
  async getNFTs(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/nfts/${queryString ? `?${queryString}` : ''}`);
  }

  async getNFT(id) {
    return this.request(`/nfts/${id}/`);
  }

  async createNFT(data) {
    return this.request('/nfts/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async mintNFT(id, data) {
    return this.request(`/nfts/${id}/mint/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async listNFTForSale(id) {
    return this.request(`/nfts/${id}/list_for_sale/`, {
      method: 'POST',
    });
  }

  async transferOwnership(id, data) {
    return this.request(`/nfts/${id}/transfer_ownership/`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Utilities
  async getUtilities(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/utilities/${queryString ? `?${queryString}` : ''}`);
  }

  async createUtility(data) {
    return this.request('/utilities/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Ownership
  async getOwnerships(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/ownerships/${queryString ? `?${queryString}` : ''}`);
  }

  async createOwnership(data) {
    return this.request('/ownerships/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Impact Scores
  async getImpactScores(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/impact-scores/${queryString ? `?${queryString}` : ''}`);
  }

  async createImpactScore(data) {
    return this.request('/impact-scores/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Marketplace Stats
  async getMarketplaceStats() {
    return this.request('/marketplace-stats/current/');
  }

  async getAnalytics() {
    return this.request('/marketplace-stats/analytics/');
  }
}

export const apiService = new ApiService();
```

## React Components

### Creator Profile Component

```jsx
// components/CreatorProfile.jsx
import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const CreatorProfile = ({ creatorId }) => {
  const [creator, setCreator] = useState(null);
  const [nfts, setNfts] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCreatorData = async () => {
      try {
        setLoading(true);
        const [creatorData, nftsData, productsData] = await Promise.all([
          apiService.getCreator(creatorId),
          apiService.getCreators({ creator: creatorId }),
          apiService.getProducts({ creator: creatorId })
        ]);
        
        setCreator(creatorData);
        setNfts(nftsData.results || []);
        setProducts(productsData.results || []);
      } catch (error) {
        console.error('Error fetching creator data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCreatorData();
  }, [creatorId]);

  if (loading) {
    return <div>Loading creator profile...</div>;
  }

  if (!creator) {
    return <div>Creator not found</div>;
  }

  return (
    <div className="creator-profile">
      <div className="creator-header">
        <img 
          src={creator.profile_image || '/default-avatar.png'} 
          alt={creator.user.username}
          className="creator-avatar"
        />
        <div className="creator-info">
          <h2>{creator.user.username}</h2>
          <p className="wallet-address">{creator.wallet_address}</p>
          <div className="reputation-score">
            Reputation: {creator.reputation_score}/100
          </div>
          <div className="skills">
            {creator.skills.map(skill => (
              <span key={skill} className="skill-tag">{skill}</span>
            ))}
          </div>
        </div>
      </div>

      <div className="creator-content">
        <div className="products-section">
          <h3>Products ({products.length})</h3>
          <div className="products-grid">
            {products.map(product => (
              <div key={product.id} className="product-card">
                <h4>{product.name}</h4>
                <p>{product.description}</p>
                <span className="product-type">{product.product_type}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="nfts-section">
          <h3>NFTs ({nfts.length})</h3>
          <div className="nfts-grid">
            {nfts.map(nft => (
              <div key={nft.id} className="nft-card">
                <h4>{nft.token_id}</h4>
                <p>Product: {nft.product.name}</p>
                <div className="nft-status">
                  {nft.is_minted && <span className="minted">Minted</span>}
                  {nft.is_listed && <span className="listed">Listed</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreatorProfile;
```

### NFT Marketplace Component

```jsx
// components/NFTMarketplace.jsx
import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const NFTMarketplace = () => {
  const [nfts, setNfts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    is_listed: true,
    ordering: '-created_at'
  });

  useEffect(() => {
    fetchNFTs();
  }, [filters]);

  const fetchNFTs = async () => {
    try {
      setLoading(true);
      const data = await apiService.getNFTs(filters);
      setNfts(data.results || []);
    } catch (error) {
      console.error('Error fetching NFTs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleMintNFT = async (nftId) => {
    try {
      await apiService.mintNFT(nftId, {
        blockchain: 'Ethereum',
        metadata_uri: 'https://ipfs.io/metadata.json'
      });
      fetchNFTs(); // Refresh the list
    } catch (error) {
      console.error('Error minting NFT:', error);
    }
  };

  const handleListForSale = async (nftId) => {
    try {
      await apiService.listNFTForSale(nftId);
      fetchNFTs(); // Refresh the list
    } catch (error) {
      console.error('Error listing NFT:', error);
    }
  };

  if (loading) {
    return <div>Loading marketplace...</div>;
  }

  return (
    <div className="nft-marketplace">
      <div className="marketplace-header">
        <h1>NFT Marketplace</h1>
        <div className="filters">
          <select 
            value={filters.is_listed} 
            onChange={(e) => setFilters({...filters, is_listed: e.target.value})}
          >
            <option value={true}>Listed Only</option>
            <option value={false}>All NFTs</option>
          </select>
        </div>
      </div>

      <div className="nfts-grid">
        {nfts.map(nft => (
          <div key={nft.id} className="nft-card">
            <div className="nft-image">
              {/* Add NFT image here */}
            </div>
            <div className="nft-info">
              <h3>{nft.token_id}</h3>
              <p className="product-name">{nft.product.name}</p>
              <p className="creator">by {nft.creator.user.username}</p>
              
              <div className="nft-utilities">
                {nft.utilities.map(utility => (
                  <span key={utility.id} className="utility-tag">
                    {utility.utility_type}
                  </span>
                ))}
              </div>

              <div className="nft-ownership">
                {nft.ownerships.map(ownership => (
                  <div key={ownership.id} className="ownership-info">
                    {ownership.creator.user.username}: {ownership.percentage}%
                  </div>
                ))}
              </div>

              <div className="nft-actions">
                {!nft.is_minted && (
                  <button 
                    onClick={() => handleMintNFT(nft.id)}
                    className="btn-mint"
                  >
                    Mint NFT
                  </button>
                )}
                
                {nft.is_minted && !nft.is_listed && (
                  <button 
                    onClick={() => handleListForSale(nft.id)}
                    className="btn-list"
                  >
                    List for Sale
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NFTMarketplace;
```

### Product Creation Form

```jsx
// components/ProductForm.jsx
import React, { useState } from 'react';
import { apiService } from '../services/api';

const ProductForm = ({ onProductCreated }) => {
  const [formData, setFormData] = useState({
    name: '',
    product_type: 'ArtCraft',
    category: '',
    description: '',
    is_physical: false,
    is_digital: false,
    is_redeemable: false,
    has_digital_scan: false,
    is_license_based: false,
    creator_id: 1 // This should come from user context
  });

  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const product = await apiService.createProduct(formData);
      onProductCreated(product);
      setFormData({
        name: '',
        product_type: 'ArtCraft',
        category: '',
        description: '',
        is_physical: false,
        is_digital: false,
        is_redeemable: false,
        has_digital_scan: false,
        is_license_based: false,
        creator_id: 1
      });
    } catch (error) {
      console.error('Error creating product:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="product-form">
      <h2>Create New Product</h2>
      
      <div className="form-group">
        <label htmlFor="name">Product Name</label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="product_type">Product Type</label>
        <select
          id="product_type"
          name="product_type"
          value={formData.product_type}
          onChange={handleChange}
        >
          <option value="ArtCraft">Art & Craft</option>
          <option value="Music">Music</option>
          <option value="Fashion">Fashion</option>
          <option value="Tourism">Tourism</option>
          <option value="Heritage">Heritage</option>
          <option value="Software">Software</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="category">Category</label>
        <input
          type="text"
          id="category"
          name="category"
          value={formData.category}
          onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            name="is_physical"
            checked={formData.is_physical}
            onChange={handleChange}
          />
          Physical Product
        </label>
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            name="is_digital"
            checked={formData.is_digital}
            onChange={handleChange}
          />
          Digital Product
        </label>
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            name="is_redeemable"
            checked={formData.is_redeemable}
            onChange={handleChange}
          />
          Redeemable
        </label>
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            name="has_digital_scan"
            checked={formData.has_digital_scan}
            onChange={handleChange}
          />
          Has Digital Scan
        </label>
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            name="is_license_based"
            checked={formData.is_license_based}
            onChange={handleChange}
          />
          License Based
        </label>
      </div>

      <button type="submit" disabled={loading}>
        {loading ? 'Creating...' : 'Create Product'}
      </button>
    </form>
  );
};

export default ProductForm;
```

### Dashboard Component

```jsx
// components/Dashboard.jsx
import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [statsData, analyticsData] = await Promise.all([
        apiService.getMarketplaceStats(),
        apiService.getAnalytics()
      ]);
      
      setStats(statsData);
      setAnalytics(analyticsData);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Marketplace Dashboard</h1>
      
      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total NFTs</h3>
            <p className="stat-number">{stats.total_nfts}</p>
          </div>
          <div className="stat-card">
            <h3>Total Creators</h3>
            <p className="stat-number">{stats.total_creators}</p>
          </div>
          <div className="stat-card">
            <h3>Active Listings</h3>
            <p className="stat-number">{stats.active_listings}</p>
          </div>
          <div className="stat-card">
            <h3>Total Volume</h3>
            <p className="stat-number">${stats.total_volume}</p>
          </div>
        </div>
      )}

      {analytics && (
        <div className="analytics-section">
          <h2>Analytics</h2>
          
          <div className="analytics-grid">
            <div className="analytics-card">
              <h3>Products by Type</h3>
              <div className="chart">
                {analytics.products_by_type.map(item => (
                  <div key={item.product_type} className="chart-item">
                    <span>{item.product_type}</span>
                    <span>{item.count}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="analytics-card">
              <h3>NFTs by Blockchain</h3>
              <div className="chart">
                {analytics.nfts_by_blockchain.map(item => (
                  <div key={item.blockchain} className="chart-item">
                    <span>{item.blockchain}</span>
                    <span>{item.count}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="analytics-card">
              <h3>Recent Activity</h3>
              <div className="activity-list">
                {analytics.recent_activity.map(activity => (
                  <div key={activity.id} className="activity-item">
                    <span className="activity-type">{activity.action_type}</span>
                    <span className="activity-nft">{activity.nft}</span>
                    <span className="activity-time">
                      {new Date(activity.timestamp).toLocaleDateString()}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
```

## CSS Styling

```css
/* styles/marketplace.css */
.creator-profile {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.creator-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.creator-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

.creator-info h2 {
  margin: 0 0 10px 0;
  color: #333;
}

.wallet-address {
  font-family: monospace;
  color: #666;
  margin-bottom: 10px;
}

.reputation-score {
  font-weight: bold;
  color: #007bff;
  margin-bottom: 10px;
}

.skills {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.skill-tag {
  background: #e9ecef;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  color: #495057;
}

.nft-marketplace {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.marketplace-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.nfts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.nft-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nft-info h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.product-name {
  color: #666;
  margin-bottom: 5px;
}

.creator {
  color: #007bff;
  font-size: 14px;
  margin-bottom: 10px;
}

.utility-tag {
  background: #28a745;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
  margin-right: 5px;
}

.nft-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.btn-mint, .btn-list {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-mint {
  background: #007bff;
  color: white;
}

.btn-list {
  background: #28a745;
  color: white;
}

.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-number {
  font-size: 2em;
  font-weight: bold;
  color: #007bff;
  margin: 10px 0 0 0;
}

.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.analytics-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.chart-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.activity-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.activity-type {
  background: #007bff;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
}

.product-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-group textarea {
  height: 100px;
  resize: vertical;
}

.form-group input[type="checkbox"] {
  width: auto;
  margin-right: 8px;
}

button {
  background: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
```

## Integration Steps

1. **Install Dependencies**
```bash
npm install axios
```

2. **Set up API Service**
Copy the `api.js` service file to your project.

3. **Create Components**
Copy the React components to your project structure.

4. **Add CSS**
Include the CSS styles in your project.

5. **Update App.js**
```jsx
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import NFTMarketplace from './components/NFTMarketplace';
import CreatorProfile from './components/CreatorProfile';
import ProductForm from './components/ProductForm';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/marketplace" element={<NFTMarketplace />} />
          <Route path="/creator/:id" element={<CreatorProfile />} />
          <Route path="/create-product" element={<ProductForm />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
```

6. **Start Development**
```bash
npm start
```

Make sure your Django backend is running on `http://localhost:8000` before testing the frontend integration.