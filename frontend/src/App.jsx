import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { LanguageProvider } from './context/LanguageContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ProtectedRoute from './components/ProtectedRoute';

// Pages
import LandingPage from './pages/LandingPage';
import SearchDestinations from './pages/SearchDestinations';
import DestinationDetails from './pages/DestinationDetails';
import AIPlanner from './pages/AIPlanner';
import ChatBot from './pages/ChatBot';
import EmergencyContacts from './pages/EmergencyContacts';
import TripHistory from './pages/TripHistory';
import Dashboard from './pages/Dashboard';
import AdminDashboard from './pages/AdminDashboard';
import Login from './pages/Login';
import Register from './pages/Register';

import { Toaster } from 'react-hot-toast';

function App() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <AuthProvider>
          <Router>
            <div className="flex flex-col min-h-screen">
              {/* Global Navigation Header */}
              <Navbar />
              
              {/* Dynamic Pages viewport content */}
              <main className="flex-grow">
                <Routes>
                  <Route path="/" element={<LandingPage />} />
                  <Route path="/explore" element={<SearchDestinations />} />
                  <Route path="/destination/:destId" element={<DestinationDetails />} />
                  <Route path="/planner" element={
                    <ProtectedRoute>
                      <AIPlanner />
                    </ProtectedRoute>
                  } />
                  <Route path="/assistant" element={
                    <ProtectedRoute>
                      <ChatBot />
                    </ProtectedRoute>
                  } />
                  <Route path="/emergency" element={<EmergencyContacts />} />
                  
                  {/* Protected User Routes */}
                  <Route path="/dashboard" element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                  } />
                  <Route path="/history" element={
                    <ProtectedRoute>
                      <TripHistory />
                    </ProtectedRoute>
                  } />
                  
                  {/* Protected Admin Panel Route */}
                  <Route path="/admin" element={
                    <ProtectedRoute adminOnly={true}>
                      <AdminDashboard />
                    </ProtectedRoute>
                  } />
                  
                  {/* Auth routes */}
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                </Routes>
              </main>
              
              {/* Global Footer */}
              <Footer />
            </div>

            {/* Global toast notification system */}
            <Toaster 
              position="top-right" 
              toastOptions={{
                duration: 4000,
                style: {
                  background: '#1e293b',
                  color: '#fff',
                  borderRadius: '1rem',
                  fontWeight: '600',
                  fontSize: '0.875rem'
                },
                success: {
                  style: {
                    background: '#064e3b',
                    border: '1px solid #047857'
                  }
                },
                error: {
                  style: {
                    background: '#7f1d1d',
                    border: '1px solid #b91c1c'
                  }
                }
              }} 
            />
          </Router>
        </AuthProvider>
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App;
