import React, { useState } from 'react';
import { TrendingUp, TrendingDown, DollarSign, PieChart, Calendar, Filter, Download, ArrowUpRight, ArrowDownRight } from 'lucide-react';

const PortfolioPage = () => {
  const [timeRange, setTimeRange] = useState('1M');
  const [selectedMetric, setSelectedMetric] = useState('value');

  const portfolioData = {
    totalValue: 13250,
    totalInvested: 10700,
    totalReturns: 2550,
    roiPercentage: 23.8,
    assets: [
      {
        id: 1,
        name: "Kenyan Coffee Collection NFT",
        invested: 5000,
        currentValue: 6225,
        returns: 1225,
        roi: 24.5,
        allocation: 47,
        performance: [100, 105, 110, 115, 120, 125, 124.5]
      },
      {
        id: 2,
        name: "Traditional Maasai Art Series",
        invested: 3200,
        currentValue: 3782,
        returns: 582,
        roi: 18.2,
        allocation: 28.5,
        performance: [100, 102, 108, 112, 118, 118.2]
      },
      {
        id: 3,
        name: "Sustainable Fashion Line",
        invested: 2500,
        currentValue: 2803,
        returns: 303,
        roi: 12.1,
        allocation: 21.2,
        performance: [100, 98, 103, 107, 110, 112.1]
      }
    ],
    monthlyPerformance: [
      { month: 'Jan', value: 10700, returns: 0 },
      { month: 'Feb', value: 11200, returns: 500 },
      { month: 'Mar', value: 11800, returns: 1100 },
      { month: 'Apr', value: 12400, returns: 1700 },
      { month: 'May', value: 12900, returns: 2200 },
      { month: 'Jun', value: 13250, returns: 2550 }
    ]
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-cyan-50">  
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Portfolio Performance</h1>
              <p className="text-gray-600">Track your investment performance and analytics</p>
            </div>
            <div className="flex items-center space-x-4">
              <select 
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                className="px-4 py-2 text-gray-600 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 transition-all"
              >
                <option value="1W">1 Week</option>
                <option value="1M">1 Month</option>
                <option value="3M">3 Months</option>
                <option value="6M">6 Months</option>
                <option value="1Y">1 Year</option>
              </select>
              <button className="flex items-center px-6 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-xl hover:from-cyan-600 hover:to-blue-700 transition-all duration-300 shadow-lg">
                <Download className="h-4 w-4 mr-2" />
                Export
              </button>
            </div>
          </div>
        </div>

        {/* Performance Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-2xl shadow-lg border border-cyan-100">
            <div className="flex items-center justify-between mb-3">
              <p className="text-sm font-semibold text-gray-600">Total Portfolio Value</p>
              <div className="p-2 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg">
                <DollarSign className="h-5 w-5 text-white" />
              </div>
            </div>
            <p className="text-3xl font-bold text-gray-900">${portfolioData.totalValue.toLocaleString()}</p>
            <div className="flex items-center mt-3">
              <ArrowUpRight className="h-4 w-4 text-cyan-600 mr-1" />
              <span className="text-sm text-cyan-600 font-bold">+{portfolioData.roiPercentage}%</span>
            </div>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow-lg border border-cyan-100">
            <div className="flex items-center justify-between mb-3">
              <p className="text-sm font-semibold text-gray-600">Total Invested</p>
              <div className="p-2 bg-gradient-to-r from-blue-500 to-cyan-600 rounded-lg">
                <TrendingUp className="h-5 w-5 text-white" />
              </div>
            </div>
            <p className="text-3xl font-bold text-gray-900">${portfolioData.totalInvested.toLocaleString()}</p>
            <p className="text-sm text-blue-600 mt-3 font-medium">Principal amount</p>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow-lg border border-cyan-100">
            <div className="flex items-center justify-between mb-3">
              <p className="text-sm font-semibold text-gray-600">Total Returns</p>
              <div className="p-2 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg">
                <TrendingUp className="h-5 w-5 text-white" />
              </div>
            </div>
            <p className="text-3xl font-bold text-cyan-600">+${portfolioData.totalReturns.toLocaleString()}</p>
            <p className="text-sm text-cyan-600 mt-3 font-medium">Profit earned</p>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow-lg border border-cyan-100">
            <div className="flex items-center justify-between mb-3">
              <p className="text-sm font-semibold text-gray-600">Active Assets</p>
              <div className="p-2 bg-gradient-to-r from-blue-600 to-cyan-500 rounded-lg">
                <PieChart className="h-5 w-5 text-white" />
              </div>
            </div>
            <p className="text-3xl font-bold text-gray-900">{portfolioData.assets.length}</p>
            <p className="text-sm text-blue-600 mt-3 font-medium">Diversified portfolio</p>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Performance Chart */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-cyan-100">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Performance Chart</h2>
                <div className="flex space-x-2 bg-gray-100 rounded-lg p-1">
                  <button 
                    onClick={() => setSelectedMetric('value')}
                    className={`px-4 py-2 text-sm rounded-lg transition-all duration-300 ${
                      selectedMetric === 'value' 
                        ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg' 
                        : 'text-gray-600 hover:bg-white hover:shadow-sm'
                    }`}
                  >
                    Value
                  </button>
                  <button 
                    onClick={() => setSelectedMetric('returns')}
                    className={`px-4 py-2 text-sm rounded-lg transition-all duration-300 ${
                      selectedMetric === 'returns' 
                        ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg' 
                        : 'text-gray-600 hover:bg-white hover:shadow-sm'
                    }`}
                  >
                    Returns
                  </button>
                </div>
              </div>
              
              {/* Chart Visualization */}
              <div className="h-72 flex items-end space-x-4 bg-gradient-to-t from-cyan-50 to-transparent p-6 rounded-xl">
                {portfolioData.monthlyPerformance.map((data) => (
                  <div key={data.month} className="flex-1 flex flex-col items-center">
                    <div 
                      className="w-full rounded-t-lg transition-all duration-500 hover:shadow-lg cursor-pointer relative group"
                      style={{
                        background: `linear-gradient(to top, #06b6d4, #2563eb)`,
                        height: `${selectedMetric === 'value' 
                          ? (data.value / 15000) * 220 
                          : Math.max((data.returns / 3000) * 220, 15)
                        }px`
                      }}
                    >
                      <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                        {selectedMetric === 'value' ? `$${data.value.toLocaleString()}` : `$${data.returns.toLocaleString()}`}
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 mt-3 font-medium">{data.month}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Asset Performance */}
            <div className="bg-white rounded-2xl shadow-lg border border-cyan-100">
              <div className="p-6 border-b border-cyan-100 bg-gradient-to-r from-white to-cyan-50 rounded-t-2xl">
                <h2 className="text-2xl font-bold text-gray-900">Asset Performance</h2>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {portfolioData.assets.map((asset) => (
                    <div key={asset.id} className="border-2 border-gray-100 rounded-xl p-6 hover:border-cyan-300 hover:shadow-lg transition-all duration-300 bg-gradient-to-r from-white to-gray-50">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="font-bold text-gray-900 text-lg">{asset.name}</h3>
                        <div className="flex items-center space-x-2 bg-gradient-to-r from-cyan-500 to-blue-600 text-white px-4 py-2 rounded-lg">
                          {asset.roi > 0 ? (
                            <ArrowUpRight className="h-4 w-4" />
                          ) : (
                            <ArrowDownRight className="h-4 w-4" />
                          )}
                          <span className="font-bold">
                            {asset.roi > 0 ? '+' : ''}{asset.roi}%
                          </span>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div className="bg-white p-3 rounded-lg border border-cyan-100">
                          <p className="text-gray-600 font-medium">Invested</p>
                          <p className="font-bold text-gray-900">${asset.invested.toLocaleString()}</p>
                        </div>
                        <div className="bg-white p-3 rounded-lg border border-cyan-100">
                          <p className="text-gray-600 font-medium">Current Value</p>
                          <p className="font-bold text-cyan-600">${asset.currentValue.toLocaleString()}</p>
                        </div>
                        <div className="bg-white p-3 rounded-lg border border-cyan-100">
                          <p className="text-gray-600 font-medium">Returns</p>
                          <p className={`font-bold ${asset.returns > 0 ? 'text-cyan-600' : 'text-red-500'}`}>
                            {asset.returns > 0 ? '+' : ''}${asset.returns.toLocaleString()}
                          </p>
                        </div>
                        <div className="bg-white p-3 rounded-lg border border-cyan-100">
                          <p className="text-gray-600 font-medium">Allocation</p>
                          <p className="font-bold text-blue-600">{asset.allocation}%</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Portfolio Allocation */}
            <div className="bg-white p-6 rounded-2xl shadow-lg border border-cyan-100">
              <h3 className="font-bold text-gray-900 mb-4 text-lg">Portfolio Allocation</h3>
              <div className="space-y-4">
                {portfolioData.assets.map((asset, index) => (
                  <div key={asset.id} className="flex items-center justify-between p-3 bg-gradient-to-r from-cyan-50 to-blue-50 rounded-lg border border-cyan-100">
                    <div className="flex items-center space-x-3">
                      <div 
                        className="w-4 h-4 rounded-full border-2 border-white shadow-sm"
                        style={{backgroundColor: index === 0 ? '#06b6d4' : index === 1 ? '#2563eb' : '#0891b2'}}
                      ></div>
                      <span className="text-sm text-gray-700 font-medium truncate">{asset.name.split(' ').slice(0, 2).join(' ')}</span>
                    </div>
                    <span className="text-sm font-bold text-blue-600">{asset.allocation}%</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Performance Metrics */}
            <div className="bg-gradient-to-br from-blue-600 via-cyan-600 to-cyan-500 p-6 rounded-2xl text-white shadow-lg">
              <h3 className="font-bold mb-4 text-lg">Key Metrics</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center bg-white/20 backdrop-blur-sm p-3 rounded-lg border border-white/30">
                  <span className="opacity-90">Best Performer</span>
                  <span className="font-bold">Coffee NFT</span>
                </div>
                <div className="flex justify-between items-center bg-white/20 backdrop-blur-sm p-3 rounded-lg border border-white/30">
                  <span className="opacity-90">Avg. Hold Time</span>
                  <span className="font-bold">4.2 months</span>
                </div>
                <div className="flex justify-between items-center bg-white/20 backdrop-blur-sm p-3 rounded-lg border border-white/30">
                  <span className="opacity-90">Success Rate</span>
                  <span className="font-bold">87%</span>
                </div>
                <div className="flex justify-between items-center bg-white/20 backdrop-blur-sm p-3 rounded-lg border border-white/30">
                  <span className="opacity-90">Risk Score</span>
                  <span className="font-bold">Low</span>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white p-6 rounded-2xl shadow-lg border border-cyan-100">
              <h3 className="font-bold text-gray-900 mb-4 text-lg">Quick Actions</h3>
              <div className="space-y-3">
                <button className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 text-white py-4 px-4 rounded-xl hover:from-cyan-600 hover:to-blue-700 transition-all duration-300 text-left flex items-center font-medium shadow-lg">
                  <TrendingUp className="h-5 w-5 mr-3" />
                  Rebalance Portfolio
                </button>
                <button className="w-full border-2 border-cyan-200 text-gray-700 py-4 px-4 rounded-xl hover:bg-gradient-to-r hover:from-cyan-50 hover:to-blue-50 hover:border-cyan-300 transition-all duration-300 text-left flex items-center font-medium">
                  <Filter className="h-5 w-5 mr-3 text-cyan-600" />
                  Set Performance Alerts
                </button>
                <button className="w-full border-2 border-cyan-200 text-gray-700 py-4 px-4 rounded-xl hover:bg-gradient-to-r hover:from-cyan-50 hover:to-blue-50 hover:border-cyan-300 transition-all duration-300 text-left flex items-center font-medium">
                  <Download className="h-5 w-5 mr-3 text-cyan-600" />
                  Download Report
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PortfolioPage;