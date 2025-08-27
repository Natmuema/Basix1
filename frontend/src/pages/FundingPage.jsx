import React, { useState } from 'react';
import { Calculator, TrendingUp, Shield, Clock, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

const FundingPage = () => {
  const [investmentAmount, setInvestmentAmount] = useState(1000);
  const [investmentTerm, setInvestmentTerm] = useState(12);
  const [isAlertsModalOpen, setIsAlertsModalOpen] = useState(false);

  const calculateReturns = () => {
    const monthlyRate = 0.02; // 2% monthly return
    return investmentAmount * Math.pow(1 + monthlyRate, investmentTerm);
  };

  const projectedReturns = calculateReturns();
  const totalGain = projectedReturns - investmentAmount;
  const roiPercentage = ((totalGain / investmentAmount) * 100).toFixed(1);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-cyan-50">
      {/* Header */}
      <div className="bg-gradient-to-r text-black">
        <div className="max-w-7xl mx-auto px-4 py-12">
          <h1 className="text-4xl font-bold mb-3">Investment & Funding</h1>
          <p className="text-gray-500 text-lg">Manage your investments and explore funding opportunities</p>
        </div>
      </div>
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Investment Calculator */}
          <div className="lg:col-span-2 space-y-8">
            <div className="bg-white p-8 rounded-2xl shadow-lg border border-cyan-100">
              <div className="flex items-center space-x-3 mb-6">
                <div className="p-2 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg">
                  <Calculator className="h-6 w-6 text-white" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Investment Calculator</h2>
              </div>
              
              <div className="grid md:grid-cols-2 gap-8">
                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-3">
                      Investment Amount (USD)
                    </label>
                    <div className="relative">
                      <span className=" absolute left-4 top-1/2 -translate-y-1/2 text-gray-600 font-medium">$</span>
                      <input
                        type="number"
                        value={investmentAmount}
                        onChange={(e) => setInvestmentAmount(Number(e.target.value))}
                        className="w-full pl-10 pr-4 py-4 text-gray-700 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-cyan-500 focus:ring-2 focus:ring-cyan-200 transition-all"
                        min="100"
                        step="100"
                      />
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-3">
                      Investment Term (Months)
                    </label>
                    <input
                      type="range"
                      min="3"
                      max="24"
                      value={investmentTerm}
                      onChange={(e) => setInvestmentTerm(Number(e.target.value))}
                      className="w-full h-3 bg-gradient-to-r from-cyan-200 to-blue-200 rounded-lg appearance-none cursor-pointer slider"
                      style={{
                        background: `linear-gradient(to right, #06b6d4 0%, #06b6d4 ${((investmentTerm - 3) / 21) * 100}%, #e2e8f0 ${((investmentTerm - 3) / 21) * 100}%, #e2e8f0 100%)`
                      }}
                    />
                    <div className="flex justify-between text-sm text-gray-600 mt-2">
                      <span>3 months</span>
                      <span className="font-bold text-cyan-600">{investmentTerm} months</span>
                      <span>24 months</span>
                    </div>
                  </div>
                </div>
                
                <div className="bg-gradient-to-br from-cyan-50 via-blue-50 to-white p-6 rounded-xl border border-cyan-200">
                  <h3 className="font-bold text-gray-900 mb-4 text-lg">Projected Returns</h3>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Initial Investment:</span>
                      <span className="font-bold text-lg">${investmentAmount.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Projected Value:</span>
                      <span className="font-bold text-cyan-600 text-lg">${Math.round(projectedReturns).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-600">Total Gain:</span>
                      <span className="font-bold text-cyan-600 text-lg">+${Math.round(totalGain).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between items-center border-t-2 border-cyan-200 pt-4">
                      <span className="text-gray-900 font-bold">ROI:</span>
                      <span className="font-bold text-blue-600 text-2xl">+{roiPercentage}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Funding Opportunities */}
            <div className="bg-white rounded-2xl shadow-lg border border-cyan-100">
              <div className="p-6 border-b border-cyan-100 bg-gradient-to-r from-white to-cyan-50 rounded-t-2xl">
                <h2 className="text-2xl font-bold text-gray-900">Featured Opportunities</h2>
              </div>
              <div className="p-6">
                <div className="space-y-6">
                  {[
                    {
                      title: "Organic Tea Plantation Tokens",
                      creator: "David Mwangi",
                      target: 25000,
                      raised: 18500,
                      backers: 47,
                      roi: "28.5%",
                      risk: "Low",
                      term: "12 months",
                      image: "https://images.pexels.com/photos/1638280/pexels-photo-1638280.jpeg?auto=compress&cs=tinysrgb&w=300"
                    },
                    {
                      title: "Handwoven Textile Collection",
                      creator: "Mary Nyokabi",
                      target: 15000,
                      raised: 8200,
                      backers: 23,
                      roi: "22.1%",
                      risk: "Medium",
                      term: "8 months",
                      image: "https://images.pexels.com/photos/3985062/pexels-photo-3985062.jpeg?auto=compress&cs=tinysrgb&w=300"
                    }
                  ].map((opportunity, index) => (
                    <div key={index} className="border-2 border-gray-100 rounded-xl p-6 hover:border-cyan-300 hover:shadow-lg transition-all duration-300 bg-gradient-to-r from-white to-gray-50">
                      <div className="flex items-start space-x-6">
                        <img 
                          src={opportunity.image} 
                          alt={opportunity.title}
                          className="w-24 h-24 rounded-xl object-cover flex-shrink-0 border-2 border-cyan-100"
                        />
                        <div className="flex-1">
                          <div className="flex items-start justify-between mb-3">
                            <div>
                              <h3 className="font-bold text-gray-900 text-lg">{opportunity.title}</h3>
                              <p className="text-cyan-600 font-medium">by {opportunity.creator}</p>
                            </div>
                            <div className="text-right bg-gradient-to-r from-cyan-500 to-blue-600 text-white px-4 py-2 rounded-lg">
                              <p className="text-xl font-bold">{opportunity.roi}</p>
                              <p className="text-xs opacity-90">Expected ROI</p>
                            </div>
                          </div>
                          
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                            <div className="bg-white p-3 rounded-lg border border-gray-100">
                              <p className="text-xs text-gray-600 font-medium">Target</p>
                              <p className="font-bold text-gray-900">${opportunity.target.toLocaleString()}</p>
                            </div>
                            <div className="bg-white p-3 rounded-lg border border-gray-100">
                              <p className="text-xs text-gray-600 font-medium">Raised</p>
                              <p className="font-bold text-cyan-600">${opportunity.raised.toLocaleString()}</p>
                            </div>
                            <div className="bg-white p-3 rounded-lg border border-gray-100">
                              <p className="text-xs text-gray-600 font-medium">Risk Level</p>
                              <p className={`font-bold ${
                                opportunity.risk === 'Low' ? 'text-green-500' : 
                                opportunity.risk === 'Medium' ? 'text-yellow-500' : 'text-red-500'
                              }`}>{opportunity.risk}</p>
                            </div>
                            <div className="bg-white p-3 rounded-lg border border-gray-100">
                              <p className="text-xs text-gray-600 font-medium">Term</p>
                              <p className="font-bold text-blue-600">{opportunity.term}</p>
                            </div>
                          </div>
                          
                          <div className="mb-4">
                            <div className="w-full bg-gray-200 rounded-full h-3">
                              <div 
                                className="bg-gradient-to-r from-cyan-500 to-blue-500 h-3 rounded-full transition-all duration-500" 
                                style={{width: `${(opportunity.raised / opportunity.target) * 100}%`}}
                              ></div>
                            </div>
                          </div>
                          
                          <div className="flex items-center justify-between">
                            <div className="text-sm text-gray-600">
                              <span className="font-medium text-blue-600">{opportunity.backers} backers</span> • {Math.round((opportunity.raised / opportunity.target) * 100)}% funded
                            </div>
                            <button className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white px-6 py-3 rounded-lg hover:from-cyan-600 hover:to-blue-700 transition-all duration-300 flex items-center font-medium shadow-lg">
                              Invest Now
                              <ArrowRight className="h-4 w-4 ml-2" />
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
            {/* Market Insights */}
            <div className="bg-gradient-to-br from-blue-600 via-cyan-600 to-cyan-500 p-6 rounded-2xl text-white shadow-lg">
              <h3 className="font-bold mb-4 flex items-center text-lg">
                <TrendingUp className="h-6 w-6 mr-3" />
                Market Insights
              </h3>
              <div className="space-y-3">
                <div className="bg-white/20 backdrop-blur-sm p-4 rounded-lg border border-white/30">
                  <p className="text-sm font-bold">Hot Sector</p>
                  <p className="text-xs opacity-90">Sustainable Agriculture +42%</p>
                </div>
                <div className="bg-white/20 backdrop-blur-sm p-4 rounded-lg border border-white/30">
                  <p className="text-sm font-bold">AI Prediction</p>
                  <p className="text-xs opacity-90">Coffee assets trending up</p>
                </div>
                <div className="bg-white/20 backdrop-blur-sm p-4 rounded-lg border border-white/30">
                  <p className="text-sm font-bold">Risk Alert</p>
                  <p className="text-xs opacity-90">Diversification recommended</p>
                </div>
              </div>
            </div>

            {/* Investment Tips */}
            <div className="bg-white p-6 rounded-2xl shadow-lg border border-cyan-100">
              <h3 className="font-bold text-gray-900 mb-4 flex items-center text-lg">
                <div className="p-2 bg-gradient-to-r from-green-400 to-cyan-500 rounded-lg mr-3">
                  <Shield className="h-5 w-5 text-white" />
                </div>
                Smart Investing
              </h3>
              <div className="space-y-4">
                {[
                  "Diversify across multiple assets to reduce risk",
                  "Start with smaller amounts to test the market", 
                  "Consider longer terms for better returns",
                  "Monitor AI insights for market trends"
                ].map((tip, index) => (
                  <div key={index} className="flex items-start space-x-3 p-3 bg-gradient-to-r from-cyan-50 to-blue-50 rounded-lg border border-cyan-100">
                    <div className="w-2 h-2 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                    <p className="text-sm text-gray-700 font-medium">{tip}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white p-6 rounded-2xl shadow-lg border border-cyan-100">
              <h3 className="font-bold text-gray-900 mb-4 text-lg">Quick Actions</h3>
              <div className="space-y-3">
                <Link to="/portfolio" className="w-full bg-gradient-to-r from-cyan-500 to-blue-600 text-white py-4 px-4 rounded-xl hover:from-cyan-600 hover:to-blue-700 transition-all duration-300 text-left flex items-center font-medium shadow-lg">
                  <TrendingUp className="h-5 w-5 mr-3" />
                  View Portfolio Performance
                </Link>

                <Link to="/investment-alerts" className="w-full border-2 border-cyan-200 text-gray-700 py-4 px-4 rounded-xl hover:bg-gradient-to-r hover:from-cyan-50 hover:to-blue-50 hover:border-cyan-300 transition-all duration-300 text-left flex items-center font-medium">
                  <Clock className="h-5 w-5 mr-3 text-cyan-600" />
                  Set Investment Alerts
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          height: 20px;
          width: 20px;
          border-radius: 50%;
          background: linear-gradient(135deg, #06b6d4, #2563eb);
          cursor: pointer;
          border: 2px solid white;
          box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }

        .slider::-moz-range-thumb {
          height: 20px;
          width: 20px;
          border-radius: 50%;
          background: linear-gradient(135deg, #06b6d4, #2563eb);
          cursor: pointer;
          border: 2px solid white;
          box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }
      `}</style>
    </div>
  );
};

export default FundingPage;
