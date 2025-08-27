# Frontend Authentication System

This document explains the authentication system implemented in the frontend and how it integrates with the Django backend.

## Overview

The frontend uses a comprehensive authentication system with JWT tokens, protected routes, and user state management. The system is built using React Context API and integrates seamlessly with the Django REST Framework backend.

## Components

### 1. AuthContext (`src/context/Authcontext.jsx`)

The main authentication context that provides:
- User state management
- Login/logout functionality
- Token management
- Automatic token refresh
- API interceptors for authentication

**Key Features:**
- JWT token storage and management
- Automatic token refresh on expiration
- User session persistence
- API request/response interceptors
- Error handling for authentication failures

### 2. ProtectedRoute (`src/components/ProtectedRoute.jsx`)

A wrapper component that protects routes from unauthorized access:
- Redirects unauthenticated users to login
- Shows loading state while checking authentication
- Seamlessly integrates with React Router

### 3. API Service (`src/services/api.js`)

Centralized API service with:
- Pre-configured axios instance
- Automatic token injection
- Error handling and token refresh
- Organized API endpoints for all backend services

### 4. useApi Hook (`src/hooks/useApi.js`)

Custom hook for API calls with:
- Loading states
- Error handling
- Consistent API call patterns

## Authentication Flow

### 1. Login Process
```javascript
const { login } = useAuth();

try {
  await login(email, password, userType);
  // User is now authenticated and redirected
} catch (error) {
  // Handle login errors
}
```

### 2. Registration Process
```javascript
const { register } = useAuth();

try {
  await register({
    name: 'John Doe',
    email: 'john@example.com',
    password: 'password123',
    userType: 'creator'
  });
  // User is registered and automatically logged in
} catch (error) {
  // Handle registration errors
}
```

### 3. Protected Routes
```javascript
<Route path="/dashboard" element={
  <ProtectedRoute>
    <Dashboard />
  </ProtectedRoute>
} />
```

### 4. API Calls
```javascript
import { creatorsAPI } from '../services/api';
import useApi from '../hooks/useApi';

const { loading, error, execute } = useApi();

const fetchCreators = async () => {
  try {
    const result = await execute(creatorsAPI.getAll);
    // Handle success
  } catch (error) {
    // Error is automatically handled by useApi
  }
};
```

## User Types

The system supports two user types:
- **Creator**: Artists, developers, content creators
- **Investor**: Users who invest in and purchase assets

## Token Management

### Storage
- Access tokens are stored in `localStorage` as `basix_token`
- Refresh tokens are stored as `basix_refresh_token`
- User data is stored as `basix_user`

### Automatic Refresh
- Tokens are automatically refreshed when they expire
- Failed requests due to expired tokens trigger automatic logout
- Users are redirected to login when authentication fails

## API Integration

### Backend Endpoints
The frontend integrates with these Django backend endpoints:
- `POST /api/token/` - Login
- `POST /api/token/refresh/` - Refresh token
- `POST /api/token/verify/` - Verify token
- `POST /api/token/blacklist/` - Logout
- `GET /api/creators/` - Get creators
- `POST /api/creators/` - Create creator

### Error Handling
- Network errors are handled gracefully
- Authentication errors trigger automatic logout
- User-friendly error messages are displayed
- Loading states provide feedback during API calls

## Security Features

1. **Token-based Authentication**: JWT tokens for secure authentication
2. **Automatic Token Refresh**: Seamless token renewal
3. **Protected Routes**: Unauthorized access prevention
4. **Secure Storage**: Tokens stored in localStorage with proper cleanup
5. **Error Handling**: Comprehensive error handling and user feedback

## Usage Examples

### Checking Authentication Status
```javascript
const { isAuthenticated, user } = useAuth();

if (isAuthenticated) {
  console.log('User is logged in:', user.name);
}
```

### Making Authenticated API Calls
```javascript
import { productsAPI } from '../services/api';

// The token is automatically included in the request
const products = await productsAPI.getAll();
```

### Handling Authentication Errors
```javascript
const { login } = useAuth();

try {
  await login(email, password, userType);
} catch (error) {
  // Error message is automatically extracted and displayed
  console.error('Login failed:', error.message);
}
```

## Configuration

### API Base URL
The API base URL is configured in `src/services/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

### Token Storage Keys
- `basix_token`: Access token
- `basix_refresh_token`: Refresh token
- `basix_user`: User data

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the Django backend has CORS properly configured
2. **Token Expiration**: Tokens are automatically refreshed, but manual logout may be needed
3. **Network Errors**: Check if the Django backend is running on the correct port
4. **Authentication Failures**: Verify user credentials and backend authentication setup

### Debug Mode
Enable debug logging by adding to the browser console:
```javascript
localStorage.setItem('debug_auth', 'true');
```

## Future Enhancements

1. **Remember Me**: Implement persistent login functionality
2. **Two-Factor Authentication**: Add 2FA support
3. **Social Login**: Integrate with social media platforms
4. **Role-based Access**: Implement more granular permissions
5. **Session Management**: Add session timeout and management features