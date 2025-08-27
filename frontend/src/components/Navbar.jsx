import React, { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { User, Wallet, Menu, X, Bell } from 'lucide-react';
import { useAuth } from '../context/Authcontext';

const Navbar = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <nav className="sticky top-0 z-50 bg-transparent">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 backdrop-blur-lg rounded-2xl px-8 py-4 border border-blue-500/20 shadow-lg my-4 text-white">
          {/* Logo */}
          <div className="flex-shrink-0">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
              Basix IP
            </h1>
            <p className="text-xs font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
              Marketplace
            </p>
          </div>

          {/* Desktop Navigation Links */}
          <div className="hidden md:block">
            <div className="flex items-center space-x-8">
              <NavLink
                to="/"
                className="px-4 py-3 text-lg font-bold text-white hover:text-cyan-400 hover:bg-blue-500/10 rounded-lg transition-colors"
              >
                Home
              </NavLink>
              {isAuthenticated && (
                <>
                  <NavLink
                    to="/dashboard"
                    className="px-4 py-3 text-lg font-bold text-white hover:text-cyan-400 hover:bg-blue-500/10 rounded-lg transition-colors"
                  >
                    Dashboard
                  </NavLink>
                  <NavLink
                    to="/assets"
                    className="px-4 py-3 text-lg font-bold text-white hover:text-cyan-400 hover:bg-blue-500/10 rounded-lg transition-colors"
                  >
                    Assets
                  </NavLink>
                  <NavLink
                    to="/funding"
                    className="px-4 py-3 text-lg font-bold text-white hover:text-cyan-400 hover:bg-blue-500/10 rounded-lg transition-colors"
                  >
                    Funding
                  </NavLink>
                </>
              )}
            </div>
          </div>

          {/* Desktop Action Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated && (
              <button className="p-2 text-cyan-400 hover:text-white transition-colors">
                <Bell className="h-5 w-5" />
              </button>
            )}
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-cyan-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-semibold">
                      {user?.name?.charAt(0) || user?.email?.charAt(0) || 'U'}
                    </span>
                  </div>
                  <span className="text-white font-medium">
                    {user?.name || user?.email}
                  </span>
                </div>
                <button 
                  onClick={handleLogout}
                  className="flex items-center space-x-2 bg-gradient-to-r from-red-500 to-red-600 text-white px-4 py-2 rounded-lg hover:from-red-600 hover:to-red-700 transition-colors"
                >
                  <span>Logout</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <Link to="/login">
                  <button className="flex items-center space-x-2 bg-gradient-to-r from-cyan-400 to-blue-400 text-white px-4 py-2 rounded-lg hover:from-cyan-500 hover:to-blue-500 transition-colors">
                    <User className="h-4 w-4" />
                    <span>Login</span>
                  </button>
                </Link>
                <Link to="/register">
                  <button className="flex items-center space-x-2 bg-gradient-to-r from-green-500 to-green-600 text-white px-4 py-2 rounded-lg hover:from-green-600 hover:to-green-700 transition-colors">
                    <span>Register</span>
                  </button>
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={toggleMobileMenu}
              className="text-white hover:text-cyan-400 p-2 rounded-md transition-colors"
            >
              {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden">
          <div className="mx-4 mb-4 px-6 py-4 space-y-2 bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 backdrop-blur-lg rounded-2xl border border-blue-500/20 shadow-lg text-white">
            <NavLink
              to="/"
              className="block px-4 py-3 font-bold text-white hover:text-cyan-400 hover:bg-blue-500/10 rounded-lg transition-colors"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Home
            </NavLink>
            {isAuthenticated && (
              <>
                <NavLink
                  to="/dashboard"
                  className="block px-4 py-3 font-bold text-white hover:text-cyan-400 hover:bg-blue-500/10 rounded-lg transition-colors"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Dashboard
                </NavLink>
                <NavLink
                  to="/assets"
                  className="block px-4 py-3 font-bold text-white hover:text-cyan-400 hover:bg-blue-500/10 rounded-lg transition-colors"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Assets
                </NavLink>
                <NavLink
                  to="/funding"
                  className="block px-4 py-3 font-bold text-white hover:text-cyan-400 hover:bg-blue-500/10 rounded-lg transition-colors"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Funding
                </NavLink>
              </>
            )}
            
            <div className="pt-4 space-y-2">
              {isAuthenticated ? (
                <button
                  onClick={() => {
                    handleLogout();
                    setIsMobileMenuOpen(false);
                  }}
                  className="w-full bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white px-4 py-3 rounded-lg flex items-center justify-center space-x-2 font-medium transition-all"
                >
                  <span>Logout</span>
                </button>
              ) : (
                <>
                  <Link
                    to="/login"
                    className="flex items-center justify-center space-x-2 w-full px-4 py-3 border border-blue-400/20 hover:bg-blue-500/10 text-white rounded-lg transition-colors font-medium"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <User size={16} />
                    <span>Login</span>
                  </Link>
                  <Link
                    to="/register"
                    className="w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white px-4 py-3 rounded-lg flex items-center justify-center space-x-2 font-medium transition-all"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <span>Register</span>
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;