import React, { useState } from 'react';
import { Wallet, Send, ArrowDownLeft, ArrowUpRight, Shield, Copy, ExternalLink, CreditCard, TrendingUp, Eye, EyeOff} from 'lucide-react';
import {walletData} from '../constants';

const WalletPage = () => {
  const [selectedTab, setSelectedTab] = useState('overview');
  const [showBalance, setShowBalance] = useState(true);

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Address copied to clipboard!');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900" id='wallet'>
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent mb-2">
            Cardano Wallet
          </h1>
          <p className="text-slate-300 text-lg">Manage your ADA and asset tokens</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Balance Card - Same as Main Wallet */}
            <div className="bg-gradient-to-br from-slate-800 via-blue-800 to-slate-900 p-6 rounded-2xl shadow-xl text-white border border-cyan-400/20">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className="bg-cyan-400/20 p-3 rounded-xl backdrop-blur-sm">
                    <Wallet className="h-8 w-8 text-cyan-300" />
                  </div>
                  <h2 className="text-2xl font-bold">Main Wallet</h2>
                </div>
                <div className="flex items-center space-x-3">
                  <button
                    onClick={() => setShowBalance(!showBalance)}
                    className="bg-cyan-400/20 hover:bg-cyan-400/30 p-2 rounded-lg transition-all duration-200"
                  >
                    {showBalance ? (
                      <Eye className="h-5 w-5 text-cyan-300" />
                    ) : (
                      <EyeOff className="h-5 w-5 text-cyan-300" />
                    )}
                  </button>
                  <div className="bg-cyan-400/20 p-2 rounded-lg">
                    <Shield className="h-6 w-6 text-cyan-300" />
                  </div>
                </div>
              </div>
              
              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  <p className="text-slate-300 mb-2 text-sm font-medium">ADA Balance</p>
                  <p className="text-5xl font-bold mb-2">
                    {showBalance ? walletData.balance.ada.toLocaleString() : '••••••'}
                  </p>
                  <p className="text-slate-300 text-lg">
                    ≈ {showBalance ? `${walletData.balance.usd.toLocaleString()} USD` : '$•••••• USD'}
                  </p>
                </div>
                <div className="flex flex-col justify-center">
                  <div className="bg-white/10 p-5 rounded-xl backdrop-blur-sm border border-white/20">
                    <p className="text-sm text-slate-300 mb-2 font-medium">Wallet Address</p>
                    <div className="flex items-center space-x-3">
                      <code className="text-sm font-mono truncate text-white/90">
                        {walletData.address.substring(0, 20)}...
                      </code>
                      <button 
                        onClick={() => copyToClipboard(walletData.address)}
                        className="bg-white/20 hover:bg-white/30 p-2 rounded-lg transition-all duration-200 hover:scale-105"
                      >
                        <Copy className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <button className="bg-gradient-to-br from-slate-800 via-blue-800 to-slate-900 p-6 rounded-2xl shadow-xl text-white border border-cyan-400/20 hover:bg-white/5 transition-all duration-300 hover:scale-105 group">
                <div className="bg-white/20 p-3 rounded-xl mx-auto mb-3 w-fit group-hover:bg-cyan-400/30 transition-colors">
                  <Send className="h-6 w-6 text-white" />
                </div>
                <p className="font-semibold text-white">Send</p>
              </button>
              <button className="bg-gradient-to-br from-slate-800 via-blue-800 to-slate-900 p-6 rounded-2xl shadow-xl text-white border border-cyan-400/20 hover:bg-white/5 transition-all duration-300 hover:scale-105 group">
                <div className="bg-white/20 p-3 rounded-xl mx-auto mb-3 w-fit group-hover:bg-cyan-400/30 transition-colors">
                  <ArrowDownLeft className="h-6 w-6 text-white" />
                </div>
                <p className="font-semibold text-white">Receive</p>
              </button>
              <button className="bg-gradient-to-br from-slate-800 via-blue-800 to-slate-900 p-6 rounded-2xl shadow-xl text-white border border-cyan-400/20 hover:bg-white/5 transition-all duration-300 hover:scale-105 group">
                <div className="bg-white/20 p-3 rounded-xl mx-auto mb-3 w-fit group-hover:bg-cyan-400/30 transition-colors">
                  <CreditCard className="h-6 w-6 text-white" />
                </div>
                <p className="font-semibold text-white">Buy ADA</p>
              </button>
              <button className="bg-gradient-to-br from-slate-800 via-blue-800 to-slate-900 p-6 rounded-2xl shadow-xl text-white border border-cyan-400/20 hover:bg-white/5 transition-all duration-300 hover:scale-105 group">
                <div className="bg-white/20 p-3 rounded-xl mx-auto mb-3 w-fit group-hover:bg-cyan-400/30 transition-colors">
                  <ExternalLink className="h-6 w-6 text-white" />
                </div>
                <p className="font-semibold text-white">Stake</p>
              </button>
            </div>

            {/* Tabs Content - Similar to Main Wallet Style */}
            <div className="bg-gradient-to-br from-slate-800 via-blue-800 to-slate-900 rounded-2xl shadow-lg border border-cyan-400/20">
              <div className="border-b border-slate-200/20">
                <nav className="flex space-x-8 px-6">
                  {[
                    { id: 'overview', label: 'Overview' },
                    { id: 'transactions', label: 'Transactions' },
                    { id: 'tokens', label: 'Assets & Tokens' }
                  ].map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setSelectedTab(tab.id)}
                      className={`py-4 px-2 border-b-2 font-semibold text-sm transition-all duration-200 ${
                        selectedTab === tab.id
                          ? 'border-cyan-400 text-cyan-300'
                          : 'border-transparent text-slate-400 hover:text-white hover:border-slate-400'
                      }`}
                    >
                      {tab.label}
                    </button>
                  ))}
                </nav>
              </div>

              <div className="p-6 text-white">
                {selectedTab === 'overview' && (
                  <div className="grid md:grid-cols-2 gap-8">
                    <div>
                      <h3 className="font-bold text-white mb-6 text-lg">Portfolio Value</h3>
                      <div className="space-y-4">
                        <div className="flex justify-between items-center p-3 bg-white/10 rounded-lg border border-white/20">
                          <span className="text-slate-300 font-medium">ADA Holdings</span>
                          <span className="font-bold text-white">
                            {showBalance ? `${walletData.balance.usd.toLocaleString()}` : '$••••••'}
                          </span>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-white/10 rounded-lg border border-white/20">
                          <span className="text-slate-300 font-medium">Asset Tokens</span>
                          <span className="font-bold text-white">
                            {showBalance ? '$3,640.00' : '$••••••'}
                          </span>
                        </div>
                        <div className="flex justify-between items-center p-4 bg-white/10 rounded-lg border border-cyan-400/30">
                          <span className="font-bold text-white">Total Value</span>
                          <span className="font-bold text-xl text-cyan-300">
                            {showBalance ? `${(walletData.balance.usd + 3640).toLocaleString()}` : '$••••••'}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div>
                      <h3 className="font-bold text-white mb-6 text-lg">Recent Activity</h3>
                      <div className="space-y-4">
                        {walletData.transactions.slice(0, 3).map((tx) => (
                          <div key={tx.id} className="flex items-center justify-between p-4 bg-white/10 rounded-xl hover:bg-white/20 transition-colors border border-white/20">
                            <div className="flex items-center space-x-4">
                              <div className={`p-2 rounded-lg ${
                                tx.type === 'receive' ? 'bg-cyan-400/20' : 'bg-white/20'
                              }`}>
                                {tx.type === 'receive' ? (
                                  <ArrowDownLeft className="h-5 w-5 text-cyan-300" />
                                ) : (
                                  <ArrowUpRight className="h-5 w-5 text-white" />
                                )}
                              </div>
                              <div>
                                <p className="font-semibold text-white">{tx.type === 'receive' ? 'Received' : 'Sent'}</p>
                                <p className="text-sm text-slate-300">{tx.timestamp}</p>
                              </div>
                            </div>
                            <span className={`font-bold ${tx.type === 'receive' ? 'text-cyan-300' : 'text-white'}`}>
                              {showBalance ? `${tx.type === 'receive' ? '+' : '-'}${tx.amount} ADA` : '•••• ADA'}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {selectedTab === 'transactions' && (
                  <div className="space-y-6">
                    <div className="flex justify-between items-center">
                      <h3 className="font-bold text-white text-lg">Transaction History</h3>
                      <button className="bg-cyan-400 hover:bg-cyan-500 text-slate-900 px-4 py-2 rounded-lg font-semibold transition-colors">
                        View All
                      </button>
                    </div>
                    {walletData.transactions.map((tx) => (
                      <div key={tx.id} className="bg-white/10 border border-white/20 rounded-xl p-5 hover:bg-white/20 transition-all duration-200">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-4">
                            <div className={`p-3 rounded-xl ${
                              tx.type === 'receive' ? 'bg-cyan-400/20' : 'bg-white/20'
                            }`}>
                              {tx.type === 'receive' ? (
                                <ArrowDownLeft className="h-6 w-6 text-cyan-300" />
                              ) : (
                                <ArrowUpRight className="h-6 w-6 text-white" />
                              )}
                            </div>
                            <div>
                              <p className="font-bold text-white">{tx.type === 'receive' ? tx.from : tx.to}</p>
                              <p className="text-slate-300">{tx.timestamp}</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className={`font-bold text-lg ${
                              tx.type === 'receive' ? 'text-cyan-300' : 'text-white'
                            }`}>
                              {showBalance ? `${tx.type === 'receive' ? '+' : '-'}${tx.amount} ${tx.asset}` : '•••• ADA'}
                            </p>
                            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-cyan-400/20 text-cyan-300">
                              {tx.status}
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {selectedTab === 'tokens' && (
                  <div className="space-y-6">
                    <h3 className="font-bold text-white text-lg">Your Assets & Tokens</h3>
                    {walletData.tokens.map((token, index) => (
                      <div key={index} className="bg-white/10 border border-white/20 rounded-xl p-5 hover:bg-white/20 transition-all duration-200">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-4">
                            <div className="w-14 h-14 bg-gradient-to-r from-cyan-400 to-blue-500 rounded-xl flex items-center justify-center text-white font-bold text-lg shadow-lg">
                              {token.symbol.charAt(0)}
                            </div>
                            <div>
                              <p className="font-bold text-white text-lg">{token.name}</p>
                              <p className="text-slate-300 font-medium">{token.symbol}</p>
                            </div>
                          </div>
                          <div className="text-right">
                            <p className="font-bold text-xl text-white">
                              {showBalance ? token.balance.toLocaleString() : '••••••'}
                            </p>
                            <div className="flex items-center space-x-3">
                              <span className="text-slate-300 font-medium">
                                {showBalance ? token.value : '$••••••'}
                              </span>
                              <span className={`text-sm font-bold px-2 py-1 rounded-full ${
                                token.change.startsWith('+') 
                                  ? 'bg-cyan-400/20 text-cyan-300' 
                                  : 'bg-white/20 text-white'
                              }`}>
                                {showBalance ? token.change : '••••'}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Sidebar - Matching Main Wallet Style */}
          <div className="space-y-6">
            {/* Staking Rewards */}
            <div className="bg-gradient-to-br from-slate-800 via-blue-800 to-slate-900 p-6 rounded-2xl shadow-xl text-white border border-cyan-400/20">
              <h3 className="font-bold mb-6 text-lg flex items-center">
                <div className="bg-white/20 p-2 rounded-lg mr-3">
                  <ExternalLink className="h-5 w-5" />
                </div>
                Staking Rewards
              </h3>
              <div className="space-y-4">
                <div className="bg-white/10 p-4 rounded-xl backdrop-blur-sm border border-white/20">
                  <p className="text-slate-300 text-sm font-medium mb-1">Staked Amount</p>
                  <p className="text-3xl font-bold">
                    {showBalance ? '1,500 ADA' : '•••• ADA'}
                  </p>
                </div>
                <div className="bg-white/10 p-4 rounded-xl backdrop-blur-sm border border-white/20">
                  <p className="text-slate-300 text-sm font-medium mb-1">Rewards Earned</p>
                  <p className="text-xl font-bold text-cyan-300">
                    {showBalance ? '+68.5 ADA' : '+•• ADA'}
                  </p>
                </div>
                <div className="bg-white/10 p-4 rounded-xl backdrop-blur-sm border border-white/20">
                  <p className="text-slate-300 text-sm font-medium mb-1">APY</p>
                  <p className="text-xl font-bold text-cyan-300">4.2%</p>
                </div>
              </div>
            </div>

            {/* Wallet Security */}
            <div className="bg-gradient-to-br from-slate-800 via-blue-800 to-slate-900 p-6 rounded-2xl shadow-xl text-white border border-cyan-400/20">
              <h3 className="font-bold text-white mb-6 flex items-center text-lg">
                <div className="bg-white/20 p-2 rounded-lg mr-3">
                  <Shield className="h-5 w-5 text-cyan-300" />
                </div>
                Security Status
              </h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-white/10 rounded-lg border border-white/20">
                  <span className="font-medium text-slate-300">Hardware Wallet</span>
                  <span className="text-cyan-300 font-bold">Connected</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-white/10 rounded-lg border border-white/20">
                  <span className="font-medium text-slate-300">2FA Enabled</span>
                  <span className="text-cyan-300 font-bold">Active</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-white/10 rounded-lg border border-white/20">
                  <span className="font-medium text-slate-300">Backup Status</span>
                  <span className="text-cyan-300 font-bold">Complete</span>
                </div>
              </div>
            </div>

            {/* Quick Stats */}
            <div className="bg-gradient-to-br from-slate-800 via-blue-800 to-slate-900 p-6 rounded-2xl shadow-xl text-white border border-cyan-400/20">
              <h3 className="font-bold text-white mb-6 text-lg">Network Stats</h3>
              <div className="space-y-4">
                <div className="flex justify-between p-3 bg-white/10 rounded-lg border border-white/20">
                  <span className="font-medium text-slate-300">Current Epoch</span>
                  <span className="font-bold text-white">428</span>
                </div>
                <div className="flex justify-between p-3 bg-white/10 rounded-lg border border-white/20">
                  <span className="font-medium text-slate-300">Block Height</span>
                  <span className="font-bold text-white">8,234,567</span>
                </div>
                <div className="flex justify-between p-3 bg-white/10 rounded-lg border border-white/20">
                  <span className="font-medium text-slate-300">Network Fee</span>
                  <span className="font-bold text-cyan-300">0.17 ADA</span>
                </div>
                <div className="flex justify-between p-3 bg-white/10 rounded-lg border border-white/20">
                  <span className="font-medium text-slate-300">Confirmation Time</span>
                  <span className="font-bold text-cyan-300">~20 sec</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WalletPage;