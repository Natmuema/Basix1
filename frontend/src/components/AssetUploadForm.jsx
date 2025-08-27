import React, { useState } from 'react';
import { X, Upload, Image, Package, Globe, Zap } from 'lucide-react';

const AssetUploadForm = ({ onClose }) => {
  const [isOpen, setIsOpen] = useState(true);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'art',
    assetType: 'digital',
    price: '',
    royaltyRate: '10',
    supply: '1',
    utility: [],
    collaborators: ''
  });

  const [dragOver, setDragOver] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const categories = [
    { id: 'art', label: 'Digital Art' },
    { id: 'music', label: 'Music' },
    { id: 'collectibles', label: 'Collectibles' },
    { id: 'crafts', label: 'Handcrafts' },
    { id: 'experiences', label: 'Experiences' },
    { id: 'other', label: 'Other' }
  ];

  const utilityOptions = [
    'Revenue sharing',
    'Exclusive access',
    'Physical redemption',
    'Virtual experiences',
    'Voting rights',
    'Community membership'
  ];

  const handleClose = () => {
    setIsOpen(false);
    if (onClose) {
      onClose(); // Let parent component handle navigation
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // Simulate minting process
      await new Promise(resolve => setTimeout(resolve, 2000));
      alert('Asset minting initiated! This would trigger blockchain transaction and MeTTa knowledge graph update.');
      handleClose();
    } catch (error) {
      console.error('Minting failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUtilityChange = (utility) => {
    setFormData(prev => ({
      ...prev,
      utility: prev.utility.includes(utility)
        ? prev.utility.filter(u => u !== utility)
        : [...prev.utility, utility]
    }));
  };

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      handleClose();
    }
  };

  if (!isOpen) {
    return (
      <div className="fixed bottom-8 right-8 z-50" id='open-asset-upload-form'>
        <button
          onClick={() => setIsOpen(true)}
          className="bg-gradient-to-r font-bold  from-cyan-400 to-blue-400 text-white p-4 rounded-full shadow-2xl hover:shadow-purple-500/25 transition-all duration-300 hover:scale-110"
        >
          <Package className="w-6 h-6" />
        </button>
      </div>
    );
  }

  return (
    <div 
      className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" 
      id='asset-upload-form'
      onClick={handleOverlayClick}
    >
      <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-100 bg-gradient-to-r from-purple-50 to-blue-50">
          <div>
            <h2 className="text-2xl font-bold bg-gradient-to-r  from-cyan-400 to-blue-400 bg-clip-text text-transparent">
              Create New Asset
            </h2>
            <p className="text-gray-600 mt-1">Mint your digital or phygital asset with AI-powered features</p>
          </div>
          <button
            onClick={handleClose}
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-white rounded-lg transition-all duration-200"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="p-6 space-y-8">
          {/* Asset Type Selection */}
          <div>
            <label className="block text-sm font-semibold text-gray-900 mb-3">Asset Type</label>
            <div className="grid grid-cols-2 gap-4">
              <button
                type="button"
                onClick={() => setFormData(prev => ({ ...prev, assetType: 'digital' }))}
                className={`p-4 border-2 rounded-xl transition-all duration-200 group ${
                  formData.assetType === 'digital'
                    ? 'border-blue-500 bg-blue-50 shadow-lg shadow-blue-100'
                    : 'border-gray-200 hover:border-blue-300 hover:bg-blue-50/50'
                }`}
              >
                <Globe className={`w-6 h-6 mx-auto mb-2 transition-colors duration-200 ${
                  formData.assetType === 'digital' ? 'text-blue-600' : 'text-gray-500 group-hover:text-blue-500'
                }`} />
                <div className="font-semibold text-gray-900">Digital</div>
                <div className="text-sm text-gray-600">Pure digital asset (NFT)</div>
              </button>
              
              <button
                type="button"
                onClick={() => setFormData(prev => ({ ...prev, assetType: 'phygital' }))}
                className={`p-4 border-2 rounded-xl transition-all duration-200 group ${
                  formData.assetType === 'phygital'
                    ? 'border-purple-500 bg-purple-50 shadow-lg shadow-purple-100'
                    : 'border-gray-200 hover:border-purple-300 hover:bg-purple-50/50'
                }`}
              >
                <Package className={`w-6 h-6 mx-auto mb-2 transition-colors duration-200 ${
                  formData.assetType === 'phygital' ? 'text-purple-600' : 'text-gray-500 group-hover:text-purple-500'
                }`} />
                <div className="font-semibold text-gray-900">Phygital</div>
                <div className="text-sm text-gray-600">Physical + Digital hybrid</div>
              </button>
            </div>
          </div>

          {/* File Upload */}
          <div>
            <label className="block text-sm font-semibold text-gray-900 mb-3">Asset File</label>
            <div
              className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 ${
                dragOver 
                  ? 'border-cyan-400 bg-purple-50 scale-[1.02]' 
                  : 'border-gray-300 hover:border-cyan-300 hover:bg-purple-50/30'
              }`}
              onDragOver={(e) => {
                e.preventDefault();
                setDragOver(true);
              }}
              onDragLeave={() => setDragOver(false)}
              onDrop={(e) => {
                e.preventDefault();
                setDragOver(false);
                // Handle file drop
                console.log('File dropped:', e.dataTransfer.files);
              }}
            >
              <Upload className={`w-8 h-8 mx-auto mb-4 transition-colors duration-200 ${
                dragOver ? 'text-purple-600' : 'text-gray-400'
              }`} />
              <p className="text-gray-600 mb-2">Drag and drop your file here, or click to browse</p>
              <p className="text-sm text-gray-500 mb-4">Supports images, videos, audio, and documents</p>
              <button
                type="button"
                className="px-6 py-2 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-lg hover:from-purple-200 hover:to-blue-200 transition-all duration-200 font-medium"
              >
                Choose File
              </button>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Left Column */}
            <div className="space-y-6">
              {/* Basic Info */}
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">Title</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
                  placeholder="Enter asset title"
                  className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                  placeholder="Describe your asset and its unique features"
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none transition-all duration-200"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">Category</label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData(prev => ({ ...prev, category: e.target.value }))}
                  className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                >
                  {categories.map(category => (
                    <option key={category.id} value={category.id}>{category.label}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Right Column */}
            <div className="space-y-6">
              {/* Pricing */}
              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">Initial Price (ETH)</label>
                <input
                  type="number"
                  step="0.001"
                  value={formData.price}
                  onChange={(e) => setFormData(prev => ({ ...prev, price: e.target.value }))}
                  placeholder="0.1"
                  className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                  required
                />
                <div className="mt-3 p-4 bg-gradient-to-r from-blue-50 to-cyan-50 border border-blue-200 rounded-xl">
                  <div className="flex items-start space-x-3">
                    <div className="p-1 bg-blue-100 rounded-lg">
                      <Zap className="w-4 h-4 text-blue-600" />
                    </div>
                    <div className="text-sm">
                      <div className="font-semibold text-blue-900 mb-1">AI Pricing Suggestion</div>
                      <div className="text-blue-700">Based on similar assets, 0.15 ETH is optimal for market entry.</div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-900 mb-2">Supply</label>
                  <input
                    type="number"
                    min="1"
                    value={formData.supply}
                    onChange={(e) => setFormData(prev => ({ ...prev, supply: e.target.value }))}
                    className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-semibold text-gray-900 mb-2">Royalty (%)</label>
                  <input
                    type="number"
                    min="0"
                    max="50"
                    value={formData.royaltyRate}
                    onChange={(e) => setFormData(prev => ({ ...prev, royaltyRate: e.target.value }))}
                    className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-900 mb-2">Collaborators (Optional)</label>
                <input
                  type="text"
                  value={formData.collaborators}
                  onChange={(e) => setFormData(prev => ({ ...prev, collaborators: e.target.value }))}
                  placeholder="Wallet addresses separated by commas"
                  className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                />
                <p className="text-sm text-gray-500 mt-2">Add collaborators for shared ownership</p>
              </div>
            </div>
          </div>

          {/* Utility Selection */}
          <div>
            <label className="block text-sm font-semibold text-gray-900 mb-3">Asset Utility</label>
            <div className="grid md:grid-cols-3 gap-3">
              {utilityOptions.map(utility => (
                <label key={utility} className="flex items-center space-x-3 p-4 border border-gray-200 rounded-xl hover:bg-gradient-to-r hover:from-purple-50 hover:to-blue-50 cursor-pointer transition-all duration-200 group">
                  <input
                    type="checkbox"
                    checked={formData.utility.includes(utility)}
                    onChange={() => handleUtilityChange(utility)}
                    className="w-4 h-4 text-blue-600 bg-white border-2 border-gray-300 rounded focus:ring-blue-500 focus:ring-2 transition-all duration-200"
                  />
                  <span className="text-sm text-gray-700 group-hover:text-gray-900 transition-colors duration-200">{utility}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Submit Buttons */}
          <div className="flex items-center justify-end space-x-4 pt-6 border-t border-gray-100">
            <button
              type="button"
              onClick={handleClose}
              className="px-6 py-3 border-2 border-gray-200 text-gray-700 rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all duration-200 font-semibold"
            >
              Cancel
            </button>
            <button
              onClick={handleSubmit}
              disabled={isLoading}
              className="px-6 py-3 bg-gradient-to-r  from-cyan-400 to-blue-400 text-white rounded-xl hover:shadow-xl hover:shadow-purple-500/25 transition-all duration-300 font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              {isLoading ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Minting...</span>
                </>
              ) : (
                <>
                  <Package className="w-4 h-4" />
                  <span>Mint Asset</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AssetUploadForm;