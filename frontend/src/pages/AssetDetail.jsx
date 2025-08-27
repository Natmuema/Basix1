import React from 'react';
import { ArrowLeft, Share2, Heart, TrendingUp, Users, Clock, Shield } from 'lucide-react';

const AssetDetail = () => {
  // Mock data - would come from API
  const asset = {
    id: 1,
    title: "Kenyan Coffee Collection NFT",
    creator: {
      name: "Sarah Wanjiku",
      avatar: "https://images.pexels.com/photos/1239291/pexels-photo-1239291.jpeg?auto=compress&cs=tinysrgb&w=100",
      verified: true
    },
    description: "Authentic Kenyan coffee collection featuring premium single-origin beans from the highlands of Mount Kenya. Each NFT represents ownership of a specific coffee batch with full traceability from farm to cup.",
    images: [
      "https://images.pexels.com/photos/894695/pexels-photo-894695.jpeg?auto=compress&cs=tinysrgb&w=800",
      "https://images.pexels.com/photos/1695052/pexels-photo-1695052.jpeg?auto=compress&cs=tinysrgb&w=800",
      "https://images.pexels.com/photos/2238309/pexels-photo-2238309.jpeg?auto=compress&cs=tinysrgb&w=800"
    ],
    currentPrice: "$2,850",
    targetFunding: "$15,000",
    funded: 85,
    backers: 127,
    timeLeft: "23 days",
    status: "Active",
    category: "Phygital Asset",
    roi: "+24.5%",
    attributes: [
      { trait: "Origin", value: "Mount Kenya Highlands" },
      { trait: "Processing", value: "Washed Process" },
      { trait: "Altitude", value: "1,800m - 2,100m" },
      { trait: "Batch Size", value: "500kg" },
      { trait: "Harvest Year", value: "2024" },
      { trait: "Certification", value: "Fair Trade & Organic" }
    ]
  };

  return (
    <div className="min-h-screen bg-gray-50">      
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Breadcrumb */}
        <div className="flex items-center space-x-2 text-sm text-gray-600 mb-6">
          <a href="/dashboard" className="hover:text-blue-600 flex items-center">
            <ArrowLeft className="h-4 w-4 mr-1" />
            Dashboard
          </a>
          <span>/</span>
          <span className="text-gray-900">Asset Details</span>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Asset Images and Info */}
          <div className="lg:col-span-2 space-y-6">
            {/* Main Image */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
              <img 
                src={asset.images[0]} 
                alt={asset.title}
                className="w-full h-96 object-cover"
              />
            </div>

            {/* Thumbnail Images */}
            <div className="flex space-x-4">
              {asset.images.slice(1).map((image, index) => (
                <img 
                  key={index}
                  src={image} 
                  alt={`${asset.title} ${index + 2}`}
                  className="w-24 h-24 rounded-lg object-cover border border-gray-200 cursor-pointer hover:border-blue-400 transition-colors"
                />
              ))}
            </div>

            {/* Description */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Description</h2>
              <p className="text-gray-700 leading-relaxed">{asset.description}</p>
            </div>

            {/* Attributes */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Asset Properties</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {asset.attributes.map((attr, index) => (
                  <div key={index} className="border border-gray-200 p-3 rounded-lg">
                    <p className="text-sm text-gray-600">{attr.trait}</p>
                    <p className="font-medium text-gray-900">{attr.value}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Provenance & AI Insights */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">AI Market Analysis</h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <TrendingUp className="h-5 w-5 text-blue-600" />
                    <span className="font-medium">Market Trend</span>
                  </div>
                  <span className="text-green-600 font-semibold">Strong Growth (+34%)</span>
                </div>
                <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <Shield className="h-5 w-5 text-green-600" />
                    <span className="font-medium">Risk Assessment</span>
                  </div>
                  <span className="text-green-600 font-semibold">Low Risk</span>
                </div>
                <div className="flex items-center justify-between p-4 bg-purple-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <Clock className="h-5 w-5 text-purple-600" />
                    <span className="font-medium">Optimal Hold Time</span>
                  </div>
                  <span className="text-purple-600 font-semibold">6-12 months</span>
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Asset Header */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
              <div className="flex items-center justify-between mb-4">
                <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                  {asset.category}
                </span>
                <div className="flex items-center space-x-2">
                  <button className="p-2 text-gray-400 hover:text-red-500 transition-colors">
                    <Heart className="h-5 w-5" />
                  </button>
                  <button className="p-2 text-gray-400 hover:text-blue-500 transition-colors">
                    <Share2 className="h-5 w-5" />
                  </button>
                </div>
              </div>
              
              <h1 className="text-2xl font-bold text-gray-900 mb-2">{asset.title}</h1>
              
              {/* Creator Info */}
              <div className="flex items-center space-x-3 mb-6">
                <img 
                  src={asset.creator.avatar} 
                  alt={asset.creator.name}
                  className="w-10 h-10 rounded-full"
                />
                <div>
                  <div className="flex items-center space-x-1">
                    <span className="font-medium text-gray-900">{asset.creator.name}</span>
                    {asset.creator.verified && (
                      <Shield className="h-4 w-4 text-blue-500" />
                    )}
                  </div>
                  <span className="text-sm text-gray-600">Creator</span>
                </div>
              </div>

              {/* Current Price */}
              <div className="mb-6">
                <p className="text-sm text-gray-600 mb-1">Current Investment Price</p>
                <div className="flex items-center justify-between">
                  <p className="text-3xl font-bold text-gray-900">{asset.currentPrice}</p>
                  <span className="text-green-600 font-semibold text-lg">{asset.roi}</span>
                </div>
              </div>

              {/* Funding Progress */}
              <div className="mb-6">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-gray-700">Funding Progress</span>
                  <span className="text-sm font-medium text-blue-600">{asset.funded}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
                  <div 
                    className="bg-blue-600 h-3 rounded-full transition-all duration-300" 
                    style={{width: `${asset.funded}%`}}
                  ></div>
                </div>
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <p className="text-sm text-gray-600">Target</p>
                    <p className="font-semibold text-gray-900">{asset.targetFunding}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Backers</p>
                    <p className="font-semibold text-gray-900">{asset.backers}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Time Left</p>
                    <p className="font-semibold text-gray-900">{asset.timeLeft}</p>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="space-y-3">
                <a 
                  href="/funding"
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg transition-colors flex items-center justify-center"
                >
                  <Users className="h-5 w-5 mr-2" />
                  Invest in this Asset
                </a>
                <button className="w-full border border-blue-600 text-blue-600 hover:bg-blue-50 font-medium py-3 px-6 rounded-lg transition-colors">
                  Add to Watchlist
                </button>
              </div>
            </div>

            {/* Cardano Wallet Info */}
            <div className="bg-gradient-to-r from-blue-600 to-cyan-600 p-6 rounded-xl text-white">
              <h3 className="font-semibold mb-3">Blockchain Details</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="opacity-80">Network:</span>
                  <span>Cardano</span>
                </div>
                <div className="flex justify-between">
                  <span className="opacity-80">Token Standard:</span>
                  <span>Native Token</span>
                </div>
                <div className="flex justify-between">
                  <span className="opacity-80">Smart Contract:</span>
                  <span className="truncate ml-2">addr1qx2f...</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AssetDetail;