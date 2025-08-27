import React from 'react';
import { useAuth } from '../context/Authcontext';
import CreatorDashboard from '../components/CreatorDashboard';
import InvestorDashboard from '../components/InvestorDashboard';

const Dashboard = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      {user?.userType === 'creator' ? <CreatorDashboard /> : <InvestorDashboard />}
    </div>
  );
};

export default Dashboard;
