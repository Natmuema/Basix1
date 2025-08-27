import React from 'react'
import { DollarSign, TrendingUp, PieChart, Star, Search, Filter } from 'lucide-react'

// Mock data to replace the imports
const investments = [
  {
    id: 1,
    title: "Kenyan Coffee Collection NFT",
    creator: "Sarah Wanjiku",
    investment: "$5,000",
    returns: "+24.5%",
    status: "Active",
    image: "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=150&h=150&fit=crop"
  },
  {
    id: 2,
    title: "Traditional Maasai Art Series",
    creator: "Joseph Kiprotich",
    investment: "$3,200",
    returns: "+18.2%",
    status: "Active",
    image: "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=150&h=150&fit=crop"
  },
  {
    id: 3,
    title: "Sustainable Fashion Line",
    creator: "Grace Auma",
    investment: "$2,500",
    returns: "+12.1%",
    status: "Growing",
    image: "https://images.unsplash.com/photo-1445205170230-053b83016050?w=150&h=150&fit=crop"
  }
];

const opportunities = [
  {
    id: 4,
    title: "Solar Energy Cooperative",
    creator: "Tech Innovators Kenya",
    raised: "$45,000",
    target: "$100,000",
    backers: 234,
    timeLeft: "15 days",
    image: "https://images.unsplash.com/photo-1509391366360-2e959784a276?w=150&h=150&fit=crop"
  },
  {
    id: 5,
    title: "Organic Farming Initiative",
    creator: "Green Valley Farms",
    raised: "$28,500",
    target: "$75,000",
    backers: 156,
    timeLeft: "23 days",
    image: "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=150&h=150&fit=crop"
  }
];

const InvestorDashboard = () => {
  return (
     <div className="max-w-7xl mx-auto px-4 py-8 bg-white min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Investor Dashboard</h1>
        <p className="text-gray-600">Discover opportunities and manage your portfolio</p>
      </div>

      {/* Portfolio Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-cyan-100 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Invested</p>
              <p className="text-2xl font-bold text-blue-900">$10,700</p>
            </div>
            <DollarSign className="h-8 w-8 text-cyan-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-cyan-100 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Portfolio Value</p>
              <p className="text-2xl font-bold text-cyan-600">$13,250</p>
            </div>
            <TrendingUp className="h-8 w-8 text-cyan-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-cyan-100 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Returns</p>
              <p className="text-2xl font-bold text-blue-600">+23.8%</p>
            </div>
            <PieChart className="h-8 w-8 text-cyan-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-cyan-100 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Active Assets</p>
              <p className="text-2xl font-bold text-blue-700">8</p>
            </div>
            <Star className="h-8 w-8 text-cyan-500" />
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Current Investments */}
        <div className="lg:col-span-2 space-y-8">
          <div className="bg-white rounded-xl shadow-sm border border-cyan-100">
            <div className="p-6 border-b border-cyan-100">
              <h2 className="text-xl font-semibold text-gray-900">Your Portfolio</h2>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {investments.map((investment) => (
                  <div key={investment.id} className="border border-cyan-200 rounded-lg p-4 hover:bg-cyan-50 transition-colors">
                    <div className="flex items-center space-x-4">
                      <img 
                        src={investment.image} 
                        alt={investment.title}
                        className="w-16 h-16 rounded-lg object-cover"
                      />
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <h3 className="font-semibold text-gray-900">{investment.title}</h3>
                          <span className={`px-2 py-1 text-xs rounded-full bg-cyan-100 text-cyan-800`}>
                            {investment.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">by {investment.creator}</p>
                        <div className="flex items-center justify-between mt-2">
                          <div className="flex items-center space-x-4">
                            <span className="text-sm text-blue-600">
                              Invested: <span className="font-medium">{investment.investment}</span>
                            </span>
                            <span className="text-sm text-cyan-600 font-medium">
                              {investment.returns}
                            </span>
                          </div>
                          <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
                            View Details
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Investment Opportunities */}
          <div className="bg-white rounded-xl shadow-sm border border-cyan-100">
            <div className="p-6 border-b border-cyan-100">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold text-gray-900">Investment Opportunities</h2>
                <div className="flex space-x-2">
                  <button className="p-2 bg-gradient-to-r from-cyan-400 to-blue-400 hover:text-blue-600 border border-cyan-200 rounded-lg">
                    <Search className="h-4 w-4" />
                  </button>
                  <button className="p-2 text-blue-400 hover:text-blue-600 border border-cyan-200 rounded-lg">
                    <Filter className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {opportunities.map((opportunity) => (
                  <div key={opportunity.id} className="border border-cyan-200 rounded-lg p-4 hover:bg-cyan-50 transition-colors">
                    <div className="flex items-center space-x-4">
                      <img 
                        src={opportunity.image} 
                        alt={opportunity.title}
                        className="w-16 h-16 rounded-lg object-cover"
                      />
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900">{opportunity.title}</h3>
                        <p className="text-sm text-gray-600 mt-1">by {opportunity.creator}</p>

                        <div className="mt-3">
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-blue-600">Progress</span>
                            <span className="font-medium text-blue-900">{opportunity.raised} / {opportunity.target}</span>
                          </div>
                          <div className="w-full bg-cyan-100 rounded-full h-2">
                            <div 
                              className="font-bold bg-gradient-to-r from-cyan-400 to-blue-400 h-2 rounded-full" 
                              style={{width: `${(parseInt(opportunity.raised.replace('$', '').replace(',', '')) / parseInt(opportunity.target.replace('$', '').replace(',', ''))) * 100}%`}}
                            ></div>
                          </div>
                        </div>
                        
                        <div className="flex items-center justify-between mt-3">
                          <div className="flex items-center space-x-4 text-sm text-blue-600">
                            <span>{opportunity.backers} backers</span>
                            <span>{opportunity.timeLeft} left</span>
                          </div>
                          <button className="bg-gradient-to-r from-cyan-400 to-blue-400 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700 transition-colors">
                            Invest Now
                          </button>
                        </div>
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
          {/* AI Investment Insights */}
          <div className="bg-gradient-to-r from-blue-600 to-cyan-500 p-6 rounded-xl text-white">
            <h3 className="font-semibold mb-4">AI Investment Insights</h3>
            <div className="space-y-3">
              <div className="bg-white/20 p-3 rounded-lg">
                <p className="text-sm font-medium">High-potential sectors</p>
                <p className="text-xs opacity-80">Sustainable agriculture +42%</p>
              </div>
              <div className="bg-white/20 p-3 rounded-lg">
                <p className="text-sm font-medium">Risk assessment</p>
                <p className="text-xs opacity-80">Your portfolio: Low risk</p>
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-cyan-100">
            <h3 className="font-semibold text-gray-900 mb-4">Market Trends</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">African Art</span>
                <span className="text-sm font-medium text-cyan-600">+15.2%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Sustainable Products</span>
                <span className="text-sm font-medium text-cyan-600">+28.5%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Digital Assets</span>
                <span className="text-sm font-medium text-blue-600">+12.8%</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Agriculture Tech</span>
                <span className="text-sm font-medium text-cyan-600">+34.1%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default InvestorDashboard