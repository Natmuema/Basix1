import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Configure axios defaults
  const API_BASE_URL = 'http://localhost:8000/api';

  // Create axios instance with base URL
  const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Add request interceptor to include auth token
  api.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('basix_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  // Add response interceptor to handle token expiration
  api.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 401) {
        // Token expired or invalid
        logout();
      }
      return Promise.reject(error);
    }
  );

  useEffect(() => {
    // Check if user is already logged in
    const savedUser = localStorage.getItem('basix_user');
    const token = localStorage.getItem('basix_token');
    
    if (savedUser && token) {
      setUser(JSON.parse(savedUser));
      setIsAuthenticated(true);
    }
    setIsLoading(false);
  }, []);

  const login = async (email, password, userType) => {
    setIsLoading(true);
    try {
      // Use the users app login endpoint
      const response = await api.post('/auth/login/', {
        username: email, // Django expects username field
        password: password,
      });

      const { user: userData, tokens } = response.data;
      
      const userInfo = {
        id: userData.id,
        email: userData.email,
        name: userData.username,
        userType: userData.user_type,
        wallet_address: userData.wallet_address,
        is_verified: userData.is_verified,
        profile_image: userData.profile_image,
        bio: userData.bio,
        phone_number: userData.phone_number,
        first_name: userData.first_name,
        last_name: userData.last_name,
      };
      
      setUser(userInfo);
      setIsAuthenticated(true);
      localStorage.setItem('basix_user', JSON.stringify(userInfo));
      localStorage.setItem('basix_token', tokens.access);
      localStorage.setItem('basix_refresh_token', tokens.refresh);
      
      return userInfo;
    } catch (error) {
      console.error("Login error:", error);
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      } else if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      } else {
        throw new Error("Login failed. Please check your credentials.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (userData) => {
    setIsLoading(true);
    try {
      // Use the users app register endpoint
      const response = await api.post('/auth/register/', {
        username: userData.name,
        email: userData.email,
        password: userData.password,
        password_confirm: userData.password,
        first_name: userData.name.split(' ')[0] || userData.name,
        last_name: userData.name.split(' ').slice(1).join(' ') || '',
        user_type: userData.userType,
        phone_number: userData.phone_number || '',
        creator_profile: userData.userType === 'creator' ? {
          skills: ['general'],
          reputation_score: 0,
          experience_years: 0,
        } : undefined,
        investor_profile: userData.userType === 'investor' ? {
          investment_preferences: [],
          risk_tolerance: 'medium',
          investment_budget: 0,
          preferred_categories: [],
        } : undefined,
      });

      const { user: userInfo, tokens } = response.data;
      
      const userProfile = {
        id: userInfo.id,
        email: userInfo.email,
        name: userInfo.username,
        userType: userInfo.user_type,
        wallet_address: userInfo.wallet_address,
        is_verified: userInfo.is_verified,
        profile_image: userInfo.profile_image,
        bio: userInfo.bio,
        phone_number: userInfo.phone_number,
        first_name: userInfo.first_name,
        last_name: userInfo.last_name,
      };
      
      setUser(userProfile);
      setIsAuthenticated(true);
      localStorage.setItem('basix_user', JSON.stringify(userProfile));
      localStorage.setItem('basix_token', tokens.access);
      localStorage.setItem('basix_refresh_token', tokens.refresh);
      
      return response.data;
    } catch (error) {
      console.error("Registration error:", error);
      if (error.response?.data?.error) {
        throw new Error(error.response.data.error);
      } else if (error.response?.data?.username) {
        throw new Error(`Username: ${error.response.data.username[0]}`);
      } else if (error.response?.data?.email) {
        throw new Error(`Email: ${error.response.data.email[0]}`);
      } else if (error.response?.data?.password) {
        throw new Error(`Password: ${error.response.data.password[0]}`);
      } else {
        throw new Error("Registration failed. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      // Call backend logout endpoint
      const token = localStorage.getItem('basix_token');
      if (token) {
        await api.post('/auth/logout/', {
          refresh: localStorage.getItem('basix_refresh_token'),
        });
      }
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      // Clear local state regardless of API call success
      setUser(null);
      setIsAuthenticated(false);
      localStorage.removeItem('basix_user');
      localStorage.removeItem('basix_token');
      localStorage.removeItem('basix_refresh_token');
    }
  };

  const refreshToken = async () => {
    try {
      const refresh = localStorage.getItem('basix_refresh_token');
      if (!refresh) {
        throw new Error('No refresh token available');
      }

      const response = await api.post('/token/refresh/', {
        refresh: refresh,
      });

      const { access } = response.data;
      localStorage.setItem('basix_token', access);
      return access;
    } catch (error) {
      console.error("Token refresh error:", error);
      logout();
      throw error;
    }
  };

  const updateUser = (userData) => {
    setUser(userData);
    localStorage.setItem('basix_user', JSON.stringify(userData));
  };

  const getCurrentUser = async () => {
    try {
      const response = await api.get('/auth/me/');
      const userData = response.data;
      
      const userInfo = {
        id: userData.id,
        email: userData.email,
        name: userData.username,
        userType: userData.user_type,
        wallet_address: userData.wallet_address,
        is_verified: userData.is_verified,
        profile_image: userData.profile_image,
        bio: userData.bio,
        phone_number: userData.phone_number,
        first_name: userData.first_name,
        last_name: userData.last_name,
      };
      
      updateUser(userInfo);
      return userInfo;
    } catch (error) {
      console.error("Get current user error:", error);
      throw error;
    }
  };

  return (
    <AuthContext.Provider value={{ 
      user, 
      login, 
      register, 
      logout, 
      isLoading, 
      isAuthenticated,
      updateUser,
      refreshToken,
      getCurrentUser,
      api // Export the configured axios instance
    }}>
      {children}
    </AuthContext.Provider>
  );
};