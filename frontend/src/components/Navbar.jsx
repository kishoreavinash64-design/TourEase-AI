import React, { useState } from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import ThemeToggle from './ThemeToggle';
import { 
  Compass, Sparkles, MessageSquare, PhoneCall, History, 
  User, LogOut, Menu, X, Globe, ShieldAlert 
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const Navbar = () => {
  const { user, logout } = useAuth();
  const { toggleLanguage, t, language } = useLanguage();
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsOpen(false);
  };

  const navItems = [
    { to: '/explore', label: t('navSearch'), icon: Compass },
    { to: '/planner', label: t('navPlanner'), icon: Sparkles },
    { to: '/assistant', label: t('navChatbot'), icon: MessageSquare },
    { to: '/emergency', label: t('navEmergency'), icon: PhoneCall },
  ];

  if (user) {
    navItems.push({ to: '/history', label: t('navHistory'), icon: History });
  }

  const activeStyle = "flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-sm font-semibold text-emerald-600 bg-emerald-50 dark:bg-emerald-950/50 dark:text-emerald-400 transition-all";
  const inactiveStyle = "flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800 transition-all";

  return (
    <nav className="sticky top-0 z-50 glass shadow-sm transition-all duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-400 to-teal-600 flex items-center justify-center text-white shadow-md shadow-emerald-500/20 group-hover:scale-105 transition-transform">
              <Compass className="w-5 h-5 animate-pulse" />
            </div>
            <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-emerald-600 to-teal-500 bg-clip-text text-transparent dark:from-emerald-400 dark:to-teal-300">
              {t('brand')}
            </span>
          </Link>

          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center gap-2">
            {navItems.map((item) => (
              <NavLink 
                key={item.to} 
                to={item.to}
                className={({ isActive }) => isActive ? activeStyle : inactiveStyle}
              >
                <item.icon className="w-4 h-4" />
                {item.label}
              </NavLink>
            ))}
          </div>

          {/* Actions & Profile */}
          <div className="hidden md:flex items-center gap-3">
            {/* Language Toggle */}
            <button
              onClick={toggleLanguage}
              className="flex items-center gap-1 px-3 py-1.5 text-xs font-semibold uppercase tracking-wider text-slate-600 border border-slate-200 dark:border-slate-800 rounded-xl hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800 transition-colors"
              title="Change Language"
            >
              <Globe className="w-3.5 h-3.5 text-emerald-500" />
              <span>{language === 'en' ? 'हिन्दी' : 'English'}</span>
            </button>

            {/* Dark Mode */}
            <ThemeToggle />

            {/* User Session */}
            {user ? (
              <div className="flex items-center gap-3">
                {user.role === 'admin' && (
                  <NavLink 
                    to="/admin" 
                    className={({ isActive }) => isActive 
                      ? "flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-sm font-semibold text-rose-600 bg-rose-50 dark:bg-rose-950/30 dark:text-rose-400" 
                      : "flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-sm font-medium text-slate-600 hover:text-rose-600 hover:bg-rose-50 dark:text-slate-400 dark:hover:bg-rose-950/20"
                    }
                  >
                    <ShieldAlert className="w-4 h-4 text-rose-500" />
                    <span>{t('navAdmin')}</span>
                  </NavLink>
                )}

                <Link 
                  to="/dashboard" 
                  className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 transition-colors"
                >
                  <User className="w-4 h-4 text-slate-600 dark:text-slate-400" />
                  <span className="text-sm font-semibold text-slate-700 dark:text-slate-200">
                    {user.full_name.split(' ')[0]}
                  </span>
                </Link>

                <button
                  onClick={handleLogout}
                  className="p-2 rounded-xl text-slate-500 hover:text-rose-600 hover:bg-rose-50 dark:text-slate-400 dark:hover:bg-rose-950/30 transition-colors"
                  title={t('navLogout')}
                >
                  <LogOut className="w-5 h-5" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="px-4 py-2 rounded-xl text-sm font-semibold text-slate-700 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800 transition-colors"
                >
                  {t('navLogin')}
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 rounded-xl text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700 shadow-md shadow-emerald-600/10 hover-scale"
                >
                  {t('navRegister')}
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="flex md:hidden items-center gap-2">
            <button
              onClick={toggleLanguage}
              className="p-2 text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800 rounded-xl"
              title="Change Language"
            >
              <Globe className="w-5 h-5 text-emerald-500" />
            </button>
            <ThemeToggle />
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="p-2 rounded-xl text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-850"
            >
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Drawer */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2 }}
            className="md:hidden glass border-t border-slate-200 dark:border-slate-850 overflow-hidden shadow-inner"
          >
            <div className="px-2 pt-2 pb-4 space-y-1 sm:px-3">
              {navItems.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  onClick={() => setIsOpen(false)}
                  className={({ isActive }) => 
                    `flex items-center gap-3 px-4 py-3 rounded-xl text-base font-semibold ${
                      isActive 
                        ? 'text-emerald-600 bg-emerald-50 dark:bg-emerald-950/40 dark:text-emerald-400' 
                        : 'text-slate-600 hover:bg-slate-50 dark:text-slate-400 dark:hover:bg-slate-850'
                    }`
                  }
                >
                  <item.icon className="w-5 h-5" />
                  {item.label}
                </NavLink>
              ))}

              {user && user.role === 'admin' && (
                <NavLink
                  to="/admin"
                  onClick={() => setIsOpen(false)}
                  className={({ isActive }) => 
                    `flex items-center gap-3 px-4 py-3 rounded-xl text-base font-semibold ${
                      isActive 
                        ? 'text-rose-600 bg-rose-50 dark:bg-rose-950/40 dark:text-rose-400' 
                        : 'text-slate-600 hover:bg-rose-50 dark:text-slate-400 dark:hover:bg-rose-850'
                    }`
                  }
                >
                  <ShieldAlert className="w-5 h-5 text-rose-500" />
                  {t('navAdmin')}
                </NavLink>
              )}

              <hr className="my-2 border-slate-200 dark:border-slate-800" />

              {user ? (
                <>
                  <Link
                    to="/dashboard"
                    onClick={() => setIsOpen(false)}
                    className="flex items-center gap-3 px-4 py-3 rounded-xl text-base font-semibold text-slate-600 hover:bg-slate-50 dark:text-slate-400 dark:hover:bg-slate-850"
                  >
                    <User className="w-5 h-5" />
                    <span>{user.full_name}</span>
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-base font-semibold text-rose-600 hover:bg-rose-50 dark:text-rose-400 dark:hover:bg-rose-950/20 text-left"
                  >
                    <LogOut className="w-5 h-5" />
                    <span>{t('navLogout')}</span>
                  </button>
                </>
              ) : (
                <div className="grid grid-cols-2 gap-2 p-2">
                  <Link
                    to="/login"
                    onClick={() => setIsOpen(false)}
                    className="flex justify-center items-center py-2.5 rounded-xl text-sm font-semibold text-slate-700 bg-slate-100 hover:bg-slate-200 dark:text-slate-300 dark:bg-slate-800 dark:hover:bg-slate-700"
                  >
                    {t('navLogin')}
                  </Link>
                  <Link
                    to="/register"
                    onClick={() => setIsOpen(false)}
                    className="flex justify-center items-center py-2.5 rounded-xl text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700"
                  >
                    {t('navRegister')}
                  </Link>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

export default Navbar;
