import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Package, ArrowRight, Eye, EyeOff, User, Building } from 'lucide-react';
import { useAuth } from '../context/Authcontext';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    userType: 'creator'
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const { login, isLoading } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Client-side validation
    if (!formData.email.trim()) {
      setError('Please enter your email address');
      return;
    }

    if (!formData.password.trim()) {
      setError('Please enter your password');
      return;
    }

    try {
      await login(formData.email, formData.password, formData.userType);
      navigate('/dashboard');
    } catch (error) {
      setError(error.message || 'Login failed. Please check your credentials.');
    }
  };

  return (
    <div className="min-h-screen " id='login'>
      <div className="flex min-h-screen">
        {/* Left Side - Branding */}
        <div className="hidden lg:flex lg:w-1/2 flex-col justify-center px-12 text-white">
          <div className="mb-8">
            <div className="flex items-center space-x-2 mb-6">
              <Package className="h-10 w-10 text-blue-400" />
              <span className="font-bold text-3xl">BASIX IP Marketplace</span>
            </div>
            <h1 className="text-4xl font-bold mb-4">
              Welcome Back to the
              <span className="text-blue-400"> Future</span>
            </h1>
            <p className="text-xl text-blue-100 leading-relaxed">
              Continue building your asset portfolio and connecting with 
              global opportunities on Africa's leading IP marketplace.
            </p>
          </div>
        </div>

        {/* Right Side - Login Form */}
        <div className="flex-1 flex flex-col justify-center px-8 py-12 lg:px-12">
          <div className="max-w-md mx-auto w-full">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-white mb-2">Sign In</h2>
              <p className="text-blue-200">Access your BASIX account</p>
            </div>

            {/* Error Message */}
            {error && (
              <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-300 text-sm">
                {error}
              </div>
            )}

            {/* User Type Selection */}
            <div className="mb-8">
              <div className="grid grid-cols-2 gap-4">
                <button
                  type="button"
                  onClick={() => setFormData({...formData, userType: 'creator'})}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    formData.userType === 'creator' 
                      ? 'border-blue-400 bg-blue-400/20 text-white' 
                      : 'border-gray-600 bg-gray-800/50 text-gray-300 hover:border-blue-500'
                  }`}
                >
                  <User className="h-6 w-6 mx-auto mb-2" />
                  <div className="font-medium text-sm">Creator</div>
                </button>
                
                <button
                  type="button"
                  onClick={() => setFormData({...formData, userType: 'investor'})}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    formData.userType === 'investor' 
                      ? 'border-blue-400 bg-blue-400/20 text-white' 
                      : 'border-gray-600 bg-gray-800/50 text-gray-300 hover:border-blue-500'
                  }`}
                >
                  <Building className="h-6 w-6 mx-auto mb-2" />
                  <div className="font-medium text-sm">Investor</div>
                </button>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-blue-200 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  className="w-full px-4 py-3 bg-gray-800/50 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-400 text-white placeholder-gray-400"
                  placeholder="Enter your email"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-blue-200 mb-2">
                  Password
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    className="w-full px-4 py-3 bg-gray-800/50 border border-gray-600 rounded-lg focus:outline-none focus:border-blue-400 text-white placeholder-gray-400 pr-12"
                    placeholder="Enter your password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
                  >
                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <label className="flex items-center">
                  <input type="checkbox" className="rounded border-gray-600 bg-gray-800" />
                  <span className="ml-2 text-sm text-blue-200">Remember me</span>
                </label>
                <Link to="#" className="text-sm text-blue-400 hover:text-blue-300">
                  Forgot password?
                </Link>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-3 rounded-lg font-medium text-white transition-colors flex items-center justify-center group"
              >
                {isLoading ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <>
                    Sign In
                    <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-200" />
                  </>
                )}
              </button>
            </form>

            <div className="mt-8 text-center">
              <p className="text-blue-200">
                Don't have an account?{' '}
                <Link to="/register" className="text-blue-400 hover:text-blue-300 font-medium">
                  Create account
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;