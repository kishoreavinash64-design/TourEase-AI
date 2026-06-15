import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLanguage } from '../context/LanguageContext';
import { 
  History, Calendar, Banknote, Trash2, MapPin, 
  ChevronDown, ChevronUp, Bed, Utensils, Compass 
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'react-hot-toast';

export const TripHistory = () => {
  const { t } = useLanguage();
  const [itineraries, setItineraries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/api/itineraries');
        setItineraries(response.data);
      } catch (err) {
        console.error('Error loading trip history:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm('Remove this itinerary from your history?')) return;
    try {
      await axios.delete(`/api/itineraries/${id}`);
      setItineraries(prev => prev.filter(item => item.id !== id));
      toast.success('Itinerary deleted.');
      if (expandedId === id) setExpandedId(null);
    } catch (err) {
      console.error('Error deleting itinerary:', err);
      toast.error('Failed to delete itinerary.');
    }
  };

  const toggleExpand = (id) => {
    setExpandedId(prev => (prev === id ? null : id));
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950">
        <div className="w-8 h-8 border-3 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-10 min-h-screen">
      {/* Page Title */}
      <div className="flex items-center gap-3 mb-8">
        <div className="p-3 bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 rounded-2xl">
          <History className="w-6 h-6" />
        </div>
        <div>
          <h1 className="text-3xl font-extrabold text-slate-850 dark:text-white tracking-tight">
            {t('navHistory')}
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">
            Access your previously planned trip schedules.
          </p>
        </div>
      </div>

      {itineraries.length === 0 ? (
        <div className="text-center py-20 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm p-8">
          <Compass className="w-12 h-12 text-slate-300 dark:text-slate-700 mx-auto animate-pulse mb-3" />
          <h3 className="text-lg font-bold text-slate-800 dark:text-white">No planned trips found</h3>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1.5">
            Use our AI Planner to generate custom schedules!
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {itineraries.map((trip) => {
            // Parse details safely
            let details = null;
            try {
              details = JSON.parse(trip.day_wise_details);
            } catch (err) {
              console.error(err);
            }

            const isExpanded = expandedId === trip.id;

            return (
              <div
                key={trip.id}
                className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm overflow-hidden transition-all duration-300 hover:border-slate-350 dark:hover:border-slate-700"
              >
                {/* Header Collapsible Trigger */}
                <div
                  onClick={() => toggleExpand(trip.id)}
                  className="p-5 flex items-center justify-between cursor-pointer select-none"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-6">
                    <div>
                      <h3 className="font-extrabold text-lg text-slate-850 dark:text-white flex items-center gap-1.5">
                        <MapPin className="w-4 h-4 text-emerald-500 shrink-0" />
                        <span>{trip.destination_name}</span>
                      </h3>
                      <p className="text-xs text-slate-400 mt-1">
                        Planned on {new Date(trip.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    
                    <div className="flex items-center gap-4 text-xs font-semibold text-slate-500 dark:text-slate-400">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3.5 h-3.5 text-emerald-500" />
                        <span>{trip.num_days} Days</span>
                      </span>
                      <span className="flex items-center gap-1">
                        <Banknote className="w-3.5 h-3.5 text-emerald-500" />
                        <span>₹{trip.budget}</span>
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <button
                      onClick={(e) => handleDelete(trip.id, e)}
                      className="p-2 text-slate-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/20 rounded-xl transition-colors shrink-0"
                      title="Delete trip history"
                    >
                      <Trash2 className="w-4.5 h-4.5" />
                    </button>
                    <div className="text-slate-400">
                      {isExpanded ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                    </div>
                  </div>
                </div>

                {/* Day List Details Expanded Panel */}
                <AnimatePresence>
                  {isExpanded && details && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      transition={{ duration: 0.25 }}
                      className="border-t border-slate-100 dark:border-slate-850 bg-slate-50/50 dark:bg-slate-950/30 p-6 space-y-6 overflow-hidden"
                    >
                      {details.days?.map((dayObj, dayIdx) => (
                        <div
                          key={dayIdx}
                          className="bg-white dark:bg-slate-900 border border-slate-150 dark:border-slate-850 rounded-2xl p-5 shadow-sm space-y-4"
                        >
                          <h4 className="font-extrabold text-sm text-slate-850 dark:text-white border-b border-slate-105 dark:border-slate-850 pb-2">
                            Day {dayObj.day}
                          </h4>

                          {dayObj.accommodation && (
                            <div className="flex items-center gap-3 text-sm">
                              <div className="p-2 bg-blue-50 dark:bg-blue-950 text-blue-600 dark:text-blue-400 rounded-xl">
                                <Bed className="w-4 h-4" />
                              </div>
                              <div>
                                <p className="text-[10px] font-bold text-slate-450 uppercase tracking-wide">{t('accomodationLabel')}</p>
                                <p className="font-semibold text-slate-700 dark:text-slate-350">{dayObj.accommodation}</p>
                              </div>
                            </div>
                          )}

                          <div className="space-y-3.5">
                            {dayObj.activities?.map((act, actIdx) => (
                              <div key={actIdx} className="flex gap-2.5 items-start pl-2">
                                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-2 shrink-0"></div>
                                <div>
                                  <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wide">
                                    {act.time}
                                  </span>
                                  <p className="text-sm font-semibold text-slate-800 dark:text-slate-205 mt-0.5">
                                    {act.activity}
                                  </p>
                                  {act.cost > 0 && (
                                    <p className="text-[10px] text-slate-400 font-bold mt-0.5">Cost: ₹{act.cost}</p>
                                  )}
                                </div>
                              </div>
                            ))}
                          </div>

                          {dayObj.meals && (
                            <div className="flex flex-wrap gap-2 pt-2 border-t border-slate-100 dark:border-slate-800 text-xs">
                              <span className="px-2.5 py-1 rounded bg-slate-50 dark:bg-slate-950 text-slate-500 font-semibold">
                                🍳 {dayObj.meals.breakfast}
                              </span>
                              <span className="px-2.5 py-1 rounded bg-slate-50 dark:bg-slate-950 text-slate-500 font-semibold">
                                🍲 {dayObj.meals.lunch}
                              </span>
                              <span className="px-2.5 py-1 rounded bg-slate-50 dark:bg-slate-950 text-slate-500 font-semibold">
                                🍽️ {dayObj.meals.dinner}
                              </span>
                            </div>
                          )}
                        </div>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default TripHistory;
