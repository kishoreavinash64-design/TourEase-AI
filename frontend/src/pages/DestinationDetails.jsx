import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import MapComponent from '../components/MapComponent';
import { 
  Heart, Star, MapPin, Calendar, Clock, Banknote, 
  Map, MessageSquare, ChevronLeft, Send, Sparkles, Building, Phone 
} from 'lucide-react';
import { motion } from 'framer-motion';
import { toast } from 'react-hot-toast';

export const DestinationDetails = () => {
  const { destId } = useParams();
  const { t } = useLanguage();
  const { token, user } = useAuth();
  
  const [place, setPlace] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [favorited, setFavorited] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Review posting state
  const [newRating, setNewRating] = useState(5);
  const [newComment, setNewComment] = useState('');
  const [submittingReview, setSubmittingReview] = useState(false);

  // Active picture gallery index
  const [activeImageIdx, setActiveImageIdx] = useState(0);

  useEffect(() => {
    const fetchPlaceDetails = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Get details
        const detailsRes = await axios.get(`/api/destinations/${destId}`);
        setPlace(detailsRes.data);
        
        // Get reviews
        const reviewsRes = await axios.get(`/api/reviews/destination/${destId}`);
        setReviews(reviewsRes.data);

        // Check if favorited (only if logged in)
        if (token) {
          const favsRes = await axios.get('/api/favorites');
          const isFav = favsRes.data.some(f => f.destination_id === parseInt(destId));
          setFavorited(isFav);
        }
      } catch (err) {
        console.error('Error fetching destination details:', err);
        setError('Failed to fetch details for this destination.');
      } finally {
        setLoading(false);
      }
    };

    fetchPlaceDetails();
  }, [destId, token]);

  const toggleFavorite = async () => {
    if (!token) {
      toast.error(t('authRequiredMsg'));
      return;
    }
    try {
      const response = await axios.post('/api/favorites/toggle', { destination_id: parseInt(destId) });
      const isFav = response.data.favorited;
      setFavorited(isFav);
      if (isFav) {
        toast.success(t('favoriteSuccess'));
      } else {
        toast.success(t('favoriteRemove'));
      }
    } catch (err) {
      console.error('Error toggling favorite:', err);
      toast.error('Could not save favorite destination.');
    }
  };

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    if (!token) {
      toast.error(t('authRequiredMsg'));
      return;
    }
    if (!newComment.trim()) {
      toast.error('Please write a feedback comment.');
      return;
    }

    try {
      setSubmittingReview(true);
      const response = await axios.post('/api/reviews', {
        destination_id: parseInt(destId),
        rating: newRating,
        comment: newComment
      });
      
      toast.success('Review posted successfully!');
      setNewComment('');
      setNewRating(5);
      
      // Reload reviews
      const reviewsRes = await axios.get(`/api/reviews/destination/${destId}`);
      setReviews(reviewsRes.data);

      // Re-fetch place details to refresh the average rating
      const detailsRes = await axios.get(`/api/destinations/${destId}`);
      setPlace(detailsRes.data);
    } catch (err) {
      console.error('Error posting review:', err);
      toast.error('Failed to post review. Please try again.');
    } finally {
      setSubmittingReview(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-950">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-slate-500 dark:text-slate-400 font-medium">Gathering Local Information...</p>
        </div>
      </div>
    );
  }

  if (error || !place) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center">
        <div className="p-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm">
          <h2 className="text-2xl font-extrabold text-slate-800 dark:text-white mb-2">Error Loading Place</h2>
          <p className="text-slate-500 dark:text-slate-400 mb-6">{error || 'Destination not found'}</p>
          <Link to="/explore" className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold">
            Back to Explore
          </Link>
        </div>
      </div>
    );
  }

  // Parse safety variables for JSON columns
  let attractions = [];
  let services = [];
  try {
    if (place.nearby_attractions) {
      attractions = typeof place.nearby_attractions === 'string' 
        ? JSON.parse(place.nearby_attractions) 
        : place.nearby_attractions;
    }
    if (place.nearby_services) {
      services = typeof place.nearby_services === 'string' 
        ? JSON.parse(place.nearby_services) 
        : place.nearby_services;
    }
  } catch (e) {
    console.error('Error parsing JSON string column:', e);
  }

  const imageList = place.images
    ? place.images.split(',')
    : ['https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?auto=format&fit=crop&q=80&w=800'];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 min-h-screen">
      {/* Back button */}
      <Link
        to="/explore"
        className="inline-flex items-center gap-1 text-sm font-bold text-slate-500 hover:text-emerald-600 dark:hover:text-emerald-400 mb-6"
      >
        <ChevronLeft className="w-4 h-4" />
        <span>Back to Explore</span>
      </Link>

      {/* Main Grid: Info and Gallery */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-12">
        {/* Left Side: Images */}
        <div className="lg:col-span-6 space-y-4">
          <div className="relative aspect-[4/3] rounded-3xl overflow-hidden shadow-md bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
            <img
              src={imageList[activeImageIdx]}
              alt={place.name}
              className="w-full h-full object-cover"
            />
            {/* Heart Favorite button */}
            <button
              onClick={toggleFavorite}
              className="absolute top-4 right-4 p-3 rounded-2xl bg-white/90 dark:bg-slate-900/90 hover:scale-105 transition-all shadow-md focus:outline-none z-30"
              title="Save to favorites"
            >
              <Heart
                className={`w-6 h-6 transition-colors ${
                  favorited 
                    ? 'fill-rose-500 text-rose-500' 
                    : 'text-slate-600 dark:text-slate-300'
                }`}
              />
            </button>
          </div>
          
          {/* Thumbnails list */}
          {imageList.length > 1 && (
            <div className="flex gap-3 overflow-x-auto pb-2">
              {imageList.map((imgUrl, idx) => (
                <button
                  key={idx}
                  onClick={() => setActiveImageIdx(idx)}
                  className={`w-20 h-20 rounded-xl overflow-hidden border-2 shrink-0 transition-all ${
                    activeImageIdx === idx 
                      ? 'border-emerald-500 scale-95 shadow-md' 
                      : 'border-transparent hover:border-slate-300'
                  }`}
                >
                  <img src={imgUrl} alt={`${place.name} thumb ${idx}`} className="w-full h-full object-cover" />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Right Side: Primary Info */}
        <div className="lg:col-span-6 flex flex-col justify-between space-y-6">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="px-3 py-1 rounded-xl text-xs font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/50 dark:text-emerald-300">
                {place.category?.name || 'Heritage'}
              </span>
              <span className="px-3 py-1 rounded-xl text-xs font-bold bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-300">
                {place.budget_category}
              </span>
            </div>

            <h1 className="text-3xl md:text-5xl font-extrabold text-slate-800 dark:text-white leading-tight mb-4">
              {place.name}
            </h1>

            <div className="flex items-center gap-4 text-sm font-semibold text-slate-500 dark:text-slate-400 mb-6">
              <span className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400">
                <MapPin className="w-4 h-4" />
                {place.state}
              </span>
              <span className="flex items-center gap-1">
                <Star className="w-4 h-4 fill-amber-400 text-amber-400" />
                <span className="text-slate-800 dark:text-slate-200">{place.rating > 0 ? place.rating : '4.5'}</span>
                <span>({reviews.length} reviews)</span>
              </span>
            </div>

            <p className="text-slate-600 dark:text-slate-355 leading-relaxed text-base font-medium mb-6">
              {place.description}
            </p>
          </div>

          {/* Place specific details table */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm">
            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-emerald-50 dark:bg-emerald-950/40 rounded-xl text-emerald-600 dark:text-emerald-400">
                <Clock className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('detailsTimings')}</p>
                <p className="text-sm font-semibold text-slate-700 dark:text-slate-200 line-clamp-1" title={place.timings || "Sunrise to Sunset"}>
                  {place.timings || "Sunrise to Sunset"}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-emerald-50 dark:bg-emerald-950/40 rounded-xl text-emerald-600 dark:text-emerald-400">
                <Banknote className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('detailsEntryFee')}</p>
                <p className="text-sm font-bold text-slate-700 dark:text-slate-200">
                  {place.entry_fee > 0 ? `₹${place.entry_fee}` : t('freeEntry')}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-emerald-50 dark:bg-emerald-950/40 rounded-xl text-emerald-600 dark:text-emerald-400">
                <Calendar className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Best Months</p>
                <p className="text-sm font-semibold text-slate-700 dark:text-slate-200 line-clamp-1" title={place.best_months || "Oct to Mar"}>
                  {place.best_months || "October - March"}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Interactive OSM Map & Amenities Section */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-12">
        {/* Map Rendering Container */}
        <div className="lg:col-span-8 space-y-4">
          <div className="flex items-center gap-2">
            <Map className="w-5 h-5 text-emerald-500" />
            <h2 className="text-2xl font-extrabold text-slate-800 dark:text-white tracking-tight">
              Interactive Map & Nearby Services
            </h2>
          </div>
          <MapComponent destName={place.name} lat={place.latitude} lng={place.longitude} nearbyServices={services} />
        </div>

        {/* Nearby attractions and travel guides */}
        <div className="lg:col-span-4 space-y-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-emerald-500" />
            <h2 className="text-2xl font-extrabold text-slate-800 dark:text-white tracking-tight">
              {t('nearbyAttractions')}
            </h2>
          </div>
          
          <div className="space-y-4 max-h-[450px] overflow-y-auto pr-1">
            {attractions.length === 0 ? (
              <p className="text-slate-500 dark:text-slate-400 text-sm">No secondary attractions logged nearby.</p>
            ) : (
              attractions.map((attr, idx) => (
                <div key={idx} className="p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm hover:border-emerald-500 transition-colors">
                  <div className="flex justify-between items-center gap-2 mb-1.5">
                    <h4 className="font-extrabold text-sm text-slate-800 dark:text-white">{attr.name}</h4>
                    <span className="text-xs font-bold bg-emerald-55 dark:bg-emerald-950/45 text-emerald-600 dark:text-emerald-400 px-2 py-0.5 rounded-lg shrink-0">
                      {attr.distance}
                    </span>
                  </div>
                  <p className="text-xs text-slate-500 dark:text-slate-400">{attr.description}</p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Reviews and feedback block */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mb-12">
        {/* Left: Review List */}
        <div className="lg:col-span-8 space-y-6">
          <div className="flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-emerald-500" />
            <h2 className="text-2xl font-extrabold text-slate-800 dark:text-white tracking-tight">
              {t('reviewsHeader')}
            </h2>
          </div>

          <div className="space-y-4">
            {reviews.length === 0 ? (
              <div className="p-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl text-center text-slate-500 dark:text-slate-400">
                {t('noReviews')}
              </div>
            ) : (
              reviews.map((rev) => (
                <div key={rev.id} className="p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl shadow-sm">
                  <div className="flex justify-between items-center mb-2">
                    <div>
                      <h4 className="font-extrabold text-slate-800 dark:text-white text-sm">{rev.user_name || 'Anonymous Traveler'}</h4>
                      <p className="text-xs text-slate-400">{new Date(rev.created_at).toLocaleDateString()}</p>
                    </div>
                    
                    {/* Star output */}
                    <div className="flex gap-0.5">
                      {Array(5).fill(0).map((_, i) => (
                        <Star
                          key={i}
                          className={`w-3.5 h-3.5 ${
                            i < rev.rating 
                              ? 'fill-amber-400 text-amber-400' 
                              : 'text-slate-250 dark:text-slate-700'
                          }`}
                        />
                      ))}
                    </div>
                  </div>
                  <p className="text-sm text-slate-600 dark:text-slate-350">{rev.comment}</p>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right: Write a Review Form */}
        <div className="lg:col-span-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm sticky top-24">
            <h3 className="text-xl font-extrabold text-slate-800 dark:text-white mb-4">
              {t('addReviewTitle')}
            </h3>

            {token ? (
              <form onSubmit={handleReviewSubmit} className="space-y-4">
                {/* Rating selection */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">{t('ratingLabel')}</label>
                  <div className="flex gap-1.5">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        type="button"
                        onClick={() => setNewRating(star)}
                        className="p-1 focus:outline-none"
                      >
                        <Star
                          className={`w-7 h-7 transition-colors ${
                            star <= newRating
                              ? 'fill-amber-400 text-amber-400'
                              : 'text-slate-300 dark:text-slate-700 hover:text-amber-300'
                          }`}
                        />
                      </button>
                    ))}
                  </div>
                </div>

                {/* Comment box */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Your Feedback</label>
                  <textarea
                    rows={4}
                    placeholder={t('commentLabel')}
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    className="w-full p-3.5 bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 font-medium text-sm"
                  />
                </div>

                {/* Submit button */}
                <button
                  type="submit"
                  disabled={submittingReview}
                  className="w-full py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm shadow-md disabled:opacity-50 hover-scale"
                >
                  {submittingReview ? 'Posting...' : t('submitReviewBtn')}
                </button>
              </form>
            ) : (
              <div className="text-center py-6">
                <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">{t('loginToReview')}</p>
                <Link
                  to="/login"
                  className="inline-block w-full py-2.5 rounded-xl bg-slate-150 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-sm font-bold transition-colors"
                >
                  Log In
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DestinationDetails;
