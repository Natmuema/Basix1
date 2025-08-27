import React, { useState } from 'react';
import AssetCard from '../components/AssetCard';
import {assets} from '../constants'
import { Search, Filter, Grid, List, TrendingUp, Clock } from 'lucide-react';
import { div } from 'framer-motion/client';

const Assets = () => {
    const [viewMode, setViewMode] = useState('grid');
  const [sortBy, setSortBy] = useState('trending');
  const [filterType, setFilterType] = useState('all');

   const filteredAssets = assets.filter(asset => {
    if (filterType === 'all') return true;
    return asset.type.toLowerCase() === filterType.toLowerCase();
  });

  return (
    
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 " id='assets'>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">Assets</h1>
        <p className="text-xl bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">Discover and invest in AI-powered assets from creators worldwide</p>
      </div>

      {/* Filters and Search */}
      <div className=" bg-transparent rounded-2xl border border-transparent p-6 mb-8">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0 lg:space-x-6">
          {/* Search */}
          <div className="relative flex-1">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-white-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search assets, creators, or categories..."
              className="w-full pl-12 pr-4 py-3 border border-blue-800 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent "
            />
          </div>

          {/* Filters */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Filter className="w-4 h-4 text-blue-600" />
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="px-3 py-2 text-white bg-transparent border-blue-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              >
                <option value="all">All Types</option>
                <option value="digital">Digital</option>
                <option value="phygital">Phygital</option>
              </select>
            </div>

            <div className="flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-blue-600" />
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-3 py-2 border border-blue-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              >
                <option value="trending">Trending</option>
                <option value="price-low">Price: Low to High</option>
                <option value="price-high">Price: High to Low</option>
                <option value="recent">Recently Listed</option>
              </select>
            </div>

            <div className="flex items-center space-x-1 border border-blue-800 rounded-lg p-1">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 rounded ${viewMode === 'grid' ? 'bg-purple-100 text-cyan-600' : 'text-gray-600'}`}
              >
                <Grid className="w-4 h-4" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 rounded ${viewMode === 'list' ? 'bg-purple-100 text-cyan-600' : 'text-gray-600'}`}
              >
                <List className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Results Summary */}
      <div className="flex items-center justify-between mb-6">
        <p className="text-gray-600">
          <span className="font-semibold text-gray-900">{filteredAssets.length}</span> assets found
        </p>
        <div className="flex items-center space-x-2 text-sm text-gray-500">
          <Clock className="w-4 h-4" />
          <span>Updated 2 minutes ago</span>
        </div>
      </div>

      {/* Assets Grid */}
      <div className={
        viewMode === 'grid' 
          ? 'grid md:grid-cols-2 lg:grid-cols-3 gap-8' 
          : 'space-y-4'
      }>
        {filteredAssets.map((asset) => (
          <AssetCard key={asset.id} asset={asset} />
        ))}
      </div>

      {/* Load More */}
      <div className="text-center mt-12">
        <button className="px-8 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 rounded-xl hover:border-cyan-500 hover:shadow-lg transition-all duration-300 font-semibold">
          Load More Assets
        </button>
      </div>
    </div>

   
  )
}

export default Assets