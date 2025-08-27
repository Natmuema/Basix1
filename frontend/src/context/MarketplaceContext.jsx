import React, { createContext, useContext, useState, useEffect } from 'react';
import { 
  creatorsService, 
  nftsService, 
  productsService, 
  utilitiesService 
} from '../services';

const MarketplaceContext = createContext(undefined);

export const useMarketplace = () => {
  const context = useContext(MarketplaceContext);
  if (context === undefined) {
    throw new Error('useMarketplace must be used within a MarketplaceProvider');
  }
  return context;
};

export const MarketplaceProvider = ({ children }) => {
  // State
  const [creators, setCreators] = useState([]);
  const [products, setProducts] = useState([]);
  const [nfts, setNfts] = useState([]);
  const [marketStats, setMarketStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  // Fetch creators
  const fetchCreators = async (page = 1) => {
    try {
      setLoading(true);
      const data = await creatorsService.getAll(page);
      setCreators(data.results || []);
      setTotalPages(Math.ceil(data.count / 20));
      setCurrentPage(page);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching creators:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch products with filters
  const fetchProducts = async (filters = {}) => {
    try {
      setLoading(true);
      const data = await productsService.getAll(filters);
      setProducts(data.results || []);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching products:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch NFTs with filters
  const fetchNFTs = async (filters = {}) => {
    try {
      setLoading(true);
      const data = await nftsService.getAll(filters);
      setNfts(data.results || []);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching NFTs:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch marketplace statistics
  const fetchMarketStats = async () => {
    try {
      const stats = await utilitiesService.getCurrentStats();
      setMarketStats(stats);
    } catch (err) {
      console.error('Error fetching market stats:', err);
    }
  };

  // Create a new product
  const createProduct = async (productData) => {
    try {
      setLoading(true);
      const product = await productsService.create(productData);
      await fetchProducts(); // Refresh products list
      return { success: true, data: product };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  // Create a new NFT
  const createNFT = async (nftData) => {
    try {
      setLoading(true);
      const nft = await nftsService.create(nftData);
      await fetchNFTs(); // Refresh NFTs list
      return { success: true, data: nft };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  // Contribute funding to an NFT
  const contributeFunding = async (nftId, amount) => {
    try {
      const result = await nftsService.contributeFunding(nftId, amount);
      
      // Update the NFT in local state
      setNfts(prevNfts => 
        prevNfts.map(nft => 
          nft.id === nftId 
            ? { ...nft, ...result }
            : nft
        )
      );
      
      return { success: true, data: result };
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    }
  };

  // Get NFT by ID
  const getNFTById = async (id) => {
    try {
      const nft = await nftsService.getById(id);
      return { success: true, data: nft };
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  // Get product by ID
  const getProductById = async (id) => {
    try {
      const product = await productsService.getById(id);
      return { success: true, data: product };
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  // Get creator by ID
  const getCreatorById = async (id) => {
    try {
      const creator = await creatorsService.getById(id);
      return { success: true, data: creator };
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  // Get top creators
  const getTopCreators = async (limit = 10) => {
    try {
      const data = await creatorsService.getTopCreators(limit);
      return { success: true, data };
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  // Get high impact NFTs
  const getHighImpactNFTs = async (minScore = 80) => {
    try {
      const data = await nftsService.getHighImpact(minScore);
      return { success: true, data };
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  // Check utility access
  const checkUtilityAccess = async (creatorId, nftId) => {
    try {
      const access = await utilitiesService.checkUtilityAccess(creatorId, nftId);
      return { success: true, data: access };
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchCreators();
    fetchProducts();
    fetchNFTs();
    fetchMarketStats();
  }, []);

  // Clear error after 5 seconds
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(null), 5000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  const value = {
    // State
    creators,
    products,
    nfts,
    marketStats,
    loading,
    error,
    currentPage,
    totalPages,
    
    // Methods
    fetchCreators,
    fetchProducts,
    fetchNFTs,
    fetchMarketStats,
    createProduct,
    createNFT,
    contributeFunding,
    getNFTById,
    getProductById,
    getCreatorById,
    getTopCreators,
    getHighImpactNFTs,
    checkUtilityAccess,
    setError
  };

  return (
    <MarketplaceContext.Provider value={value}>
      {children}
    </MarketplaceContext.Provider>
  );
};

export default MarketplaceContext;