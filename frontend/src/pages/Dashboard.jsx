import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import DestinationCard from '../components/DestinationCard';
import { 
  User, Heart, Calendar, MessageSquare, Compass, 
  MapPin, Sparkles, LogOut, Settings 
} from 'lucide-react';
import { motion } from 'framer-motion';

export const Dashboard = () => {
  const { user, logout } = useAuth();
  const { t } = useLanguage();

  const [favs, setFavs] = useState([]);
  const [trips, setTrips] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardDetails = async () => {
      try {
        setLoading(true);
        // Get user's favorites
        const favsRes = await axios.get('/api/favorites');
        setFavs(favsRes.data);
        
        // Get user's trips
        const tripsRes = await axios.get('/api/itineraries');
        setTrips(tripsRes.data);
      } catch (err) {
        console.error('Error fetching dashboard details:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardDetails();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950">
        <div className="w-8 h-8 border-3 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 min-h-screen">
      {/* 1. User Header Block */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm mb-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-emerald-500 to-teal-600 flex items-center justify-center text-white text-2xl font-black shadow-md">
            {user?.full_name ? user.full_name.charAt(0) : <User />}
          </div>
          <div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-850 dark:text-white leading-tight">
              {t('dashWelcome', { name: user?.full_name || 'Traveler' })}
            </h1>
            <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">
              {t('dashSubtitle')}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {user?.role === 'admin' && (
            <Link
              to="/admin"
              className="px-4 py-2.5 rounded-xl border border-rose-250 hover:bg-rose-50 text-rose-600 dark:text-rose-400 dark:hover:bg-rose-950/20 text-sm font-bold transition-all"
            >
              Go to Admin Panel
            </Link>
          )}
          <button
            onClick={logout}
            className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-sm font-bold transition-all"
          >
            <LogOut className="w-4 h-4" />
            <span>{t('navLogout')}</span>
          </button>
        </div>
      </div>

      {/* 2. Stats Summary Counters */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mb-10">
        <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm flex items-center gap-4">
          <div className="p-3.5 bg-rose-100 dark:bg-rose-950/50 rounded-2xl text-rose-500">
            <Heart className="w-6 h-6 fill-rose-500" />
          </div>
          <div>
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('statFavorites')}</h4>
            <p className="text-3xl font-black text-slate-850 dark:text-white mt-1">{favs.length}</p>
          </div>
        </div>

        <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm flex items-center gap-4">
          <div className="p-3.5 bg-emerald-100 dark:bg-emerald-950/50 rounded-2xl text-emerald-600 dark:text-emerald-450">
            <Calendar className="w-6 h-6" />
          </div>
          <div>
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('statItineraries')}</h4>
            <p className="text-3xl font-black text-slate-850 dark:text-white mt-1">{trips.length}</p>
          </div>
        </div>

        <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm flex items-center gap-4 sm:col-span-2 md:col-span-1">
          <div className="p-3.5 bg-blue-100 dark:bg-blue-950/50 rounded-2xl text-blue-500">
            <MessageSquare className="w-6 h-6" />
          </div>
          <div>
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Help Sessions</h4>
            <p className="text-3xl font-black text-slate-850 dark:text-white mt-1">Active</p>
          </div>
        </div>
      </div>

      {/* 3. Favorites and Recent Trips block */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Saved Places */}
        <div className="lg:col-span-8 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-extrabold text-slate-850 dark:text-white tracking-tight flex items-center gap-2">
              <Heart className="w-5 h-5 text-rose-500 fill-rose-500" />
              <span>Saved Places</span>
            </h2>
            <Link to="/explore" className="text-xs font-bold text-emerald-600 hover:underline">
              Browse More &rarr;
            </Link>
          </div>

          {favs.length === 0 ? (
            <div className="p-10 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl text-center">
              <Compass className="w-10 h-10 text-slate-300 dark:text-slate-700 mx-auto mb-3" />
              <p className="text-sm font-bold text-slate-500 dark:text-slate-400">No favorited places saved yet.</p>
              <Link
                to="/explore"
                className="mt-3 inline-block px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs"
              >
                Find Places
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {favs.map((fav) => (
                <div key={fav.id}>
                  {/* Build basic card properties compatible with DestinationCard */}
                  <DestinationCard 
                    place={{
                      id: fav.destination_id,
                      name: fav.destination.name,
                      state: fav.destination.state,
                      description: "",
                      images: fav.destination.images,
                      budget_category: "Mid-range",
                      rating: 4.5,
                      is_trending: false
                    }} 
                  />
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Itineraries Summary */}
        <div className="lg:col-span-4 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-extrabold text-slate-850 dark:text-white tracking-tight flex items-center gap-2">
              <Calendar className="w-5 h-5 text-emerald-500" />
              <span>Recent Plans</span>
            </h2>
            <Link to="/history" className="text-xs font-bold text-emerald-600 hover:underline">
              View History &rarr;
            </Link>
          </div>

          {trips.length === 0 ? (
            <div className="p-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl text-center">
              <Sparkles className="w-8 h-8 text-slate-350 mx-auto mb-3" />
              <p className="text-sm font-bold text-slate-500 dark:text-slate-450">No saved travel plans.</p>
              <Link
                to="/planner"
                className="mt-3 inline-block px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs"
              >
                Plan custom itinerary
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {trips.slice(0, 3).map((trip) => (
                <div
                  key={trip.id}
                  className="p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm hover:border-emerald-500 transition-colors"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-extrabold text-sm text-slate-800 dark:text-white">{trip.destination_name}</h4>
                      <p className="text-[10px] text-slate-450 mt-0.5">{new Date(trip.created_at).toLocaleDateString()}</p>
                    </div>
                    <span className="text-xs font-bold bg-emerald-55 dark:bg-emerald-950/45 text-emerald-605 dark:text-emerald-400 px-2.5 py-1 rounded-lg">
                      {trip.num_days} Days
                    </span>
                  </div>
                  <div className="flex justify-between items-center mt-3 pt-3 border-t border-slate-50 dark:border-slate-850">
                    <span className="text-xs text-slate-500 font-bold">₹{trip.budget} Budget</span>
                    <Link
                      to="/history"
                      className="text-xs font-bold text-emerald-600 hover:underline"
                    >
                      View Details &rarr;
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
