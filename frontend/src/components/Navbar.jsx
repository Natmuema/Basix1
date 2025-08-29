import React, { useState } from 'react';
import { TrendingUp, Menu, X, User, Bell } from 'lucide-react';
import { Link, NavLink } from 'react-router-dom';
import { useAuth } from '../context/Authcontext';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
  };

  return (
    <header className="bg-transparent shadow-sm border-b border-transparent sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="bg-green-700 p-2 rounded-lg">
              <TrendingUp className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">ChumsGrow</h1>
              <p className="text-xs text-gray-500">Your Path to Smarter Investments</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <NavLink to="/" className="text-gray-700 hover:text-green-700 font-medium transition-colors">
              Home
            </NavLink>
            <NavLink to="/risk-profiler" className="text-gray-700 hover:text-green-700 font-medium transition-colors">
              Risk Profiler
            </NavLink>
            <NavLink to="/learning-hub" className="text-gray-700 hover:text-green-700 font-medium transition-colors">
              Learning Hub
            </NavLink>
            <NavLink to="/insights" className="text-gray-700 hover:text-green-700 font-medium transition-colors">
              Market Insights
            </NavLink>
          </nav>

          {/* Actions */}
          <div className="hidden md:flex items-center space-x-4">
            <button className="p-2 text-gray-400 hover:text-gray-600 transition-colors">
              <Bell className="h-5 w-5" />
            </button>
            {isAuthenticated() ? (
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-green-700 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-semibold">
                      {user?.full_name?.charAt(0) || user?.username?.charAt(0) || 'U'}
                    </span>
                  </div>
                  <span className="text-gray-700 font-medium">
                    {user?.full_name || user?.username}
                  </span>
                </div>
                <button 
                  onClick={handleLogout}
                  className="flex items-center space-x-2 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
                >
                  <span>Logout</span>
                </button>
              </div>
            ) : (
              <NavLink to="/auth">
                <button className="flex items-center space-x-2 bg-green-700 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors">
                  <User className="h-4 w-4" />
                  <span>Login</span>
                </button>
              </NavLink>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-2 text-gray-400 hover:text-gray-600"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-200">
            <nav className="flex flex-col space-y-4">
              <NavLink to="/" className="text-gray-700 hover:text-green-600 font-medium transition-colors">
                Home
              </NavLink>
              <NavLink to="/risk-profiler" className="text-gray-700 hover:text-green-600 font-medium transition-colors">
                Risk Profiler
              </NavLink>
              <NavLink to="/learning-hub" className="text-gray-700 hover:text-green-600 font-medium transition-colors">
                Learning Hub
              </NavLink>
              <NavLink to="/insights" className="text-gray-700 hover:text-green-600 font-medium transition-colors">
                Market Insights
              </NavLink>
              {isAuthenticated() ? (
                <button 
                  onClick={handleLogout}
                  className="flex items-center space-x-2 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors w-full justify-center"
                >
                  <span>Logout</span>
                </button>
              ) : (
                <NavLink to="/auth">
                  <button className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors w-full justify-center">
                    <User className="h-4 w-4" />
                    <span>Login</span>
                  </button>
                </NavLink>
              )}
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Navbar;