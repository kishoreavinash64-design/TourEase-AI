import React from 'react';
import { Link } from 'react-router-dom';
import { Star, MapPin, Sparkles } from 'lucide-react';
import { motion } from 'framer-motion';
import { useLanguage } from '../context/LanguageContext';

export const DestinationCard = ({ place }) => {
  const { t } = useLanguage();

  // Pick first image from comma-separated list
  const imageUrl = place.images
    ? place.images.split(',')[0]
    : 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&q=80&w=800';

  // Budget category color coding
  const budgetColors = {
    'Budget': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/50 dark:text-emerald-300',
    'Mid-range': 'bg-blue-100 text-blue-800 dark:bg-blue-950/50 dark:text-blue-300',
    'Luxury': 'bg-purple-100 text-purple-800 dark:bg-purple-950/50 dark:text-purple-300',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.4 }}
      whileHover={{ y: -6 }}
      className="group bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col h-full"
    >
      {/* Cover Image */}
      <div className="relative aspect-[4/3] overflow-hidden bg-slate-100">
        <img
          src={imageUrl}
          alt={place.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          loading="lazy"
        />
        
        {/* Badges Overlaid */}
        <div className="absolute top-4 left-4 right-4 flex justify-between items-center z-20">
          <span className="px-3 py-1.5 rounded-xl text-xs font-bold bg-white/95 dark:bg-slate-900/95 shadow-sm text-slate-800 dark:text-slate-100 flex items-center gap-1">
            <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
            <span>{place.rating > 0 ? place.rating : '4.5'}</span>
          </span>

          {place.is_trending && (
            <span className="px-3 py-1.5 rounded-xl text-xs font-bold bg-gradient-to-r from-amber-500 to-orange-500 text-white flex items-center gap-1 shadow-sm">
              <Sparkles className="w-3.5 h-3.5 fill-white" />
              <span>Trending</span>
            </span>
          )}
        </div>
      </div>

      {/* Description & Details */}
      <div className="p-5 flex flex-col flex-grow">
        <div className="flex items-center gap-1 text-xs font-medium text-slate-400 dark:text-slate-500 mb-2">
          <MapPin className="w-3.5 h-3.5 text-emerald-500" />
          <span>{place.state}</span>
        </div>

        <h3 className="text-xl font-bold text-slate-800 dark:text-white leading-tight mb-2 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
          {place.name}
        </h3>

        <p className="text-sm text-slate-500 dark:text-slate-400 line-clamp-2 mb-4 flex-grow">
          {place.description}
        </p>

        <div className="flex items-center justify-between border-t border-slate-100 dark:border-slate-800 pt-4 mt-auto">
          {/* Budget Badge */}
          <span className={`px-2.5 py-1 rounded-lg text-xs font-bold ${budgetColors[place.budget_category] || 'bg-slate-100'}`}>
            {place.budget_category}
          </span>

          {/* Details CTA Link */}
          <Link
            to={`/destination/${place.id}`}
            className="text-sm font-bold text-emerald-600 dark:text-emerald-400 hover:text-emerald-700 dark:hover:text-emerald-300 flex items-center gap-1"
          >
            <span>{t('viewDetails')}</span>
            <span className="transition-transform group-hover:translate-x-1">&rarr;</span>
          </Link>
        </div>
      </div>
    </motion.div>
  );
};

export default DestinationCard;
