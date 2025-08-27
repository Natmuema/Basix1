import React, {useState} from 'react';
import { Plus, TrendingUp, DollarSign, Package, Eye, Users, BarChart3, Handshake, FileText } from 'lucide-react';
import { Link } from 'react-router-dom';
import AssetUploadForm from './AssetUploadForm';

const CreatorDashboard = () => {
  const [selectedAssetTab, setSelectedAssetTab] = useState('overview');
   const [isAssetFormOpen, setIsAssetFormOpen] = useState(false);

  const assets = [
    {
      id: 1,
      title: "Kenyan Coffee Collection NFT",
      type: "Phygital Asset",
      status: "Active",
      funded: 85,
      revenue: "$12,340",
      image: "https://images.pexels.com/photos/894695/pexels-photo-894695.jpeg?auto=compress&cs=tinysrgb&w=300"
    },
    {
      id: 2,
      title: "Traditional Maasai Art Series",
      type: "IP Rights",
      status: "Funding",
      funded: 42,
      revenue: "$3,250",
      image: "https://images.pexels.com/photos/1070359/pexels-photo-1070359.jpeg?auto=compress&cs=tinysrgb&w=300"
    },
    {
      id: 3,
      title: "Sustainable Fashion Line",
      type: "Product Launch",
      status: "Planning",
      funded: 15,
      revenue: "$580",
      image: "https://images.pexels.com/photos/1536619/pexels-photo-1536619.jpeg?auto=compress&cs=tinysrgb&w=300"
    }
  ];

  const collaborations = [
    {
      id: 1,
      assetId: 1,
      collaborator: "David Mwangi",
      role: "Co-Creator",
      contribution: "Photography & Design",
      ownership: "25%",
      status: "Active",
      joinedDate: "2024-01-10"
    },
    {
      id: 2,
      assetId: 1,
      collaborator: "Grace Auma",
      role: "Marketing Partner",
      contribution: "Brand Strategy",
      ownership: "15%",
      status: "Active",
      joinedDate: "2024-01-15"
    },
    {
      id: 3,
      assetId: 2,
      collaborator: "Joseph Kiprotich",
      role: "Cultural Advisor",
      contribution: "Authenticity Verification",
      ownership: "20%",
      status: "Pending",
      joinedDate: "2024-01-20"
    }
  ];

  const analytics = {
    totalViews: 15420,
    uniqueVisitors: 8750,
    conversionRate: 12.5,
    avgTimeOnPage: "3m 45s",
    topReferrers: [
      { source: "Social Media", percentage: 45, visitors: 3938 },
      { source: "Direct Traffic", percentage: 30, visitors: 2625 },
      { source: "Search Engines", percentage: 15, visitors: 1313 },
      { source: "Email Marketing", percentage: 10, visitors: 875 }
    ],
    monthlyGrowth: [
      { month: "Jan", views: 2100, sales: 850 },
      { month: "Feb", views: 2800, sales: 1200 },
      { month: "Mar", views: 3200, sales: 1450 },
      { month: "Apr", views: 3800, sales: 1680 },
      { month: "May", views: 4200, sales: 1920 },
      { month: "Jun", views: 4650, sales: 2150 }
    ]
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 bg-white min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Creator Dashboard</h1>
        <p className="text-gray-600">Manage your assets and track performance</p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Assets</p>
              <p className="text-2xl font-bold text-navy-900">12</p>
            </div>
            <Package className="h-8 w-8 text-blue-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Revenue</p>
              <p className="text-2xl font-bold text-green-600">$16,170</p>
            </div>
            <DollarSign className="h-8 w-8 text-green-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Avg. Funding</p>
              <p className="text-2xl font-bold text-blue-600">47%</p>
            </div>
            <TrendingUp className="h-8 w-8 text-blue-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Investors</p>
              <p className="text-2xl font-bold text-purple-600">147</p>
            </div>
            <Users className="h-8 w-8 text-purple-600" />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid lg:grid-cols-3 gap-8">
        {/* Assets List */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100">
            <div className="p-6 border-b border-gray-100">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold text-gray-900">Your Assets</h2>
                <button
                  onClick={() => setIsAssetFormOpen(true)}
                  className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Plus className="h-4 w-4 mr-2" />
                  Create Asset
                </button>
              </div>
            </div>
            
            <div className="p-6">
              {/* Asset Tabs */}
              <div className="border-b border-gray-200 mb-6">
                <nav className="flex space-x-8">
                  {[
                    { id: 'overview', label: 'Overview', icon: FileText },
                    { id: 'collaborations', label: 'Collaborations', icon: Handshake },
                    { id: 'analytics', label: 'Analytics', icon: BarChart3 }
                  ].map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setSelectedAssetTab(tab.id)}
                      className={`py-3 px-1 border-b-2 font-medium text-sm transition-colors flex items-center space-x-2 ${
                        selectedAssetTab === tab.id
                          ? 'border-blue-500 text-blue-600'
                          : 'border-transparent text-gray-500 hover:text-gray-700'
                      }`}
                    >
                      <tab.icon className="h-4 w-4" />
                      <span>{tab.label}</span>
                    </button>
                  ))}
                </nav>
              </div>

              {/* Tab Content */}
              {selectedAssetTab === 'overview' && (
                <div className="space-y-4">
                  {assets.map((asset) => (
                    <div key={asset.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors">
                      <div className="flex items-center space-x-4">
                        <img 
                          src={asset.image} 
                          alt={asset.title}
                          className="w-16 h-16 rounded-lg object-cover"
                        />
                        <div className="flex-1">
                          <div className="flex items-center justify-between">
                            <h3 className="font-semibold text-gray-900">{asset.title}</h3>
                            <span className={`px-2 py-1 text-xs rounded-full ${
                              asset.status === 'Active' ? 'bg-green-100 text-green-800' :
                              asset.status === 'Funding' ? 'bg-blue-100 text-blue-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {asset.status}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 mt-1">{asset.type}</p>
                          <div className="flex items-center justify-between mt-2">
                            <div className="flex items-center space-x-4">
                              <span className="text-sm text-gray-600">
                                Funded: <span className="font-medium">{asset.funded}%</span>
                              </span>
                              <span className="text-sm text-gray-600">
                                Revenue: <span className="font-medium text-green-600">{asset.revenue}</span>
                              </span>
                            </div>
                            <Link 
                              to={`/asset/${asset.id}`}
                              className="flex items-center text-blue-600 hover:text-blue-700 text-sm"
                            >
                              <Eye className="h-4 w-4 mr-1" />
                              View
                            </Link>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {selectedAssetTab === 'collaborations' && (
                <div className="space-y-4">
                  <div className="flex justify-between items-center mb-4">
                    <h3 className="font-semibold text-gray-900">Active Collaborations</h3>
                    <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm">
                      Invite Collaborator
                    </button>
                  </div>
                  
                  {collaborations.map((collab) => (
                    <div key={collab.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                          <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                            {collab.collaborator.split(' ').map(n => n[0]).join('')}
                          </div>
                          <div>
                            <h4 className="font-semibold text-gray-900">{collab.collaborator}</h4>
                            <p className="text-sm text-gray-600">{collab.role}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <span className={`px-2 py-1 text-xs rounded-full ${
                            collab.status === 'Active' ? 'bg-green-100 text-green-800' :
                            collab.status === 'Pending' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {collab.status}
                          </span>
                        </div>
                      </div>
                      
                      <div className="grid grid-cols-3 gap-4 mt-4 text-sm">
                        <div>
                          <p className="text-gray-600">Contribution</p>
                          <p className="font-medium">{collab.contribution}</p>
                        </div>
                        <div>
                          <p className="text-gray-600">Ownership</p>
                          <p className="font-medium text-blue-600">{collab.ownership}</p>
                        </div>
                        <div>
                          <p className="text-gray-600">Joined</p>
                          <p className="font-medium">{collab.joinedDate}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {selectedAssetTab === 'analytics' && (
                <div className="space-y-6">
                  {/* Key Metrics */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <p className="text-sm text-blue-600 font-medium">Total Views</p>
                      <p className="text-2xl font-bold text-blue-900">{analytics.totalViews.toLocaleString()}</p>
                    </div>
                    <div className="bg-green-50 p-4 rounded-lg">
                      <p className="text-sm text-green-600 font-medium">Unique Visitors</p>
                      <p className="text-2xl font-bold text-green-900">{analytics.uniqueVisitors.toLocaleString()}</p>
                    </div>
                    <div className="bg-purple-50 p-4 rounded-lg">
                      <p className="text-sm text-purple-600 font-medium">Conversion Rate</p>
                      <p className="text-2xl font-bold text-purple-900">{analytics.conversionRate}%</p>
                    </div>
                    <div className="bg-orange-50 p-4 rounded-lg">
                      <p className="text-sm text-orange-600 font-medium">Avg. Time</p>
                      <p className="text-2xl font-bold text-orange-900">{analytics.avgTimeOnPage}</p>
                    </div>
                  </div>

                  {/* Traffic Sources */}
                  <div className="bg-white border border-gray-200 rounded-lg p-6">
                    <h4 className="font-semibold text-gray-900 mb-4">Traffic Sources</h4>
                    <div className="space-y-3">
                      {analytics.topReferrers.map((referrer, index) => (
                        <div key={index} className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <div 
                              className="w-3 h-3 rounded-full"
                              style={{backgroundColor: `hsl(${index * 90}, 70%, 50%)`}}
                            ></div>
                            <span className="text-sm font-medium text-gray-900">{referrer.source}</span>
                          </div>
                          <div className="flex items-center space-x-4">
                            <span className="text-sm text-gray-600">{referrer.visitors.toLocaleString()} visitors</span>
                            <span className="text-sm font-medium text-gray-900">{referrer.percentage}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Monthly Growth Chart */}
                  <div className="bg-white border border-gray-200 rounded-lg p-6">
                    <h4 className="font-semibold text-gray-900 mb-4">Monthly Performance</h4>
                    <div className="h-64 flex items-end space-x-4">
                      {analytics.monthlyGrowth.map((data) => (
                        <div key={data.month} className="flex-1 flex flex-col items-center">
                          <div className="flex space-x-1 mb-2">
                            <div 
                              className="w-4 bg-blue-600 rounded-t-lg transition-all duration-300"
                              style={{height: `${(data.views / 5000) * 200}px`}}
                            ></div>
                            <div 
                              className="w-4 bg-green-600 rounded-t-lg transition-all duration-300"
                              style={{height: `${(data.sales / 2500) * 200}px`}}
                            ></div>
                          </div>
                          <p className="text-xs text-gray-600">{data.month}</p>
                        </div>
                      ))}
                    </div>
                    <div className="flex justify-center space-x-6 mt-4">
                      <div className="flex items-center space-x-2">
                        <div className="w-3 h-3 bg-blue-600 rounded"></div>
                        <span className="text-sm text-gray-600">Views</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className="w-3 h-3 bg-green-600 rounded"></div>
                        <span className="text-sm text-gray-600">Sales</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* AI Insights */}
          <div className="bg-gradient-to-r from-blue-600 to-cyan-600 p-6 rounded-xl text-white">
            <h3 className="font-semibold mb-4">AI Market Insights</h3>
            <div className="space-y-3">
              <div className="bg-white/20 p-3 rounded-lg">
                <p className="text-sm font-medium">Coffee NFTs trending</p>
                <p className="text-xs opacity-80">+35% interest this week</p>
              </div>
              <div className="bg-white/20 p-3 rounded-lg">
                <p className="text-sm font-medium">Optimal pricing detected</p>
                <p className="text-xs opacity-80">Consider 15% price adjustment</p>
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <Link 
                to="/open-asset-upload-form" 
                className="block w-full text-gray-600 text-left p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <Plus className="h-5 w-5 text-blue-600" />
                  <span className="font-medium">Create New Asset</span>
                </div>
              </Link>
              <Link 
                to="/funding" 
                className="block w-full text-left p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                  <span className="font-medium text-gray-600">View Funding</span>
                </div>
              </Link>
              <Link 
                to="/wallet" 
                className="block w-full text-left p-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center space-x-3">
                  <DollarSign className="h-5 w-5 text-purple-600" />
                  <span className="font-medium text-gray-600">Manage Wallet</span>
                </div>
              </Link>
            </div>
          </div>
        </div>
      </div>
      
      <AssetUploadForm 
        isOpen={isAssetFormOpen} 
        onClose={() => setIsAssetFormOpen(false)} 
      />
    </div>
  );
};

export default CreatorDashboard;

