import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { Search, Compass, MapPin, Sparkles, Shield, Eye, Flame, Map } from 'lucide-react';
import { motion } from 'framer-motion';
import { useLanguage } from '../context/LanguageContext';
import DestinationCard from '../components/DestinationCard';

export const LandingPage = () => {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const [categories, setCategories] = useState([]);
  const [trendingPlaces, setTrendingPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLandingData = async () => {
      try {
        setLoading(true);
        // Get categories
        const catRes = await axios.get('/api/destinations/categories');
        setCategories(catRes.data);

        // Get trending places
        const trendRes = await axios.get('/api/destinations?trending=true');
        setTrendingPlaces(trendRes.data.slice(0, 3)); // show top 3
      } catch (err) {
        console.error('Error loading landing page data:', err);
        setError('Unable to fetch latest destinations. Please check if backend is running.');
      } finally {
        setLoading(false);
      }
    };
    fetchLandingData();
  }, []);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/explore?search=${encodeURIComponent(searchQuery)}`);
    } else {
      navigate('/explore');
    }
  };

  const selectCategory = (catId) => {
    navigate(`/explore?category=${catId}`);
  };

  return (
    <div className="w-full bg-slate-50 dark:bg-slate-950 transition-colors duration-200">
      {/* 1. Hero Section */}
      <div className="relative min-h-[600px] flex items-center justify-center py-20 px-4 overflow-hidden">
        {/* Background Image with overlay */}
        <div className="absolute inset-0 z-0">
          <img
            src="https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&q=80&w=1600"
            alt="Tourism India"
            className="w-full h-full object-cover filter brightness-[0.35]"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-slate-50 dark:from-slate-950 via-transparent to-transparent z-10" />
        </div>

        {/* Hero Content */}
        <div className="relative z-20 max-w-4xl mx-auto text-center flex flex-col items-center">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-4xl md:text-6xl font-extrabold text-white tracking-tight leading-none mb-6 drop-shadow-md"
          >
            {t('heroTitle')}
          </motion.h1>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="text-lg md:text-xl text-slate-200 max-w-2xl font-medium mb-10 leading-relaxed"
          >
            {t('heroSubtitle')}
          </motion.p>

          {/* Search Input Container */}
          <motion.form
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4, delay: 0.4 }}
            onSubmit={handleSearchSubmit}
            className="w-full max-w-2xl bg-white dark:bg-slate-900 p-2 rounded-2xl md:rounded-3xl shadow-2xl flex flex-col md:flex-row gap-2 border border-slate-200/50 dark:border-slate-800"
          >
            <div className="flex items-center gap-2 flex-grow px-3">
              <Search className="w-5 h-5 text-slate-400 shrink-0" />
              <input
                type="text"
                placeholder={t('searchPlaceholder')}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full py-3 bg-transparent text-slate-800 dark:text-slate-100 border-none outline-none placeholder-slate-400 font-medium text-base"
              />
            </div>
            <button
              type="submit"
              className="py-3 px-8 rounded-xl md:rounded-2xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-base shadow-lg shadow-emerald-600/10 hover-scale shrink-0"
            >
              {t('searchBtn')}
            </button>
          </motion.form>
        </div>
      </div>

      {/* 2. Feature Stats Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 -mt-16 relative z-30">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-md flex items-start gap-4 hover-scale"
          >
            <div className="p-3 bg-emerald-100 dark:bg-emerald-950 rounded-2xl text-emerald-600 dark:text-emerald-400">
              <Map className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-extrabold text-lg text-slate-800 dark:text-white">Live OSM Integration</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                Pin attractions, nearby hospitals, hotels, and tourist services with active routing vectors.
              </p>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 15 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-md flex items-start gap-4 hover-scale"
          >
            <div className="p-3 bg-emerald-100 dark:bg-emerald-950 rounded-2xl text-emerald-600 dark:text-emerald-400">
              <Sparkles className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-extrabold text-lg text-slate-800 dark:text-white">AI Travel Planner</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                Enter your days and budget. Gemini constructs day-by-day itineraries complete with stay advice.
              </p>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 15 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-md flex items-start gap-4 hover-scale"
          >
            <div className="p-3 bg-emerald-100 dark:bg-emerald-950 rounded-2xl text-emerald-600 dark:text-emerald-400">
              <Shield className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-extrabold text-lg text-slate-800 dark:text-white">Verified Security</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                Access emergency state contacts, police control rooms, tourist helplines, and fire services instantly.
              </p>
            </div>
          </motion.div>
        </div>
      </div>

      {/* 3. Categories Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-extrabold text-slate-800 dark:text-white tracking-tight">
            Browse Destinations by Category
          </h2>
          <p className="text-slate-500 dark:text-slate-400 mt-2">
            Tailor your search based on the kind of experience you are seeking.
          </p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
          {loading ? (
            Array(5).fill(0).map((_, idx) => (
              <div key={idx} className="h-28 bg-slate-200 dark:bg-slate-800 rounded-2xl animate-pulse" />
            ))
          ) : (
            categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => selectCategory(cat.id)}
                className="p-6 bg-white dark:bg-slate-900 hover:bg-emerald-50 dark:hover:bg-emerald-950/30 border border-slate-200 dark:border-slate-800 rounded-2xl flex flex-col items-center justify-center text-center gap-3 shadow-sm hover:border-emerald-500 hover:shadow-md transition-all duration-300 group"
              >
                <div className="w-10 h-10 rounded-full bg-slate-100 dark:bg-slate-800 group-hover:bg-emerald-100 dark:group-hover:bg-emerald-900/50 flex items-center justify-center text-slate-500 dark:text-slate-400 group-hover:text-emerald-600 transition-colors">
                  <Compass className="w-5 h-5" />
                </div>
                <span className="font-bold text-sm text-slate-700 dark:text-slate-200 group-hover:text-slate-900 dark:group-hover:text-white">
                  {cat.name}
                </span>
              </button>
            ))
          )}
        </div>
      </div>

      {/* 4. Trending Destinations */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex flex-col md:flex-row items-center justify-between mb-10 gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2 justify-center md:justify-start">
              <Flame className="w-5 h-5 text-orange-500 fill-orange-500" />
              <h2 className="text-3xl font-extrabold text-slate-800 dark:text-white tracking-tight">
                {t('trendingTitle')}
              </h2>
            </div>
            <p className="text-slate-500 dark:text-slate-400 text-center md:text-left">
              {t('trendingSubtitle')}
            </p>
          </div>
          <Link
            to="/explore"
            className="px-5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 font-bold hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors flex items-center gap-1 shrink-0"
          >
            <span>Explore All Places</span>
            <span>&rarr;</span>
          </Link>
        </div>

        {/* Loading Skeletons */}
        {loading && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {Array(3).fill(0).map((_, idx) => (
              <div key={idx} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl overflow-hidden shadow-sm flex flex-col h-full animate-pulse">
                <div className="aspect-[4/3] bg-slate-200 dark:bg-slate-800" />
                <div className="p-5 space-y-3 flex-grow">
                  <div className="h-4 bg-slate-200 dark:bg-slate-800 rounded w-1/4" />
                  <div className="h-6 bg-slate-200 dark:bg-slate-800 rounded w-3/4" />
                  <div className="h-4 bg-slate-200 dark:bg-slate-800 rounded w-full" />
                  <div className="h-4 bg-slate-200 dark:bg-slate-800 rounded w-5/6" />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Error handling */}
        {error && (
          <div className="p-6 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900 text-red-700 dark:text-red-400 rounded-2xl text-center">
            <p className="font-semibold">{error}</p>
            <p className="text-sm mt-1">Please launch the FastAPI backend using `uvicorn app.main:app --reload` and seed database using `python app/seed.py`.</p>
          </div>
        )}

        {/* Places Grid */}
        {!loading && !error && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {trendingPlaces.map((place) => (
              <DestinationCard key={place.id} place={place} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default LandingPage;
