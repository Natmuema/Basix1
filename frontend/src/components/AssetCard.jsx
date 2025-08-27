import React from 'react';
import { Link } from 'react-router-dom';
import { Users, TrendingUp, Shield, ExternalLink } from 'lucide-react';

const AssetCard = ({ asset }) => {
  return (
    <div className="bg-white rounded-2xl border border-gray-100 overflow-hidden hover:shadow-xl transition-all duration-300 group">
      <div className="relative">
        <img 
          src={asset.image} 
          alt={asset.title}
          className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-500"
        />
        <div className="absolute top-4 left-4 flex space-x-2">
          <span className={`px-2 py-1 text-xs font-medium rounded-full ${
            asset.type === 'Phygital' 
              ? 'bg-purple-100 text-purple-700' 
              : 'bg-blue-100 text-blue-700'
          }`}>
            {asset.type}
          </span>
          {asset.verified && (
            <div className="p-1 bg-green-100 rounded-full">
              <Shield className="w-3 h-3 text-green-600" />
            </div>
          )}
        </div>
        <div className="absolute top-4 right-4">
          <Link
            to={`/asset/${asset.id}`}
            className="p-2 bg-white/90 rounded-full hover:bg-white transition-colors"
          >
            <ExternalLink className="w-4 h-4 text-gray-700" />
          </Link>
        </div>
      </div>

      <div className="p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
          {asset.title}
        </h3>
        <p className="text-sm text-gray-600 mb-4">by {asset.creator}</p>

        <div className="space-y-3">
          {/* Price */}
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-500">Current Price</span>
            <span className="text-lg font-bold text-gray-900">{asset.price}</span>
          </div>

          {/* Funding Progress */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-500">Funding</span>
              <span className="text-sm font-medium text-gray-900">{asset.fundingProgress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-gradient-to-r from-purple-500 to-blue-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${asset.fundingProgress}%` }}
              ></div>
            </div>
          </div>

          {/* Stats */}
          <div className="flex items-center justify-between pt-2 border-t border-gray-100">
            <div className="flex items-center space-x-1">
              <Users className="w-4 h-4 text-gray-400" />
              <span className="text-sm text-gray-600">{asset.collaborators} owners</span>
            </div>
            <div className="flex items-center space-x-1">
              <TrendingUp className="w-4 h-4 text-green-500" />
              <span className="text-sm text-green-600">+12.5%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AssetCard;