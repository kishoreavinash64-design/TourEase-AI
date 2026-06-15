import React from 'react';
import { useLanguage } from '../context/LanguageContext';
import { Heart } from 'lucide-react';

export const Footer = () => {
  const { t } = useLanguage();

  return (
    <footer className="border-t border-slate-200 bg-white dark:border-slate-900 dark:bg-slate-950 py-8 transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-extrabold text-lg bg-gradient-to-r from-emerald-600 to-teal-500 bg-clip-text text-transparent dark:from-emerald-400 dark:to-teal-300">
              {t('brand')}
            </span>
            <span className="text-sm text-slate-400">| Smart Tourism Information System</span>
          </div>
          
          <div className="flex items-center gap-1.5 text-sm text-slate-500 dark:text-slate-400">
            <span>Made for SIH 2026 with</span>
            <Heart className="w-4 h-4 text-rose-500 fill-rose-500 animate-bounce" />
            <span>in India</span>
          </div>

          <div className="text-xs text-slate-400 dark:text-slate-500">
            &copy; {new Date().getFullYear()} TourEase AI. All rights reserved.
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
