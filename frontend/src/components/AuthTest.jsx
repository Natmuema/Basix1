import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/Authcontext';
import { usersAPI, authAPI } from '../services/api';
import useApi from '../hooks/useApi';

const AuthTest = () => {
  const { user, isAuthenticated, login, logout, register } = useAuth();
  const { loading, error, execute } = useApi();
  const [users, setUsers] = useState([]);
  const [testResult, setTestResult] = useState('');
  const [currentUser, setCurrentUser] = useState(null);
  const [userStats, setUserStats] = useState(null);

  const testLogin = async () => {
    try {
      await login('testuser@example.com', 'password123', 'creator');
      setTestResult('✅ Login successful!');
    } catch (error) {
      setTestResult(`❌ Login failed: ${error.message}`);
    }
  };

  const testRegister = async () => {
    try {
      await register({
        name: 'Test User',
        email: 'testuser@example.com',
        password: 'password123',
        userType: 'creator',
        phone_number: '+1234567890'
      });
      setTestResult('✅ Registration successful!');
    } catch (error) {
      setTestResult(`❌ Registration failed: ${error.message}`);
    }
  };

  const testLogout = () => {
    logout();
    setTestResult('✅ Logout successful!');
  };

  const testGetUsers = async () => {
    try {
      const result = await execute(usersAPI.getAll);
      setUsers(result.data.results || []);
      setTestResult('✅ Get users API call successful!');
    } catch (error) {
      setTestResult(`❌ Get users API call failed: ${error.message}`);
    }
  };

  const testGetCreators = async () => {
    try {
      const result = await execute(usersAPI.getCreators);
      setUsers(result.data);
      setTestResult('✅ Get creators API call successful!');
    } catch (error) {
      setTestResult(`❌ Get creators API call failed: ${error.message}`);
    }
  };

  const testGetCurrentUser = async () => {
    try {
      const result = await execute(authAPI.me);
      setCurrentUser(result.data);
      setTestResult('✅ Get current user API call successful!');
    } catch (error) {
      setTestResult(`❌ Get current user API call failed: ${error.message}`);
    }
  };

  const testGetUserStats = async () => {
    try {
      const result = await execute(authAPI.stats);
      setUserStats(result.data);
      setTestResult('✅ Get user stats API call successful!');
    } catch (error) {
      setTestResult(`❌ Get user stats API call failed: ${error.message}`);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      testGetCurrentUser();
      testGetUserStats();
    }
  }, [isAuthenticated]);

  return (
    <div className="p-6 bg-gray-800 rounded-lg max-w-6xl mx-auto mt-8">
      <h2 className="text-2xl font-bold text-white mb-4">Users App Authentication Test</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Authentication Status & Actions */}
        <div className="space-y-4">
          <div className="p-4 bg-gray-700 rounded-lg">
            <h3 className="text-lg font-semibold text-white mb-2">Authentication Status</h3>
            <p className="text-gray-300">
              Is Authenticated: <span className={isAuthenticated ? 'text-green-400' : 'text-red-400'}>
                {isAuthenticated ? 'Yes' : 'No'}
              </span>
            </p>
            {user && (
              <div className="mt-2 space-y-1">
                <p className="text-gray-300">
                  User: <span className="text-blue-400">{user.name} ({user.email})</span>
                </p>
                <p className="text-gray-300">
                  Type: <span className="text-blue-400">{user.userType}</span>
                </p>
                <p className="text-gray-300">
                  Wallet: <span className="text-blue-400">{user.wallet_address}</span>
                </p>
                <p className="text-gray-300">
                  Verified: <span className={user.is_verified ? 'text-green-400' : 'text-red-400'}>
                    {user.is_verified ? 'Yes' : 'No'}
                  </span>
                </p>
              </div>
            )}
          </div>

          <div className="p-4 bg-gray-700 rounded-lg">
            <h3 className="text-lg font-semibold text-white mb-2">Test Actions</h3>
            <div className="space-y-2">
              <button
                onClick={testRegister}
                disabled={isAuthenticated}
                className="w-full px-4 py-2 bg-green-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Test Register (testuser@example.com)
              </button>
              <button
                onClick={testLogin}
                disabled={isAuthenticated}
                className="w-full px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Test Login (testuser@example.com)
              </button>
              <button
                onClick={testLogout}
                disabled={!isAuthenticated}
                className="w-full px-4 py-2 bg-red-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Test Logout
              </button>
              <button
                onClick={testGetUsers}
                disabled={!isAuthenticated || loading}
                className="w-full px-4 py-2 bg-purple-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Loading...' : 'Test Get All Users'}
              </button>
              <button
                onClick={testGetCreators}
                disabled={!isAuthenticated || loading}
                className="w-full px-4 py-2 bg-yellow-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Loading...' : 'Test Get Creators'}
              </button>
              <button
                onClick={testGetCurrentUser}
                disabled={!isAuthenticated || loading}
                className="w-full px-4 py-2 bg-indigo-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Loading...' : 'Test Get Current User'}
              </button>
              <button
                onClick={testGetUserStats}
                disabled={!isAuthenticated || loading}
                className="w-full px-4 py-2 bg-pink-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Loading...' : 'Test Get User Stats'}
              </button>
            </div>
          </div>
        </div>

        {/* Middle Column - Test Results & Errors */}
        <div className="space-y-4">
          {testResult && (
            <div className="p-4 bg-gray-700 rounded-lg">
              <h3 className="text-lg font-semibold text-white mb-2">Test Result</h3>
              <p className="text-gray-300">{testResult}</p>
            </div>
          )}

          {error && (
            <div className="p-4 bg-red-900 rounded-lg">
              <h3 className="text-lg font-semibold text-white mb-2">Error</h3>
              <p className="text-red-300">{error}</p>
            </div>
          )}

          {currentUser && (
            <div className="p-4 bg-gray-700 rounded-lg">
              <h3 className="text-lg font-semibold text-white mb-2">Current User (API Response)</h3>
              <div className="space-y-2">
                <div className="p-2 bg-gray-600 rounded">
                  <p className="text-white">User: {currentUser.username} ({currentUser.email})</p>
                  <p className="text-white">Type: {currentUser.user_type}</p>
                  <p className="text-white">Wallet: {currentUser.wallet_address}</p>
                  <p className="text-white">Verified: {currentUser.is_verified ? 'Yes' : 'No'}</p>
                  <p className="text-white">Joined: {new Date(currentUser.date_joined).toLocaleDateString()}</p>
                </div>
              </div>
            </div>
          )}

          {userStats && (
            <div className="p-4 bg-gray-700 rounded-lg">
              <h3 className="text-lg font-semibold text-white mb-2">User Statistics</h3>
              <div className="space-y-2">
                <div className="p-2 bg-gray-600 rounded">
                  <p className="text-white">Total Products: {userStats.total_products}</p>
                  <p className="text-white">Total Investments: {userStats.total_investments}</p>
                  <p className="text-white">Reputation Score: {userStats.reputation_score}</p>
                  <p className="text-white">Total Earnings: ${userStats.total_earnings}</p>
                  <p className="text-white">Total Spent: ${userStats.total_spent}</p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Column - Users List */}
        <div className="space-y-4">
          {users.length > 0 && (
            <div className="p-4 bg-gray-700 rounded-lg">
              <h3 className="text-lg font-semibold text-white mb-2">Users (API Response)</h3>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {users.map((user) => (
                  <div key={user.id} className="p-2 bg-gray-600 rounded">
                    <p className="text-white">{user.username} - {user.email}</p>
                    <p className="text-gray-300 text-sm">Type: {user.user_type}</p>
                    <p className="text-gray-300 text-sm">Wallet: {user.wallet_address}</p>
                    <p className="text-gray-300 text-sm">Verified: {user.is_verified ? 'Yes' : 'No'}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthTest;