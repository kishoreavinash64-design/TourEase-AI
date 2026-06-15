import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLanguage } from '../context/LanguageContext';
import { Phone, Shield, ShieldAlert, HeartPulse, Flame, Compass } from 'lucide-react';
import { motion } from 'framer-motion';

export const EmergencyContacts = () => {
  const { t } = useLanguage();
  const [contacts, setContacts] = useState([]);
  const [selectedState, setSelectedState] = useState('');
  const [loading, setLoading] = useState(true);

  // Hardcoded national helplines for quick access
  const nationalHelplines = [
    { name: "National Emergency Number", number: "112", icon: ShieldAlert, color: "bg-rose-500" },
    { name: "Police Control Room", number: "100", icon: Shield, color: "bg-blue-500" },
    { name: "Ambulance / Medical", number: "102", icon: HeartPulse, color: "bg-emerald-500" },
    { name: "Fire Station Services", number: "101", icon: Flame, color: "bg-orange-500" },
    { name: "National Tourist Helpline", number: "1363", icon: Compass, color: "bg-purple-500" }
  ];

  useEffect(() => {
    const fetchEmergencyContacts = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/api/emergency');
        setContacts(response.data);
      } catch (err) {
        console.error('Error loading emergency contacts:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchEmergencyContacts();
  }, []);

  const activeContact = contacts.find(c => c.state === selectedState);

  return (
    <div className="max-w-4xl mx-auto px-4 py-10 min-h-screen">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto mb-10">
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="inline-flex p-3.5 bg-rose-100 dark:bg-rose-950/40 rounded-2xl text-rose-600 dark:text-rose-400 mb-4"
        >
          <Phone className="w-8 h-8 animate-pulse" />
        </motion.div>
        <h1 className="text-3xl font-extrabold text-slate-850 dark:text-white tracking-tight">
          {t('emergencyTitle')}
        </h1>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-2">
          {t('emergencySubtitle')}
        </p>
      </div>

      {/* National Helplines Grid */}
      <div className="mb-10">
        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">National Toll-Free Services</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-4">
          {nationalHelplines.map((hl, idx) => (
            <div
              key={idx}
              className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm flex flex-col items-center justify-center text-center gap-3"
            >
              <div className={`w-9 h-9 rounded-full ${hl.color} flex items-center justify-center text-white shadow-md`}>
                <hl.icon className="w-4.5 h-4.5" />
              </div>
              <div>
                <p className="text-[10px] font-bold text-slate-400 leading-tight">{hl.name}</p>
                <a
                  href={`tel:${hl.number}`}
                  className="block text-xl font-black text-emerald-600 dark:text-emerald-400 mt-1 hover:underline"
                >
                  {hl.number}
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* State Specific Helpline Section */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm">
        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">State Government Specific Lines</h3>
        
        {/* Dropdown filter */}
        <div className="max-w-md mb-6">
          <label className="block text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2">
            {t('emergencySearchLabel')}
          </label>
          {loading ? (
            <div className="h-10 bg-slate-100 dark:bg-slate-800 rounded-xl animate-pulse" />
          ) : (
            <select
              value={selectedState}
              onChange={(e) => setSelectedState(e.target.value)}
              className="w-full p-3 bg-slate-50 dark:bg-slate-950 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-rose-500 font-bold"
            >
              <option value="">-- Select State --</option>
              {contacts.map((c) => (
                <option key={c.id} value={c.state}>{c.state}</option>
              ))}
            </select>
          )}
        </div>

        {/* Display selected state details */}
        {activeContact ? (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-6 border-t border-slate-100 dark:border-slate-850 pt-6"
          >
            {/* Police */}
            <div className="p-4 bg-slate-50 dark:bg-slate-950 border border-slate-150 dark:border-slate-850 rounded-2xl flex items-center justify-between">
              <div>
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('contactPolice')}</p>
                <p className="text-lg font-extrabold text-slate-700 dark:text-slate-250 mt-0.5">{activeContact.police_contact}</p>
              </div>
              <a
                href={`tel:${activeContact.police_contact}`}
                className="p-3 bg-rose-500 text-white rounded-xl shadow hover:bg-rose-600 hover-scale"
              >
                <Phone className="w-4 h-4" />
              </a>
            </div>

            {/* Medical */}
            <div className="p-4 bg-slate-50 dark:bg-slate-950 border border-slate-150 dark:border-slate-850 rounded-2xl flex items-center justify-between">
              <div>
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('contactMedical')}</p>
                <p className="text-lg font-extrabold text-slate-700 dark:text-slate-250 mt-0.5">{activeContact.medical_contact}</p>
              </div>
              <a
                href={`tel:${activeContact.medical_contact}`}
                className="p-3 bg-emerald-500 text-white rounded-xl shadow hover:bg-emerald-600 hover-scale"
              >
                <Phone className="w-4 h-4" />
              </a>
            </div>

            {/* Fire */}
            <div className="p-4 bg-slate-50 dark:bg-slate-950 border border-slate-150 dark:border-slate-850 rounded-2xl flex items-center justify-between">
              <div>
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('contactFire')}</p>
                <p className="text-lg font-extrabold text-slate-700 dark:text-slate-250 mt-0.5">{activeContact.fire_contact}</p>
              </div>
              <a
                href={`tel:${activeContact.fire_contact}`}
                className="p-3 bg-orange-500 text-white rounded-xl shadow hover:bg-orange-600 hover-scale"
              >
                <Phone className="w-4 h-4" />
              </a>
            </div>

            {/* Disaster */}
            <div className="p-4 bg-slate-50 dark:bg-slate-950 border border-slate-150 dark:border-slate-850 rounded-2xl flex items-center justify-between">
              <div>
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('contactDisaster')}</p>
                <p className="text-lg font-extrabold text-slate-700 dark:text-slate-250 mt-0.5">{activeContact.disaster_management}</p>
              </div>
              <a
                href={`tel:${activeContact.disaster_management}`}
                className="p-3 bg-blue-500 text-white rounded-xl shadow hover:bg-blue-600 hover-scale"
              >
                <Phone className="w-4 h-4" />
              </a>
            </div>

            {/* Tourist */}
            <div className="p-4 bg-slate-50 dark:bg-slate-950 border border-slate-150 dark:border-slate-850 rounded-2xl flex items-center justify-between sm:col-span-2">
              <div>
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('contactTourist')}</p>
                <p className="text-lg font-extrabold text-slate-700 dark:text-slate-250 mt-0.5">{activeContact.tourist_helpline}</p>
              </div>
              <a
                href={`tel:${activeContact.tourist_helpline}`}
                className="p-3 bg-purple-500 text-white rounded-xl shadow hover:bg-purple-600 hover-scale"
              >
                <Phone className="w-4 h-4" />
              </a>
            </div>
          </motion.div>
        ) : (
          selectedState && (
            <p className="text-xs text-slate-400 mt-4">Helplines not configured. Call National Emergency 112.</p>
          )
        )}
      </div>
    </div>
  );
};

export default EmergencyContacts;
