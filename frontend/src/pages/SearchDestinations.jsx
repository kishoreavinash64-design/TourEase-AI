import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import axios from 'axios';
import { Search, SlidersHorizontal, MapPin, Tag, Landmark, CalendarDays, Compass } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import DestinationCard from '../components/DestinationCard';

export const SearchDestinations = () => {
  const { t } = useLanguage();
  const [searchParams, setSearchParams] = useSearchParams();
  
  // States from query parameters or default
  const [searchVal, setSearchVal] = useState(searchParams.get('search') || '');
  const [selectedState, setSelectedState] = useState(searchParams.get('state') || '');
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || '');
  const [selectedBudget, setSelectedBudget] = useState(searchParams.get('budget') || '');
  const [selectedSeason, setSelectedSeason] = useState(searchParams.get('season') || '');

  const [categories, setCategories] = useState([]);
  const [destinations, setDestinations] = useState([]);
  const [filteredDestinations, setFilteredDestinations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // States list in India for dropdown
  const indianStates = [
    "Goa", "Himachal Pradesh", "Kerala", "Rajasthan", "Uttar Pradesh", "Maharashtra", 
    "Karnataka", "Tamil Nadu", "Delhi", "Jammu and Kashmir", "West Bengal"
  ].sort();

  const seasons = [
    { value: "January", label: "Winter (January/February)" },
    { value: "May", label: "Summer (May/June)" },
    { value: "August", label: "Monsoon (August/September)" },
    { value: "October", label: "Autumn (October/November)" },
    { value: "December", label: "Holiday Peak (December)" }
  ];

  // Fetch categories on startup
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get('/api/destinations/categories');
        setCategories(response.data);
      } catch (err) {
        console.error('Error fetching categories:', err);
      }
    };
    fetchCategories();
  }, []);

  // Sync state variables with URLSearchParams (in case of nav link redirects)
  useEffect(() => {
    setSearchVal(searchParams.get('search') || '');
    setSelectedState(searchParams.get('state') || '');
    setSelectedCategory(searchParams.get('category') || '');
    setSelectedBudget(searchParams.get('budget') || '');
    setSelectedSeason(searchParams.get('season') || '');
  }, [searchParams]);

  // Fetch matching destinations based on active search parameters
  useEffect(() => {
    const fetchDestinations = async () => {
      try {
        setLoading(true);
        setError(null);

        // Construct search queries (excluding searchVal to filter instantly client-side)
        const params = {};
        if (selectedState) params.state = selectedState;
        if (selectedCategory) params.category_id = selectedCategory;
        if (selectedBudget) params.budget = selectedBudget;
        if (selectedSeason) params.season = selectedSeason;

        const response = await axios.get('/api/destinations', { params });
        setDestinations(response.data || []);
      } catch (err) {
        console.error('Error loading search results:', err);
        setError('Could not retrieve search results. Check backend status.');
      } finally {
        setLoading(false);
      }
    };

    fetchDestinations();
  }, [selectedState, selectedCategory, selectedBudget, selectedSeason]);

  // Client-side filtering logic with robust null checks and error handling
  useEffect(() => {
    try {
      if (!destinations || !Array.isArray(destinations)) {
        setFilteredDestinations([]);
        return;
      }

      if (!searchVal || typeof searchVal !== 'string' || !searchVal.trim()) {
        setFilteredDestinations(destinations);
        return;
      }

      const query = searchVal.toLowerCase().trim();
      
      const filtered = destinations.filter((dest) => {
        if (!dest) return false;

        // Null checks and lowercase searches across name, state, city, and category
        const nameMatch = dest.name && typeof dest.name === 'string'
          ? dest.name.toLowerCase().includes(query)
          : false;

        const stateMatch = dest.state && typeof dest.state === 'string'
          ? dest.state.toLowerCase().includes(query)
          : false;

        const cityMatch = dest.city && typeof dest.city === 'string'
          ? dest.city.toLowerCase().includes(query)
          : false;

        const categoryMatch = dest.category && dest.category.name && typeof dest.category.name === 'string'
          ? dest.category.name.toLowerCase().includes(query)
          : false;

        return nameMatch || stateMatch || cityMatch || categoryMatch;
      });

      setFilteredDestinations(filtered);
    } catch (err) {
      // Console error handling prevents the entire page from crashing and showing blank
      console.error("Error filtering destinations on client search:", err);
      setFilteredDestinations(destinations || []);
    }
  }, [searchVal, destinations]);

  const handleSearchChange = (e) => {
    const val = e.target.value;
    setSearchVal(val);
    updateSearchParams('search', val);
  };

  const updateSearchParams = (key, value) => {
    const nextParams = new URLSearchParams(searchParams);
    if (value) {
      nextParams.set(key, value);
    } else {
      nextParams.delete(key);
    }
    setSearchParams(nextParams);
  };

  const clearFilters = () => {
    setSearchVal('');
    setSelectedState('');
    setSelectedCategory('');
    setSelectedBudget('');
    setSelectedSeason('');
    setSearchParams({});
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 min-h-screen">
      {/* Page Title */}
      <div className="mb-8">
        <h1 className="text-3xl md:text-4xl font-extrabold text-slate-800 dark:text-white tracking-tight">
          {t('searchTitle')}
        </h1>
        <p className="text-slate-500 dark:text-slate-400 mt-1">
          Explore and filter destinations to match your exact trip itinerary plans.
        </p>
      </div>

      {/* Filter Toolbar */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm mb-10 space-y-4">
        
        {/* Search bar input */}
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            placeholder={t('searchPlaceholder')}
            value={searchVal}
            onChange={handleSearchChange}
            className="w-full pl-12 pr-4 py-3.5 bg-slate-50 dark:bg-slate-950 text-slate-880 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-2xl outline-none focus:border-emerald-500 transition-colors font-medium"
          />
        </div>

        {/* Dropdowns Filters */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
          {/* State Filter */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <MapPin className="w-3.5 h-3.5 text-emerald-500" />
              <span>State</span>
            </label>
            <select
              value={selectedState}
              onChange={(e) => {
                setSelectedState(e.target.value);
                updateSearchParams('state', e.target.value);
              }}
              className="w-full p-3 bg-slate-50 dark:bg-slate-950 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold"
            >
              <option value="">{t('searchFilterState')}</option>
              {indianStates.map((st) => (
                <option key={st} value={st}>{st}</option>
              ))}
            </select>
          </div>

          {/* Category Filter */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <Landmark className="w-3.5 h-3.5 text-emerald-500" />
              <span>Category</span>
            </label>
            <select
              value={selectedCategory}
              onChange={(e) => {
                setSelectedCategory(e.target.value);
                updateSearchParams('category', e.target.value);
              }}
              className="w-full p-3 bg-slate-50 dark:bg-slate-950 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold"
            >
              <option value="">{t('searchFilterCategory')}</option>
              {categories.map((cat) => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
          </div>

          {/* Budget Filter */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <Tag className="w-3.5 h-3.5 text-emerald-500" />
              <span>Budget</span>
            </label>
            <select
              value={selectedBudget}
              onChange={(e) => {
                setSelectedBudget(e.target.value);
                updateSearchParams('budget', e.target.value);
              }}
              className="w-full p-3 bg-slate-50 dark:bg-slate-950 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold"
            >
              <option value="">{t('searchFilterBudget')}</option>
              <option value="Budget">Budget Friendly</option>
              <option value="Mid-range">Mid-range Style</option>
              <option value="Luxury">Luxury Standard</option>
            </select>
          </div>

          {/* Season Filter */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <CalendarDays className="w-3.5 h-3.5 text-emerald-500" />
              <span>Best Season</span>
            </label>
            <select
              value={selectedSeason}
              onChange={(e) => {
                setSelectedSeason(e.target.value);
                updateSearchParams('season', e.target.value);
              }}
              className="w-full p-3 bg-slate-50 dark:bg-slate-950 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold"
            >
              <option value="">{t('searchFilterSeason')}</option>
              {seasons.map((se) => (
                <option key={se.value} value={se.value}>{se.label}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Clear Filters CTA */}
        <div className="flex justify-end pt-2">
          <button
            onClick={clearFilters}
            className="flex items-center gap-1.5 text-sm font-bold text-slate-400 hover:text-slate-700 dark:hover:text-white transition-colors"
          >
            <SlidersHorizontal className="w-4 h-4" />
            <span>Clear Filters</span>
          </button>
        </div>
      </div>

      {/* Loading States */}
      {loading && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {Array(6).fill(0).map((_, idx) => (
            <div key={idx} className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl overflow-hidden shadow-sm flex flex-col h-full animate-pulse">
              <div className="aspect-[4/3] bg-slate-200 dark:bg-slate-800" />
              <div className="p-5 space-y-3 flex-grow">
                <div className="h-4 bg-slate-200 dark:bg-slate-850 rounded w-1/4" />
                <div className="h-6 bg-slate-250 dark:bg-slate-850 rounded w-3/4" />
                <div className="h-4 bg-slate-250 dark:bg-slate-850 rounded w-full" />
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Error States */}
      {error && (
        <div className="p-6 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900 text-red-700 dark:text-red-400 rounded-2xl text-center">
          <p className="font-semibold">{error}</p>
        </div>
      )}

      {/* Search results listing */}
      {!loading && !error && (
        <>
          {filteredDestinations.length === 0 ? (
            <div className="text-center py-20 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-10 shadow-sm">
              <Compass className="w-12 h-12 text-slate-350 mx-auto animate-bounce mb-4" />
              <h3 className="text-xl font-bold text-slate-800 dark:text-white">No destinations found</h3>
              <p className="text-sm text-slate-505 dark:text-slate-400 mt-1.5">
                Try adjusting your search keywords or reset the active filters.
              </p>
              <button
                onClick={clearFilters}
                className="mt-6 px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm shadow-md hover-scale"
              >
                Reset Search
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {filteredDestinations.map((place) => (
                <DestinationCard key={place.id} place={place} />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default SearchDestinations;
