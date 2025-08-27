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
      const response = await api.post('/token/', {
        username: email, // Django expects username field
        password: password,
      });

      const { access, refresh } = response.data;
      
      // Get user details
      const userResponse = await api.get('/creators/', {
        headers: {
          Authorization: `Bearer ${access}`,
        },
      });

      // Find the user by email
      const userData = userResponse.data.results?.find(
        creator => creator.user.email === email
      ) || {
        id: Math.random().toString(36).substr(2, 9),
        user: { email, username: email },
        wallet_address: 'temp_wallet',
        skills: [],
        reputation_score: 0,
      };

      const userInfo = {
        id: userData.id,
        email: userData.user.email,
        name: userData.user.username,
        userType: userType,
        wallet_address: userData.wallet_address,
        skills: userData.skills,
        reputation_score: userData.reputation_score,
      };
      
      setUser(userInfo);
      setIsAuthenticated(true);
      localStorage.setItem('basix_user', JSON.stringify(userInfo));
      localStorage.setItem('basix_token', access);
      localStorage.setItem('basix_refresh_token', refresh);
      
      return userInfo;
    } catch (error) {
      console.error("Login error:", error);
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      } else if (error.response?.data?.non_field_errors) {
        throw new Error(error.response.data.non_field_errors[0]);
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
      // First, create a Django user
      const userResponse = await api.post('/creators/', {
        user: {
          username: userData.name,
          email: userData.email,
          password: userData.password,
          first_name: userData.name.split(' ')[0] || userData.name,
          last_name: userData.name.split(' ').slice(1).join(' ') || '',
        },
        wallet_address: `wallet_${Date.now()}`, // Generate a temporary wallet address
        skills: userData.userType === 'creator' ? ['general'] : [],
        reputation_score: 0,
      });

      // After successful registration, log the user in
      await login(userData.email, userData.password, userData.userType);
      return userResponse.data;
    } catch (error) {
      console.error("Registration error:", error);
      if (error.response?.data?.user?.username) {
        throw new Error(`Username: ${error.response.data.user.username[0]}`);
      } else if (error.response?.data?.user?.email) {
        throw new Error(`Email: ${error.response.data.user.email[0]}`);
      } else if (error.response?.data?.user?.password) {
        throw new Error(`Password: ${error.response.data.user.password[0]}`);
      } else {
        throw new Error("Registration failed. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      // Call backend logout endpoint if available
      const token = localStorage.getItem('basix_token');
      if (token) {
        await api.post('/token/blacklist/', {
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
      api // Export the configured axios instance
    }}>
      {children}
    </AuthContext.Provider>
  );
};