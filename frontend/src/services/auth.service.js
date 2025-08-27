import api from './api';

export const authService = {
  // Login user
  login: async (email, password) => {
    return api.post('/auth/login/', {
      email,
      password
    });
  },

  // Register new user
  register: async (userData) => {
    return api.post('/auth/register/', userData);
  },

  // Logout user
  logout: async () => {
    return api.post('/auth/logout/');
  },

  // Get current user
  getCurrentUser: async () => {
    return api.get('/auth/user/');
  },

  // Update user profile
  updateProfile: async (userData) => {
    return api.patch('/auth/user/', userData);
  },

  // Change password
  changePassword: async (oldPassword, newPassword) => {
    return api.post('/auth/change-password/', {
      old_password: oldPassword,
      new_password: newPassword
    });
  },

  // Request password reset
  requestPasswordReset: async (email) => {
    return api.post('/auth/password-reset/', { email });
  },

  // Reset password with token
  resetPassword: async (token, newPassword) => {
    return api.post('/auth/password-reset/confirm/', {
      token,
      new_password: newPassword
    });
  }
};

export default authService;