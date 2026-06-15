import React, { createContext, useContext, useState, useEffect } from 'react';

const LanguageContext = createContext(null);

const translations = {
  en: {
    // Navigation
    brand: "TourEase AI",
    navHome: "Home",
    navDashboard: "Dashboard",
    navSearch: "Explore",
    navPlanner: "AI Planner",
    navChatbot: "AI Assistant",
    navEmergency: "Emergency",
    navHistory: "My Trips",
    navAdmin: "Admin Panel",
    navLogout: "Log Out",
    navLogin: "Sign In",
    navRegister: "Sign Up",
    languageLabel: "हिन्दी",

    // Hero / Landing
    heroTitle: "Discover Your Next Indian Adventure",
    heroSubtitle: "Explore hand-picked destinations, craft AI-powered custom itineraries, and view local amenities on live maps.",
    searchPlaceholder: "Search by state, city, category, or attraction...",
    searchBtn: "Search",
    trendingTitle: "Trending Destinations",
    trendingSubtitle: "Most visited tourist attractions loved by travelers this season",
    viewDetails: "View Details",
    freeEntry: "Free Entry",
    inr: "INR",

    // Dashboard
    dashWelcome: "Welcome back, {name}!",
    dashSubtitle: "Explore your saved destinations, historical trips, and tourism insights.",
    statFavorites: "Saved Favorites",
    statItineraries: "Planned Trips",
    statReviews: "Reviews Written",
    trendingPlaces: "Trending Near You",

    // Search Page
    searchTitle: "Find Your Perfect Gateway",
    searchFilterState: "All States",
    searchFilterCategory: "All Categories",
    searchFilterBudget: "All Budgets",
    searchFilterSeason: "All Seasons",
    noPlacesFound: "No destinations match your filters. Try adjusting your search!",

    // Destination Details
    detailsTimings: "Timings",
    detailsEntryFee: "Entry Fee",
    detailsBestMonths: "Best Months to Visit",
    nearbyAttractions: "Nearby Attractions",
    nearbyServices: "Nearby Tourism Amenities",
    reviewsHeader: "Visitor Reviews & Ratings",
    noReviews: "No reviews yet. Be the first to share your experience!",
    addReviewTitle: "Write a Review",
    ratingLabel: "Rating",
    commentLabel: "Share your experience...",
    submitReviewBtn: "Post Review",
    loginToReview: "Please log in to submit a review.",
    favoriteSuccess: "Added to favorites!",
    favoriteRemove: "Removed from favorites.",

    // AI Planner
    plannerTitle: "AI Trip Itinerary Planner",
    plannerSubtitle: "Provide your travel preferences, and our Gemini AI agent will generate a customized day-by-day itinerary.",
    fieldDestination: "Where do you want to go?",
    fieldDays: "Number of Days (1-14)",
    fieldBudget: "Total Budget (INR)",
    generateBtn: "Generate Itinerary with AI",
    generatingBtn: "Crafting your itinerary...",
    saveItineraryBtn: "Save Itinerary to Profile",
    itinerarySavedMsg: "Itinerary saved to your trip history!",
    accomodationLabel: "Stay Recommendation",
    breakfastLabel: "Breakfast",
    lunchLabel: "Lunch",
    dinnerLabel: "Dinner",
    activitiesLabel: "Day Schedule",
    tipsLabel: "Important Local Tips",

    // Chatbot
    chatTitle: "AI Travel Companion",
    chatSubtitle: "Ask me anything about Indian tourist places, cultural guidelines, budget hacks, or transportation tips.",
    chatInputPlaceholder: "Type your query here (e.g. How to visit Taj Mahal?)...",
    chatSendBtn: "Send",
    chatClearBtn: "Clear Chat",

    // Emergency Contacts
    emergencyTitle: "National & State Emergency Helplines",
    emergencySubtitle: "Access direct helpline numbers for safety, tourist support, medical aid, and fire services across Indian states.",
    emergencySearchLabel: "Select State to Filter",
    contactPolice: "Police Control Room",
    contactMedical: "Medical Emergency",
    contactFire: "Fire Station",
    contactDisaster: "Disaster Management",
    contactTourist: "Tourist Helpline",

    // Admin Dashboard
    adminStats: "Dashboard Analytics",
    adminTotalUsers: "Registered Users",
    adminTotalPlaces: "Total Destinations",
    adminTotalReviews: "Reviews Moderated",
    adminTotalFavorites: "Favorites Saved",
    adminCategoryBreakdown: "Destinations by Category",
    adminStateBreakdown: "Destinations by State",
    adminExportTitle: "Export System Reports (CSV)",
    adminExportUsers: "Export Users List",
    adminExportDestinations: "Export Destinations",
    adminExportReviews: "Export Reviews",
    adminManageDestinations: "Manage Destinations",
    adminAddBtn: "Add New Destination",
    adminEditBtn: "Edit",
    adminDeleteBtn: "Delete",
    adminConfirmDelete: "Are you sure you want to delete this place?",
    
    // Admin Destination Form
    adminFormAddTitle: "Add New Tourist Destination",
    adminFormEditTitle: "Edit Destination Details",
    adminFormName: "Destination Name",
    adminFormState: "State",
    adminFormCategory: "Category",
    adminFormDescription: "Description",
    adminFormImages: "Image URLs (Comma separated)",
    adminFormEntryFee: "Entry Fee (INR)",
    adminFormTimings: "Timings",
    adminFormBestMonths: "Best Months (Comma separated)",
    adminFormLat: "Latitude (Map center)",
    adminFormLng: "Longitude (Map center)",
    adminFormAttractions: "Nearby Attractions (JSON List)",
    adminFormServices: "Nearby Services (JSON List)",
    adminFormBudgetCategory: "Budget Category",
    adminFormTrending: "Mark as Trending",
    adminFormSave: "Save Destination",
    adminFormCancel: "Cancel",

    // Auth
    loginTitle: "Welcome Back to TourEase",
    registerTitle: "Begin Your Journey",
    fieldFullName: "Full Name",
    fieldEmail: "Email Address",
    fieldPassword: "Password",
    noAccount: "Don't have an account?",
    haveAccount: "Already registered?",
    authRequiredMsg: "Please log in to access this feature."
  },
  hi: {
    // Navigation
    brand: "टूरईज AI",
    navHome: "मुख्य पृष्ठ",
    navDashboard: "डैशबोर्ड",
    navSearch: "खोजें",
    navPlanner: "AI प्लानर",
    navChatbot: "AI सहायक",
    navEmergency: "आपातकालीन",
    navHistory: "मेरी यात्राएं",
    navAdmin: "एडमिन पैनल",
    navLogout: "लॉग आउट",
    navLogin: "लॉग इन",
    navRegister: "साइन अप",
    languageLabel: "English",

    // Hero / Landing
    heroTitle: "अपनी अगली भारतीय साहसिक यात्रा की खोज करें",
    heroSubtitle: "चुनिंदा स्थलों का पता लगाएं, AI-संचालित यात्रा कार्यक्रम बनाएं, और मानचित्रों पर स्थानीय सेवाओं को देखें।",
    searchPlaceholder: "राज्य, शहर, श्रेणी या आकर्षण द्वारा खोजें...",
    searchBtn: "खोजें",
    trendingTitle: "लोकप्रिय गंतव्य स्थल",
    trendingSubtitle: "इस मौसम में यात्रियों द्वारा सबसे अधिक पसंद किए गए पर्यटन आकर्षण",
    viewDetails: "विवरण देखें",
    freeEntry: "मुफ़्त प्रवेश",
    inr: "रुपये",

    // Dashboard
    dashWelcome: "वापसी पर स्वागत है, {name}!",
    dashSubtitle: "अपने सहेजे गए गंतव्यों, यात्रा इतिहास और पर्यटन अंतर्दृष्टि का पता लगाएं।",
    statFavorites: "सहेजे गए पसंदीदा",
    statItineraries: "नियोजित यात्राएं",
    statReviews: "लिखी गई समीक्षाएं",
    trendingPlaces: "आपके आस-पास लोकप्रिय",

    // Search Page
    searchTitle: "अपना सही गंतव्य खोजें",
    searchFilterState: "सभी राज्य",
    searchFilterCategory: "सभी श्रेणियां",
    searchFilterBudget: "सभी बजट",
    searchFilterSeason: "सभी मौसम",
    noPlacesFound: "आपके फिल्टर से मेल खाने वाला कोई गंतव्य नहीं मिला। अपनी खोज बदलें!",

    // Destination Details
    detailsTimings: "खुलने का समय",
    detailsEntryFee: "प्रवेश शुल्क",
    detailsBestMonths: "घूमने के लिए सबसे अच्छे महीने",
    nearbyAttractions: "आस-पास के आकर्षण",
    nearbyServices: "आस-पास की पर्यटन सुविधाएं",
    reviewsHeader: "यात्री समीक्षाएं और रेटिंग",
    noReviews: "अभी तक कोई समीक्षा नहीं है। अपना अनुभव साझा करने वाले पहले व्यक्ति बनें!",
    addReviewTitle: "समीक्षा लिखें",
    ratingLabel: "रेटिंग",
    commentLabel: "अपना अनुभव साझा करें...",
    submitReviewBtn: "समीक्षा पोस्ट करें",
    loginToReview: "समीक्षा सबमिट करने के लिए कृपया लॉग इन करें।",
    favoriteSuccess: "पसंदीदा में जोड़ा गया!",
    favoriteRemove: "पसंदीदा से हटा दिया गया।",

    // AI Planner
    plannerTitle: "AI यात्रा कार्यक्रम नियोजक",
    plannerSubtitle: "अपनी यात्रा प्राथमिकताएं प्रदान करें, और हमारा जेमिनी AI आपके लिए एक अनुकूलित दिन-वार यात्रा कार्यक्रम तैयार करेगा।",
    fieldDestination: "आप कहाँ जाना चाहते हैं?",
    fieldDays: "दिनों की संख्या (1-14)",
    fieldBudget: "कुल बजट (INR)",
    generateBtn: "AI के साथ यात्रा कार्यक्रम बनाएं",
    generatingBtn: "आपका यात्रा कार्यक्रम तैयार किया जा रहा है...",
    saveItineraryBtn: "यात्रा कार्यक्रम को सहेजें",
    itinerarySavedMsg: "यात्रा कार्यक्रम आपके इतिहास में सहेज लिया गया है!",
    accomodationLabel: "रुकने की सिफारिश",
    breakfastLabel: "नाश्ता",
    lunchLabel: "दोपहर का भोजन",
    dinnerLabel: "रात का भोजन",
    activitiesLabel: "दिन की गतिविधियां",
    tipsLabel: "महत्वपूर्ण स्थानीय सुझाव",

    // Chatbot
    chatTitle: "AI यात्रा साथी",
    chatSubtitle: "मुझसे भारतीय पर्यटन स्थलों, सांस्कृतिक दिशानिर्देशों, बजट हैक या परिवहन युक्तियों के बारे में कुछ भी पूछें।",
    chatInputPlaceholder: "अपना प्रश्न यहाँ टाइप करें (जैसे: ताजमहल कैसे जाएँ?)...",
    chatSendBtn: "भेजें",
    chatClearBtn: "चैट साफ करें",

    // Emergency Contacts
    emergencyTitle: "राष्ट्रीय और राज्य आपातकालीन हेल्पलाइन",
    emergencySubtitle: "भारतीय राज्यों में सुरक्षा, पर्यटक सहायता, चिकित्सा सहायता और अग्निशमन सेवाओं के लिए सीधे हेल्पलाइन नंबर प्राप्त करें।",
    emergencySearchLabel: "फिल्टर करने के लिए राज्य चुनें",
    contactPolice: "पुलिस नियंत्रण कक्ष",
    contactMedical: "चिकित्सा आपातकाल",
    contactFire: "दमकल केंद्र",
    contactDisaster: "आपदा प्रबंधन",
    contactTourist: "पर्यटक हेल्पलाइन",

    // Admin Dashboard
    adminStats: "डैशबोर्ड विश्लेषण",
    adminTotalUsers: "पंजीकृत उपयोगकर्ता",
    adminTotalPlaces: "कुल गंतव्य स्थल",
    adminTotalReviews: "समीक्षित समीक्षाएं",
    adminTotalFavorites: "सहेजे गए पसंदीदा",
    adminCategoryBreakdown: "श्रेणी द्वारा गंतव्य",
    adminStateBreakdown: "राज्य द्वारा गंतव्य",
    adminExportTitle: "सिस्टम रिपोर्ट निर्यात करें (CSV)",
    adminExportUsers: "उपयोगकर्ताओं की सूची निर्यात करें",
    adminExportDestinations: "गंतव्यों की सूची निर्यात करें",
    adminExportReviews: "समीक्षाओं की सूची निर्यात करें",
    adminManageDestinations: "गंतव्य प्रबंधन",
    adminAddBtn: "नया गंतव्य जोड़ें",
    adminEditBtn: "संपादित करें",
    adminDeleteBtn: "हटाएं",
    adminConfirmDelete: "क्या आप निश्चित रूप से इस स्थान को हटाना चाहते हैं?",

    // Admin Destination Form
    adminFormAddTitle: "नया पर्यटन स्थल जोड़ें",
    adminFormEditTitle: "गंतव्य विवरण संपादित करें",
    adminFormName: "गंतव्य का नाम",
    adminFormState: "राज्य",
    adminFormCategory: "श्रेणी",
    adminFormDescription: "विवरण",
    adminFormImages: "छवि URL (अल्पविराम से अलग)",
    adminFormEntryFee: "प्रवेश शुल्क (रुपये)",
    adminFormTimings: "खुलने का समय",
    adminFormBestMonths: "सर्वश्रेष्ठ महीने (अल्पविराम से अलग)",
    adminFormLat: "अक्षांश (मैप केंद्र)",
    adminFormLng: "रेखांश (मैप केंद्र)",
    adminFormAttractions: "आस-पास के आकर्षण (JSON सूची)",
    adminFormServices: "आस-पास की सेवाएं (JSON सूची)",
    adminFormBudgetCategory: "बजट श्रेणी",
    adminFormTrending: "ट्रेंडिंग के रूप में चिह्नित करें",
    adminFormSave: "गंतव्य सहेजें",
    adminFormCancel: "रद्द करें",

    // Auth
    loginTitle: "टूरईज में आपका स्वागत है",
    registerTitle: "अपनी यात्रा शुरू करें",
    fieldFullName: "पूरा नाम",
    fieldEmail: "ईमेल पता",
    fieldPassword: "पासवर्ड",
    noAccount: "खाता नहीं है?",
    haveAccount: "पहले से पंजीकृत हैं?",
    authRequiredMsg: "कृपया इस सुविधा का उपयोग करने के लिए लॉग इन करें।"
  }
};

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(localStorage.getItem('language') || 'en');

  useEffect(() => {
    localStorage.setItem('language', language);
  }, [language]);

  const toggleLanguage = () => {
    setLanguage((prev) => (prev === 'en' ? 'hi' : 'en'));
  };

  const t = (key, replacements = {}) => {
    let text = translations[language][key] || translations['en'][key] || key;
    
    // Perform dynamic replacements (e.g., {name})
    Object.keys(replacements).forEach((placeholder) => {
      text = text.replace(`{${placeholder}}`, replacements[placeholder]);
    });
    
    return text;
  };

  const value = {
    language,
    toggleLanguage,
    t
  };

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
};

export const useLanguage = () => useContext(LanguageContext);
