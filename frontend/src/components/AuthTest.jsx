import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/Authcontext';
import { creatorsAPI } from '../services/api';
import useApi from '../hooks/useApi';

const AuthTest = () => {
  const { user, isAuthenticated, login, logout } = useAuth();
  const { loading, error, execute } = useApi();
  const [creators, setCreators] = useState([]);
  const [testResult, setTestResult] = useState('');

  const testLogin = async () => {
    try {
      await login('alice@example.com', 'password123', 'creator');
      setTestResult('✅ Login successful!');
    } catch (error) {
      setTestResult(`❌ Login failed: ${error.message}`);
    }
  };

  const testLogout = () => {
    logout();
    setTestResult('✅ Logout successful!');
  };

  const testApiCall = async () => {
    try {
      const result = await execute(creatorsAPI.getAll);
      setCreators(result.data.results || []);
      setTestResult('✅ API call successful!');
    } catch (error) {
      setTestResult(`❌ API call failed: ${error.message}`);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      testApiCall();
    }
  }, [isAuthenticated]);

  return (
    <div className="p-6 bg-gray-800 rounded-lg max-w-2xl mx-auto mt-8">
      <h2 className="text-2xl font-bold text-white mb-4">Authentication Test</h2>
      
      <div className="space-y-4">
        <div className="p-4 bg-gray-700 rounded-lg">
          <h3 className="text-lg font-semibold text-white mb-2">Authentication Status</h3>
          <p className="text-gray-300">
            Is Authenticated: <span className={isAuthenticated ? 'text-green-400' : 'text-red-400'}>
              {isAuthenticated ? 'Yes' : 'No'}
            </span>
          </p>
          {user && (
            <p className="text-gray-300">
              User: <span className="text-blue-400">{user.name} ({user.email})</span>
            </p>
          )}
        </div>

        <div className="p-4 bg-gray-700 rounded-lg">
          <h3 className="text-lg font-semibold text-white mb-2">Test Actions</h3>
          <div className="space-y-2">
            <button
              onClick={testLogin}
              disabled={isAuthenticated}
              className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Test Login
            </button>
            <button
              onClick={testLogout}
              disabled={!isAuthenticated}
              className="ml-2 px-4 py-2 bg-red-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Test Logout
            </button>
            <button
              onClick={testApiCall}
              disabled={!isAuthenticated || loading}
              className="ml-2 px-4 py-2 bg-green-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Loading...' : 'Test API Call'}
            </button>
          </div>
        </div>

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

        {creators.length > 0 && (
          <div className="p-4 bg-gray-700 rounded-lg">
            <h3 className="text-lg font-semibold text-white mb-2">Creators (API Response)</h3>
            <div className="space-y-2">
              {creators.map((creator) => (
                <div key={creator.id} className="p-2 bg-gray-600 rounded">
                  <p className="text-white">{creator.user.username} - {creator.wallet_address}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AuthTest;