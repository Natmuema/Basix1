import React, { createContext, useContext, useState, useEffect } from 'react';

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

  useEffect(() => {
    // Check if user is already logged in
    const savedUser = localStorage.getItem('basix_user');
    const token = localStorage.getItem('basix_token');
    
    if (savedUser && token) {
      setUser(JSON.parse(savedUser));
    }
    setIsLoading(false);
  }, []);

  const login = async (email, password, userType) => {
    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:5001/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: email, // Your backend expects username field
          password: password,
          userType: userType
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        const userData = {
          id: data.user.id || Math.random().toString(36).substr(2, 9),
          email: data.user.email,
          name: data.user.username,
          userType: userType
        };
        
        setUser(userData);
        localStorage.setItem('basix_user', JSON.stringify(userData));
        
        // Store token if your backend provides one in the future
        if (data.token) {
          localStorage.setItem('basix_token', data.token);
        }
        
        return userData;
      } else {
        throw new Error(data.message || "Login failed");
      }
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (userData) => {
    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:5001/api/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: userData.name,
          email: userData.email,
          password: userData.password,
          userType: userData.userType
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        // After successful registration, log the user in
        await login(userData.email, userData.password, userData.userType);
        return data;
      } else {
        throw new Error(data.message || "Registration failed");
      }
    } catch (error) {
      console.error("Registration error:", error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      // Call backend logout endpoint
      await fetch("http://localhost:5001/api/logout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem('basix_token')}` // If you implement JWT
        },
      });
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      // Clear local state regardless of API call success
      setUser(null);
      localStorage.removeItem('basix_user');
      localStorage.removeItem('basix_token');
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
};