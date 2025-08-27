import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Package, User, Building, ArrowRight, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../context/Authcontext';

const Register = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    userType: 'creator'
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [error, setError] = useState('');
  
  const { register, isLoading } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Client-side validation
    if (!formData.name.trim()) {
      setError('Please enter your full name');
      return;
    }

    if (!formData.email.trim()) {
      setError('Please enter your email address');
      return;
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      await register(formData);
      // Registration successful, redirect to dashboard
      navigate('/dashboard');
    } catch (error) {
      setError(error.message || 'Registration failed. Please try again.');
    }
  };

  return (
    <div className="min-h-screen " id='register'>
      <div className="flex min-h-screen">
        {/* Left Side - Branding */}
        <div className="hidden lg:flex lg:w-1/2 flex-col justify-center px-12 text-white">
          <div className="mb-8">
            <div className="flex items-center space-x-3 mb-8">
              <div className="p-2 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-lg">
                <Package className="h-8 w-8 text-white" />
              </div>
              <span className="font-bold text-3xl bg-gradient-to-r from-white to-cyan-200 bg-clip-text text-transparent">BASIX IP Marketplace</span>
            </div>
            <h1 className="text-5xl font-bold mb-6 leading-tight">
              Join the Future of
              <br />
              <span className="bg-gradient-to-r from-cyan-400 to-blue-300 bg-clip-text text-transparent">
                Asset Monetization
              </span>
            </h1>
            <p className="text-xl text-blue-100 leading-relaxed opacity-90">
              Whether you're a creator looking to monetize your assets or an investor 
              seeking innovative opportunities, BASIX connects you to a world of possibilities.
            </p>
          </div>
          
          <div className="space-y-4">
            {[
              'AI-powered asset valuation',
              'Cardano blockchain security',
              'Global marketplace access'
            ].map((feature, index) => (
              <div key={index} className="flex items-center space-x-4 group">
                <div className="w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full group-hover:scale-110 transition-transform duration-200"></div>
                <span className="text-lg text-blue-100 group-hover:text-white transition-colors duration-200">{feature}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Right Side - Registration Form */}
        <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
          <div className="w-full max-w-md">
            {/* Glass morphism container */}
            <div className="backdrop-blur-xl bg-white/10 border border-white/20 rounded-2xl p-8 shadow-2xl">
              <div className="text-center mb-8">
                {/* Mobile logo */}
                <div className="lg:hidden flex items-center justify-center space-x-3 mb-6">
                  <div className="p-2 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-lg">
                    <Package className="h-6 w-6 text-white" />
                  </div>
                  <span className="font-bold text-2xl bg-gradient-to-r from-white to-cyan-200 bg-clip-text text-transparent">BASIX</span>
                </div>
                
                <h2 className="text-3xl font-bold text-white mb-2">Create Account</h2>
                <p className="text-blue-200/80">Choose your path to success</p>
              </div>

              {/* Error Message */}
              {error && (
                <div className="mb-6 p-4 bg-red-500/20 border border-red-500/50 rounded-xl text-red-300 text-sm">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                {/* User Type Selection */}
                <div className="mb-8">
                  <div className="grid grid-cols-2 gap-4">
                    <button
                      type="button"
                      onClick={() => setFormData({...formData, userType: 'creator'})}
                      className={`p-4 rounded-xl border-2 transition-all duration-200 group ${
                        formData.userType === 'creator' 
                          ? 'border-cyan-400 bg-cyan-400/20 text-white shadow-lg shadow-cyan-400/25' 
                          : 'border-white/20 bg-white/5 text-blue-200 hover:border-cyan-400/50 hover:bg-white/10'
                      }`}
                    >
                      <User className="h-8 w-8 mx-auto mb-2 group-hover:scale-110 transition-transform duration-200" />
                      <div className="font-semibold">Creator</div>
                      <div className="text-xs mt-1 opacity-80">Artists, Entrepreneurs</div>
                    </button>
                    
                    <button
                      type="button"
                      onClick={() => setFormData({...formData, userType: 'investor'})}
                      className={`p-4 rounded-xl border-2 transition-all duration-200 group ${
                        formData.userType === 'investor' 
                          ? 'border-cyan-400 bg-cyan-400/20 text-white shadow-lg shadow-cyan-400/25' 
                          : 'border-white/20 bg-white/5 text-blue-200 hover:border-cyan-400/50 hover:bg-white/10'
                      }`}
                    >
                      <Building className="h-8 w-8 mx-auto mb-2 group-hover:scale-110 transition-transform duration-200" />
                      <div className="font-semibold">Investor</div>
                      <div className="text-xs mt-1 opacity-80">Fund & Support</div>
                    </button>
                  </div>
                </div>

                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-blue-200 mb-2">
                      Full Name
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl focus:outline-none focus:border-cyan-400 focus:bg-white/15 text-white placeholder-blue-300/60 transition-all duration-200 backdrop-blur-sm"
                      placeholder="Enter your full name"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-blue-200 mb-2">
                      Email Address
                    </label>
                    <input
                      type="email"
                      required
                      value={formData.email}
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                      className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl focus:outline-none focus:border-cyan-400 focus:bg-white/15 text-white placeholder-blue-300/60 transition-all duration-200 backdrop-blur-sm"
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
                        className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl focus:outline-none focus:border-cyan-400 focus:bg-white/15 text-white placeholder-blue-300/60 pr-12 transition-all duration-200 backdrop-blur-sm"
                        placeholder="Create a strong password"
                        minLength="6"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-blue-300/70 hover:text-white transition-colors duration-200"
                      >
                        {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-blue-200 mb-2">
                      Confirm Password
                    </label>
                    <div className="relative">
                      <input
                        type={showConfirmPassword ? 'text' : 'password'}
                        required
                        value={formData.confirmPassword}
                        onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
                        className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-xl focus:outline-none focus:border-cyan-400 focus:bg-white/15 text-white placeholder-blue-300/60 pr-12 transition-all duration-200 backdrop-blur-sm"
                        placeholder="Confirm your password"
                      />
                      <button
                        type="button"
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-blue-300/70 hover:text-white transition-colors duration-200"
                      >
                        {showConfirmPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                      </button>
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={isLoading}
                    className="w-full bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-3 rounded-xl font-medium text-white transition-all duration-200 flex items-center justify-center shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 hover:scale-[1.02] active:scale-[0.98] group"
                  >
                    {isLoading ? (
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    ) : (
                      <>
                        Create Account
                        <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform duration-200" />
                      </>
                    )}
                  </button>
                </div>
              </form>

              <div className="mt-8 text-center">
                <p className="text-blue-200/80">
                  Already have an account?{' '}
                  <button 
                    onClick={() => navigate('/login')}
                    className="text-cyan-400 hover:text-cyan-300 font-medium transition-colors duration-200 underline decoration-transparent hover:decoration-cyan-300 underline-offset-2"
                  >
                    Sign in
                  </button>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;