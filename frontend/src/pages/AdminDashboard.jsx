import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { 
  ShieldAlert, Users, Landmark, Heart, MessageSquare, 
  Download, Plus, Edit3, Trash2, X, Sparkles, MapPin, 
  Percent, Globe, AlertTriangle 
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'react-hot-toast';

export const AdminDashboard = () => {
  const { user } = useAuth();
  const { t } = useLanguage();
  
  const [stats, setStats] = useState(null);
  const [destinations, setDestinations] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Modal form states
  const [showModal, setShowModal] = useState(false);
  const [editId, setEditId] = useState(null);
  const [formName, setFormName] = useState('');
  const [formState, setFormState] = useState('');
  const [formCategoryId, setFormCategoryId] = useState('');
  const [formDescription, setFormDescription] = useState('');
  const [formImages, setFormImages] = useState('');
  const [formEntryFee, setFormEntryFee] = useState(0);
  const [formTimings, setFormTimings] = useState('');
  const [formBestMonths, setFormBestMonths] = useState('');
  const [formLat, setFormLat] = useState(20.0);
  const [formLng, setFormLng] = useState(77.0);
  const [formBudgetCategory, setFormBudgetCategory] = useState('Mid-range');
  const [formIsTrending, setFormIsTrending] = useState(false);

  // Fetch admin dashboard details
  const fetchAdminData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const statsRes = await axios.get('/api/admin/stats');
      setStats(statsRes.data);

      const destsRes = await axios.get('/api/destinations');
      setDestinations(destsRes.data);

      const catsRes = await axios.get('/api/destinations/categories');
      setCategories(catsRes.data);
      if (catsRes.data.length > 0) setFormCategoryId(catsRes.data[0].id.toString());
    } catch (err) {
      console.error('Error fetching admin data:', err);
      setError('Unable to fetch admin statistics. Confirm permissions and backend status.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdminData();
  }, []);

  const handleCsvExport = async (endpoint, filename) => {
    try {
      toast.loading('Compiling report...', { id: 'csv-export' });
      const response = await axios.get(endpoint, { responseType: 'blob' });
      
      const blobUrl = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = blobUrl;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success('CSV Report exported!', { id: 'csv-export' });
    } catch (err) {
      console.error('Export error:', err);
      toast.error('Failed to export report.', { id: 'csv-export' });
    }
  };

  const handleOpenAddModal = () => {
    setEditId(null);
    setFormName('');
    setFormState('');
    setFormCategoryId(categories[0]?.id?.toString() || '');
    setFormDescription('');
    setFormImages('');
    setFormEntryFee(0);
    setFormTimings('9:00 AM - 5:00 PM');
    setFormBestMonths('October - March');
    setFormLat(20.0);
    setFormLng(77.0);
    setFormBudgetCategory('Mid-range');
    setFormIsTrending(false);
    setShowModal(true);
  };

  const handleOpenEditModal = (place) => {
    setEditId(place.id);
    setFormName(place.name);
    setFormState(place.state);
    setFormCategoryId(place.category_id.toString());
    setFormDescription(place.description);
    setFormImages(place.images || '');
    setFormEntryFee(place.entry_fee || 0);
    setFormTimings(place.timings || '');
    setFormBestMonths(place.best_months || '');
    setFormLat(place.latitude);
    setFormLng(place.longitude);
    setFormBudgetCategory(place.budget_category);
    setFormIsTrending(place.is_trending);
    setShowModal(true);
  };

  const handleDeleteDestination = async (id) => {
    if (!window.confirm('Delete this tourist destination from database?')) return;
    try {
      await axios.delete(`/api/admin/destinations/${id}`);
      toast.success('Destination deleted.');
      fetchAdminData();
    } catch (err) {
      console.error('Delete error:', err);
      toast.error('Failed to delete destination.');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formName.trim() || !formState.trim() || !formDescription.trim()) {
      toast.error('Please enter name, state, and description.');
      return;
    }

    // Prepare default nearby items coordinates
    const nearbyAttractionsMock = JSON.stringify([
      { name: "Local Market", distance: "1.2 km", description: "Vibrant shopping alley featuring handmade goods." },
      { name: "Scenic Sunset Point", distance: "2 km", description: "Scenic elevation ideal for sunset viewing." }
    ]);
    
    const nearbyServicesMock = JSON.stringify([
      { name: "Grand Vista Stay", type: "Hotel", latitude: parseFloat(formLat) + 0.002, longitude: parseFloat(formLng) - 0.003, contact: "022 1234567" },
      { name: "Spicy Bites Diner", type: "Restaurant", latitude: parseFloat(formLat) - 0.001, longitude: parseFloat(formLng) + 0.002, contact: "022 9876543" },
      { name: "City Health Care", type: "Hospital", latitude: parseFloat(formLat) + 0.005, longitude: parseFloat(formLng) + 0.005, contact: "102" }
    ]);

    const payload = {
      category_id: parseInt(formCategoryId),
      name: formName,
      state: formState,
      description: formDescription,
      images: formImages,
      entry_fee: parseFloat(formEntryFee),
      timings: formTimings,
      best_months: formBestMonths,
      latitude: parseFloat(formLat),
      longitude: parseFloat(formLng),
      nearby_attractions: nearbyAttractionsMock,
      nearby_services: nearbyServicesMock,
      is_trending: formIsTrending,
      budget_category: formBudgetCategory
    };

    try {
      if (editId) {
        // Edit API call
        await axios.put(`/api/admin/destinations/${editId}`, payload);
        toast.success('Destination updated successfully!');
      } else {
        // Create API call
        await axios.post('/api/admin/destinations', payload);
        toast.success('New destination created!');
      }
      setShowModal(false);
      fetchAdminData();
    } catch (err) {
      console.error('Submit error:', err);
      toast.error(err.response?.data?.detail || 'Failed to save destination.');
    }
  };

  if (loading && !stats) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950">
        <div className="w-8 h-8 border-3 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 min-h-screen">
      {/* Page Header */}
      <div className="flex items-center gap-3 mb-8">
        <div className="p-3 bg-rose-100 dark:bg-rose-950/40 text-rose-600 dark:text-rose-400 rounded-2xl">
          <ShieldAlert className="w-6 h-6 animate-pulse" />
        </div>
        <div>
          <h1 className="text-3xl font-extrabold text-slate-850 dark:text-white tracking-tight">
            {t('navAdmin')}
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">
            System health, database metrics, CSV exports, and tourist spot management.
          </p>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-2xl mb-8">
          {error}
        </div>
      )}

      {/* 1. Stats Cards Grid */}
      {stats && (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 mb-10">
          <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm flex items-center gap-4">
            <div className="p-3 bg-blue-100 dark:bg-blue-950 rounded-2xl text-blue-600 dark:text-blue-400">
              <Users className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('adminTotalUsers')}</p>
              <p className="text-2xl font-black text-slate-850 dark:text-white mt-0.5">{stats.total_users}</p>
            </div>
          </div>

          <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm flex items-center gap-4">
            <div className="p-3 bg-emerald-100 dark:bg-emerald-950 rounded-2xl text-emerald-600 dark:text-emerald-400">
              <Landmark className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('adminTotalPlaces')}</p>
              <p className="text-2xl font-black text-slate-850 dark:text-white mt-0.5">{stats.total_destinations}</p>
            </div>
          </div>

          <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm flex items-center gap-4">
            <div className="p-3 bg-rose-100 dark:bg-rose-950 rounded-2xl text-rose-500">
              <Heart className="w-6 h-6 fill-rose-500" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('adminTotalFavorites')}</p>
              <p className="text-2xl font-black text-slate-850 dark:text-white mt-0.5">{stats.total_favorites}</p>
            </div>
          </div>

          <div className="p-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm flex items-center gap-4">
            <div className="p-3 bg-amber-100 dark:bg-amber-950 rounded-2xl text-amber-500">
              <MessageSquare className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('adminTotalReviews')}</p>
              <p className="text-2xl font-black text-slate-850 dark:text-white mt-0.5">{stats.total_reviews}</p>
            </div>
          </div>
        </div>
      )}

      {/* 2. CSV Exports & Visual Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-10">
        
        {/* CSV Download Toolbar */}
        <div className="lg:col-span-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-lg font-extrabold text-slate-850 dark:text-white mb-2">{t('adminExportTitle')}</h3>
            <p className="text-xs text-slate-400 mb-6">Secure Excel-compatible CSV exports for compliance and documentation.</p>
          </div>
          <div className="space-y-3">
            <button
              onClick={() => handleCsvExport('/api/admin/export/users', 'tourease_users_report.csv')}
              className="w-full flex items-center justify-between p-3.5 bg-slate-50 hover:bg-slate-100 dark:bg-slate-950 dark:hover:bg-slate-850 rounded-2xl text-slate-700 dark:text-slate-200 text-sm font-bold border border-slate-200 dark:border-slate-800 hover-scale"
            >
              <span className="flex items-center gap-2">
                <Users className="w-4 h-4 text-blue-500" />
                <span>{t('adminExportUsers')}</span>
              </span>
              <Download className="w-4 h-4 text-slate-400" />
            </button>
            <button
              onClick={() => handleCsvExport('/api/admin/export/destinations', 'tourease_places_report.csv')}
              className="w-full flex items-center justify-between p-3.5 bg-slate-50 hover:bg-slate-100 dark:bg-slate-950 dark:hover:bg-slate-850 rounded-2xl text-slate-700 dark:text-slate-200 text-sm font-bold border border-slate-200 dark:border-slate-800 hover-scale"
            >
              <span className="flex items-center gap-2">
                <Landmark className="w-4 h-4 text-emerald-500" />
                <span>{t('adminExportDestinations')}</span>
              </span>
              <Download className="w-4 h-4 text-slate-400" />
            </button>
            <button
              onClick={() => handleCsvExport('/api/admin/export/reviews', 'tourease_reviews_report.csv')}
              className="w-full flex items-center justify-between p-3.5 bg-slate-50 hover:bg-slate-100 dark:bg-slate-950 dark:hover:bg-slate-850 rounded-2xl text-slate-700 dark:text-slate-200 text-sm font-bold border border-slate-200 dark:border-slate-800 hover-scale"
            >
              <span className="flex items-center gap-2">
                <MessageSquare className="w-4 h-4 text-amber-500" />
                <span>{t('adminExportReviews')}</span>
              </span>
              <Download className="w-4 h-4 text-slate-400" />
            </button>
          </div>
        </div>

        {/* Categories Count Progress Display */}
        <div className="lg:col-span-7 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm">
          <h3 className="text-lg font-extrabold text-slate-850 dark:text-white mb-4">{t('adminCategoryBreakdown')}</h3>
          <div className="space-y-4">
            {stats && Object.keys(stats.by_category).length === 0 ? (
              <p className="text-xs text-slate-400">No category breakdown logs available.</p>
            ) : (
              stats && Object.entries(stats.by_category).map(([name, count], idx) => {
                const percentage = Math.min(100, Math.round((count / stats.total_destinations) * 100));
                return (
                  <div key={idx} className="space-y-1.5">
                    <div className="flex justify-between text-xs font-bold text-slate-600 dark:text-slate-350">
                      <span>{name}</span>
                      <span>{count} destinations ({percentage}%)</span>
                    </div>
                    <div className="w-full h-2 bg-slate-100 dark:bg-slate-950 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-emerald-500 rounded-full transition-all duration-500"
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>

      {/* 3. CRUD Destinations Management List */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm overflow-hidden p-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <h2 className="text-xl font-extrabold text-slate-850 dark:text-white tracking-tight">
              {t('adminManageDestinations')}
            </h2>
            <p className="text-xs text-slate-400">Add, update, or remove tourism places from the live system.</p>
          </div>
          <button
            onClick={handleOpenAddModal}
            className="flex items-center gap-1.5 px-4.5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-sm shadow-md hover-scale shrink-0 self-start sm:self-center"
          >
            <Plus className="w-4.5 h-4.5" />
            <span>{t('adminAddBtn')}</span>
          </button>
        </div>

        {/* Places Table */}
        <div className="overflow-x-auto pr-1">
          <table className="w-full text-left border-collapse min-w-[600px]">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-805 text-xs font-bold text-slate-400 uppercase tracking-wider">
                <th className="pb-3 pl-2">Name</th>
                <th className="pb-3">State</th>
                <th className="pb-3">Category</th>
                <th className="pb-3">Budget</th>
                <th className="pb-3">Entry Fee</th>
                <th className="pb-3 text-right pr-2">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-850 text-sm font-semibold text-slate-700 dark:text-slate-300">
              {destinations.map((place) => (
                <tr key={place.id} className="hover:bg-slate-50/50 dark:hover:bg-slate-950/20">
                  <td className="py-3.5 pl-2 font-bold text-slate-800 dark:text-white">{place.name}</td>
                  <td className="py-3.5 flex items-center gap-1 text-emerald-650 dark:text-emerald-400">
                    <MapPin className="w-3.5 h-3.5" />
                    <span>{place.state}</span>
                  </td>
                  <td className="py-3.5">{place.category?.name || 'Heritage'}</td>
                  <td className="py-3.5">
                    <span className="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300 font-bold">
                      {place.budget_category}
                    </span>
                  </td>
                  <td className="py-3.5">₹{place.entry_fee}</td>
                  <td className="py-3.5 text-right pr-2">
                    <div className="flex justify-end gap-2">
                      <button
                        onClick={() => handleOpenEditModal(place)}
                        className="p-1.5 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-950/25 rounded-lg transition-colors"
                        title="Edit place details"
                      >
                        <Edit3 className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteDestination(place.id)}
                        className="p-1.5 text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/25 rounded-lg transition-colors"
                        title="Delete place"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add / Edit Form Modal Dialog */}
      <AnimatePresence>
        {showModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setShowModal(false)}
              className="absolute inset-0 bg-slate-950/60 backdrop-blur-sm"
            />

            {/* Modal Body */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 15 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 15 }}
              className="relative w-full max-w-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-2xl p-6 overflow-hidden max-h-[90vh] flex flex-col"
            >
              <div className="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-850 shrink-0">
                <h3 className="text-xl font-extrabold text-slate-850 dark:text-white">
                  {editId ? t('adminFormEditTitle') : t('adminFormAddTitle')}
                </h3>
                <button
                  onClick={() => setShowModal(false)}
                  className="p-1.5 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-450 hover:text-slate-700"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Scrollable Form Fields */}
              <form onSubmit={handleSubmit} className="flex-grow overflow-y-auto py-4 space-y-4 pr-1">
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {/* Destination Name */}
                  <div className="flex flex-col gap-1">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-wide">{t('adminFormName')}</label>
                    <input
                      type="text"
                      value={formName}
                      onChange={(e) => setFormName(e.target.value)}
                      placeholder="e.g., Anjuna Beach"
                      className="p-3 bg-slate-50 dark:bg-slate-950 text-slate-850 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold text-sm"
                      required
                    />
                  </div>

                  {/* State */}
                  <div className="flex flex-col gap-1">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-wide">{t('adminFormState')}</label>
                    <input
                      type="text"
                      value={formState}
                      onChange={(e) => setFormState(e.target.value)}
                      placeholder="e.g., Goa"
                      className="p-3 bg-slate-50 dark:bg-slate-950 text-slate-850 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold text-sm"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  {/* Category select */}
                  <div className="flex flex-col gap-1">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-wide">{t('adminFormCategory')}</label>
                    <select
                      value={formCategoryId}
                      onChange={(e) => setFormCategoryId(e.target.value)}
                      className="p-3 bg-slate-50 dark:bg-slate-950 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-bold text-sm"
                    >
                      {categories.map((cat) => (
                        <option key={cat.id} value={cat.id}>{cat.name}</option>
                      ))}
                    </select>
                  </div>

                  {/* Budget select */}
                  <div className="flex flex-col gap-1">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-wide">{t('adminFormBudgetCategory')}</label>
                    <select
                      value={formBudgetCategory}
                      onChange={(e) => setFormBudgetCategory(e.target.value)}
                      className="p-3 bg-slate-50 dark:bg-slate-950 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-bold text-sm"
                    >
                      <option value="Budget">Budget</option>
                      <option value="Mid-range">Mid-range</option>
                      <option value="Luxury">Luxury</option>
                    </select>
                  </div>

                  {/* Entry fee */}
                  <div className="flex flex-col gap-1">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-wide">{t('adminFormEntryFee')}</label>
                    <input
                      type="number"
                      min="0"
                      value={formEntryFee}
                      onChange={(e) => setFormEntryFee(e.target.value)}
                      className="p-3 bg-slate-50 dark:bg-slate-950 text-slate-850 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold text-sm"
                    />
                  </div>
                </div>

                {/* Description */}
                <div className="flex flex-col gap-1">
                  <label className="text-xs font-bold text-slate-400 uppercase tracking-wide">{t('adminFormDescription')}</label>
                  <textarea
                    rows={3}
                    value={formDescription}
                    onChange={(e) => setFormDescription(e.target.value)}
                    placeholder="Enter thorough detailed descriptive notes..."
                    className="p-3 bg-slate-50 dark:bg-slate-950 text-slate-850 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold text-sm"
                    required
                  />
                </div>

                {/* Images */}
                <div className="flex flex-col gap-1">
                  <label className="text-xs font-bold text-slate-400 uppercase tracking-wide">{t('adminFormImages')}</label>
                  <input
                    type="text"
                    value={formImages}
                    onChange={(e) => setFormImages(e.target.value)}
                    placeholder="e.g., https://url1.jpg, https://url2.jpg"
                    className="p-3 bg-slate-50 dark:bg-slate-950 text-slate-850 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold text-sm"
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {/* Timings */}
                  <div className="flex flex-col gap-1">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-wide">{t('adminFormTimings')}</label>
                    <input
                      type="text"
                      value={formTimings}
                      onChange={(e) => setFormTimings(e.target.value)}
                      placeholder="e.g., 9:00 AM - 6:00 PM"
                      className="p-3 bg-slate-50 dark:bg-slate-950 text-slate-850 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold text-sm"
                    />
                  </div>

                  {/* Best Months */}
                  <div className="flex flex-col gap-1">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-wide">{t('adminFormBestMonths')}</label>
                    <input
                      type="text"
                      value={formBestMonths}
                      onChange={(e) => setFormBestMonths(e.target.value)}
                      placeholder="e.g., November, December, January"
                      className="p-3 bg-slate-50 dark:bg-slate-950 text-slate-850 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold text-sm"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {/* Latitude */}
                  <div className="flex flex-col gap-1">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-wide">{t('adminFormLat')}</label>
                    <input
                      type="number"
                      step="any"
                      value={formLat}
                      onChange={(e) => setFormLat(e.target.value)}
                      className="p-3 bg-slate-50 dark:bg-slate-950 text-slate-850 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold text-sm"
                      required
                    />
                  </div>

                  {/* Longitude */}
                  <div className="flex flex-col gap-1">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-wide">{t('adminFormLng')}</label>
                    <input
                      type="number"
                      step="any"
                      value={formLng}
                      onChange={(e) => setFormLng(e.target.value)}
                      className="p-3 bg-slate-50 dark:bg-slate-950 text-slate-850 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-semibold text-sm"
                      required
                    />
                  </div>
                </div>

                {/* Trending Checkbox */}
                <div className="flex items-center gap-2 py-2">
                  <input
                    type="checkbox"
                    id="isTrending"
                    checked={formIsTrending}
                    onChange={(e) => setFormIsTrending(e.target.checked)}
                    className="w-4 h-4 text-emerald-600 focus:ring-emerald-500 border-slate-300 rounded"
                  />
                  <label htmlFor="isTrending" className="text-xs font-bold text-slate-600 dark:text-slate-300 uppercase tracking-wide cursor-pointer">
                    {t('adminFormTrending')}
                  </label>
                </div>

                {/* Actions shrink border */}
                <div className="flex gap-3 justify-end border-t border-slate-100 dark:border-slate-850 pt-4 shrink-0">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="px-5 py-2.5 border border-slate-200 dark:border-slate-800 text-slate-550 rounded-xl text-sm font-bold hover:bg-slate-50"
                  >
                    {t('adminFormCancel')}
                  </button>
                  <button
                    type="submit"
                    className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-sm font-bold shadow-md hover-scale"
                  >
                    {t('adminFormSave')}
                  </button>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default AdminDashboard;
