import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { UserPlus, Mail, Lock, User, Compass } from 'lucide-react';
import { motion } from 'framer-motion';
import { toast } from 'react-hot-toast';

export const Register = () => {
  const { t } = useLanguage();
  const { register } = useAuth();
  const navigate = useNavigate();

  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!fullName.trim() || !email.trim() || !password.trim()) {
      toast.error('All fields are required.');
      return;
    }
    if (password.length < 6) {
      toast.error('Password must be at least 6 characters.');
      return;
    }

    try {
      setLoading(true);
      const res = await register(email, password, fullName);
      
      if (res.success) {
        toast.success('Registration successful! Please sign in.');
        navigate('/login');
      } else {
        toast.error(res.message);
      }
    } catch (err) {
      console.error(err);
      toast.error('An unexpected registration failure occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 bg-slate-50 dark:bg-slate-950 transition-colors">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-8 shadow-xl"
      >
        {/* Brand Header */}
        <div className="text-center mb-8">
          <div className="inline-flex w-12 h-12 rounded-2xl bg-gradient-to-tr from-emerald-400 to-teal-600 items-center justify-center text-white shadow-md shadow-emerald-500/20 mb-4">
            <Compass className="w-6 h-6 animate-spin-slow" />
          </div>
          <h2 className="text-2xl font-black text-slate-850 dark:text-white tracking-tight">
            {t('registerTitle')}
          </h2>
          <p className="text-xs text-slate-400 mt-1">Join TourEase and maps safety contacts</p>
        </div>

        {/* Inputs list */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Full Name */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
              <User className="w-3.5 h-3.5 text-emerald-500" />
              <span>{t('fieldFullName')}</span>
            </label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="e.g., Jane Doe"
              className="p-3 bg-slate-50 dark:bg-slate-950 text-slate-850 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold text-sm"
              required
            />
          </div>

          {/* Email */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
              <Mail className="w-3.5 h-3.5 text-emerald-500" />
              <span>{t('fieldEmail')}</span>
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="e.g., traveler@tourease.com"
              className="p-3 bg-slate-50 dark:bg-slate-950 text-slate-850 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold text-sm"
              required
            />
          </div>

          {/* Password */}
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
              <Lock className="w-3.5 h-3.5 text-emerald-500" />
              <span>{t('fieldPassword')}</span>
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Min 6 characters"
              className="p-3 bg-slate-50 dark:bg-slate-950 text-slate-850 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold text-sm"
              required
            />
          </div>

          {/* Action button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl shadow-lg shadow-emerald-600/10 disabled:opacity-50 hover-scale text-sm flex items-center justify-center gap-1.5"
          >
            <UserPlus className="w-4 h-4" />
            <span>{loading ? 'Creating Account...' : t('navRegister')}</span>
          </button>
        </form>

        <div className="text-center mt-6 pt-6 border-t border-slate-100 dark:border-slate-800">
          <p className="text-xs text-slate-500">
            {t('haveAccount')}{' '}
            <Link to="/login" className="font-bold text-emerald-600 hover:underline">
              {t('navLogin')}
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default Register;
