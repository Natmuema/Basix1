import React, { useState } from 'react';
import { TrendingUp, Users, Clock, DollarSign } from 'lucide-react';
import { useMarketplace } from '../context/MarketplaceContext';
import { useAuth } from '../context/Authcontext';

const AssetCardUpdated = ({ nft }) => {
  const [showFundingModal, setShowFundingModal] = useState(false);
  const [fundingAmount, setFundingAmount] = useState('');
  const [isContributing, setIsContributing] = useState(false);
  
  const { contributeFunding } = useMarketplace();
  const { user } = useAuth();

  const handleFundingContribution = async () => {
    if (!fundingAmount || parseFloat(fundingAmount) <= 0) return;

    setIsContributing(true);
    const result = await contributeFunding(nft.id, parseFloat(fundingAmount));
    
    if (result.success) {
      setShowFundingModal(false);
      setFundingAmount('');
      // You could show a success toast here
      alert('Funding contribution successful!');
    } else {
      alert(`Error: ${result.error}`);
    }
    setIsContributing(false);
  };

  // Calculate days left (mock calculation - you'd need actual deadline)
  const daysLeft = 30; // This should come from your NFT data

  return (
    <>
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700 hover:border-blue-500 transition-all duration-300 hover:shadow-xl hover:shadow-blue-500/20 overflow-hidden group">
        {/* Asset Image */}
        <div className="relative h-48 overflow-hidden">
          <img 
            src={nft.product_image || 'https://via.placeholder.com/400x300'} 
            alt={nft.name}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
          />
          <div className="absolute top-2 right-2">
            <span className={`px-3 py-1 rounded-full text-xs font-medium ${
              nft.is_funded ? 'bg-green-500/20 text-green-400' : 'bg-blue-500/20 text-blue-400'
            }`}>
              {nft.is_funded ? 'Funded' : 'Funding'}
            </span>
          </div>
          <div className="absolute top-2 left-2">
            <span className="px-3 py-1 rounded-full text-xs font-medium bg-purple-500/20 text-purple-400">
              {nft.product_type}
            </span>
          </div>
        </div>

        {/* Asset Details */}
        <div className="p-6">
          <h3 className="text-lg font-semibold text-white mb-2 line-clamp-1">
            {nft.name}
          </h3>
          
          <p className="text-gray-400 text-sm mb-4 line-clamp-2">
            {nft.product_category} • Token: {nft.token_id.slice(0, 8)}...
          </p>

          {/* Metrics */}
          <div className="grid grid-cols-2 gap-3 mb-4">
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-green-400" />
              <span className="text-sm text-gray-300">
                Impact: {nft.impact_score?.toFixed(1) || 'N/A'}
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <Users className="w-4 h-4 text-blue-400" />
              <span className="text-sm text-gray-300">
                {nft.ownerships?.length || 0} Owners
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-yellow-400" />
              <span className="text-sm text-gray-300">{daysLeft}d left</span>
            </div>
            <div className="flex items-center space-x-2">
              <DollarSign className="w-4 h-4 text-purple-400" />
              <span className="text-sm text-gray-300">
                ${nft.current_funding?.toLocaleString() || '0'}
              </span>
            </div>
          </div>

          {/* Funding Progress */}
          <div className="mb-4">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-400">Funding Progress</span>
              <span className="text-white font-medium">
                {nft.funding_percentage?.toFixed(1) || 0}%
              </span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div 
                className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${Math.min(nft.funding_percentage || 0, 100)}%` }}
              />
            </div>
            <div className="flex justify-between text-xs mt-1">
              <span className="text-gray-500">
                ${nft.current_funding?.toLocaleString() || '0'}
              </span>
              <span className="text-gray-500">
                ${nft.funding_threshold?.toLocaleString() || '0'}
              </span>
            </div>
          </div>

          {/* Impact Scores */}
          <div className="flex space-x-2 mb-4">
            <div className="flex-1 bg-gray-700/50 rounded-lg p-2 text-center">
              <div className="text-xs text-gray-400">Heritage</div>
              <div className="text-sm font-semibold text-green-400">
                {nft.heritage_value || 0}
              </div>
            </div>
            <div className="flex-1 bg-gray-700/50 rounded-lg p-2 text-center">
              <div className="text-xs text-gray-400">Sustainability</div>
              <div className="text-sm font-semibold text-blue-400">
                {nft.sustainability_score || 0}
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-2">
            <button className="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm font-medium transition-colors">
              View Details
            </button>
            {!nft.is_funded && user && (
              <button 
                onClick={() => setShowFundingModal(true)}
                className="flex-1 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 rounded-lg text-sm font-medium transition-colors"
              >
                Contribute
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Funding Modal */}
      {showFundingModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-2xl p-6 max-w-md w-full mx-4 border border-gray-700">
            <h3 className="text-xl font-bold text-white mb-4">
              Contribute to {nft.name}
            </h3>
            
            <div className="mb-4">
              <label className="block text-sm text-gray-400 mb-2">
                Contribution Amount (USD)
              </label>
              <input
                type="number"
                value={fundingAmount}
                onChange={(e) => setFundingAmount(e.target.value)}
                placeholder="Enter amount"
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
                min="1"
                step="0.01"
              />
            </div>

            <div className="bg-gray-700/50 rounded-lg p-4 mb-4">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">Current Funding</span>
                <span className="text-white">
                  ${nft.current_funding?.toLocaleString() || '0'}
                </span>
              </div>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-400">Funding Goal</span>
                <span className="text-white">
                  ${nft.funding_threshold?.toLocaleString() || '0'}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Remaining</span>
                <span className="text-green-400">
                  ${((nft.funding_threshold || 0) - (nft.current_funding || 0)).toLocaleString()}
                </span>
              </div>
            </div>

            <div className="flex space-x-3">
              <button
                onClick={() => setShowFundingModal(false)}
                className="flex-1 px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg font-medium transition-colors"
                disabled={isContributing}
              >
                Cancel
              </button>
              <button
                onClick={handleFundingContribution}
                className="flex-1 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 rounded-lg font-medium transition-colors disabled:opacity-50"
                disabled={isContributing || !fundingAmount || parseFloat(fundingAmount) <= 0}
              >
                {isContributing ? 'Contributing...' : 'Contribute'}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default AssetCardUpdated;