import json
import logging
import httpx
from typing import List, Dict, Any, Optional
from .config import settings

logger = logging.getLogger(__name__)

def clean_json_response(text: str) -> str:
    """Strips markdown code blocks from the response to get raw JSON."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

async def call_gemini_api(prompt: str, response_mime_type: Optional[str] = None) -> Optional[str]:
    """Helper to call Gemini API directly via HTTP."""
    api_key = settings.GEMINI_API_KEY
    if not api_key or "YOUR_GEMINI_API_KEY" in api_key or api_key.strip() == "":
        logger.warning("Gemini API key is not configured or is default. Using fallback.")
        return None

    # We use gemini-1.5-flash for speed and reliability
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    contents = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    if response_mime_type == "application/json":
        contents["generationConfig"] = {"responseMimeType": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=contents)
            if response.status_code == 200:
                result = response.json()
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                return text
            else:
                logger.error(f"Gemini API returned error {response.status_code}: {response.text}")
                return None
    except Exception as e:
        logger.error(f"Exception during Gemini API call: {str(e)}")
        return None

async def generate_itinerary_ai(destination: str, num_days: int, budget: float, language: str = "en") -> Dict[str, Any]:
    """Generates day-wise travel itineraries using Gemini or mock fallback."""
    lang_instruction = "Respond in Hindi." if language == "hi" else "Respond in English."
    
    prompt = f"""
    You are a professional travel planner. Generate a highly detailed, personalized day-wise travel itinerary for "{destination}" for {num_days} days.
    The budget is {budget} INR. {lang_instruction}

    You must output a valid JSON object. Do NOT wrap the JSON in ```json or any other formatting.
    The JSON structure MUST look exactly like this:
    {{
      "destination": "{destination}",
      "num_days": {num_days},
      "budget": {budget},
      "days": [
        {{
          "day": 1,
          "accommodation": "Name or area of recommended stay",
          "meals": {{
            "breakfast": "Recommended breakfast local food or place",
            "lunch": "Recommended lunch spot and cuisine",
            "dinner": "Recommended dinner spot with description"
          }},
          "activities": [
            {{
              "time": "Morning",
              "activity": "Detailed activity name, visiting tips",
              "cost": 150
            }},
            {{
              "time": "Afternoon",
              "activity": "Activity name and details",
              "cost": 200
            }},
            {{
              "time": "Evening",
              "activity": "Evening activity, sunset viewing or local market",
              "cost": 0
            }}
          ]
        }}
      ],
      "tips": [
        "Packing advice, local customs, bargaining, best transport options"
      ]
    }}
    """
    
    response_text = await call_gemini_api(prompt, response_mime_type="application/json")
    
    if response_text:
        try:
            cleaned = clean_json_response(response_text)
            return json.loads(cleaned)
        except Exception as e:
            logger.error(f"Failed to parse Gemini itinerary JSON: {str(e)}. Falling back to mock generator.")
            
    # Mock fallback generator
    return generate_mock_itinerary(destination, num_days, budget, language)

async def get_chatbot_reply_ai(user_message: str, chat_history: List[Dict[str, str]], language: str = "en") -> str:
    """Answers tourist questions using Gemini or mock responses."""
    lang_instruction = "Respond in Hindi." if language == "hi" else "Respond in English."
    
    # Format chat history for prompt context
    history_str = ""
    for msg in chat_history[-6:]:  # Take last 6 messages for context
        role = "User" if msg["sender"] == "user" else "Assistant"
        history_str += f"{role}: {msg['message']}\n"
        
    prompt = f"""
    You are TourEase AI, an friendly, knowledgeable travel assistant for tourists visiting India. 
    Provide advice about attractions, budget tips, local cuisine, transport, safety, and culture.
    {lang_instruction}
    
    Here is the recent conversation history:
    {history_str}
    User: {user_message}
    Assistant:"""
    
    reply = await call_gemini_api(prompt)
    if reply:
        return reply.strip()
        
    # Mock fallback chatbot response
    return get_mock_chatbot_reply(user_message, language)

async def get_recommendations_ai(preferences: Dict[str, Any], destinations_list: List[Dict[str, Any]], language: str = "en") -> List[int]:
    """Recommends destination IDs based on preferences like budget, category, state, and season."""
    # Since recommending IDs requires aligning database items, we construct a lightweight ranking query
    # and feed the items to Gemini to pick the best indices.
    places_str = "\n".join([f"ID: {d['id']}, Name: {d['name']}, State: {d['state']}, Category: {d['category']}, Budget: {d['budget_category']}, Season: {d['best_months']}" for d in destinations_list])
    
    prompt = f"""
    Based on these tourist preferences:
    - Target Budget Category: {preferences.get('budget', 'Any')}
    - Category Preference: {preferences.get('category', 'Any')}
    - Preferred State: {preferences.get('state', 'Any')}
    - Current Season/Month: {preferences.get('month', 'Any')}
    
    Rank the top 5 destination IDs that match best from the list below. Return ONLY a JSON list of integers representing the best destination IDs, e.g. [3, 1, 5]. Do NOT include explanations.
    
    Destinations list:
    {places_str}
    """
    
    response_text = await call_gemini_api(prompt, response_mime_type="application/json")
    if response_text:
        try:
            cleaned = clean_json_response(response_text)
            ids = json.loads(cleaned)
            if isinstance(ids, list):
                return [int(x) for x in ids if str(x).isdigit() or isinstance(x, int)]
        except Exception as e:
            logger.error(f"Failed to parse Gemini recommendation IDs: {str(e)}")
            
    # Simple Python filtering if Gemini fails or is not config'd
    ranked_ids = []
    category_pref = preferences.get('category', '').lower()
    budget_pref = preferences.get('budget', '').lower()
    state_pref = preferences.get('state', '').lower()
    month_pref = preferences.get('month', '').lower()
    
    scored_destinations = []
    for d in destinations_list:
        score = 0
        if category_pref and category_pref in d['category'].lower():
            score += 3
        if budget_pref and budget_pref in d['budget_category'].lower():
            score += 2
        if state_pref and state_pref in d['state'].lower():
            score += 2
        if month_pref:
            # Check if preferred month lies within best_months
            best_m = d.get('best_months', '') or ''
            if month_pref in best_m.lower():
                score += 3
        
        scored_destinations.append((score, d['id']))
        
    scored_destinations.sort(reverse=True, key=lambda x: x[0])
    return [item[1] for item in scored_destinations[:5]]

# --- MOCK GENERATORS ---

def generate_mock_itinerary(destination: str, num_days: int, budget: float, language: str = "en") -> Dict[str, Any]:
    """Generates a high-quality mock day-wise itinerary in English or Hindi."""
    is_hindi = language == "hi"
    
    stay_options = {
        "luxury": "Heritage Villa / 5-Star Boutique Resort" if not is_hindi else "हेरिटेज विला / 5-स्टार बुटीक रिसॉर्ट",
        "mid-range": "Cozy Premium Hotel near City Center" if not is_hindi else "सिटी सेंटर के पास आरामदायक प्रीमियम होटल",
        "budget": "Local Backpacker Hostel / Homestay" if not is_hindi else "स्थानीय बैकपैकर हॉस्टल / होमस्टे"
    }
    
    b_cat = "budget"
    if budget > 25000:
        b_cat = "luxury"
    elif budget > 8000:
        b_cat = "mid-range"
        
    accommodation = stay_options[b_cat]
    
    # Generic activity pool
    activities_pool = [
        {"act": "Explore iconic historical monuments and local museum", "cost": 100, "act_hi": "प्रतिष्ठित ऐतिहासिक स्मारकों और स्थानीय संग्रहालय का अन्वेषण करें"},
        {"act": "Guided walk around old bazaar and sampling street food delicacies", "cost": 150, "act_hi": "पुराने बाजार का निर्देशित भ्रमण और स्थानीय स्ट्रीट फूड व्यंजनों का स्वाद लेना"},
        {"act": "Nature trek and sightseeing around viewpoints", "cost": 0, "act_hi": "प्रकृति ट्रेक और सुंदर दृश्यों के आसपास भ्रमण"},
        {"act": "Leisurely shopping for local handicrafts and souvenir collection", "cost": 0, "act_hi": "स्थानीय हस्तशिल्प और स्मृति चिन्हों की खरीदारी"},
        {"act": "Boating, water activities or local heritage performance show", "cost": 300, "act_hi": "नौकाविहार, जल गतिविधियां या स्थानीय सांस्कृतिक शो"},
        {"act": "Visit to spiritual temples, churches or local meditation center", "cost": 50, "act_hi": "आध्यात्मिक मंदिरों, चर्चों या स्थानीय ध्यान केंद्र का दौरा"}
    ]
    
    days = []
    for day_num in range(1, num_days + 1):
        act1 = activities_pool[(day_num * 2) % len(activities_pool)]
        act2 = activities_pool[(day_num * 2 + 1) % len(activities_pool)]
        act3 = activities_pool[(day_num * 2 + 2) % len(activities_pool)]
        
        days.append({
            "day": day_num,
            "accommodation": f"{accommodation} (Day {day_num})" if not is_hindi else f"{accommodation} (दिन {day_num})",
            "meals": {
                "breakfast": "Traditional Local Breakfast & Chai" if not is_hindi else "पारंपरिक स्थानीय नाश्ता और चाय",
                "lunch": "Authentic Regional Thali Meal" if not is_hindi else "प्रामाणिक क्षेत्रीय थाली भोजन",
                "dinner": "Speciality Dining at a Top-rated Restaurant" if not is_hindi else "शीर्ष-रेटेड रेस्तरां में विशेष भोजन"
            },
            "activities": [
                {
                    "time": "Morning" if not is_hindi else "सुबह",
                    "activity": act1["act"] if not is_hindi else act1["act_hi"],
                    "cost": act1["cost"]
                },
                {
                    "time": "Afternoon" if not is_hindi else "दोपहर",
                    "activity": act2["act"] if not is_hindi else act2["act_hi"],
                    "cost": act2["cost"]
                },
                {
                    "time": "Evening" if not is_hindi else "शाम",
                    "activity": act3["act"] if not is_hindi else act3["act_hi"],
                    "cost": act3["cost"]
                }
            ]
        })
        
    tips = [
        "Carry cash since small local vendors do not always accept cards." if not is_hindi else "नकद साथ रखें क्योंकि छोटे स्थानीय विक्रेता हमेशा कार्ड स्वीकार नहीं करते हैं।",
        "Book entry tickets online in advance to skip long queues." if not is_hindi else "लंबी कतारों से बचने के लिए प्रवेश टिकट पहले से ऑनलाइन बुक करें।",
        "Use local transport like auto-rickshaws or e-rickshaws for short travel." if not is_hindi else "कम दूरी की यात्रा के लिए ऑटो-रिक्शा या ई-रिक्शा जैसे स्थानीय परिवहन का उपयोग करें।",
        "Hire registered local guides only and bargain politely at souvenir shops." if not is_hindi else "केवल पंजीकृत स्थानीय गाइड ही किराए पर लें और स्मृति चिन्हों की दुकानों पर विनम्रता से मोलभाव करें।"
    ]
    
    return {
        "destination": destination,
        "num_days": num_days,
        "budget": budget,
        "days": days,
        "tips": tips
    }

def get_mock_chatbot_reply(user_message: str, language: str = "en") -> str:
    """Provides smart mock chatbot replies for travel queries."""
    msg = user_message.lower()
    is_hindi = language == "hi"
    
    if is_hindi:
        if "ताज" in msg or "taj" in msg:
            return "ताजमहल उत्तर प्रदेश के आगरा में स्थित है। यह शुक्रवार को छोड़कर हर दिन सुबह 6 बजे से शाम 7 बजे तक खुला रहता है। ऑनलाइन टिकट लेना बेहतर होता है।"
        elif "बजट" in msg or "सस्ता" in msg:
            return "कम बजट में यात्रा करने के लिए: 1. होटल के बजाय होमस्टे या बैकपैकर हॉस्टल चुनें। 2. स्थानीय बस या ट्रेन का उपयोग करें। 3. स्ट्रीट फूड का आनंद लें जो स्वादिष्ट और सस्ता होता है।"
        elif "मौसम" in msg or "घूमने" in msg:
            return "भारत में घूमने के लिए अक्टूबर से मार्च का समय सबसे अच्छा माना जाता है, जब मौसम सुहावना और ठंडा रहता है। हालांकि, मानसून में पश्चिमी घाट और केरल भी सुंदर लगते हैं।"
        elif "सुरक्षा" in msg or "हेल्पलाइन" in msg:
            return "भारत में राष्ट्रीय पर्यटक हेल्पलाइन नंबर 1363 है, जो 24/7 उपलब्ध है। यात्रा के दौरान आपातकालीन संपर्क जानकारी हमेशा अपने पास रखें।"
        else:
            return f"नमस्ते! मैं आपका टूरिस्ट गाइड हूँ। आपने पूछा: '{user_message}'। मैं आपकी यात्रा योजना, बजट, टिकट बुकिंग या भारत में पर्यटन स्थलों के बारे में मदद कर सकता हूँ। कृपया अपना प्रश्न पूछें!"
    else:
        if "taj" in msg or "agra" in msg:
            return "The Taj Mahal is located in Agra, Uttar Pradesh. It is open daily except Fridays from sunrise to sunset (approx 6:00 AM to 7:00 PM). Foreign tourist tickets cost INR 1100 + taxes, and SAARC/BIMSTEC cost INR 540. Indian citizens cost INR 50."
        elif "budget" in msg or "cheap" in msg:
            return "To save money on your trip: \n1. Use Indian Railways (Sleeper/3AC classes) or state transport buses instead of private taxis.\n2. Stay in government-approved homestays or backpacker hostels.\n3. Try regional street food which is authentic, delicious, and highly budget-friendly."
        elif "weather" in msg or "best time" in msg or "season" in msg:
            return "Generally, October to March is the best window to visit India as the weather is pleasant nationwide. If you love snow, visit Himachal or Kashmir in January. For green landscapes and backwaters, Kerala during August/September is beautiful."
        elif "safety" in msg or "emergency" in msg:
            return "Safety is important. Keep photocopy documents, avoid isolated places at night, and use registered transport apps (Uber/Ola). The Tourist Helpline is 1363, and the Emergency national number is 112."
        else:
            return f"Hello! I am TourEase AI assistant. I received your message: '{user_message}'. I can guide you with day-by-day itineraries, recommend hidden gems, details on entry tickets, or share local food recommendations. What would you like to know?"
