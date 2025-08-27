import React, { useState } from 'react';
import { X, Upload, Image, Package, Globe, Zap } from 'lucide-react';
import { useMarketplace } from '../context/MarketplaceContext';
import { useAuth } from '../context/Authcontext';
import { useNavigate } from 'react-router-dom';

const AssetUploadFormUpdated = ({ onClose }) => {
  const navigate = useNavigate();
  const { createProduct, createNFT } = useMarketplace();
  const { creator } = useAuth();
  
  const [isOpen, setIsOpen] = useState(true);
  const [formData, setFormData] = useState({
    // Product fields
    title: '',
    description: '',
    category: 'ArtCraft',
    productType: 'ArtCraft',
    assetType: 'digital',
    
    // NFT fields
    tokenId: '',
    fundingThreshold: '',
    heritageValue: 50,
    sustainabilityScore: 50,
    sdgAlignment: [],
    
    // Utilities
    utilities: [],
    
    // Files
    image: null,
    digitalFile: null,
    
    // Additional
    collaborators: ''
  });

  const [dragOver, setDragOver] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadStep, setUploadStep] = useState(1); // 1: Product, 2: NFT

  const productTypes = [
    { id: 'ArtCraft', label: 'Art & Craft' },
    { id: 'Music', label: 'Music' },
    { id: 'Fashion', label: 'Fashion' },
    { id: 'Tourism', label: 'Tourism' },
    { id: 'Heritage', label: 'Heritage' },
    { id: 'Software', label: 'Software' }
  ];

  const categories = {
    ArtCraft: ['Beadwork', 'Painting', 'Sculpture', 'Other'],
    Music: ['Afrobeat', 'Traditional', 'Contemporary', 'Other'],
    Fashion: ['Textile', 'Jewelry', 'Accessories', 'Other'],
    Software: ['AI/ML', 'Gaming', 'Tools', 'Other'],
    Tourism: ['Other'],
    Heritage: ['Other']
  };

  const utilityOptions = [
    { id: 'provenance', label: 'Provenance' },
    { id: 'resale_rights', label: 'Resale Rights' },
    { id: 'streaming_rights', label: 'Streaming Rights' },
    { id: 'royalties', label: 'Royalties' },
    { id: 'redeem_physical', label: 'Redeem Physical Item' },
    { id: 'digital_wearable', label: 'Digital Wearable' },
    { id: 'redeemable_experience', label: 'Redeemable Experience' },
    { id: 'archive_access', label: 'Archive Access' },
    { id: 'license_key', label: 'License Key' },
    { id: 'lifetime_access', label: 'Lifetime Access' }
  ];

  const sdgOptions = [
    'Artisan_Economy', 'Women_Empowerment', 'Culture', 'Education',
    'Tourism', 'Wildlife_Protection', 'Innovation', 'Tech4Good',
    'Entertainment', 'Digital_Content', 'Creative_Economy'
  ];

  const handleClose = () => {
    setIsOpen(false);
    if (onClose) {
      onClose();
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e) => {
    const { name, files } = e.target;
    if (files && files[0]) {
      setFormData(prev => ({ ...prev, [name]: files[0] }));
    }
  };

  const handleUtilityToggle = (utility) => {
    setFormData(prev => ({
      ...prev,
      utilities: prev.utilities.includes(utility)
        ? prev.utilities.filter(u => u !== utility)
        : [...prev.utilities, utility]
    }));
  };

  const handleSDGToggle = (sdg) => {
    setFormData(prev => ({
      ...prev,
      sdgAlignment: prev.sdgAlignment.includes(sdg)
        ? prev.sdgAlignment.filter(s => s !== sdg)
        : [...prev.sdgAlignment, sdg]
    }));
  };

  const generateTokenId = () => {
    const prefix = formData.productType.toUpperCase();
    const random = Math.random().toString(36).substr(2, 9);
    setFormData(prev => ({ ...prev, tokenId: `${prefix}_${random}` }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      if (uploadStep === 1) {
        // Step 1: Create Product
        const productData = {
          name: formData.title,
          product_type: formData.productType,
          description: formData.description,
          category: formData.category,
          is_physical: formData.assetType === 'physical' || formData.assetType === 'phygital',
          is_digital: formData.assetType === 'digital' || formData.assetType === 'phygital',
          has_digital_scan: formData.assetType === 'phygital',
          is_redeemable: formData.utilities.includes('redeem_physical') || formData.utilities.includes('redeemable_experience'),
          is_license_based: formData.productType === 'Software' && formData.utilities.includes('license_key'),
          image: formData.image,
          digital_file: formData.digitalFile
        };

        const productResult = await createProduct(productData);
        
        if (productResult.success) {
          // Move to NFT creation step
          setFormData(prev => ({ ...prev, productId: productResult.data.id }));
          setUploadStep(2);
          
          // Auto-generate token ID if not set
          if (!formData.tokenId) {
            generateTokenId();
          }
        } else {
          alert(`Error creating product: ${productResult.error}`);
        }
      } else {
        // Step 2: Create NFT
        const nftData = {
          token_id: formData.tokenId || generateTokenId(),
          name: `NFT ${formData.title}`,
          product_id: formData.productId,
          funding_threshold: parseFloat(formData.fundingThreshold) || 1000,
          heritage_value: parseInt(formData.heritageValue),
          sustainability_score: parseInt(formData.sustainabilityScore),
          sdg_alignment: formData.sdgAlignment,
          utilities: formData.utilities
        };

        const nftResult = await createNFT(nftData);
        
        if (nftResult.success) {
          alert('Asset created successfully!');
          navigate('/assets');
          handleClose();
        } else {
          alert(`Error creating NFT: ${nftResult.error}`);
        }
      }
    } catch (error) {
      console.error('Error creating asset:', error);
      alert('Failed to create asset. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4 overflow-y-auto">
      <div className="bg-gray-900 rounded-2xl w-full max-w-3xl max-h-[90vh] overflow-y-auto">
        <div className="sticky top-0 bg-gray-900 p-6 border-b border-gray-800 flex justify-between items-center">
          <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            {uploadStep === 1 ? 'Create Product' : 'Create NFT'}
          </h2>
          <button
            onClick={handleClose}
            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {uploadStep === 1 ? (
            <>
              {/* Product Information */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-white">Product Information</h3>
                
                <div>
                  <label className="block text-sm text-gray-400 mb-2">Title *</label>
                  <input
                    type="text"
                    name="title"
                    value={formData.title}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 text-white"
                    placeholder="Enter asset title"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-400 mb-2">Description *</label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 text-white resize-none"
                    placeholder="Describe your asset..."
                    rows="4"
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Product Type *</label>
                    <select
                      name="productType"
                      value={formData.productType}
                      onChange={(e) => {
                        handleInputChange(e);
                        setFormData(prev => ({ ...prev, category: 'Other' }));
                      }}
                      className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 text-white"
                      required
                    >
                      {productTypes.map(type => (
                        <option key={type.id} value={type.id}>{type.label}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Category *</label>
                    <select
                      name="category"
                      value={formData.category}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 text-white"
                      required
                    >
                      {categories[formData.productType]?.map(cat => (
                        <option key={cat} value={cat}>{cat}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm text-gray-400 mb-2">Asset Type *</label>
                  <div className="grid grid-cols-3 gap-3">
                    {['digital', 'physical', 'phygital'].map(type => (
                      <button
                        key={type}
                        type="button"
                        onClick={() => setFormData(prev => ({ ...prev, assetType: type }))}
                        className={`p-3 rounded-lg border transition-all ${
                          formData.assetType === type
                            ? 'border-blue-500 bg-blue-500/20 text-blue-400'
                            : 'border-gray-700 hover:border-gray-600 text-gray-400'
                        }`}
                      >
                        <div className="flex flex-col items-center space-y-1">
                          {type === 'digital' && <Globe className="w-5 h-5" />}
                          {type === 'physical' && <Package className="w-5 h-5" />}
                          {type === 'phygital' && <Zap className="w-5 h-5" />}
                          <span className="text-sm capitalize">{type}</span>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>

                {/* File Uploads */}
                <div>
                  <label className="block text-sm text-gray-400 mb-2">Product Image</label>
                  <input
                    type="file"
                    name="image"
                    onChange={handleFileChange}
                    accept="image/*"
                    className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 text-white"
                  />
                </div>

                {(formData.assetType === 'digital' || formData.assetType === 'phygital') && (
                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Digital File</label>
                    <input
                      type="file"
                      name="digitalFile"
                      onChange={handleFileChange}
                      className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 text-white"
                    />
                  </div>
                )}
              </div>
            </>
          ) : (
            <>
              {/* NFT Information */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-white">NFT Configuration</h3>
                
                <div className="bg-gray-800/50 rounded-lg p-4">
                  <p className="text-sm text-gray-400">Creating NFT for:</p>
                  <p className="text-white font-medium">{formData.title}</p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Token ID</label>
                    <div className="flex space-x-2">
                      <input
                        type="text"
                        name="tokenId"
                        value={formData.tokenId}
                        onChange={handleInputChange}
                        className="flex-1 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 text-white"
                        placeholder="Auto-generated"
                      />
                      <button
                        type="button"
                        onClick={generateTokenId}
                        className="px-4 py-3 bg-blue-500 hover:bg-blue-600 rounded-lg text-white"
                      >
                        Generate
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm text-gray-400 mb-2">Funding Threshold (USD) *</label>
                    <input
                      type="number"
                      name="fundingThreshold"
                      value={formData.fundingThreshold}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:outline-none focus:border-blue-500 text-white"
                      placeholder="1000"
                      min="1"
                      required
                    />
                  </div>
                </div>

                {/* Impact Scores */}
                <div className="space-y-3">
                  <h4 className="text-sm font-medium text-white">Impact Scores</h4>
                  
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-400">Heritage Value</span>
                      <span className="text-white">{formData.heritageValue}</span>
                    </div>
                    <input
                      type="range"
                      name="heritageValue"
                      value={formData.heritageValue}
                      onChange={handleInputChange}
                      min="0"
                      max="100"
                      className="w-full"
                    />
                  </div>

                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-gray-400">Sustainability Score</span>
                      <span className="text-white">{formData.sustainabilityScore}</span>
                    </div>
                    <input
                      type="range"
                      name="sustainabilityScore"
                      value={formData.sustainabilityScore}
                      onChange={handleInputChange}
                      min="0"
                      max="100"
                      className="w-full"
                    />
                  </div>
                </div>

                {/* Utilities */}
                <div>
                  <label className="block text-sm text-gray-400 mb-2">Utilities</label>
                  <div className="grid grid-cols-2 gap-2">
                    {utilityOptions.map(option => (
                      <label
                        key={option.id}
                        className="flex items-center space-x-2 p-3 bg-gray-800 rounded-lg cursor-pointer hover:bg-gray-700"
                      >
                        <input
                          type="checkbox"
                          checked={formData.utilities.includes(option.id)}
                          onChange={() => handleUtilityToggle(option.id)}
                          className="rounded text-blue-500"
                        />
                        <span className="text-sm text-gray-300">{option.label}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* SDG Alignment */}
                <div>
                  <label className="block text-sm text-gray-400 mb-2">SDG Alignment</label>
                  <div className="flex flex-wrap gap-2">
                    {sdgOptions.map(sdg => (
                      <button
                        key={sdg}
                        type="button"
                        onClick={() => handleSDGToggle(sdg)}
                        className={`px-3 py-1 rounded-full text-xs transition-all ${
                          formData.sdgAlignment.includes(sdg)
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                        }`}
                      >
                        {sdg.replace(/_/g, ' ')}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </>
          )}

          <div className="flex justify-between items-center pt-6 border-t border-gray-800">
            {uploadStep === 2 && (
              <button
                type="button"
                onClick={() => setUploadStep(1)}
                className="px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-medium transition-colors"
              >
                Back
              </button>
            )}
            
            <div className="flex space-x-3 ml-auto">
              <button
                type="button"
                onClick={handleClose}
                className="px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-medium transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 rounded-lg font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Processing...' : uploadStep === 1 ? 'Next' : 'Create NFT'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AssetUploadFormUpdated;