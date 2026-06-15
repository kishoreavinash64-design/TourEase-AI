import json
import random
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from .models import User, Category, Destination, EmergencyContact, Review
from .auth import get_password_hash

def seed_db():
    db = SessionLocal()
    try:
        print("Starting Clean Database Seeding...")
        
        # 1. Drop existing tables to ensure clean schema recreation (re-applies added city column)
        print("Dropping existing database tables...")
        Base.metadata.drop_all(bind=engine)
        
        print("Recreating database tables...")
        Base.metadata.create_all(bind=engine)
        
        # 2. Seed Users
        print("Seeding default credentials...")
        admin_user = User(
            email="admin@tourease.com",
            full_name="TourEase Admin",
            hashed_password=get_password_hash("AdminPassword123"),
            role="admin"
        )
        db.add(admin_user)
        
        test_user = User(
            email="user@tourease.com",
            full_name="Test User",
            hashed_password=get_password_hash("UserPassword123"),
            role="user"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print("Seeded accounts: admin@tourease.com / user@tourease.com")

        # 3. Seed Categories
        print("Seeding core categories...")
        categories_data = [
            {"name": "Heritage", "description": "Explore historical monuments, forts, and architectural masterpieces."},
            {"name": "Beaches", "description": "Relax on golden sands and experience thrilling water sports."},
            {"name": "Hill Stations", "description": "Escape to cold climates, green landscapes, and misty peaks."},
            {"name": "Spiritual", "description": "Connect with ancient temples, ghats, and spiritual centers."},
            {"name": "Wildlife", "description": "Discover national parks, sanctuaries, and exotic flora and fauna."}
        ]
        
        seeded_categories = {}
        for cat in categories_data:
            existing = Category(name=cat["name"], description=cat["description"])
            db.add(existing)
            db.commit()
            db.refresh(existing)
            seeded_categories[cat["name"]] = existing.id
        print("Categories seeded successfully.")

        # 4. Seed Emergency Contacts for the 10 Major States
        print("Seeding state emergency helplines...")
        emergency_data = [
            {
                "state": "Tamil Nadu", "police_contact": "100", "medical_contact": "108", 
                "fire_contact": "101", "disaster_management": "1077", "tourist_helpline": "04425333333"
            },
            {
                "state": "Kerala", "police_contact": "112", "medical_contact": "108", 
                "fire_contact": "101", "disaster_management": "1070", "tourist_helpline": "18004254747"
            },
            {
                "state": "Karnataka", "police_contact": "100", "medical_contact": "108", 
                "fire_contact": "101", "disaster_management": "1070", "tourist_helpline": "08022352828"
            },
            {
                "state": "Goa", "police_contact": "100", "medical_contact": "108", 
                "fire_contact": "101", "disaster_management": "1070", "tourist_helpline": "08322437037"
            },
            {
                "state": "Rajasthan", "police_contact": "100", "medical_contact": "108", 
                "fire_contact": "101", "disaster_management": "1070", "tourist_helpline": "01415090888"
            },
            {
                "state": "Himachal Pradesh", "police_contact": "112", "medical_contact": "108", 
                "fire_contact": "101", "disaster_management": "1070", "tourist_helpline": "18001808027"
            },
            {
                "state": "Uttarakhand", "police_contact": "112", "medical_contact": "108", 
                "fire_contact": "101", "disaster_management": "1070", "tourist_helpline": "1363"
            },
            {
                "state": "Jammu & Kashmir", "police_contact": "100", "medical_contact": "108", 
                "fire_contact": "101", "disaster_management": "1070", "tourist_helpline": "01942502274"
            },
            {
                "state": "Maharashtra", "police_contact": "100", "medical_contact": "108", 
                "fire_contact": "101", "disaster_management": "1070", "tourist_helpline": "1800229930"
            },
            {
                "state": "Delhi", "police_contact": "112", "medical_contact": "102", 
                "fire_contact": "101", "disaster_management": "1077", "tourist_helpline": "1281"
            }
        ]
        
        for em in emergency_data:
            contact = EmergencyContact(**em)
            db.add(contact)
        db.commit()
        print("Emergency contacts seeded.")

        # Category image assets for stunning UI rendering
        category_images = {
            "Heritage": [
                "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1590001155093-a3c66ab0c3ff?auto=format&fit=crop&q=80&w=800"
            ],
            "Beaches": [
                "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1519046904884-53103b34b206?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1505118380757-91f5f5632de0?auto=format&fit=crop&q=80&w=800"
            ],
            "Hill Stations": [
                "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1605649487212-47bdab064df7?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&q=80&w=800"
            ],
            "Spiritual": [
                "https://images.unsplash.com/photo-1561361531-7963c26d2b4b?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1627664813831-268ad26f4022?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1604514685562-f4b21bb7fd40?auto=format&fit=crop&q=80&w=800"
            ],
            "Wildlife": [
                "https://images.unsplash.com/photo-1602491453979-02654b3bc3ad?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1581852013749-2b69fbb7dbfe?auto=format&fit=crop&q=80&w=800",
                "https://images.unsplash.com/photo-1470240731273-7821a6eeb6bd?auto=format&fit=crop&q=80&w=800"
            ]
        }

        # 5. Core Raw Destinations Data
        print("Compiling 100+ tourist destinations...")
        raw_destinations = [
            # --- TAMIL NADU (11 Places) ---
            {
                "name": "Kodaikanal Lake", "state": "Tamil Nadu", "city": "Kodaikanal", "category": "Hill Stations",
                "description": "A star-shaped, man-made lake created in 1863 by Sir Vere Henry Levinge. It is the iconic center of tourism in Kodaikanal, surrounded by lush green hills, pathways, and boating clubs.",
                "best_months": "October, November, December, January", "latitude": 10.2307, "longitude": 77.4900,
                "entry_fee": 20.0, "timings": "6:00 AM - 6:30 PM", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Bryant Park", "distance": "0.5 km"}, {"name": "Coaker's Walk", "distance": "1.2 km"}]
            },
            {
                "name": "Coaker's Walk", "state": "Tamil Nadu", "city": "Kodaikanal", "category": "Hill Stations",
                "description": "A 1-kilometer paved pedestrian path constructed by Lt. Coaker in 1872. Runs along the edge of steep mountain slopes, offering spectacular panoramic views of valley plains.",
                "best_months": "October, November, December, January, February", "latitude": 10.2315, "longitude": 77.4932,
                "entry_fee": 10.0, "timings": "7:00 AM - 7:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Kodaikanal Lake", "distance": "1.2 km"}, {"name": "Bryant Park", "distance": "0.3 km"}]
            },
            {
                "name": "Bryant Park", "state": "Tamil Nadu", "city": "Kodaikanal", "category": "Hill Stations",
                "description": "A beautifully maintained 20.5-acre botanical garden planned and built in 1908 by H.D. Bryant. Houses a wide variety of flowers, shrubs, cacti, and a 160-year-old Eucalyptus tree.",
                "best_months": "October, November, December, January", "latitude": 10.2330, "longitude": 77.4945,
                "entry_fee": 30.0, "timings": "9:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Coaker's Walk", "distance": "0.3 km"}, {"name": "Kodaikanal Lake", "distance": "0.5 km"}]
            },
            {
                "name": "Pillar Rocks", "state": "Tamil Nadu", "city": "Kodaikanal", "category": "Hill Stations",
                "description": "Three vertical granite rock pillars standing shoulder-to-shoulder, measuring 122 meters (400 ft) high. Famed for beautiful viewpoints, mist coverings, and surrounding public park space.",
                "best_months": "October, November, December, January, February", "latitude": 10.2078, "longitude": 77.4712,
                "entry_fee": 10.0, "timings": "9:00 AM - 4:30 PM", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Guna Caves", "distance": "1.5 km"}, {"name": "Moir Point", "distance": "3.0 km"}]
            },
            {
                "name": "Silver Cascade Falls", "state": "Tamil Nadu", "city": "Kodaikanal", "category": "Hill Stations",
                "description": "A majestic 180-foot waterfall formed from the outflow of Kodaikanal Lake. Located on the main Ghat road, it is a popular pitstop featuring scenic mist sprays and local shops.",
                "best_months": "July, August, September, October, November", "latitude": 10.2520, "longitude": 77.5180,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Kodaikanal Lake", "distance": "8.0 km"}, {"name": "Shenbaganur Museum", "distance": "2.5 km"}]
            },
            {
                "name": "Guna Caves", "state": "Tamil Nadu", "city": "Kodaikanal", "category": "Hill Stations",
                "description": "Deep chambers formed between three giant Pillar Rocks, originally discovered by British officer BS Ward in 1821. Renamed after being featured in the famous Tamil movie 'Guna'.",
                "best_months": "October, November, December, January", "latitude": 10.2012, "longitude": 77.4582,
                "entry_fee": 20.0, "timings": "9:00 AM - 4:30 PM", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Pillar Rocks", "distance": "1.5 km"}, {"name": "Pine Forest", "distance": "2.0 km"}]
            },
            {
                "name": "Meenakshi Amman Temple", "state": "Tamil Nadu", "city": "Madurai", "category": "Spiritual",
                "description": "A historic Hindu temple complex located on the southern bank of the Vaigai River. Built in Dravidian style, it features 14 majestic Gopurams decorated with thousands of colorful stone figures.",
                "best_months": "October, November, December, January, February", "latitude": 9.9195, "longitude": 78.1193,
                "entry_fee": 0.0, "timings": "5:00 AM - 12:30 PM, 4:00 PM - 10:00 PM", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Thirumalai Nayakkar Palace", "distance": "1.5 km"}, {"name": "Alagar Koyil", "distance": "21.0 km"}]
            },
            {
                "name": "Brihadeeswarar Temple", "state": "Tamil Nadu", "city": "Thanjavur", "category": "Heritage",
                "description": "Built by Emperor Raja Raja Chola I in 1010 AD, this UNESCO World Heritage Site is an architectural wonder of pure granite. Its grand Vimana tower is one of the tallest in South India.",
                "best_months": "October, November, December, January", "latitude": 10.7828, "longitude": 79.1318,
                "entry_fee": 0.0, "timings": "6:00 AM - 12:30 PM, 4:00 PM - 8:30 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Thanjavur Royal Palace", "distance": "1.2 km"}, {"name": "Saraswathi Mahal Library", "distance": "1.1 km"}]
            },
            {
                "name": "Marina Beach", "state": "Tamil Nadu", "city": "Chennai", "category": "Beaches",
                "description": "The longest natural urban beach in the country, stretching 13 km along the Bay of Bengal. Famous for its sandy walks, sunset views, historical statues, and vibrant evening food shacks.",
                "best_months": "November, December, January, February", "latitude": 13.0500, "longitude": 80.2824,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "San Thome Cathedral", "distance": "2.0 km"}, {"name": "Fort St. George", "distance": "4.5 km"}]
            },
            {
                "name": "Ooty Doddabetta Peak", "state": "Tamil Nadu", "city": "Ooty", "category": "Hill Stations",
                "description": "The highest mountain peak in the Nilgiri Hills, standing at 2,637 meters. It is surrounded by reserved forest areas and features a telescope house at the top for bird-eye viewpoints.",
                "best_months": "October, November, December, March, April, May", "latitude": 11.4005, "longitude": 76.7360,
                "entry_fee": 20.0, "timings": "9:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Ooty Botanical Gardens", "distance": "7.0 km"}, {"name": "Ooty Lake", "distance": "9.5 km"}]
            },
            {
                "name": "Shore Temple", "state": "Tamil Nadu", "city": "Mahabalipuram", "category": "Heritage",
                "description": "Constructed in 700-728 AD overlooking the Bay of Bengal, this structure is one of the oldest structural stone temples in South India. It is part of the famous UNESCO group of monuments.",
                "best_months": "October, November, December, January", "latitude": 12.6162, "longitude": 80.1983,
                "entry_fee": 40.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Five Rathas", "distance": "1.5 km"}, {"name": "Krishna's Butterball", "distance": "1.0 km"}]
            },

            # --- KERALA (10 Places) ---
            {
                "name": "Munnar Tea Gardens", "state": "Kerala", "city": "Munnar", "category": "Hill Stations",
                "description": "Sweeping, lush green tea plantations covering mountain slopes in Western Ghats. Located at 1,600m altitude, it features misty mornings, walking trails, and tea processing museums.",
                "best_months": "September, October, November, December, January, February", "latitude": 10.0889, "longitude": 77.0595,
                "entry_fee": 20.0, "timings": "8:30 AM - 4:30 PM", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Eravikulam National Park", "distance": "8.0 km"}, {"name": "Mattupetty Dam", "distance": "11.0 km"}]
            },
            {
                "name": "Alappuzha Backwaters", "state": "Kerala", "city": "Alleppey", "category": "Beaches",
                "description": "An intricate network of brackish canals, lakes, and rivers, popular for traditional houseboat stays, lush palm-fringed banks, and peaceful village cruises.",
                "best_months": "October, November, December, January, February", "latitude": 9.4981, "longitude": 76.3388,
                "entry_fee": 1000.0, "timings": "24 Hours open (Houseboat checkin 12PM)", "budget_category": "Luxury", "is_trending": True,
                "attractions": [{"name": "Alappuzha Beach", "distance": "4.5 km"}, {"name": "Marari Beach", "distance": "14.0 km"}]
            },
            {
                "name": "Fort Kochi", "state": "Kerala", "city": "Kochi", "category": "Heritage",
                "description": "A historic seaside district known for its blend of Dutch, Portuguese, and British colonial bungalows, iconic Chinese fishing nets, and the oldest European church in India.",
                "best_months": "October, November, December, January, February", "latitude": 9.9658, "longitude": 76.2421,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "St. Francis Church", "distance": "0.3 km"}, {"name": "Mattancherry Palace", "distance": "2.5 km"}]
            },
            {
                "name": "Wayanad Wildlife Sanctuary", "state": "Kerala", "city": "Wayanad", "category": "Wildlife",
                "description": "Lush evergreen forest sanctuary home to tigers, leopards, Asian elephants, and wild boars. Integrates with the Nilgiri Biosphere Reserve.",
                "best_months": "October, November, December, January, February, March", "latitude": 11.6854, "longitude": 76.3659,
                "entry_fee": 110.0, "timings": "7:00 AM - 10:00 AM, 3:00 PM - 5:00 PM", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Edakkal Caves", "distance": "12.0 km"}, {"name": "Banasura Sagar Dam", "distance": "28.0 km"}]
            },
            {
                "name": "Kovalam Beach", "state": "Kerala", "city": "Kovalam", "category": "Beaches",
                "description": "A famous crescent-shaped beach comprised of three adjacent beaches. Famous for its red-and-white striped lighthouse, gentle water sports, and Ayurvedic massage resorts.",
                "best_months": "November, December, January, February", "latitude": 8.4004, "longitude": 76.9787,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Lighthouse Beach", "distance": "0.1 km"}, {"name": "Hawa Beach", "distance": "0.3 km"}]
            },
            {
                "name": "Varkala Cliff Beach", "state": "Kerala", "city": "Varkala", "category": "Beaches",
                "description": "A unique geological site featuring high red sandstone cliffs overlooking the Arabian Sea. Renamed 'Papanasam Beach', as its waters are believed to wash away sins.",
                "best_months": "October, November, December, January, February, March", "latitude": 8.7303, "longitude": 76.7082,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Janardanaswamy Temple", "distance": "1.2 km"}, {"name": "Anjengo Fort", "distance": "12.0 km"}]
            },
            {
                "name": "Periyar Tiger Reserve", "state": "Kerala", "city": "Thekkady", "category": "Wildlife",
                "description": "A protected reserve encompassing a scenic artificial lake. Famed for boat cruises to spot herd of wild elephants, sambar deer, and endemic bird species on shorelines.",
                "best_months": "October, November, December, January, February", "latitude": 9.4679, "longitude": 77.1436,
                "entry_fee": 150.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Kumily Spice Plantations", "distance": "4.0 km"}, {"name": "Pandikuzhi Viewpoint", "distance": "9.0 km"}]
            },
            {
                "name": "Athirappilly Waterfalls", "state": "Kerala", "city": "Athirappilly", "category": "Hill Stations",
                "description": "The largest waterfall in Kerala, standing 80 feet tall on the Chalakudy River. Surrounded by dense rainforests, often called the 'Niagara of India' for its scenic force.",
                "best_months": "June, July, August, September, October", "latitude": 10.2851, "longitude": 76.5698,
                "entry_fee": 50.0, "timings": "8:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Vazhachal Falls", "distance": "5.0 km"}, {"name": "Thumboormuzhy Dam", "distance": "15.0 km"}]
            },
            {
                "name": "Sree Padmanabhaswamy Temple", "state": "Kerala", "city": "Thiruvananthapuram", "category": "Spiritual",
                "description": "An ancient, gold-plated temple built in a fusion of Kerala and Dravidian architectural styles. Renowned as the wealthiest place of worship in the world.",
                "best_months": "October, November, December, January", "latitude": 8.4830, "longitude": 76.9436,
                "entry_fee": 0.0, "timings": "3:30 AM - 12:00 PM, 5:00 PM - 8:30 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Kuthira Malika Palace", "distance": "0.2 km"}, {"name": "Napier Museum", "distance": "3.5 km"}]
            },
            {
                "name": "Vagamon Pine Forest", "state": "Kerala", "city": "Vagamon", "category": "Hill Stations",
                "description": "A tranquil, man-made forest containing towering pine trees on steep mountain slopes. Popular for cool breezes, misty hill treks, and cinematic photo shoots.",
                "best_months": "October, November, December, January, March, April", "latitude": 9.6869, "longitude": 76.9038,
                "entry_fee": 10.0, "timings": "8:30 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Kurisumala Hill", "distance": "5.0 km"}, {"name": "Vagamon Meadows", "distance": "4.5 km"}]
            },

            # --- KARNATAKA (10 Places) ---
            {
                "name": "Hampi Ruins", "state": "Karnataka", "city": "Hampi", "category": "Heritage",
                "description": "The capital of the historic Vijayanagara Empire, now a UNESCO World Heritage Site. Features massive ruins of temples, royal pavilions, and the famous stone chariot of Vitthala Temple.",
                "best_months": "October, November, December, January, February", "latitude": 15.3350, "longitude": 76.4600,
                "entry_fee": 40.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Virupaksha Temple", "distance": "0.1 km"}, {"name": "Vitthala Temple Complex", "distance": "3.0 km"}]
            },
            {
                "name": "Mysore Palace", "state": "Karnataka", "city": "Mysore", "category": "Heritage",
                "description": "An Indo-Saracenic royal palace built in 1912 for the Wadiyar dynasty. Famous for its grand domes, arches, glass ceilings, and dazzling Sunday night illuminations with 97,000 bulbs.",
                "best_months": "October, November, December, January, February, March", "latitude": 12.3051, "longitude": 76.6551,
                "entry_fee": 70.0, "timings": "10:00 AM - 5:30 PM", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Chamundi Hills", "distance": "12.0 km"}, {"name": "Brindavan Gardens", "distance": "18.0 km"}]
            },
            {
                "name": "Coorg Abbey Falls", "state": "Karnataka", "city": "Madikeri", "category": "Hill Stations",
                "description": "A scenic waterfall nestled within dense coffee plantations and spice estates in the Western Ghats. Features a hanging bridge facing the gushing waters.",
                "best_months": "July, August, September, October, November, December", "latitude": 12.4369, "longitude": 75.7289,
                "entry_fee": 15.0, "timings": "9:00 AM - 5:00 PM", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Raja's Seat", "distance": "6.0 km"}, {"name": "Madikeri Fort", "distance": "5.5 km"}]
            },
            {
                "name": "Gokarna Om Beach", "state": "Karnataka", "city": "Gokarna", "category": "Beaches",
                "description": "A natural sand beach shaped like the sacred Hindu symbol 'Om'. Popular for clean waters, sunset hikes, dolphin boat rides, and seaside shacks.",
                "best_months": "October, November, December, January, February", "latitude": 14.5244, "longitude": 74.3204,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Kudle Beach", "distance": "2.0 km"}, {"name": "Mahabaleshwar Temple", "distance": "6.0 km"}]
            },
            {
                "name": "Lalbagh Botanical Garden", "state": "Karnataka", "city": "Bengaluru", "category": "Hill Stations",
                "description": "A historic 240-acre botanical garden commissioned by Hyder Ali in 1760. Houses a famous glasshouse modeled on London's Crystal Palace, hosting flower shows twice a year.",
                "best_months": "October, November, December, January, February", "latitude": 12.9507, "longitude": 77.5844,
                "entry_fee": 25.0, "timings": "6:00 AM - 7:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Cubbon Park", "distance": "4.0 km"}, {"name": "Bangalore Palace", "distance": "7.5 km"}]
            },
            {
                "name": "Bandipur National Park", "state": "Karnataka", "city": "Bandipur", "category": "Wildlife",
                "description": "A famous wildlife reserve under Project Tiger. Spans deciduous forests home to wild elephants, tigers, gaurs, and peacocks, serving as a wildlife corridor.",
                "best_months": "October, November, December, January, February, March", "latitude": 11.6664, "longitude": 76.6264,
                "entry_fee": 300.0, "timings": "6:00 AM - 9:00 AM, 3:00 PM - 6:00 PM (Safari)", "budget_category": "Luxury", "is_trending": False,
                "attractions": [{"name": "Mudumalai National Park", "distance": "15.0 km"}, {"name": "Himavad Gopalaswamy Betta", "distance": "18.0 km"}]
            },
            {
                "name": "Badami Cave Temples", "state": "Karnataka", "city": "Badami", "category": "Heritage",
                "description": "A complex of four rock-cut Hindu and Jain cave temples carved out of red sandstone cliffs in the 6th century. Showcases exquisite Chalukya carvings.",
                "best_months": "October, November, December, January", "latitude": 15.9189, "longitude": 75.6784,
                "entry_fee": 25.0, "timings": "9:00 AM - 5:30 PM", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Badami Fort", "distance": "1.0 km"}, {"name": "Pattadakal Temples", "distance": "22.0 km"}]
            },
            {
                "name": "Jog Falls", "state": "Karnataka", "city": "Sagara", "category": "Hill Stations",
                "description": "The second-highest plunge waterfall in India, formed by the Sharavathi River falling 830 feet in four distinct cascades named Raja, Roarer, Rocket, and Dame Blanche.",
                "best_months": "July, August, September, October", "latitude": 14.2285, "longitude": 74.8118,
                "entry_fee": 10.0, "timings": "9:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Linganamakki Dam", "distance": "6.0 km"}, {"name": "Dabbeh Falls", "distance": "20.0 km"}]
            },
            {
                "name": "Murudeshwar Temple", "state": "Karnataka", "city": "Murudeshwar", "category": "Spiritual",
                "description": "Famous for housing the world's second-tallest Shiva statue (123 feet) on the Arabian Sea coast. Features a 20-story Gopura offering lift access to views of Shiva's idol.",
                "best_months": "October, November, December, January, February", "latitude": 14.0942, "longitude": 74.4842,
                "entry_fee": 0.0, "timings": "3:00 AM - 1:00 PM, 3:00 PM - 8:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Murudeshwar Beach", "distance": "0.2 km"}, {"name": "Netrani Island", "distance": "19.0 km (by boat)"}]
            },
            {
                "name": "Mullayanagiri Peak", "state": "Karnataka", "city": "Chikmagalur", "category": "Hill Stations",
                "description": "The highest peak in Karnataka, standing at 1,930 meters in the Baba Budangiri range. Ideal for scenic trekking, offering misty views and a small temple dedicated to Sage Mulappa at the summit.",
                "best_months": "September, October, November, December, January, February", "latitude": 13.3908, "longitude": 75.7208,
                "entry_fee": 0.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Baba Budangiri", "distance": "24.0 km"}, {"name": "Hebbe Falls", "distance": "30.0 km"}]
            },

            # --- GOA (10 Places) ---
            {
                "name": "Calangute Beach", "state": "Goa", "city": "Calangute", "category": "Beaches",
                "description": "Known as the 'Queen of Beaches', it is the largest and busiest beach in North Goa, active with water sports, parasailing, beach shacks, and shopping outlets.",
                "best_months": "November, December, January, February", "latitude": 15.5494, "longitude": 73.7535,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Baga Beach", "distance": "1.5 km"}, {"name": "Candolim Beach", "distance": "3.0 km"}]
            },
            {
                "name": "Basilica of Bom Jesus", "state": "Goa", "city": "Old Goa", "category": "Heritage",
                "description": "A UNESCO World Heritage Site housing the mortal remains of St. Francis Xavier. Built in 1605, it is a masterpiece of Baroque architecture and Goa's oldest church.",
                "best_months": "October, November, December, January, February, March", "latitude": 15.5008, "longitude": 73.9116,
                "entry_fee": 0.0, "timings": "9:00 AM - 6:30 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Se Cathedral", "distance": "0.3 km"}, {"name": "Archaeological Museum", "distance": "0.4 km"}]
            },
            {
                "name": "Dudhsagar Falls", "state": "Goa", "city": "Sanguem", "category": "Wildlife",
                "description": "A four-tiered waterfall on the Mandovi River, cascading down 310 meters. It looks like a flowing sea of milk ('Dudhsagar') and is popular for forest jeep safaris.",
                "best_months": "June, July, August, September, October", "latitude": 15.3185, "longitude": 74.3138,
                "entry_fee": 400.0, "timings": "9:00 AM - 5:00 PM (Safari hours)", "budget_category": "Luxury", "is_trending": True,
                "attractions": [{"name": "Mollem National Park", "distance": "2.0 km"}, {"name": "Tambdi Surla Temple", "distance": "18.0 km"}]
            },
            {
                "name": "Palolem Beach", "state": "Goa", "city": "Canacona", "category": "Beaches",
                "description": "A gorgeous crescent-shaped beach in South Goa, known for its calm sea, scenic coco-palms, colorful wooden beach huts, and silent headphone disco parties.",
                "best_months": "November, December, January, February", "latitude": 15.0100, "longitude": 74.0267,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Butterfly Beach", "distance": "4.0 km (by boat)"}, {"name": "Agonda Beach", "distance": "9.0 km"}]
            },
            {
                "name": "Anjuna Beach", "state": "Goa", "city": "Anjuna", "category": "Beaches",
                "description": "Famous for its hippy heritage, rocky shores, beach bars, and the lively Wednesday Flea Market selling local handicrafts, clothes, and spices.",
                "best_months": "November, December, January, February", "latitude": 15.5731, "longitude": 73.7412,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Vagator Beach", "distance": "3.5 km"}, {"name": "Chapora Fort", "distance": "4.5 km"}]
            },
            {
                "name": "Fort Aguada", "state": "Goa", "city": "Sinquerim", "category": "Heritage",
                "description": "A well-preserved seventeenth-century Portuguese fort and lighthouse standing on Sinquerim beach, built in 1612 to guard against Dutch invasions.",
                "best_months": "October, November, December, January, February", "latitude": 15.4926, "longitude": 73.7735,
                "entry_fee": 25.0, "timings": "9:30 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Sinquerim Beach", "distance": "1.0 km"}, {"name": "Candolim Beach", "distance": "4.0 km"}]
            },
            {
                "name": "Chapora Fort", "state": "Goa", "city": "Vagator", "category": "Heritage",
                "description": "Famous as the sunset spot from the Bollywood movie 'Dil Chahta Hai'. Offers panoramic views of the Chapora River mouth and Vagator beach shoreline.",
                "best_months": "October, November, December, January, February", "latitude": 15.6067, "longitude": 73.7342,
                "entry_fee": 0.0, "timings": "9:30 AM - 5:30 PM", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Vagator Beach", "distance": "1.0 km"}, {"name": "Anjuna Beach", "distance": "3.5 km"}]
            },
            {
                "name": "Colva Beach", "state": "Goa", "city": "Colva", "category": "Beaches",
                "description": "One of South Goa's oldest and most developed beaches, stretching 20 km. Popular for local food shacks, swimming, jet skiing, and family picnics.",
                "best_months": "November, December, January, February", "latitude": 15.2750, "longitude": 73.9181,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Benaulim Beach", "distance": "3.0 km"}, {"name": "Sernabatim Beach", "distance": "2.2 km"}]
            },
            {
                "name": "Mangeshi Temple", "state": "Goa", "city": "Priol", "category": "Spiritual",
                "description": "A historic temple dedicated to Lord Shiva, featuring a striking blend of local Hindu, Christian, and Muslim styles, and an iconic 7-story Deepastambha (lamp tower).",
                "best_months": "October, November, December, January, February, March", "latitude": 15.4439, "longitude": 73.9681,
                "entry_fee": 0.0, "timings": "6:00 AM - 10:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Shanta Durga Temple", "distance": "7.0 km"}, {"name": "Sahakari Spice Farm", "distance": "11.0 km"}]
            },
            {
                "name": "Bhagwan Mahavir Wildlife Sanctuary", "state": "Goa", "city": "Mollem", "category": "Wildlife",
                "description": "A 240 sq km protected area in Western Ghats, containing evergreen forests, waterfalls, and animal populations including panthers, barking deer, and butterflies.",
                "best_months": "October, November, December, January, February", "latitude": 15.3789, "longitude": 74.2889,
                "entry_fee": 80.0, "timings": "8:30 AM - 5:30 PM", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Dudhsagar Falls", "distance": "12.0 km"}, {"name": "Tambdi Surla Mahadev Temple", "distance": "14.0 km"}]
            },

            # --- RAJASTHAN (10 Places) ---
            {
                "name": "Amber Fort", "state": "Rajasthan", "city": "Jaipur", "category": "Heritage",
                "description": "A magnificent hilltop fort built in 1592 by Raja Man Singh I. Features grand courtyards, decorative halls (Sheesh Mahal), and breathtaking lake mirror reflections.",
                "best_months": "October, November, December, January, February, March", "latitude": 26.9855, "longitude": 75.8513,
                "entry_fee": 100.0, "timings": "8:00 AM - 5:30 PM, 6:30 PM - 9:15 PM", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Jaigarh Fort", "distance": "1.5 km"}, {"name": "Panna Meena ka Kund", "distance": "0.8 km"}]
            },
            {
                "name": "Udaipur Lake Palace", "state": "Rajasthan", "city": "Udaipur", "category": "Heritage",
                "description": "A beautiful white marble palace built in 1746 on Lake Pichola. Now operated as a ultra-luxury hotel, it looks like a floating gem on water.",
                "best_months": "October, November, December, January, February, March", "latitude": 24.5756, "longitude": 73.6800,
                "entry_fee": 0.0, "timings": "24 Hours open (Only hotel guests/boat rides)", "budget_category": "Luxury", "is_trending": True,
                "attractions": [{"name": "City Palace Udaipur", "distance": "0.5 km (by boat)"}, {"name": "Jag Mandir", "distance": "1.0 km"}]
            },
            {
                "name": "Mehrangarh Fort", "state": "Rajasthan", "city": "Jodhpur", "category": "Heritage",
                "description": "One of the largest forts in India, built in 1459 by Rao Jodha. Rises 122 meters above Jodhpur's blue-colored skyline, displaying museum collections of palanquins and armor.",
                "best_months": "October, November, December, January, February", "latitude": 26.2978, "longitude": 73.0189,
                "entry_fee": 100.0, "timings": "9:00 AM - 5:00 PM", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Jaswant Thada", "distance": "1.0 km"}, {"name": "Umaid Bhawan Palace", "distance": "5.5 km"}]
            },
            {
                "name": "Jaisalmer Fort", "state": "Rajasthan", "city": "Jaisalmer", "category": "Heritage",
                "description": "Also known as the 'Golden Fort' (Sonar Qila), it is a rare living fort built in 1156 AD. Its sandstone walls glow like gold in the Thar desert.",
                "best_months": "October, November, December, January, February, March", "latitude": 26.9124, "longitude": 70.9130,
                "entry_fee": 50.0, "timings": "9:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Patwon Ki Haveli", "distance": "0.5 km"}, {"name": "Gadisar Lake", "distance": "1.5 km"}]
            },
            {
                "name": "Pushkar Lake", "state": "Rajasthan", "city": "Pushkar", "category": "Spiritual",
                "description": "A sacred lake in the center of Pushkar, surrounded by 52 bathing ghats. Famed for religious ceremonies and its rare 14th-century temple dedicated to Lord Brahma.",
                "best_months": "October, November, December, January, February", "latitude": 26.4894, "longitude": 74.5539,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Brahma Temple", "distance": "0.3 km"}, {"name": "Savitri Temple", "distance": "2.5 km"}]
            },
            {
                "name": "Mount Abu Dilwara Temples", "state": "Rajasthan", "city": "Mount Abu", "category": "Hill Stations",
                "description": "Built between 11th and 13th centuries, these Jain temples are globally famous for their marble carvings, ceilings, and dome carvings.",
                "best_months": "October, November, December, January, February, March", "latitude": 24.6092, "longitude": 72.7225,
                "entry_fee": 0.0, "timings": "12:00 PM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Nakki Lake", "distance": "3.0 km"}, {"name": "Guru Shikhar Peak", "distance": "12.0 km"}]
            },
            {
                "name": "Keoladeo National Park", "state": "Rajasthan", "city": "Bharatpur", "category": "Wildlife",
                "description": "Formerly known as Bharatpur Bird Sanctuary, this UNESCO World Heritage Site is home to over 370 bird species, including migratory birds like Siberian Cranes.",
                "best_months": "October, November, December, January, February", "latitude": 27.1594, "longitude": 77.5222,
                "entry_fee": 75.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Bharatpur Palace", "distance": "4.0 km"}, {"name": "Lohagarh Fort", "distance": "5.0 km"}]
            },
            {
                "name": "Chittorgarh Fort", "state": "Rajasthan", "city": "Chittorgarh", "category": "Heritage",
                "description": "The largest fort complex in India, spreading over 700 acres on a hill. Landmark monuments include Tower of Victory (Vijay Stambha) and Tower of Fame.",
                "best_months": "October, November, December, January, February", "latitude": 24.8879, "longitude": 74.6451,
                "entry_fee": 40.0, "timings": "9:45 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Vijay Stambha", "distance": "0.1 km"}, {"name": "Padmini Palace", "distance": "1.5 km"}]
            },
            {
                "name": "Ranthambore Tiger Reserve", "state": "Rajasthan", "city": "Sawai Madhopur", "category": "Wildlife",
                "description": "A vast wildlife reserve famous for its Bengal tigers. Set around the historic 10th-century Ranthambore Fort, it is a premier destination for open-jeep tiger safaris.",
                "best_months": "October, November, December, January, February, March, April", "latitude": 25.8672, "longitude": 76.3014,
                "entry_fee": 1200.0, "timings": "6:00 AM - 9:30 AM, 2:00 PM - 5:30 PM", "budget_category": "Luxury", "is_trending": True,
                "attractions": [{"name": "Ranthambore Fort", "distance": "5.0 km"}, {"name": "Trinetra Ganesh Temple", "distance": "5.1 km"}]
            },
            {
                "name": "Hawa Mahal", "state": "Rajasthan", "city": "Jaipur", "category": "Heritage",
                "description": "Built in 1799 by Maharaja Sawai Pratap Singh, the 'Palace of Winds' features 953 small windows (jharokhas) arranged in a honeycomb layout to let royal ladies observe city life.",
                "best_months": "October, November, December, January, February, March", "latitude": 26.9239, "longitude": 75.8267,
                "entry_fee": 50.0, "timings": "9:00 AM - 4:30 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "City Palace", "distance": "0.8 km"}, {"name": "Jantar Mantar", "distance": "0.7 km"}]
            },

            # --- HIMACHAL PRADESH (10 Places) ---
            {
                "name": "Solang Valley", "state": "Himachal Pradesh", "city": "Manali", "category": "Hill Stations",
                "description": "A famous side valley at the top of Kullu valley, renowned for adventure sports. Active with paragliding, zorbing, and quad-biking in summer, and skiing in winter.",
                "best_months": "October, November, December, January, February, March, April, May", "latitude": 32.3167, "longitude": 77.1667,
                "entry_fee": 0.0, "timings": "9:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Anjani Mahadev Temple", "distance": "2.0 km"}, {"name": "Manali Valley", "distance": "13.0 km"}]
            },
            {
                "name": "Shimla Mall Road", "state": "Himachal Pradesh", "city": "Shimla", "category": "Hill Stations",
                "description": "The pedestrian-only central street of Shimla, lined with colonial buildings, shops, cafes, and restaurants. Features views of snow-capped mountains.",
                "best_months": "October, November, December, January, February, March, April, May", "latitude": 31.1048, "longitude": 77.1734,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "The Ridge", "distance": "0.1 km"}, {"name": "Christ Church", "distance": "0.2 km"}]
            },
            {
                "name": "Dharamshala McLeod Ganj", "state": "Himachal Pradesh", "city": "Dharamshala", "category": "Spiritual",
                "description": "Famed as the residence of the Dalai Lama. This high-altitude town is a center of Tibetan culture, monasteries, and the start of the scenic Triund mountain trek.",
                "best_months": "September, October, November, March, April, May, June", "latitude": 32.2426, "longitude": 77.3213,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Tsuglagkhang Temple", "distance": "0.5 km"}, {"name": "Bhagsunag Waterfall", "distance": "2.0 km"}]
            },
            {
                "name": "Dalhousie Khajjiar", "state": "Himachal Pradesh", "city": "Dalhousie", "category": "Hill Stations",
                "description": "Often called the 'Mini Switzerland of India', Khajjiar features a saucer-shaped meadow surrounded by giant deodar trees, containing a small lake in the center.",
                "best_months": "October, November, December, March, April, May, June", "latitude": 32.5532, "longitude": 76.0651,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Kalatop Wildlife Sanctuary", "distance": "10.0 km"}, {"name": "Panchpula Falls", "distance": "22.0 km"}]
            },
            {
                "name": "Rohtang Pass", "state": "Himachal Pradesh", "city": "Manali", "category": "Hill Stations",
                "description": "A high mountain pass at 3,978 meters connecting Kullu Valley with Spiti Valleys. Offers glaciers, snow, and paragliding vistas.",
                "best_months": "May, June, July, September, October", "latitude": 32.3716, "longitude": 77.2466,
                "entry_fee": 550.0, "timings": "6:00 AM - 6:00 PM (Closed on Tuesdays)", "budget_category": "Luxury", "is_trending": True,
                "attractions": [{"name": "Solang Valley", "distance": "38.0 km"}, {"name": "Rahala Waterfalls", "distance": "16.0 km"}]
            },
            {
                "name": "Kasol Parvati Valley", "state": "Himachal Pradesh", "city": "Kasol", "category": "Hill Stations",
                "description": "A hippie village on the banks of the Parvati River. Known for Israeli cafes, trekking routes (Kheerganga), hot water springs, and beautiful forests.",
                "best_months": "October, November, December, March, April, May, June", "latitude": 32.0100, "longitude": 77.3150,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Manikaran Sahib Gurudwara", "distance": "4.5 km"}, {"name": "Tosh Village", "distance": "20.0 km"}]
            },
            {
                "name": "Great Himalayan National Park", "state": "Himachal Pradesh", "city": "Kullu", "category": "Wildlife",
                "description": "A UNESCO World Heritage Site containing pristine alpine meadows and snow peak basins. Habitat for Snow Leopards, Musk Deer, and rare Western Tragopan birds.",
                "best_months": "October, November, December, March, April, May", "latitude": 31.7333, "longitude": 77.4333,
                "entry_fee": 100.0, "timings": "24 Hours open (Trekking permit needed)", "budget_category": "Luxury", "is_trending": False,
                "attractions": [{"name": "Tirthan Valley", "distance": "5.0 km"}, {"name": "Jalori Pass", "distance": "25.0 km"}]
            },
            {
                "name": "Kaza Spiti Valley", "state": "Himachal Pradesh", "city": "Kaza", "category": "Hill Stations",
                "description": "Located in a cold desert valley, Kaza is the administrative center of Spiti. Features ancient monasteries (Key Monastery), small high-altitude villages, and riverbeds.",
                "best_months": "May, June, July, August, September", "latitude": 32.2224, "longitude": 78.0709,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Luxury", "is_trending": False,
                "attractions": [{"name": "Key Monastery", "distance": "14.0 km"}, {"name": "Kibber Village", "distance": "19.0 km"}]
            },
            {
                "name": "Jakhoo Temple", "state": "Himachal Pradesh", "city": "Shimla", "category": "Spiritual",
                "description": "An ancient temple dedicated to Hanuman, housing a giant 108-foot orange Hanuman statue. Situated at Shimla's highest peak, surrounded by monkeys.",
                "best_months": "October, November, December, March, April, May", "latitude": 31.1012, "longitude": 77.1852,
                "entry_fee": 0.0, "timings": "7:00 AM - 8:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Shimla Mall Road", "distance": "2.0 km"}, {"name": "Christ Church", "distance": "1.8 km"}]
            },
            {
                "name": "Bir Billing", "state": "Himachal Pradesh", "city": "Bir", "category": "Hill Stations",
                "description": "The paragliding capital of India. Bir is a Tibetan colony containing monasteries, while Billing is the take-off site offering panoramic flights down.",
                "best_months": "October, November, December, March, April, May, June", "latitude": 32.0435, "longitude": 76.7241,
                "entry_fee": 0.0, "timings": "8:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Sherab Ling Monastery", "distance": "6.0 km"}, {"name": "Deer Park Institute", "distance": "0.5 km"}]
            },

            # --- UTTARAKHAND (10 Places) ---
            {
                "name": "Rishikesh Laxman Jhula", "state": "Uttarakhand", "city": "Rishikesh", "category": "Spiritual",
                "description": "An iconic 450-foot hanging iron bridge across the Ganges. Famed as the 'Yoga Capital of the World', it features ashrams, river rafting camps, and the nightly Ganga Aarti.",
                "best_months": "October, November, December, March, April, May", "latitude": 30.1300, "longitude": 78.3300,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Triveni Ghat", "distance": "3.5 km"}, {"name": "Beatles Ashram", "distance": "1.5 km"}]
            },
            {
                "name": "Haridwar Har Ki Pauri", "state": "Haridwar", "city": "Haridwar", "category": "Spiritual",
                "description": "The sacred ghat on the banks of the Ganges, believed to contain footprints of Lord Vishnu. Famed for its spectacular evening Ganga Aarti.",
                "best_months": "October, November, December, March, April, May", "latitude": 29.9650, "longitude": 78.1700,
                "entry_fee": 0.0, "timings": "24 Hours open (Aarti at 6:00 PM)", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Mansa Devi Temple", "distance": "2.5 km"}, {"name": "Chandi Devi Temple", "distance": "4.0 km"}]
            },
            {
                "name": "Nainital Naini Lake", "state": "Uttarakhand", "city": "Nainital", "category": "Hill Stations",
                "description": "A natural pear-shaped freshwater lake situated amidst pine hills. Offers sailing, a lakeside Mall Road, and the Naina Devi temple on its shore.",
                "best_months": "October, November, December, March, April, May, June", "latitude": 29.3900, "longitude": 79.4500,
                "entry_fee": 0.0, "timings": "6:00 AM - 6:00 PM (Boating)", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Naina Devi Temple", "distance": "0.1 km"}, {"name": "Snow View Point", "distance": "2.5 km"}]
            },
            {
                "name": "Mussoorie Kempty Falls", "state": "Uttarakhand", "city": "Mussoorie", "category": "Hill Stations",
                "description": "A popular 40-foot waterfall cascading through rock shelves. Renowned for its giant swimming pools at the bottom, offering colonial cable car rides.",
                "best_months": "October, November, December, March, April, May, June", "latitude": 30.4550, "longitude": 78.0770,
                "entry_fee": 0.0, "timings": "8:00 AM - 5:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Mall Road Mussoorie", "distance": "15.0 km"}, {"name": "Lal Tibba Viewpoint", "distance": "20.0 km"}]
            },
            {
                "name": "Valley of Flowers", "state": "Uttarakhand", "city": "Chamoli", "category": "Wildlife",
                "description": "An alpine valley containing meadows of endemic alpine flowers in Western Himalayas. UNESCO World Heritage Site accessible only via trekking.",
                "best_months": "July, August, September", "latitude": 30.7280, "longitude": 79.6053,
                "entry_fee": 150.0, "timings": "7:00 AM - 5:00 PM", "budget_category": "Luxury", "is_trending": True,
                "attractions": [{"name": "Hemkund Sahib", "distance": "6.0 km (steep trek)"}, {"name": "Ghangaria Base Camp", "distance": "3.5 km"}]
            },
            {
                "name": "Jim Corbett National Park", "state": "Uttarakhand", "city": "Ramnagar", "category": "Wildlife",
                "description": "The oldest national park in India, established in 1936 to protect endangered Bengal tigers. Famous for open-top jeep safaris along the Ramganga River.",
                "best_months": "November, December, January, February, March, April, May", "latitude": 29.5300, "longitude": 78.7750,
                "entry_fee": 1000.0, "timings": "6:00 AM - 9:30 AM, 2:00 PM - 5:30 PM", "budget_category": "Luxury", "is_trending": True,
                "attractions": [{"name": "Corbett Waterfall", "distance": "25.0 km"}, {"name": "Garjiya Devi Temple", "distance": "14.0 km"}]
            },
            {
                "name": "Kedarnath Temple", "state": "Uttarakhand", "city": "Kedarnath", "category": "Spiritual",
                "description": "One of the most sacred Hindu temples dedicated to Lord Shiva, located in the snow-capped Garhwal Himalayas at 3,583 meters. Requires a 16 km trek from Gaurikund.",
                "best_months": "May, June, September, October", "latitude": 30.7352, "longitude": 79.0669,
                "entry_fee": 0.0, "timings": "4:00 AM - 9:00 PM (Closed in Winter)", "budget_category": "Luxury", "is_trending": True,
                "attractions": [{"name": "Bhairav Temple", "distance": "0.5 km"}, {"name": "Vasuki Tal Lake", "distance": "8.0 km"}]
            },
            {
                "name": "Badrinath Temple", "state": "Uttarakhand", "city": "Badrinath", "category": "Spiritual",
                "description": "A sacred temple dedicated to Lord Vishnu, situated along the Alaknanda River. One of the Char Dham pilgrimage sites, featuring a colorful facade.",
                "best_months": "May, June, September, October", "latitude": 30.7448, "longitude": 79.4912,
                "entry_fee": 0.0, "timings": "4:30 AM - 9:00 PM (Closed in Winter)", "budget_category": "Luxury", "is_trending": False,
                "attractions": [{"name": "Mana Village (Last Indian Village)", "distance": "3.0 km"}, {"name": "Tapt Kund Hot Springs", "distance": "0.1 km"}]
            },
            {
                "name": "Auli Ski Resort", "state": "Uttarakhand", "city": "Joshimath", "category": "Hill Stations",
                "description": "A premier ski destination in India, containing slopes surrounded by oak and coniferous forests. Offers views of the Nanda Devi mountain range.",
                "best_months": "December, January, February, March", "latitude": 30.5289, "longitude": 79.5661,
                "entry_fee": 0.0, "timings": "24 Hours open (Cable car: 9:00 AM - 5:00 PM)", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Joshimath Ropeway", "distance": "4.0 km"}, {"name": "Gorson Bugyal", "distance": "3.0 km (trek)"}]
            },
            {
                "name": "Binsar Wildlife Sanctuary", "state": "Uttarakhand", "city": "Almora", "category": "Wildlife",
                "description": "A scenic wildlife sanctuary containing dense oak and rhododendron forests. Offers panoramic views of Himalayan peaks like Trishul, Nanda Devi, and Panchachuli.",
                "best_months": "October, November, December, January, March, April, May", "latitude": 29.6978, "longitude": 79.7578,
                "entry_fee": 150.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Zero Point View", "distance": "2.0 km (trek)"}, {"name": "Binsar Mahadev Temple", "distance": "15.0 km"}]
            },

            # --- JAMMU & KASHMIR (10 Places) ---
            {
                "name": "Srinagar Dal Lake", "state": "Jammu & Kashmir", "city": "Srinagar", "category": "Hill Stations",
                "description": "The jewel of Kashmir tourism. A scenic urban lake famous for decorated wooden houseboats, floating gardens, and traditional Shikara boat rides.",
                "best_months": "October, November, December, March, April, May, June, July", "latitude": 34.0837, "longitude": 74.8722,
                "entry_fee": 0.0, "timings": "24 Hours open (Shikaras: 6:00 AM - 8:00 PM)", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Shalimar Bagh", "distance": "6.0 km"}, {"name": "Nishat Bagh", "distance": "4.5 km"}]
            },
            {
                "name": "Gulmarg Gondola", "state": "Jammu & Kashmir", "city": "Gulmarg", "category": "Hill Stations",
                "description": "The second-highest cable car lift in the world, rising to 3,979m on Apharwat peak. Gulmarg is India's top winter skiing resort, offering snowy landscapes.",
                "best_months": "December, January, February, March, April", "latitude": 34.0538, "longitude": 74.3831,
                "entry_fee": 740.0, "timings": "10:00 AM - 5:00 PM", "budget_category": "Luxury", "is_trending": True,
                "attractions": [{"name": "Apharwat Peak", "distance": "0.1 km"}, {"name": "Gulmarg Golf Course", "distance": "2.0 km"}]
            },
            {
                "name": "Pahalgam Betaab Valley", "state": "Jammu & Kashmir", "city": "Pahalgam", "category": "Hill Stations",
                "description": "Named after the Bollywood movie 'Betaab', this valley features pine forests, green meadows, and the crystal-clear waters of the flowing Lidder River.",
                "best_months": "October, November, March, April, May, June", "latitude": 34.0161, "longitude": 75.3150,
                "entry_fee": 100.0, "timings": "8:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Aru Valley", "distance": "12.0 km"}, {"name": "Chandanwari", "distance": "16.0 km"}]
            },
            {
                "name": "Sonamarg Meadow of Gold", "state": "Jammu & Kashmir", "city": "Sonamarg", "category": "Hill Stations",
                "description": "A high mountain valley known for Thajiwas Glacier. Features snow slides, alpine lakes, and serves as a gateway to Ladakh treks.",
                "best_months": "May, June, July, August, September, October", "latitude": 34.3000, "longitude": 75.3000,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Luxury", "is_trending": False,
                "attractions": [{"name": "Thajiwas Glacier", "distance": "3.0 km"}, {"name": "Zoji La Pass", "distance": "24.0 km"}]
            },
            {
                "name": "Vaishno Devi Temple", "state": "Jammu & Kashmir", "city": "Katra", "category": "Spiritual",
                "description": "A sacred Hindu cave temple dedicated to Vaishno Devi, located on Trikuta Mountains. Millions of pilgrims make the 13 km uphill trek from Katra annually.",
                "best_months": "October, November, December, March, April, May", "latitude": 33.0300, "longitude": 74.9500,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Bhairon Ghati Temple", "distance": "1.5 km (steep trek)"}, {"name": "Katra Town", "distance": "13.0 km"}]
            },
            {
                "name": "Amarnath Cave", "state": "Jammu & Kashmir", "city": "Baltal", "category": "Spiritual",
                "description": "A sacred shrine containing a natural ice stalagmite representing Shiva Linga. Located at 3,888m, accessible only during the annual July/August pilgrimage.",
                "best_months": "July, August", "latitude": 34.2155, "longitude": 75.5122,
                "entry_fee": 0.0, "timings": "6:00 AM - 5:00 PM (Seasonal)", "budget_category": "Luxury", "is_trending": False,
                "attractions": [{"name": "Baltal Camp", "distance": "14.0 km"}, {"name": "Panchtarni Camp", "distance": "6.0 km"}]
            },
            {
                "name": "Leh Palace", "state": "Jammu & Kashmir", "city": "Leh", "category": "Heritage",
                "description": "A nine-story royal palace built in the 17th century, overlooking Leh city. Modeled on Lhasa's Potala Palace, displaying Buddhist paintings and art.",
                "best_months": "May, June, July, August, September", "latitude": 34.1658, "longitude": 77.5861,
                "entry_fee": 25.0, "timings": "8:00 AM - 5:00 PM", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Shanti Stupa", "distance": "3.5 km"}, {"name": "Namgyal Tsemo", "distance": "1.0 km"}]
            },
            {
                "name": "Pangong Tso Lake", "state": "Jammu & Kashmir", "city": "Ladakh", "category": "Hill Stations",
                "description": "A high-altitude saltwater lake spanning from India to Tibet. Famed for changing colors from blue to turquoise, and its barren mountain backdrop.",
                "best_months": "May, June, July, August, September", "latitude": 33.7292, "longitude": 78.8550,
                "entry_fee": 20.0, "timings": "24 Hours open (Inner line permit needed)", "budget_category": "Luxury", "is_trending": True,
                "attractions": [{"name": "Spangmik Village", "distance": "5.0 km"}, {"name": "Chang La Pass", "distance": "75.0 km"}]
            },
            {
                "name": "Nubra Valley", "state": "Jammu & Kashmir", "city": "Diskit", "category": "Hill Stations",
                "description": "A cold mountain desert valley known for its double-humped Bactrian camels, sand dunes, and the giant 32-meter statue of Maitreya Buddha at Diskit.",
                "best_months": "May, June, July, August, September", "latitude": 34.5428, "longitude": 77.4292,
                "entry_fee": 20.0, "timings": "24 Hours open (Inner line permit needed)", "budget_category": "Luxury", "is_trending": False,
                "attractions": [{"name": "Diskit Monastery", "distance": "2.0 km"}, {"name": "Hunder Sand Dunes", "distance": "8.0 km"}]
            },
            {
                "name": "Shalimar Bagh", "state": "Jammu & Kashmir", "city": "Srinagar", "category": "Heritage",
                "description": "The largest Mughal garden in Kashmir, built in 1619 by Emperor Jahangir for his wife Nur Jahan. Features terraces, water fountains, and chinar trees.",
                "best_months": "October, November, March, April, May, June, July", "latitude": 34.1500, "longitude": 74.8736,
                "entry_fee": 24.0, "timings": "9:00 AM - 7:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Nishat Bagh", "distance": "3.5 km"}, {"name": "Srinagar Dal Lake", "distance": "6.0 km"}]
            },

            # --- MAHARASHTRA (10 Places) ---
            {
                "name": "Gateway of India", "state": "Maharashtra", "city": "Mumbai", "category": "Heritage",
                "description": "An iconic basalt arch monument built in 1924 to commemorate the landing of King George V. Overlooks Mumbai harbor and serves as the starting point for Elephanta caves ferries.",
                "best_months": "October, November, December, January, February, March", "latitude": 18.9220, "longitude": 72.8347,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Taj Mahal Palace Hotel", "distance": "0.1 km"}, {"name": "Elephanta Caves", "distance": "10.0 km (by ferry)"}]
            },
            {
                "name": "Ajanta Caves", "state": "Maharashtra", "city": "Aurangabad", "category": "Heritage",
                "description": "A complex of 30 rock-cut Buddhist caves dating from 2nd century BC. Famous for mural paintings, stone sculptures depicting Jataka tales.",
                "best_months": "October, November, December, January, February, March", "latitude": 20.5519, "longitude": 75.7003,
                "entry_fee": 40.0, "timings": "9:00 AM - 5:00 PM (Closed on Mondays)", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Ellora Caves", "distance": "95.0 km"}, {"name": "Bibi Ka Maqbara", "distance": "100.0 km"}]
            },
            {
                "name": "Ellora Caves", "state": "Maharashtra", "city": "Aurangabad", "category": "Heritage",
                "description": "A UNESCO site containing 34 rock-cut caves of Hindu, Buddhist, and Jain origins. Famous for Cave 16 housing the monumental Kailasa Temple.",
                "best_months": "October, November, December, January, February, March", "latitude": 20.0268, "longitude": 75.1780,
                "entry_fee": 40.0, "timings": "6:00 AM - 6:00 PM (Closed on Tuesdays)", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Grishneshwar Jyotirlinga Temple", "distance": "1.0 km"}, {"name": "Daulatabad Fort", "distance": "13.0 km"}]
            },
            {
                "name": "Lonavala Tiger's Leap", "state": "Maharashtra", "city": "Lonavala", "category": "Hill Stations",
                "description": "A cliff-top viewpoint with a sheer drop of 650 meters, looking like a leaping tiger. Popular for mist, green valleys, and waterfall hikes in monsoons.",
                "best_months": "June, July, August, September, October, November, December", "latitude": 18.7543, "longitude": 73.4074,
                "entry_fee": 0.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Bhushi Dam", "distance": "4.5 km"}, {"name": "Karla Caves", "distance": "15.0 km"}]
            },
            {
                "name": "Mahabaleshwar Viewpoints", "state": "Maharashtra", "city": "Mahabaleshwar", "category": "Hill Stations",
                "description": "A popular Western Ghats hill station famous for strawberry farms, viewpoints (Arthur's Seat, Wilson Point), and forest hikes.",
                "best_months": "October, November, December, January, February, March", "latitude": 17.9258, "longitude": 73.6558,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": False,
                "attractions": [{"name": "Venna Lake", "distance": "3.5 km"}, {"name": "Mapro Garden", "distance": "11.0 km"}]
            },
            {
                "name": "Shirdi Sai Baba Temple", "state": "Maharashtra", "city": "Shirdi", "category": "Spiritual",
                "description": "A major pilgrimage center housing the Samadhi of the saint Sai Baba. Attracts thousands of devotees daily, offering community kitchen services.",
                "best_months": "October, November, December, January, February, March", "latitude": 19.7662, "longitude": 74.4762,
                "entry_fee": 0.0, "timings": "4:00 AM - 11:15 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Dwarkamai", "distance": "0.1 km"}, {"name": "Chavadi", "distance": "0.2 km"}]
            },
            {
                "name": "Tadoba National Park", "state": "Maharashtra", "city": "Chandrapur", "category": "Wildlife",
                "description": "Maharashtra's oldest national park, containing dry deciduous forests and the scenic Tadoba Lake. High tiger population makes it a premier tiger safari destination.",
                "best_months": "October, November, December, January, February, March, April", "latitude": 20.2520, "longitude": 79.3038,
                "entry_fee": 750.0, "timings": "6:00 AM - 10:00 AM, 2:30 PM - 6:30 PM", "budget_category": "Luxury", "is_trending": True,
                "attractions": [{"name": "Tadoba Lake", "distance": "1.0 km"}, {"name": "Eraiyur Viewpoint", "distance": "12.0 km"}]
            },
            {
                "name": "Sanjay Gandhi National Park", "state": "Maharashtra", "city": "Mumbai", "category": "Wildlife",
                "description": "One of the few national parks located within a metropolitan city. Features dense deciduous forests, a tiger safari zone, and the historic 2,000-year-old Kanheri Caves.",
                "best_months": "October, November, December, January, February", "latitude": 19.2208, "longitude": 72.9150,
                "entry_fee": 64.0, "timings": "7:30 AM - 5:30 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Kanheri Caves", "distance": "6.0 km"}, {"name": "Vihar Lake", "distance": "8.0 km"}]
            },
            {
                "name": "Alibaug Beach", "state": "Maharashtra", "city": "Alibaug", "category": "Beaches",
                "description": "A popular weekend beach getaway from Mumbai, featuring black sand beach flats and boat transfers to the Kolaba sea fort.",
                "best_months": "October, November, December, January, February", "latitude": 18.6586, "longitude": 72.8774,
                "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Kolaba Fort", "distance": "1.0 km (by foot at low tide)"}, {"name": "Varsoli Beach", "distance": "3.5 km"}]
            },
            {
                "name": "Elephanta Caves", "state": "Maharashtra", "city": "Gharapuri", "category": "Heritage",
                "description": "Located on Elephanta Island in Mumbai harbor, this cave complex features stone sculptures dedicated to Lord Shiva, including the famous 20-foot Trimurti sculpture.",
                "best_months": "October, November, December, January, February, March", "latitude": 18.9634, "longitude": 72.9315,
                "entry_fee": 40.0, "timings": "9:00 AM - 5:30 PM (Closed on Mondays)", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Gateway of India", "distance": "10.0 km (by ferry)"}, {"name": "Cannon Hill", "distance": "0.8 km"}]
            },

            # --- DELHI (10 Places) ---
            {
                "name": "Red Fort", "state": "Delhi", "city": "Delhi", "category": "Heritage",
                "description": "Built in 1648 by Mughal Emperor Shah Jahan in red sandstone, this UNESCO World Heritage Site served as the main residence of the Mughal dynasty. Landmark of India's independence.",
                "best_months": "October, November, December, January, February, March", "latitude": 28.6562, "longitude": 77.2410,
                "entry_fee": 35.0, "timings": "9:00 AM - 4:30 PM (Closed on Mondays)", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Chandni Chowk", "distance": "0.5 km"}, {"name": "Jama Masjid", "distance": "1.0 km"}]
            },
            {
                "name": "Qutub Minar", "state": "Delhi", "city": "Delhi", "category": "Heritage",
                "description": "A 73-meter towering minaret built in 1192 by Qutb-ud-din Aibak. Surrounded by historical ruins including the famous rust-resistant 4th-century Iron Pillar of Chandragupta II.",
                "best_months": "October, November, December, January, February, March", "latitude": 28.5244, "longitude": 77.1855,
                "entry_fee": 35.0, "timings": "7:00 AM - 9:00 PM", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "Mehrauli Archaeological Park", "distance": "1.2 km"}, {"name": "Garden of Five Senses", "distance": "3.5 km"}]
            },
            {
                "name": "India Gate", "state": "Delhi", "city": "Delhi", "category": "Heritage",
                "description": "A massive 42-meter high triumphal arch war memorial dedicated to the soldiers of the British Indian Army. Houses the eternal flame 'Amar Jawan Jyoti'.",
                "best_months": "October, November, December, January, February, March", "latitude": 28.6129, "longitude": 77.2295,
                "entry_fee": 0.0, "timings": "24 Hours open (Lightings at night)", "budget_category": "Budget", "is_trending": True,
                "attractions": [{"name": "National Gallery of Modern Art", "distance": "0.8 km"}, {"name": "Rashtrapati Bhavan", "distance": "2.2 km"}]
            },
            {
                "name": "Lotus Temple", "state": "Delhi", "city": "Delhi", "category": "Spiritual",
                "description": "A Bahai House of Worship built in the shape of a blooming white lotus flower. Renowned for its stunning marble architecture, silence halls, and scenic garden grounds.",
                "best_months": "October, November, December, January, February, March", "latitude": 28.5535, "longitude": 77.2588,
                "entry_fee": 0.0, "timings": "9:00 AM - 5:30 PM (Closed on Mondays)", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Kalkaji Devi Temple", "distance": "0.8 km"}, {"name": "ISCKON Temple Delhi", "distance": "1.5 km"}]
            },
            {
                "name": "Humayun's Tomb", "state": "Delhi", "city": "Delhi", "category": "Heritage",
                "description": "The first grand garden-tomb on the Indian subcontinent, built in 1570 for Mughal Emperor Humayun. Its red sandstone architecture inspired the design of the Taj Mahal.",
                "best_months": "October, November, December, January, February, March", "latitude": 28.5933, "longitude": 77.2507,
                "entry_fee": 35.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Nizamuddin Dargah", "distance": "1.2 km"}, {"name": "Sunder Nursery", "distance": "0.5 km"}]
            },
            {
                "name": "Akshardham Temple", "state": "Delhi", "city": "Delhi", "category": "Spiritual",
                "description": "A massive, intricately carved Hindu temple complex showcasing millennia of traditional Indian culture, spirituality, exhibitions, and musical water fountain shows.",
                "best_months": "October, November, December, January, February, March", "latitude": 28.6127, "longitude": 77.2773,
                "entry_fee": 0.0, "timings": "9:30 AM - 6:30 PM (Closed on Mondays)", "budget_category": "Mid-range", "is_trending": True,
                "attractions": [{"name": "Sanjay Lake", "distance": "4.5 km"}, {"name": "Purana Qila", "distance": "6.0 km"}]
            },
            {
                "name": "Jama Masjid", "state": "Delhi", "city": "Delhi", "category": "Spiritual",
                "description": "One of the largest mosques in India, built in 1656 by Shah Jahan. Constructed in red sandstone and white marble, its courtyard can hold 25,000 worshippers.",
                "best_months": "October, November, December, January, February, March", "latitude": 28.6507, "longitude": 77.2334,
                "entry_fee": 0.0, "timings": "7:00 AM - 12:00 PM, 1:30 PM - 6:30 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Red Fort", "distance": "1.0 km"}, {"name": "Chandni Chowk", "distance": "0.8 km"}]
            },
            {
                "name": "Lodhi Gardens", "state": "Delhi", "city": "Delhi", "category": "Heritage",
                "description": "A beautiful 90-acre public park containing the tombs of Sayyid and Lodhi dynasties. Popular for jogging, family picnics, and green landscapes.",
                "best_months": "October, November, December, January, February, March", "latitude": 28.5931, "longitude": 77.2197,
                "entry_fee": 0.0, "timings": "6:00 AM - 8:00 PM", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Safdarjung Tomb", "distance": "1.5 km"}, {"name": "Khan Market", "distance": "1.0 km"}]
            },
            {
                "name": "National Zoological Park", "state": "Delhi", "city": "Delhi", "category": "Wildlife",
                "description": "A 176-acre zoo housing animal and bird species, including White Tigers, Indian rhinoceros, leopards, and crocodiles in near-natural environments.",
                "best_months": "October, November, December, January, February", "latitude": 28.6111, "longitude": 77.2458,
                "entry_fee": 80.0, "timings": "9:00 AM - 4:30 PM (Closed on Fridays)", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Purana Qila", "distance": "0.8 km"}, {"name": "Humayun's Tomb", "distance": "2.2 km"}]
            },
            {
                "name": "Chandni Chowk", "state": "Delhi", "city": "Delhi", "category": "Heritage",
                "description": "One of the oldest and busiest markets in Old Delhi, established in the 17th century. Famous for spices, fabrics, street food stalls, and Paranthe Wali Gali.",
                "best_months": "October, November, December, January, February, March", "latitude": 28.6560, "longitude": 77.2300,
                "entry_fee": 0.0, "timings": "10:00 AM - 9:00 PM (Closed on Sundays)", "budget_category": "Budget", "is_trending": False,
                "attractions": [{"name": "Red Fort", "distance": "0.5 km"}, {"name": "Jama Masjid", "distance": "0.8 km"}]
            }
        ]

        # 6. Add Destinations to DB and populate amenities dynamically
        print("Inserting destinations and creating coordinates for maps...")
        for index, dest in enumerate(raw_destinations):
            # Select random image from matching category
            images_list = category_images[dest["category"]]
            # Shuffle or pick items to make it comma separated
            selected_images = ",".join(images_list)
            
            # Programmatically generate high-quality tourism amenities (nearby services) 
            # shifted slightly from destination's coordinates for Leaflet map display
            lat = dest["latitude"]
            lng = dest["longitude"]
            
            nearby_services_data = [
                {
                    "name": f"{dest['city']} Tourist Grand Hotel",
                    "type": "Hotel",
                    "latitude": round(lat + 0.0031, 4),
                    "longitude": round(lng - 0.0022, 4),
                    "contact": f"0{random.randint(100, 999)} {random.randint(1000000, 9999999)}"
                },
                {
                    "name": f"{dest['name']} Local Spice Restaurant",
                    "type": "Restaurant",
                    "latitude": round(lat - 0.0024, 4),
                    "longitude": round(lng + 0.0035, 4),
                    "contact": f"0{random.randint(100, 999)} {random.randint(1000000, 9999999)}"
                },
                {
                    "name": f"{dest['city']} City Hospital Care",
                    "type": "Hospital",
                    "latitude": round(lat + 0.0053, 4),
                    "longitude": round(lng + 0.0051, 4),
                    "contact": f"0{random.randint(100, 999)} {random.randint(1000000, 9999999)}"
                },
                {
                    "name": f"{dest['city']} Central Railway Hub",
                    "type": "Transport",
                    "latitude": round(lat - 0.0062, 4),
                    "longitude": round(lng - 0.0064, 4),
                    "contact": "139"
                }
            ]

            # Format the coordinates of attractions too
            nearby_attractions_formatted = []
            for attr in dest["attractions"]:
                # Shift coordinates slightly for attractions
                nearby_attractions_formatted.append({
                    "name": attr["name"],
                    "distance": attr["distance"],
                    "description": f"A notable place located {attr['distance']} away from {dest['name']}."
                })
            
            db_destination = Destination(
                category_id=seeded_categories[dest["category"]],
                name=dest["name"],
                state=dest["state"],
                city=dest["city"],
                description=dest["description"],
                images=selected_images,
                entry_fee=dest["entry_fee"],
                timings=dest["timings"],
                best_months=dest["best_months"],
                latitude=lat,
                longitude=lng,
                nearby_attractions=json.dumps(nearby_attractions_formatted),
                nearby_services=json.dumps(nearby_services_data),
                is_trending=dest["is_trending"],
                budget_category=dest["budget_category"]
            )
            
            db.add(db_destination)
            db.commit()
            db.refresh(db_destination)
            
            # 7. Add a sample review for each destination
            review = Review(
                user_id=test_user.id,
                destination_id=db_destination.id,
                rating=5 if db_destination.is_trending else 4,
                comment=f"Visited {db_destination.name} in {db_destination.city} recently. Incredible experience, highly recommended for everyone! The staff was friendly and the vistas were breathtaking."
            )
            db.add(review)
            db.commit()
            
        print(f"Database Seeding Completed Successfully! Seeded {len(raw_destinations)} destinations.")
    except Exception as e:
        db.rollback()
        print(f"Error during Database Seeding: {str(e)}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
