import React, { useState, useEffect } from 'react';
import {cards, featuredAssets} from '../constants';
import { ArrowRight, Play, Sparkles } from 'lucide-react';
import AssetCard from '../components/AssetCard';
import { Link } from 'react-router-dom';

const Homepage = () => {
      const [displayedText, setDisplayedText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isTypingComplete, setIsTypingComplete] = useState(false);
  
  const fullText = "Empowering local creators with AI + blockchain";
  const typingSpeed = 80; // milliseconds per character
  
   useEffect(() => {
    if (currentIndex < fullText.length) {
      const timer = setTimeout(() => {
        setDisplayedText(fullText.slice(0, currentIndex + 1));
        setCurrentIndex(currentIndex + 1);
      }, typingSpeed);
      
      return () => clearTimeout(timer);
    } else {
      setIsTypingComplete(true);
    }
  }, [currentIndex, fullText]);
  return (
    <>
    <div className="min-h-screen bg-gradient-to-br from-navy-900 via-blue-900 to-slate-900 text-white overflow-hidden relative" id='home'
      style={{background: 'linear-gradient(135deg, #1e293b 0%, #1e3a8a 35%, #0f172a 100%)'}}>
        {/*Hero Section */}
      <section >
        <div className="relative overflow-hidden min-h-screen flex items-center justify-center bg-gradient-to-br from-navy-900 via-blue-900 to-slate-900"
        style={{background: 'linear-gradient(135deg, #1e293b 0%, #1e3a8a 35%, #0f172a 100%)'}}>
  
      
          <div className="text-center space-y-8">
            <div className="inline-flex items-center space-x-2 bg-white/80 backdrop-blur-sm border border-cyan-200 rounded-full px-4 py-2 text-sm font-medium bg-gradient-to-r from-cyan-400 to-blue-400">
              <Sparkles className="w-4 h-4" />
              <span>MeTTa-Powered AI Marketplace</span>
            </div>
      
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-slate-500-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-72 h-72 bg-gray-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-4000"></div>
      </div>
      {/* Hero Content */} 
        <div className="text-center max-w-4xl mx-auto">
          {/* Main Heading with Typing Effect */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
            <span className="inline-block">
              {displayedText}
              <span className={`inline-block w-1 h-12 sm:h-16 lg:h-20 bg-white ml-1 ${isTypingComplete ? 'animate-pulse' : 'animate-pulse'}`}></span>
            </span>
          </h1>
          <p className={`text-xl sm:text-2xl text-gray-200 mb-8 max-w-3xl mx-auto transition-opacity duration-1000 ${isTypingComplete ? 'opacity-100' : 'opacity-0'}`}>
             Marketplace connecting local creators with global investors. 
              Tokenize physical assets, collaborate on IP, and build sustainable revenue streams 
              through blockchain technology.
          </p>

          {/* Action Buttons */}
          <div className={`flex flex-col sm:flex-row gap-4 justify-center transition-all duration-1000 ${isTypingComplete ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
            <Link to="/login" className="group bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 px-8 py-4 rounded-full font-semibold text-lg hover:bg-gray-100 transform hover:scale-105 transition-all duration-300 flex items-center justify-center shadow-xl hover:shadow-2xl">
              Get Started
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
            </Link>

            <Link to="/demo" className="group border-2 border-white text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-cyan-500 hover:text-white-900 transform hover:scale-105 transition-all duration-300 flex items-center justify-center shadow-xl hover:shadow-2xl">
              <Play className="mr-2 w-5 h-5 group-hover:scale-110 transition-transform duration-300" />
              Watch Demo
            </Link>
          </div>
          {/* Stats Section */}
          <div className={`mt-16 grid grid-cols-1 sm:grid-cols-3 gap-8 transition-all duration-1000 delay-500 ${isTypingComplete ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
            <div className="text-center">
              <div className="text-3xl sm:text-4xl font-bold text-white mb-2">1000+</div>
              <div className="text-gray-300">Active Creators</div>
            </div>
            <div className="text-center">
              <div className="text-3xl sm:text-4xl font-bold text-white mb-2">$2.5M+</div>
              <div className="text-gray-300">Funds Raised</div>
            </div>
            <div className="text-center">
              <div className="text-3xl sm:text-4xl font-bold text-white mb-2">50+</div>
              <div className="text-gray-300">Projects Launched</div>
            </div>
          </div>
        </div>
      </div>
      {/* Scroll Indicator */}
      <div className={`absolute bottom-8 left-1/2 transform -translate-x-1/2 text-white animate-bounce transition-opacity duration-1000 delay-1000 ${isTypingComplete ? 'opacity-100' : 'opacity-0'}`}>
        <div className="w-6 h-10 border-2 border-white rounded-full flex justify-center">
          <div className="w-1 h-3 bg-white rounded-full mt-2 animate-pulse"></div>
        </div>
      </div>
    </div>
      </section>

      {/*Card Section*/}
        <section className="bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16 space-y-5">
          <h2 className="text-4xl font-bold text-gray-900">
            Built for the{" "}
            <span className="text-4xl font-bold bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent">
              Future of Commerce
            </span>
          </h2> 
          <p className="text-xl text-gray-700 max-w-3xl mx-auto">
            Advanced AI agents handle pricing, funding, and provenance while you focus on creating.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {cards.map((feature, index) => (
            <div 
              key={index} 
              className="group p-8 bg-white/70 backdrop-blur-sm border border-white/50 rounded-2xl shadow-lg hover:shadow-xl hover:bg-white/80 transition-all duration-300 hover:scale-[1.02] hover:-translate-y-1"
            >
              <div className="p-3 bg-gradient-to-br from-cyan-500/10 to-blue-500/10 rounded-xl w-fit mb-6 group-hover:scale-110 group-hover:bg-gradient-to-br group-hover:from-cyan-500/20 group-hover:to-blue-500/20 transition-all duration-300">
                <feature.icon className="w-6 h-6 text-cyan-600 group-hover:text-cyan-700" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4 group-hover:text-cyan-700 transition-colors">
                {feature.title}
              </h3>
              <p className="text-gray-600 leading-relaxed group-hover:text-gray-700 transition-colors">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>

      <section className="bg-gray-50 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header Section - Improved */}
        <div className="mb-16">
          <div className="flex flex-col md:flex-row md:justify-between md:items-end gap-6">
            <div className="text-center md:text-left">
              <h2 className="text-4xl font-bold text-gray-900 mb-3">
                Featured <span className="bg-gradient-to-r from-cyan-600 to-blue-600 bg-clip-text text-transparent">Assets</span>
              </h2>
              <p className="text-xl text-gray-600">Discover trending creations from our community</p>
            </div>
            <a
              href="/assets"
              className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-xl hover:from-cyan-600 hover:to-blue-600 transition-all duration-300 group w-fit mx-auto md:mx-0 shadow-lg hover:shadow-xl"
            >
              <span className="font-medium">View All Assets</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
            </a>
          </div>
        </div>

        {/* Assets Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {featuredAssets.map((asset) => (
            <AssetCard key={asset.id} asset={asset} />
          ))}
        </div>

        {/* Optional: Show more assets hint */}
        <div className="text-center mt-12">
          <p className="text-gray-500">
            Showing 3 of 1,247 assets. 
            <a href="/assets" className="text-cyan-600 hover:text-cyan-700 font-medium ml-1">
              Browse all →
            </a>
          </p>
        </div>
      </div>
    </section>

    <section className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">Ready to Transform Your Ideas?</h2>
          <p className="text-xl text-gray-600 mb-10">
            Join the revolution of creators building sustainable revenue streams 
            through AI-powered asset tokenization.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/register" 
              className="inline-flex items-center justify-center bg-gradient-to-r from-cyan-600 to-blue-600 px-10 py-4 rounded-lg transition-all transform hover:scale-105 font-medium text-lg"
            >
              Start Your Journey
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </div>
        </div>
      </section>
    </div>
      

      
    </>
  )
}

export default Homepage