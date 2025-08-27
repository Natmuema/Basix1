import React, { useState, useEffect } from 'react';
import AssetCardUpdated from '../components/AssetCardUpdated';
import { useMarketplace } from '../context/MarketplaceContext';
import { Search, Filter, Grid, List, TrendingUp, Clock } from 'lucide-react';

const AssetsUpdated = () => {
  const [viewMode, setViewMode] = useState('grid');
  const [sortBy, setSortBy] = useState('trending');
  const [filterType, setFilterType] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [localNFTs, setLocalNFTs] = useState([]);

  const { nfts, loading, error, fetchNFTs } = useMarketplace();

  useEffect(() => {
    // Apply filters when NFTs or filter criteria change
    let filtered = [...nfts];

    // Filter by type
    if (filterType !== 'all') {
      filtered = filtered.filter(nft => 
        nft.product_type?.toLowerCase() === filterType.toLowerCase()
      );
    }

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(nft =>
        nft.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        nft.product_category?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        nft.token_id?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Sort
    switch (sortBy) {
      case 'trending':
        filtered.sort((a, b) => (b.impact_score || 0) - (a.impact_score || 0));
        break;
      case 'recent':
        filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        break;
      case 'funded':
        filtered.sort((a, b) => (b.funding_percentage || 0) - (a.funding_percentage || 0));
        break;
      default:
        break;
    }

    setLocalNFTs(filtered);
  }, [nfts, filterType, searchTerm, sortBy]);

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const refreshData = () => {
    fetchNFTs();
  };

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-red-500/20 border border-red-500 rounded-lg p-4 text-red-400">
          Error loading assets: {error}
          <button 
            onClick={refreshData}
            className="ml-4 text-sm underline hover:no-underline"
          >
            Try again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8" id='assets'>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">Assets</h1>
        <p className="text-xl bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
          Discover and invest in AI-powered assets from creators worldwide
        </p>
      </div>

      {/* Stats Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-4 border border-gray-700">
          <div className="text-2xl font-bold text-white">{nfts.length}</div>
          <div className="text-sm text-gray-400">Total Assets</div>
        </div>
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-4 border border-gray-700">
          <div className="text-2xl font-bold text-green-400">
            {nfts.filter(n => n.is_funded).length}
          </div>
          <div className="text-sm text-gray-400">Funded</div>
        </div>
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-4 border border-gray-700">
          <div className="text-2xl font-bold text-blue-400">
            ${nfts.reduce((sum, n) => sum + (n.current_funding || 0), 0).toLocaleString()}
          </div>
          <div className="text-sm text-gray-400">Total Funding</div>
        </div>
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-4 border border-gray-700">
          <div className="text-2xl font-bold text-purple-400">
            {nfts.filter(n => n.impact_score >= 80).length}
          </div>
          <div className="text-sm text-gray-400">High Impact</div>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="bg-transparent rounded-2xl border border-transparent p-6 mb-8">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0 lg:space-x-6">
          {/* Search */}
          <div className="relative flex-1">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search assets, creators, or categories..."
              value={searchTerm}
              onChange={handleSearch}
              className="w-full pl-12 pr-4 py-3 bg-gray-800/50 border border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white"
            />
          </div>

          {/* Filters */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Filter className="w-4 h-4 text-blue-400" />
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="px-3 py-2 text-white bg-gray-800/50 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              >
                <option value="all">All Types</option>
                <option value="ArtCraft">Art & Craft</option>
                <option value="Music">Music</option>
                <option value="Fashion">Fashion</option>
                <option value="Tourism">Tourism</option>
                <option value="Heritage">Heritage</option>
                <option value="Software">Software</option>
              </select>
            </div>

            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 text-white bg-gray-800/50 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            >
              <option value="trending">Trending</option>
              <option value="recent">Most Recent</option>
              <option value="funded">Most Funded</option>
            </select>

            <div className="flex items-center space-x-1 bg-gray-800/50 rounded-lg p-1">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded ${viewMode === 'grid' ? 'bg-blue-500 text-white' : 'text-gray-400 hover:text-white'}`}
              >
                <Grid className="w-4 h-4" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded ${viewMode === 'list' ? 'bg-blue-500 text-white' : 'text-gray-400 hover:text-white'}`}
              >
                <List className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="flex justify-center items-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      )}

      {/* Assets Grid/List */}
      {!loading && localNFTs.length > 0 && (
        <div className={viewMode === 'grid' 
          ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" 
          : "space-y-4"
        }>
          {localNFTs.map((nft) => (
            <AssetCardUpdated key={nft.id} nft={nft} />
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && localNFTs.length === 0 && (
        <div className="text-center py-20">
          <div className="text-gray-400 text-lg">
            {searchTerm || filterType !== 'all' 
              ? 'No assets found matching your criteria' 
              : 'No assets available yet'}
          </div>
          {(searchTerm || filterType !== 'all') && (
            <button
              onClick={() => {
                setSearchTerm('');
                setFilterType('all');
              }}
              className="mt-4 text-blue-400 hover:text-blue-300 underline"
            >
              Clear filters
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default AssetsUpdated;