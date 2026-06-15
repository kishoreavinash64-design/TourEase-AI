import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const ProtectedRoute = ({ children, adminOnly = false }) => {
  const { user, loading, token } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-slate-500 dark:text-slate-400 font-medium">Verifying Session...</p>
        </div>
      </div>
    );
  }

  if (!token) {
    // Redirect to login but save current location to return after login
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (adminOnly && user && user.role !== 'admin') {
    // Access denied for non-admins
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

export default ProtectedRoute;
