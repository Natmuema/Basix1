import React, { createContext, useContext, useState, useEffect } from 'react';
import { creatorsService } from '../services';

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
  const [creator, setCreator] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const savedUser = localStorage.getItem('basix_user');
    const token = localStorage.getItem('basix_token');
    const savedCreator = localStorage.getItem('basix_creator');
    
    if (savedUser && token) {
      setUser(JSON.parse(savedUser));
      if (savedCreator) {
        setCreator(JSON.parse(savedCreator));
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (email, password, userType) => {
    setIsLoading(true);
    try {
      // Note: This would need Django REST JWT authentication setup
      const response = await fetch(`${process.env.REACT_APP_API_URL}/auth/login/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: email,
          password: password,
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        const userData = {
          id: data.user.id,
          email: data.user.email,
          name: data.user.username,
          userType: userType
        };

        setUser(userData);
        localStorage.setItem('basix_user', JSON.stringify(userData));
        localStorage.setItem('basix_token', data.token);

        // If user is a creator, fetch their creator profile
        if (userType === 'creator' && data.creator_id) {
          const creatorData = await creatorsService.getById(data.creator_id);
          setCreator(creatorData);
          localStorage.setItem('basix_creator', JSON.stringify(creatorData));
        }

        return { success: true };
      } else {
        return { 
          success: false, 
          error: data.detail || 'Invalid credentials' 
        };
      }
    } catch (error) {
      return { 
        success: false, 
        error: 'Network error. Please try again.' 
      };
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (formData) => {
    setIsLoading(true);
    try {
      // For creator registration, create user and creator profile
      if (formData.userType === 'creator') {
        // First create user (would need Django user registration endpoint)
        const userResponse = await fetch(`${process.env.REACT_APP_API_URL}/auth/register/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: formData.email,
            email: formData.email,
            password: formData.password,
            first_name: formData.name.split(' ')[0] || '',
            last_name: formData.name.split(' ').slice(1).join(' ') || ''
          }),
        });

        if (!userResponse.ok) {
          const error = await userResponse.json();
          throw new Error(error.detail || 'Registration failed');
        }

        const userData = await userResponse.json();

        // Then create creator profile
        const creatorData = await creatorsService.create({
          username: formData.email,
          email: formData.email,
          password: formData.password,
          wallet_address: formData.walletAddress || `0x${Math.random().toString(16).substr(2, 40)}`,
          skills: formData.skills || [],
          bio: formData.bio || ''
        });

        // Auto-login after registration
        return login(formData.email, formData.password, 'creator');
      } else {
        // Regular user registration
        const response = await fetch(`${process.env.REACT_APP_API_URL}/auth/register/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: formData.email,
            email: formData.email,
            password: formData.password,
            first_name: formData.name.split(' ')[0] || '',
            last_name: formData.name.split(' ').slice(1).join(' ') || ''
          }),
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.detail || 'Registration failed');
        }

        // Auto-login after registration
        return login(formData.email, formData.password, formData.userType);
      }
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    setCreator(null);
    localStorage.removeItem('basix_user');
    localStorage.removeItem('basix_token');
    localStorage.removeItem('basix_creator');
  };

  const updateCreatorProfile = async (updates) => {
    if (!creator) return { success: false, error: 'No creator profile found' };

    try {
      const updatedCreator = await creatorsService.update(creator.id, updates);
      setCreator(updatedCreator);
      localStorage.setItem('basix_creator', JSON.stringify(updatedCreator));
      return { success: true, data: updatedCreator };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const value = {
    user,
    creator,
    isLoading,
    isAuthenticated: !!user,
    isCreator: user?.userType === 'creator',
    login,
    register,
    logout,
    updateCreatorProfile
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;