import os
import sys
import json
import random

# Ensure current directory (backend root) is in the python search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Destination, Category

# Category images for rendering the UI beautifully
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

destinations_data = [
    # === TAMIL NADU ===
    {
        "name": "Ramanathaswamy Temple", "state": "Tamil Nadu", "city": "Rameshwaram", "category": "Spiritual",
        "description": "Famous Hindu temple dedicated to Lord Shiva, known for its majestic corridors, carved pillars, and holy water tanks.",
        "best_months": "October, November, December, January, February", "latitude": 9.2881, "longitude": 79.3174,
        "entry_fee": 0.0, "timings": "5:00 AM - 1:00 PM, 3:00 PM - 9:00 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Dhanushkodi Beach", "distance": "18 km"}, {"name": "Pamban Bridge", "distance": "12 km"}]
    },
    {
        "name": "Kanyakumari Sunrise View Point", "state": "Tamil Nadu", "city": "Kanyakumari", "category": "Beaches",
        "description": "The southernmost tip of mainland India, offering stunning views of the confluence of the Arabian Sea, Bay of Bengal, and Indian Ocean.",
        "best_months": "October, November, December, January, February", "latitude": 8.0883, "longitude": 77.5385,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Vivekananda Rock Memorial", "distance": "0.5 km (by ferry)"}, {"name": "Thiruvalluvar Statue", "distance": "0.6 km"}]
    },
    {
        "name": "Mudumalai National Park and Tiger Reserve", "state": "Tamil Nadu", "city": "Masinagudi", "category": "Wildlife",
        "description": "A declared tiger reserve sharing borders with Kerala and Karnataka, sheltering endangered wildlife including Indian elephants and Bengal tigers.",
        "best_months": "September, October, November, December, January, February, March", "latitude": 11.5623, "longitude": 76.6213,
        "entry_fee": 135.0, "timings": "6:00 AM - 9:00 AM, 3:00 PM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False,
        "attractions": [{"name": "Theppakadu Elephant Camp", "distance": "1 km"}, {"name": "Moyar River Gorge", "distance": "7 km"}]
    },
    {
        "name": "Yelagiri Hill Station", "state": "Tamil Nadu", "city": "Yelagiri", "category": "Hill Stations",
        "description": "A serene, lesser-known hill station surrounded by orchards, rose gardens, and green valleys, perfect for a peaceful getaway.",
        "best_months": "November, December, January, February", "latitude": 12.5785, "longitude": 78.6384,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Punganoor Lake Park", "distance": "1.2 km"}, {"name": "Jalagamparai Waterfalls", "distance": "14 km"}]
    },
    {
        "name": "Gingee Fort", "state": "Tamil Nadu", "city": "Gingee", "category": "Heritage",
        "description": "Also known as the 'Troy of the East', this massive fort complex spans three separate hills, representing incredible ancient military architecture.",
        "best_months": "October, November, December, January", "latitude": 12.2514, "longitude": 79.4184,
        "entry_fee": 25.0, "timings": "9:00 AM - 5:30 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Rajagiri Fort Peak", "distance": "1.5 km climb"}, {"name": "Kalyana Mahal", "distance": "0.2 km"}]
    },
    {
        "name": "Hogenakkal Falls", "state": "Tamil Nadu", "city": "Dharmapuri", "category": "Hill Stations",
        "description": "Often dubbed the 'Niagara of India', these waterfalls on the Kaveri River are famous for carbonatite rocks, coracle boat rides, and therapeutic baths.",
        "best_months": "July, August, September, October, November, December", "latitude": 12.1213, "longitude": 77.7788,
        "entry_fee": 10.0, "timings": "8:00 AM - 5:30 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Melagiri Hills", "distance": "10 km"}, {"name": "Pennagaram Village", "distance": "15 km"}]
    },

    # === KERALA ===
    {
        "name": "Bekal Fort Beach", "state": "Kerala", "city": "Kasaragod", "category": "Heritage",
        "description": "The largest fort in Kerala, built in the shape of a keyhole and surrounded by a beautiful sandy beach offering views of the Arabian Sea.",
        "best_months": "October, November, December, January, February", "latitude": 12.3831, "longitude": 75.0321,
        "entry_fee": 25.0, "timings": "8:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False,
        "attractions": [{"name": "Bekal Beach Park", "distance": "0.5 km"}, {"name": "Kappil Beach", "distance": "6 km"}]
    },
    {
        "name": "Silent Valley National Park", "state": "Kerala", "city": "Palakkad", "category": "Wildlife",
        "description": "One of the last undisturbed tracts of South Indian tropical rainforests, famous for rare Lion-tailed Macaque monkeys and rich biodiversity.",
        "best_months": "December, January, February, March, April", "latitude": 11.1300, "longitude": 76.4300,
        "entry_fee": 250.0, "timings": "8:00 AM - 1:00 PM", "budget_category": "Mid-range", "is_trending": False,
        "attractions": [{"name": "Kuntipuzha River", "distance": "2 km"}, {"name": "Sairandhri Watch Tower", "distance": "0.1 km"}]
    },
    {
        "name": "Cherai Beach", "state": "Kerala", "city": "Kochi", "category": "Beaches",
        "description": "A flat, clean beach located on the northern end of Vypeen Island, renowned for frequent dolphin sightings and swimming.",
        "best_months": "November, December, January, February", "latitude": 10.1416, "longitude": 76.1783,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Pallipuram Fort", "distance": "4 km"}, {"name": "Kochi Backwaters", "distance": "1 km"}]
    },
    {
        "name": "Guruvayur Sree Krishna Temple", "state": "Kerala", "city": "Guruvayur", "category": "Spiritual",
        "description": "One of the most important pilgrimage destinations in Kerala, dedicated to Lord Krishna and famous for its elephant sanctuary.",
        "best_months": "September, October, November, December, January, February", "latitude": 10.5947, "longitude": 76.0379,
        "entry_fee": 0.0, "timings": "3:00 AM - 12:30 PM, 4:30 PM - 9:15 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Punnathurkotta Elephant Sanctuary", "distance": "3 km"}, {"name": "Chavakkad Beach", "distance": "5 km"}]
    },
    {
        "name": "Kumarakom Bird Sanctuary", "state": "Kerala", "city": "Kumarakom", "category": "Wildlife",
        "description": "A beautiful bird sanctuary on the banks of Vembanad Lake, sheltering local and migratory birds like Siberian Cranes and herons.",
        "best_months": "November, December, January, February", "latitude": 9.6268, "longitude": 76.4254,
        "entry_fee": 50.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False,
        "attractions": [{"name": "Vembanad Lake Boat Cruise", "distance": "0.1 km"}, {"name": "Aruvikkuzhi Waterfall", "distance": "18 km"}]
    },

    # === KARNATAKA ===
    {
        "name": "Gol Gumbaz Monument", "state": "Karnataka", "city": "Vijayapura", "category": "Heritage",
        "description": "The mausoleum of King Muhammad Adil Shah, boasting the second-largest dome in the world and a famous whispering gallery.",
        "best_months": "October, November, December, January, February", "latitude": 16.8302, "longitude": 75.7362,
        "entry_fee": 25.0, "timings": "10:00 AM - 5:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Ibrahim Rauza", "distance": "3 km"}, {"name": "Vijayapura Fort", "distance": "1 km"}]
    },
    {
        "name": "Nagarhole National Park", "state": "Karnataka", "city": "Kabini", "category": "Wildlife",
        "description": "A major national park in the Western Ghats, containing dense forests, waterfalls, and rich wildlife populations of tigers, leopards, and elephants.",
        "best_months": "October, November, December, January, February, March, April, May", "latitude": 12.0287, "longitude": 76.1558,
        "entry_fee": 300.0, "timings": "6:00 AM - 9:00 AM, 3:00 PM - 6:00 PM", "budget_category": "Luxury", "is_trending": True,
        "attractions": [{"name": "Kabini River Dam", "distance": "10 km"}, {"name": "Iruppu Falls", "distance": "45 km"}]
    },
    {
        "name": "Kollur Mookambika Temple", "state": "Karnataka", "city": "Kollur", "category": "Spiritual",
        "description": "A highly sacred Hindu temple located at the foothills of Kodachadri hills, dedicated to the divine mother Mookambika Devi.",
        "best_months": "September, October, November, December, January", "latitude": 13.8654, "longitude": 74.8138,
        "entry_fee": 0.0, "timings": "5:00 AM - 1:30 PM, 3:00 PM - 9:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Kodachadri Hill Trek", "distance": "20 km"}, {"name": "Sowparnika River Ghat", "distance": "0.2 km"}]
    },
    {
        "name": "Shravanabelagola Bahubali Statue", "state": "Karnataka", "city": "Hassan", "category": "Heritage",
        "description": "A historical Jain pilgrimage site home to the world's largest monolithic stone statue of Gommateshwara (Bahubali), carved in 981 AD.",
        "best_months": "October, November, December, January, February", "latitude": 12.8576, "longitude": 76.3908,
        "entry_fee": 0.0, "timings": "6:30 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Vindhyagiri Hill", "distance": "0.1 km"}, {"name": "Chandragiri Hill", "distance": "0.5 km"}]
    },
    {
        "name": "Kemmangundi Hill Station", "state": "Karnataka", "city": "Kemmangundi", "category": "Hill Stations",
        "description": "A picturesque mountain station surrounded by ornamental gardens, waterfalls, valleys, and lush coffee estates.",
        "best_months": "September, October, November, December, January, February", "latitude": 13.5484, "longitude": 75.7562,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": False,
        "attractions": [{"name": "Z Point Viewpoint", "distance": "3 km trek"}, {"name": "Hebe Waterfalls", "distance": "8 km"}]
    },

    # === GOA ===
    {
        "name": "Miramar Beach Panaji", "state": "Goa", "city": "Panaji", "category": "Beaches",
        "description": "A lovely urban beach situated near the mouth of the Mandovi River, offering spectacular sunset vistas and soft sand walks.",
        "best_months": "November, December, January, February", "latitude": 15.4851, "longitude": 73.8113,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Dona Paula Viewpoint", "distance": "3.5 km"}, {"name": "Fontainhas Latin Quarter", "distance": "4 km"}]
    },
    {
        "name": "Se Cathedral Church", "state": "Goa", "city": "Old Goa", "category": "Heritage",
        "description": "The largest church building in Asia, dedicated to St. Catherine, featuring beautiful Portuguese-Gothic architectures and a giant golden bell.",
        "best_months": "October, November, December, January, February", "latitude": 15.5032, "longitude": 73.9124,
        "entry_fee": 0.0, "timings": "7:30 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Basilica of Bom Jesus", "distance": "0.3 km"}, {"name": "St. Augustine Tower", "distance": "1 km"}]
    },
    {
        "name": "Cabo de Rama Fort Ruins", "state": "Goa", "city": "Canacona", "category": "Heritage",
        "description": "A wild and romantic clifftop fort ruin in South Goa, associated with the epic Ramayana and offering stunning views over the ocean.",
        "best_months": "October, November, December, January, February", "latitude": 15.0883, "longitude": 73.9194,
        "entry_fee": 0.0, "timings": "9:00 AM - 5:30 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Cabo de Rama Beach", "distance": "0.5 km"}, {"name": "Cola Beach Blue Lagoon", "distance": "8 km"}]
    },
    {
        "name": "Netravali Wildlife Sanctuary", "state": "Goa", "city": "Sanguem", "category": "Wildlife",
        "description": "An important wildlife corridor in Eastern Goa, rich in forest areas, bubbling lakes, waterfalls, and wild leopards.",
        "best_months": "October, November, December, January, February, March", "latitude": 15.0945, "longitude": 74.2185,
        "entry_fee": 50.0, "timings": "8:30 AM - 5:00 PM", "budget_category": "Mid-range", "is_trending": False,
        "attractions": [{"name": "Savari Waterfall", "distance": "3 km trek"}, {"name": "Mainapi Waterfall", "distance": "5 km trek"}]
    },

    # === RAJASTHAN ===
    {
        "name": "Jaswant Thada Cenotaph", "state": "Rajasthan", "city": "Jodhpur", "category": "Heritage",
        "description": "A beautiful white marble cenotaph built in 1899, often called the 'Taj Mahal of Marwar', set near a peaceful lake.",
        "best_months": "October, November, December, January, February, March", "latitude": 26.3025, "longitude": 73.0242,
        "entry_fee": 30.0, "timings": "9:00 AM - 5:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Mehrangarh Fort", "distance": "1 km"}, {"name": "Rao Jodha Desert Rock Park", "distance": "0.5 km"}]
    },
    {
        "name": "Sariska Tiger Reserve and National Park", "state": "Rajasthan", "city": "Alwar", "category": "Wildlife",
        "description": "A scenic wildlife sanctuary in the Aravalli hills, famous for Royal Bengal Tigers, leopards, hyenas, and ancient temple ruins.",
        "best_months": "October, November, December, January, February, March, April", "latitude": 27.2913, "longitude": 76.4385,
        "entry_fee": 80.0, "timings": "6:00 AM - 10:00 AM, 2:00 PM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False,
        "attractions": [{"name": "Kankwari Fort", "distance": "15 km"}, {"name": "Pandupol Hanuman Temple", "distance": "20 km"}]
    },
    {
        "name": "Dilwara Marble Jain Temples", "state": "Rajasthan", "city": "Mount Abu", "category": "Spiritual",
        "description": "A world-renowned complex of five Jain temples famous for incredibly intricate white marble carvings and pillars.",
        "best_months": "October, November, December, January, February", "latitude": 24.6112, "longitude": 72.7235,
        "entry_fee": 0.0, "timings": "12:00 PM - 5:00 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Nakki Lake", "distance": "2.5 km"}, {"name": "Sunset Point Mount Abu", "distance": "4 km"}]
    },
    {
        "name": "Kumbhalgarh Fort Walls", "state": "Rajasthan", "city": "Rajsamand", "category": "Heritage",
        "description": "A Mewar fortress famous for having the second-longest continuous wall in the world (36 km), and being the birthplace of Maharana Pratap.",
        "best_months": "October, November, December, January, February", "latitude": 25.1528, "longitude": 73.5872,
        "entry_fee": 40.0, "timings": "9:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": True,
        "attractions": [{"name": "Badal Mahal Palace", "distance": "0.2 km Climb"}, {"name": "Kumbhalgarh Wildlife Sanctuary", "distance": "2 km"}]
    },

    # === HIMACHAL PRADESH ===
    {
        "name": "Great Himalayan National Park", "state": "Himachal Pradesh", "city": "Kullu", "category": "Wildlife",
        "description": "A UNESCO World Heritage Site, home to blue sheep, snow leopards, Himalayan brown bears, and spectacular mountain treks.",
        "best_months": "September, October, November, April, May, June", "latitude": 31.7300, "longitude": 77.4200,
        "entry_fee": 100.0, "timings": "24 Hours open (Permits required)", "budget_category": "Luxury", "is_trending": False,
        "attractions": [{"name": "Tirthan Valley", "distance": "5 km"}, {"name": "Sainj Valley", "distance": "12 km"}]
    },
    {
        "name": "Hadimba Temple", "state": "Himachal Pradesh", "city": "Manali", "category": "Spiritual",
        "description": "An ancient 1553 AD wooden pagoda-style temple dedicated to Hidimba Devi, surrounded by a dense cedar forest (Dhungri Van Vihar).",
        "best_months": "October, November, December, January, February, March, April, May", "latitude": 32.2479, "longitude": 77.1797,
        "entry_fee": 0.0, "timings": "8:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Dhungri Pine Forest Park", "distance": "0.1 km"}, {"name": "Manali Mall Road", "distance": "1.5 km"}]
    },
    {
        "name": "Kasol Valley Village", "state": "Himachal Pradesh", "city": "Kasol", "category": "Hill Stations",
        "description": "A charming hamlet on the banks of the Parvati River, famous for trekking, Israeli cafes, and breathtaking alpine landscapes.",
        "best_months": "October, November, March, April, May, June", "latitude": 32.0097, "longitude": 77.3151,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Manikaran Sahib Gurudwara", "distance": "4 km"}, {"name": "Chalal Trekking Path", "distance": "1.5 km"}]
    },
    {
        "name": "Kangra Fort ruins", "state": "Himachal Pradesh", "city": "Kangra", "category": "Heritage",
        "description": "The largest fort in the Himalayas and probably the oldest dated fort in India, boasting massive ramparts and temple ruins.",
        "best_months": "September, October, November, March, April, May", "latitude": 32.0997, "longitude": 76.2558,
        "entry_fee": 150.0, "timings": "9:00 AM - 5:30 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Kangra Art Museum", "distance": "4 km"}, {"name": "Jayanti Devi Temple", "distance": "7 km"}]
    },

    # === JAMMU & KASHMIR ===
    {
        "name": "Vaishno Devi Temple Cave", "state": "Jammu & Kashmir", "city": "Katra", "category": "Spiritual",
        "description": "One of India's most visited Hindu pilgrimage centers, located in the Trikuta Mountains, requiring a 12 km trek from Katra.",
        "best_months": "March, April, May, September, October, November", "latitude": 33.0300, "longitude": 74.9500,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Bhairon Ghati Temple", "distance": "2 km trek"}, {"name": "Ardhkuwari Gufa", "distance": "6 km trek"}]
    },
    {
        "name": "Gulmarg Gondola Ride", "state": "Jammu & Kashmir", "city": "Gulmarg", "category": "Hill Stations",
        "description": "One of the highest cable cars in Asia, offering breathtaking views of snow-clad mountains and access to ski slopes.",
        "best_months": "December, January, February, March, April", "latitude": 34.0489, "longitude": 74.3804,
        "entry_fee": 740.0, "timings": "10:00 AM - 5:00 PM", "budget_category": "Luxury", "is_trending": True,
        "attractions": [{"name": "Khilanmarg Snow Valley", "distance": "5 km"}, {"name": "Gulmarg Golf Course", "distance": "1 km"}]
    },
    {
        "name": "Dachigam National Park Sanctuary", "state": "Jammu & Kashmir", "city": "Srinagar", "category": "Wildlife",
        "description": "Protected mountain forest sanctuary famous for Hangul (Kashmir Stag), leopards, musk deer, and scenic hiking trails.",
        "best_months": "May, June, July, August, September, October", "latitude": 34.1372, "longitude": 74.9362,
        "entry_fee": 25.0, "timings": "9:00 AM - 5:00 PM", "budget_category": "Mid-range", "is_trending": False,
        "attractions": [{"name": "Harwan Garden", "distance": "2 km"}, {"name": "Dal Lake", "distance": "15 km"}]
    },
    {
        "name": "Shalimar Bagh Mughal Garden", "state": "Jammu & Kashmir", "city": "Srinagar", "category": "Heritage",
        "description": "A magnificent terraced Mughal garden built by Emperor Jahangir in 1619, featuring fountains, chinars, and royal pavilions.",
        "best_months": "April, May, June, July, August, September, October", "latitude": 34.1494, "longitude": 74.8732,
        "entry_fee": 24.0, "timings": "9:00 AM - 7:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Nishat Bagh", "distance": "3.5 km"}, {"name": "Dal Lake Shoreline", "distance": "0.1 km"}]
    },

    # === MAHARASHTRA ===
    {
        "name": "Ajanta Rock Cut Caves", "state": "Maharashtra", "city": "Aurangabad", "category": "Heritage",
        "description": "UNESCO site comprising 30 rock-cut Buddhist cave monuments dating from the 2nd century BCE, famous for murals and stone carvings.",
        "best_months": "October, November, December, January, February, March", "latitude": 20.5522, "longitude": 75.7003,
        "entry_fee": 40.0, "timings": "9:00 AM - 5:00 PM (Closed on Mondays)", "budget_category": "Mid-range", "is_trending": True,
        "attractions": [{"name": "Ellora Caves", "distance": "100 km"}, {"name": "View Point Ajanta", "distance": "5 km"}]
    },
    {
        "name": "Tadoba-Andhari Tiger Reserve", "state": "Maharashtra", "city": "Chandrapur", "category": "Wildlife",
        "description": "Maharashtra's oldest and largest national park, globally famous for regular tiger sightings in deciduous forests.",
        "best_months": "October, November, December, January, February, March, April, May", "latitude": 20.2185, "longitude": 79.3113,
        "entry_fee": 1000.0, "timings": "6:00 AM - 10:00 AM, 2:00 PM - 6:00 PM", "budget_category": "Luxury", "is_trending": True,
        "attractions": [{"name": "Tadoba Lake", "distance": "2 km"}, {"name": "Eraiyur Dam", "distance": "12 km"}]
    },
    {
        "name": "Ganpatipule Beach Temple", "state": "Maharashtra", "city": "Ganpatipule", "category": "Beaches",
        "description": "A pristine white sand beach on the Konkan coast, famous for a 400-year-old self-manifested Ganesha temple overlooking the sea.",
        "best_months": "October, November, December, January, February", "latitude": 17.1513, "longitude": 73.2684,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": False,
        "attractions": [{"name": "Swayambhu Ganesha Temple", "distance": "0.1 km"}, {"name": "Prachin Konkan Museum", "distance": "1 km"}]
    },
    {
        "name": "Lonavala Tiger Point View", "state": "Maharashtra", "city": "Lonavala", "category": "Hill Stations",
        "description": "A popular cliff viewpoint offering panoramic valley views, waterfalls, and mist during monsoons.",
        "best_months": "June, July, August, September, October", "latitude": 18.7302, "longitude": 73.3484,
        "entry_fee": 0.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Bhushi Dam", "distance": "4 km"}, {"name": "Karla Caves", "distance": "15 km"}]
    },

    # === UTTARAKHAND ===
    {
        "name": "Badrinath Temple Shrine", "state": "Uttarakhand", "city": "Badrinath", "category": "Spiritual",
        "description": "A sacred Hindu temple dedicated to Lord Vishnu, located along the Alaknanda River in the Garhwal hill tracks.",
        "best_months": "May, June, September, October, November", "latitude": 30.7432, "longitude": 79.4938,
        "entry_fee": 0.0, "timings": "4:30 AM - 1:00 PM, 4:00 PM - 9:00 PM (Winter Closed)", "budget_category": "Mid-range", "is_trending": True,
        "attractions": [{"name": "Mana Village (Last Indian Village)", "distance": "3 km"}, {"name": "Tapt Kund Hot Springs", "distance": "0.1 km"}]
    },
    {
        "name": "Valley of Flowers National Park", "state": "Uttarakhand", "city": "Chamoli", "category": "Hill Stations",
        "description": "A high-altitude Himalayan valley renowned for endemic alpine flowers, meadows, and dramatic landscapes.",
        "best_months": "July, August, September", "latitude": 30.7281, "longitude": 79.6053,
        "entry_fee": 150.0, "timings": "7:00 AM - 5:00 PM", "budget_category": "Luxury", "is_trending": True,
        "attractions": [{"name": "Hemkund Sahib Gurudwara", "distance": "6 km steep trek"}, {"name": "Ghangaria Camp", "distance": "3.5 km trek"}]
    },
    {
        "name": "Jim Corbett National Park Reserve", "state": "Uttarakhand", "city": "Ramnagar", "category": "Wildlife",
        "description": "India's oldest national park, established in 1936 to protect the endangered Bengal Tiger, set at the foothills of Himalayas.",
        "best_months": "November, December, January, February, March, April, May", "latitude": 29.5300, "longitude": 78.7700,
        "entry_fee": 200.0, "timings": "6:00 AM - 9:30 AM, 2:00 PM - 5:30 PM", "budget_category": "Luxury", "is_trending": True,
        "attractions": [{"name": "Garjiya Devi Temple", "distance": "12 km"}, {"name": "Corbett Waterfalls", "distance": "25 km"}]
    },
    {
        "name": "Har Ki Pauri Ghat", "state": "Uttarakhand", "city": "Haridwar", "category": "Spiritual",
        "description": "A famous landmark ghat on the banks of the Ganges where thousands gather for the sacred evening Ganga Aarti ritual.",
        "best_months": "October, November, December, January, February, March", "latitude": 29.9585, "longitude": 78.1713,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Mansa Devi Temple", "distance": "3 km (by cable car)"}, {"name": "Chandi Devi Temple", "distance": "4 km"}]
    },

    # === ANDHRA PRADESH ===
    {
        "name": "Tirumala Venkateswara Temple", "state": "Andhra Pradesh", "city": "Tirupati", "category": "Spiritual",
        "description": "The richest and most visited Hindu temple shrine in the world, dedicated to Lord Venkateswara (Balaji) atop Seshachalam Hills.",
        "best_months": "September, October, November, December, January, February", "latitude": 13.6833, "longitude": 79.3500,
        "entry_fee": 300.0, "timings": "24 Hours open (Queue systems apply)", "budget_category": "Mid-range", "is_trending": True,
        "attractions": [{"name": "Silathoranam Natural Arch", "distance": "1 km"}, {"name": "Kapila Theertham Waterfall", "distance": "10 km"}]
    },
    {
        "name": "Araku Valley Coffee Plantations", "state": "Andhra Pradesh", "city": "Araku", "category": "Hill Stations",
        "description": "A beautiful hill station in the Eastern Ghats inhabited by local tribes, famous for organic coffee plantations and mist valleys.",
        "best_months": "October, November, December, January, February", "latitude": 18.2785, "longitude": 82.8613,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": True,
        "attractions": [{"name": "Borra Caves", "distance": "36 km"}, {"name": "Padmapuram Botanical Gardens", "distance": "2.5 km"}]
    },
    {
        "name": "Borra Caves Complex", "state": "Andhra Pradesh", "city": "Ananthagiri", "category": "Heritage",
        "description": "One of the deepest caves in India, housing stalactite and stalagmite formations of pure limestone, dating back millions of years.",
        "best_months": "October, November, December, January, February", "latitude": 18.2813, "longitude": 83.0385,
        "entry_fee": 80.0, "timings": "10:00 AM - 5:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Katiki Waterfalls", "distance": "7 km trek"}, {"name": "Araku Valley", "distance": "36 km"}]
    },
    {
        "name": "Rishikonda Beach Coast", "state": "Andhra Pradesh", "city": "Visakhapatnam", "category": "Beaches",
        "description": "A gorgeous beach with golden sand and tidy waves, popular for windsurfing, speed boating, and beachfront resorts.",
        "best_months": "October, November, December, January, February", "latitude": 17.7831, "longitude": 83.3854,
        "entry_fee": 10.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Kailasagiri Hill Park", "distance": "6 km"}, {"name": "INS Kursura Submarine Museum", "distance": "10 km"}]
    },
    {
        "name": "Veerabhadra Temple Lepakshi", "state": "Andhra Pradesh", "city": "Lepakshi", "category": "Heritage",
        "description": "A 16th-century Vijayanagara style temple complex, famous for fine carvings, mural paintings, and the mysterious Hanging Pillar.",
        "best_months": "October, November, December, January, February", "latitude": 13.8021, "longitude": 77.7913,
        "entry_fee": 0.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Lepakshi Nandi Monolith", "distance": "0.5 km"}, {"name": "Hindupur", "distance": "14 km"}]
    },
    {
        "name": "Belum Caves Network", "state": "Andhra Pradesh", "city": "Kurnool", "category": "Heritage",
        "description": "The second largest cave system in the Indian subcontinent, famous for long passages, galleries, freshwater shafts, and Buddhist remains.",
        "best_months": "October, November, December, January", "latitude": 15.1158, "longitude": 78.1132,
        "entry_fee": 65.0, "timings": "10:00 AM - 5:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Giant Buddha Statue", "distance": "0.1 km"}, {"name": "Yaganti Caves Temple", "distance": "45 km"}]
    },
    {
        "name": "Talakona Waterfall Wildlife Area", "state": "Andhra Pradesh", "city": "Chittoor", "category": "Wildlife",
        "description": "The highest waterfall in Andhra Pradesh (270 feet), located inside Sri Venkateswara National Park, rich in medicinal plants.",
        "best_months": "October, November, December, January", "latitude": 13.6268, "longitude": 79.2154,
        "entry_fee": 50.0, "timings": "6:00 AM - 5:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Canopy Rope Walkway", "distance": "0.5 km"}, {"name": "Siddheswara Swamy Temple", "distance": "0.2 km"}]
    },

    # === TELANGANA ===
    {
        "name": "Charminar Monument", "state": "Telangana", "city": "Hyderabad", "category": "Heritage",
        "description": "An iconic 1591 AD mosque with four grand minarets, built in Indo-Islamic style in the heart of old city Hyderabad.",
        "best_months": "October, November, December, January, February", "latitude": 17.3616, "longitude": 78.4747,
        "entry_fee": 25.0, "timings": "9:30 AM - 5:30 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Laad Bazaar (Bangle Market)", "distance": "0.1 km"}, {"name": "Chowmahalla Palace", "distance": "1.2 km"}]
    },
    {
        "name": "Golconda Fort Citadel", "state": "Telangana", "city": "Hyderabad", "category": "Heritage",
        "description": "A historic fortress complex, once the capital of the Qutb Shahi dynasty, famous for acoustics, water supply, and diamond mines.",
        "best_months": "October, November, December, January, February", "latitude": 17.3833, "longitude": 78.4013,
        "entry_fee": 25.0, "timings": "9:00 AM - 5:30 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Qutb Shahi Tombs", "distance": "2 km"}, {"name": "Sound and Light Show Golconda", "distance": "0.1 km"}]
    },
    {
        "name": "Kakatiya Ramappa Temple", "state": "Telangana", "city": "Mulugu", "category": "Heritage",
        "description": "A UNESCO World Heritage Site dedicated to Shiva, displaying ornate carvings and built with floating bricks that float on water.",
        "best_months": "September, October, November, December, January", "latitude": 18.2584, "longitude": 79.9431,
        "entry_fee": 40.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Ramappa Lake", "distance": "1 km"}, {"name": "Laknavaram Lake Hanging Bridge", "distance": "30 km"}]
    },
    {
        "name": "Thousand Pillar Temple Warangal", "state": "Telangana", "city": "Warangal", "category": "Spiritual",
        "description": "A star-shaped Kakatiya style temple shrine, featuring highly polished black basalt Nandi monolith and intricate pillars.",
        "best_months": "October, November, December, January, February", "latitude": 18.0053, "longitude": 79.5700,
        "entry_fee": 0.0, "timings": "6:00 AM - 8:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Warangal Fort Ruins", "distance": "6 km"}, {"name": "Bhadrakali Temple", "distance": "3 km"}]
    },
    {
        "name": "Nagarjuna Sagar Dam Area", "state": "Telangana", "city": "Nalgonda", "category": "Heritage",
        "description": "One of the world's largest masonry dams built across Krishna River, featuring a scenic island museum of Buddhist excavations.",
        "best_months": "October, November, December, January", "latitude": 16.5812, "longitude": 79.3121,
        "entry_fee": 20.0, "timings": "9:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Nagarjunakonda Island Museum", "distance": "4 km (by boat)"}, {"name": "Ethipothala Waterfalls", "distance": "15 km"}]
    },
    {
        "name": "Ananthagiri Hills Forest", "state": "Telangana", "city": "Vikarabad", "category": "Hill Stations",
        "description": "A thick forest area containing trails, waterfalls, and the source of the Musi River, popular for camping and hikes.",
        "best_months": "October, November, December, January", "latitude": 17.3512, "longitude": 77.8684,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Anantha Padmanabha Swamy Temple", "distance": "0.5 km"}, {"name": "Kotepally Reservoir Boating", "distance": "12 km"}]
    },
    {
        "name": "KBR National Park Trail", "state": "Telangana", "city": "Hyderabad", "category": "Wildlife",
        "description": "A green urban park preserving forest cover, home to peacocks, jungle cats, and over a hundred species of local birds.",
        "best_months": "October, November, December, January", "latitude": 17.4194, "longitude": 78.4172,
        "entry_fee": 40.0, "timings": "5:00 AM - 9:30 AM, 4:00 PM - 6:30 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Chiran Palace Ruins", "distance": "0.2 km"}, {"name": "Jubilee Hills", "distance": "0.1 km"}]
    },

    # === GUJARAT ===
    {
        "name": "Somnath Temple Shrine", "state": "Gujarat", "city": "Veraval", "category": "Spiritual",
        "description": "The first among the twelve holy Jyotirlinga shrines of Lord Shiva, located directly on the Arabian Sea coast, reconstructed multiple times.",
        "best_months": "October, November, December, January, February", "latitude": 20.8880, "longitude": 70.4012,
        "entry_fee": 0.0, "timings": "6:00 AM - 9:30 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Triveni Sangam Ghat", "distance": "1.5 km"}, {"name": "Bhalka Tirth Temple", "distance": "4 km"}]
    },
    {
        "name": "Dwarkadhish Temple Shrine", "state": "Gujarat", "city": "Dwarka", "category": "Spiritual",
        "description": "An ancient 5-story temple dedicated to Lord Krishna (Dwarkadhish), part of the famous Char Dham pilgrimage network.",
        "best_months": "October, November, December, January, February", "latitude": 22.2442, "longitude": 68.9684,
        "entry_fee": 0.0, "timings": "6:00 AM - 1:00 PM, 5:00 PM - 9:30 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Gomti Ghat Steps", "distance": "0.2 km"}, {"name": "Rukmini Devi Temple", "distance": "2.5 km"}]
    },
    {
        "name": "Statue of Unity Landmark", "state": "Gujarat", "city": "Kevadia", "category": "Heritage",
        "description": "The world's tallest statue (182 meters) representing Sardar Vallabhbhai Patel, set on a river island facing Narmada Dam.",
        "best_months": "October, November, December, January, February, March", "latitude": 21.8380, "longitude": 73.7191,
        "entry_fee": 150.0, "timings": "8:00 AM - 6:00 PM (Closed on Mondays)", "budget_category": "Mid-range", "is_trending": True,
        "attractions": [{"name": "Valley of Flowers Kevadia", "distance": "2 km"}, {"name": "Sardar Sarovar Dam", "distance": "3.5 km"}]
    },
    {
        "name": "Gir Forest National Park", "state": "Gujarat", "city": "Junagadh", "category": "Wildlife",
        "description": "The exclusive natural home of the endangered Asiatic Lion in the wild, comprising dry deciduous teak forests.",
        "best_months": "December, January, February, March, April", "latitude": 21.1244, "longitude": 70.8242,
        "entry_fee": 800.0, "timings": "6:00 AM - 9:00 AM, 3:00 PM - 6:00 PM (Safari)", "budget_category": "Luxury", "is_trending": True,
        "attractions": [{"name": "Kamleshwar Dam View", "distance": "12 km"}, {"name": "Devalia Safari Park", "distance": "13 km"}]
    },
    {
        "name": "Great Rann of Kutch Desert", "state": "Gujarat", "city": "Bhuj", "category": "Heritage",
        "description": "A salt marsh desert in the Thar Desert, globally famous for Rann Utsav cultural festivals under full moon nights.",
        "best_months": "November, December, January, February", "latitude": 23.7831, "longitude": 69.8654,
        "entry_fee": 100.0, "timings": "24 Hours open", "budget_category": "Luxury", "is_trending": True,
        "attractions": [{"name": "Kalo Dungar Black Hill", "distance": "25 km"}, {"name": "White Desert View Point", "distance": "0.1 km"}]
    },
    {
        "name": "Sabarmati Ashram Museum", "state": "Gujarat", "city": "Ahmedabad", "category": "Heritage",
        "description": "The peaceful home of Mahatma Gandhi for 12 years, acting as a headquarters for the Indian national independence struggle.",
        "best_months": "October, November, December, January, February, March", "latitude": 23.0603, "longitude": 72.5804,
        "entry_fee": 0.0, "timings": "8:30 AM - 6:30 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Sabarmati Riverfront Park", "distance": "1 km"}, {"name": "Adalaj Stepwell", "distance": "15 km"}]
    },
    {
        "name": "Laxmi Vilas Palace Vadodara", "state": "Gujarat", "city": "Vadodara", "category": "Heritage",
        "description": "An Indo-Saracenic palace built by Maharaja Sayajirao Gaekwad III in 1890, four times the size of Buckingham Palace.",
        "best_months": "October, November, December, January, February", "latitude": 22.2938, "longitude": 73.1908,
        "entry_fee": 200.0, "timings": "10:00 AM - 5:00 PM (Closed on Mondays)", "budget_category": "Mid-range", "is_trending": False,
        "attractions": [{"name": "Baroda Museum", "distance": "3 km"}, {"name": "Sayaji Baug Park", "distance": "3.5 km"}]
    },
    {
        "name": "Sun Temple Modhera Ruins", "state": "Gujarat", "city": "Modhera", "category": "Heritage",
        "description": "An ancient Hindu temple dedicated to the Solar deity, built in 1026 AD by Chalukya dynasty, famous for a grand stepped water reservoir.",
        "best_months": "October, November, December, January, February", "latitude": 23.5831, "longitude": 72.1384,
        "entry_fee": 25.0, "timings": "7:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Ramakunda Reservoir Steps", "distance": "0.1 km"}, {"name": "Modhera Museum", "distance": "0.2 km"}]
    },

    # === WEST BENGAL ===
    {
        "name": "Victoria Memorial Museum", "state": "West Bengal", "city": "Kolkata", "category": "Heritage",
        "description": "A magnificent white Makrana marble palace building constructed in memory of Queen Victoria, set amidst beautiful lawns.",
        "best_months": "October, November, December, January, February", "latitude": 22.5448, "longitude": 88.3426,
        "entry_fee": 60.0, "timings": "10:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Maidan Park", "distance": "0.5 km"}, {"name": "Birla Planetarium", "distance": "1 km"}]
    },
    {
        "name": "Darjeeling Toy Train Railway", "state": "West Bengal", "city": "Darjeeling", "category": "Heritage",
        "description": "A historic steam locomotive narrow-gauge railway system in the Himalayas, listed as a UNESCO World Heritage Site.",
        "best_months": "October, November, December, March, April, May", "latitude": 27.0428, "longitude": 88.2638,
        "entry_fee": 1000.0, "timings": "8:00 AM - 4:00 PM (Joyride hours)", "budget_category": "Mid-range", "is_trending": True,
        "attractions": [{"name": "Batasia Loop Garden", "distance": "5 km"}, {"name": "Ghoom Monastery", "distance": "6 km"}]
    },
    {
        "name": "Sundarbans National Mangrove Forest", "state": "West Bengal", "city": "Sajnekhali", "category": "Wildlife",
        "description": "The largest contiguous mangrove forest block in the world, famous for Royal Bengal Tigers, saltwater crocodiles, and boat safaris.",
        "best_months": "November, December, January, February", "latitude": 21.9497, "longitude": 89.1833,
        "entry_fee": 150.0, "timings": "8:30 AM - 4:00 PM (Safari boat checkin)", "budget_category": "Luxury", "is_trending": True,
        "attractions": [{"name": "Sajnekhali Watch Tower", "distance": "0.1 km"}, {"name": "Sudhanyakhali Watch Tower", "distance": "8 km (by boat)"}]
    },
    {
        "name": "Digha New Sea Beach", "state": "West Bengal", "city": "Digha", "category": "Beaches",
        "description": "A flat sandy beach on the Bay of Bengal coast, famous for seafood shacks, shallow waters safe for swimming, and ocean views.",
        "best_months": "October, November, December, January, February", "latitude": 21.6268, "longitude": 87.5123,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Marine Station Aquarium", "distance": "1.5 km"}, {"name": "Amarabati Park Lake", "distance": "2 km"}]
    },
    {
        "name": "Howrah Bridge Landmark", "state": "West Bengal", "city": "Kolkata", "category": "Heritage",
        "description": "A historic balanced cantilever steel truss bridge over the Hooghly River, carrying massive traffic and symbolizing Kolkata.",
        "best_months": "October, November, December, January, February, March", "latitude": 22.5851, "longitude": 88.3472,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Mullick Ghat Flower Market", "distance": "0.2 km"}, {"name": "Millennium Park Riverfront", "distance": "2 km"}]
    },
    {
        "name": "Dakshineswar Kali Temple Shrine", "state": "West Bengal", "city": "Kolkata", "category": "Spiritual",
        "description": "A famous Hindu temple complex located on the bank of Hooghly river, built in navaratna style, closely associated with Ramakrishna Paramahamsa.",
        "best_months": "October, November, December, January, February", "latitude": 22.6558, "longitude": 88.3584,
        "entry_fee": 0.0, "timings": "6:00 AM - 12:30 PM, 3:30 PM - 9:00 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Belur Math Monastery", "distance": "3 km (by ferry)"}, {"name": "Dakshineswar Ghat", "distance": "0.1 km"}]
    },
    {
        "name": "Tiger Hill Sunrise View", "state": "West Bengal", "city": "Darjeeling", "category": "Hill Stations",
        "description": "A high-altitude hilltop offering majestic views of the sunrise over Mount Kanchenjunga and Mount Everest peaks.",
        "best_months": "October, November, December, January, March, April", "latitude": 26.9942, "longitude": 88.2912,
        "entry_fee": 50.0, "timings": "4:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Senchal Wildlife Sanctuary", "distance": "2 km"}, {"name": "Ghoom Railway Station", "distance": "5 km"}]
    },
    {
        "name": "Kalimpong Pine Forest Trail", "state": "West Bengal", "city": "Kalimpong", "category": "Hill Stations",
        "description": "Lush pine forests on hill slopes, offering beautiful misty mountain walk pathways and cool climate conditions.",
        "best_months": "October, November, December, March, April, May", "latitude": 27.0600, "longitude": 88.4700,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Durpin Monastery Viewpoint", "distance": "3 km"}, {"name": "Deolo Hill Park", "distance": "8 km"}]
    },

    # === ODISHA ===
    {
        "name": "Konark Sun Temple Monument", "state": "Odisha", "city": "Konark", "category": "Heritage",
        "description": "A 13th-century chariot-shaped Hindu temple complex dedicated to the Sun God, built by Eastern Ganga Dynasty and famed for stone wheels.",
        "best_months": "October, November, December, January, February", "latitude": 19.8876, "longitude": 86.0945,
        "entry_fee": 40.0, "timings": "6:00 AM - 8:00 PM", "budget_category": "Mid-range", "is_trending": True,
        "attractions": [{"name": "Chandrabhaga Beach", "distance": "3.5 km"}, {"name": "Konark Museum", "distance": "0.8 km"}]
    },
    {
        "name": "Puri Shree Jagannath Temple", "state": "Odisha", "city": "Puri", "category": "Spiritual",
        "description": "An important sacred Hindu temple dedicated to Jagannath, famous for its grand annual Ratha Yatra chariot festival.",
        "best_months": "October, November, December, January, February", "latitude": 19.8048, "longitude": 85.8179,
        "entry_fee": 0.0, "timings": "5:30 AM - 10:00 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Puri Golden Beach", "distance": "1.5 km"}, {"name": "Narendra Pokhari Tank", "distance": "1 km"}]
    },
    {
        "name": "Chilika Lake Bird Sanctuary", "state": "Odisha", "city": "Rambha", "category": "Wildlife",
        "description": "The largest brackish water lagoon in Asia, famous for migratory waterbirds, Irrawaddy Dolphins, and scenic island boat safaris.",
        "best_months": "November, December, January, February", "latitude": 19.6678, "longitude": 85.3379,
        "entry_fee": 150.0, "timings": "6:00 AM - 5:30 PM (Boating hours)", "budget_category": "Mid-range", "is_trending": True,
        "attractions": [{"name": "Kalijai Island Temple", "distance": "15 km (by boat)"}, {"name": "Nalabana Bird Sanctuary", "distance": "20 km"}]
    },
    {
        "name": "Lingaraj Temple Shrine", "state": "Odisha", "city": "Bhubaneswar", "category": "Spiritual",
        "description": "The largest and oldest temple building in the temple city Bhubaneswar, representing supreme Kalinga architecture, dedicated to Shiva.",
        "best_months": "October, November, December, January", "latitude": 20.2421, "longitude": 85.8342,
        "entry_fee": 0.0, "timings": "6:00 AM - 9:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Bindusagar Lake", "distance": "0.3 km"}, {"name": "Mukteswara Temple", "distance": "1.5 km"}]
    },
    {
        "name": "Udayagiri and Khandagiri Caves Hill", "state": "Odisha", "city": "Bhubaneswar", "category": "Heritage",
        "description": "Partly natural and partly artificial rock-cut caves carved out of hills, showing historic inscriptions and Jain carvings from 2nd century BCE.",
        "best_months": "October, November, December, January, February", "latitude": 20.2581, "longitude": 85.7862,
        "entry_fee": 25.0, "timings": "9:00 AM - 5:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Rani Gumpha Cave", "distance": "0.1 km"}, {"name": "Dhauli Peace Pagoda", "distance": "12 km"}]
    },
    {
        "name": "Simlipal Tiger Reserve and Forest", "state": "Odisha", "city": "Mayurbhanj", "category": "Wildlife",
        "description": "A massive national park and elephant reserve, rich in waterfalls like Barehipani Falls, home to royal tigers and dense sal trees.",
        "best_months": "November, December, January, February, March, April", "latitude": 21.9431, "longitude": 86.4251,
        "entry_fee": 100.0, "timings": "6:00 AM - 5:00 PM", "budget_category": "Luxury", "is_trending": False,
        "attractions": [{"name": "Barehipani Waterfall", "distance": "20 km inside"}, {"name": "Joranda Falls", "distance": "25 km"}]
    },
    {
        "name": "Daringbadi Hill Station", "state": "Odisha", "city": "Kandhamal", "category": "Hill Stations",
        "description": "Popularly known as the 'Kashmir of Odisha', a peaceful hill station surrounded by pine forests, coffee gardens, and valleys.",
        "best_months": "November, December, January, February", "latitude": 20.1303, "longitude": 84.1378,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Daringbadi Pine Forest Park", "distance": "1.5 km"}, {"name": "Midubanda Waterfall", "distance": "15 km"}]
    },
    {
        "name": "Gopalpur Sea Beach Coast", "state": "Odisha", "city": "Gopalpur", "category": "Beaches",
        "description": "A quiet and calm sea resort beach in southern Odisha, famous for an old lighthouse, coconut grooves, and olive ridley sea turtle nesting.",
        "best_months": "October, November, December, January, February", "latitude": 19.2612, "longitude": 84.9123,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Gopalpur Old Lighthouse", "distance": "0.5 km"}, {"name": "Rushikulya Turtle Beach", "distance": "30 km"}]
    },

    # === ASSAM ===
    {
        "name": "Kaziranga National Park Marshlands", "state": "Assam", "city": "Kohora", "category": "Wildlife",
        "description": "A world-renowned sanctuary housing two-thirds of the world's great one-horned rhinoceros population, set along Brahmaputra valley.",
        "best_months": "November, December, January, February, March, April", "latitude": 26.5775, "longitude": 93.1712,
        "entry_fee": 100.0, "timings": "7:30 AM - 10:00 AM, 1:30 PM - 3:00 PM (Safari)", "budget_category": "Luxury", "is_trending": True,
        "attractions": [{"name": "Kaziranga National Orchid Park", "distance": "3 km"}, {"name": "Brahmaputra River Safari", "distance": "10 km"}]
    },
    {
        "name": "Kamakhya Shakti Peeth Temple", "state": "Assam", "city": "Guwahati", "category": "Spiritual",
        "description": "One of the oldest and most revered centers of Tantric Hindu worship, dedicated to Goddess Kamakhya, located on Nilachal Hill.",
        "best_months": "October, November, December, January, February", "latitude": 26.1658, "longitude": 91.7058,
        "entry_fee": 0.0, "timings": "5:30 AM - 1:00 PM, 2:30 PM - 10:00 PM", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Nilachal Hill Viewpoint", "distance": "0.1 km"}, {"name": "Umananda Island Temple", "distance": "8 km"}]
    },
    {
        "name": "Majuli River Island", "state": "Assam", "city": "Majuli", "category": "Heritage",
        "description": "The largest river island in the world, situated on the Brahmaputra River, acting as the hub of Assamese Neo-Vaishnavite culture.",
        "best_months": "October, November, December, January, February, March", "latitude": 26.9585, "longitude": 94.1713,
        "entry_fee": 0.0, "timings": "24 Hours open (Ferry timings apply)", "budget_category": "Mid-range", "is_trending": True,
        "attractions": [{"name": "Kamalabari Satra Monastery", "distance": "2 km"}, {"name": "Dakhinpat Satra Satra", "distance": "8 km"}]
    },
    {
        "name": "Manas National Park Sanctuary", "state": "Assam", "city": "Barpeta", "category": "Wildlife",
        "description": "A UNESCO site, tiger reserve, and biosphere reserve in the foothills of Bhutan hills, famous for rare golden langurs.",
        "best_months": "November, December, January, February, March, April", "latitude": 26.7378, "longitude": 90.9658,
        "entry_fee": 200.0, "timings": "6:00 AM - 4:00 PM", "budget_category": "Luxury", "is_trending": False,
        "attractions": [{"name": "Manas River Shore", "distance": "0.5 km"}, {"name": "Mathanguri Forest Lodge", "distance": "20 km inside"}]
    },
    {
        "name": "Hajo Pilgrimage Center", "state": "Assam", "city": "Hajo", "category": "Spiritual",
        "description": "An ancient sacred place for three religions: Hinduism, Buddhism, and Islam, hosting Hayagriva Madhava Temple and Poa Mecca shrine.",
        "best_months": "October, November, December, January, February", "latitude": 26.2432, "longitude": 91.5300,
        "entry_fee": 0.0, "timings": "6:00 AM - 8:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Hayagriva Madhava Temple", "distance": "0.2 km"}, {"name": "Powa Mecca Mosque Shrine", "distance": "2.5 km climb"}]
    },
    {
        "name": "Haflong Hill Lake", "state": "Assam", "city": "Haflong", "category": "Hill Stations",
        "description": "Assam's only hill station town, featuring a gorgeous central lake, pine woodlands, misty peaks, and tea gardens.",
        "best_months": "October, November, December, January, February", "latitude": 25.1812, "longitude": 93.0179,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Haflong Lake Park", "distance": "0.1 km"}, {"name": "Jatinga Bird Mystery Valley", "distance": "9 km"}]
    },
    {
        "name": "Sivasagar Rang Ghar Palace", "state": "Assam", "city": "Sivasagar", "category": "Heritage",
        "description": "A historic double-story amphitheater building built in 1744 by Ahom dynasty rulers, one of the oldest surviving amphitheaters in Asia.",
        "best_months": "October, November, December, January, February", "latitude": 26.9732, "longitude": 94.6232,
        "entry_fee": 25.0, "timings": "9:00 AM - 5:30 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Talatala Ghar Royal Palace", "distance": "3 km"}, {"name": "Sivasagar Sivadol Temple", "distance": "4 km"}]
    },

    # === ADDITIONAL HIGH QUALITY ENTRIES FROM MANDATORY LIST OF 15 STATES ===
    # === TAMIL NADU ===
    {
        "name": "Nilgiri Mountain Railway Train", "state": "Tamil Nadu", "city": "Coonoor", "category": "Heritage",
        "description": "A UNESCO World Heritage steam toy train that climbs steep track slopes from Mettupalayam to Ooty, passing valleys, forests, and tunnels.",
        "best_months": "October, November, December, January, April, May", "latitude": 11.3536, "longitude": 76.7958,
        "entry_fee": 200.0, "timings": "7:00 AM - 4:00 PM", "budget_category": "Mid-range", "is_trending": True,
        "attractions": [{"name": "Sim's Park Botanical Gardens", "distance": "2 km"}, {"name": "Dolphin's Nose Viewpoint", "distance": "10 km"}]
    },
    # === KERALA ===
    {
        "name": "Sree Padmanabhaswamy Temple Treasure", "state": "Kerala", "city": "Thiruvananthapuram", "category": "Spiritual",
        "description": "An ancient grand temple built in Dravidian style with high Gopurams, famous for golden deity status and subterranean vault treasures.",
        "best_months": "October, November, December, January, February", "latitude": 8.4831, "longitude": 76.9437,
        "entry_fee": 0.0, "timings": "3:30 AM - 12:00 PM, 5:00 PM - 8:30 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Kuthira Malika Royal Museum", "distance": "0.2 km"}, {"name": "Kovalam Beach Shore", "distance": "12 km"}]
    },
    # === KARNATAKA ===
    {
        "name": "Coorg Abbey Falls Valley", "state": "Karnataka", "city": "Madikeri", "category": "Hill Stations",
        "description": "A beautiful waterfall hidden amidst green coffee plantations and spice gardens in Coorg Hills, cascading to a small stream.",
        "best_months": "July, August, September, October, November, December", "latitude": 12.4370, "longitude": 75.7290,
        "entry_fee": 15.0, "timings": "9:00 AM - 5:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Raja's Seat Viewpoint", "distance": "6 km"}, {"name": "Madikeri Fort Palace", "distance": "5.5 km"}]
    },
    # === GOA ===
    {
        "name": "Calangute Golden Sand Beach", "state": "Goa", "city": "Calangute", "category": "Beaches",
        "description": "One of the most famous tourist hubs in North Goa, active with parasailing, water sports, beach shacks, and night events.",
        "best_months": "November, December, January, February", "latitude": 15.5495, "longitude": 73.7536,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": True,
        "attractions": [{"name": "Baga Beach Shacks", "distance": "1.5 km"}, {"name": "Fort Aguada Lighthouse", "distance": "9 km"}]
    },
    # === RAJASTHAN ===
    {
        "name": "Udaipur Lake Palace Floating", "state": "Rajasthan", "city": "Udaipur", "category": "Heritage",
        "description": "A majestic luxury palace hotel constructed on an island in Lake Pichola, offering scenic boat rides and royal hospitality.",
        "best_months": "October, November, December, January, February", "latitude": 24.5757, "longitude": 73.6801,
        "entry_fee": 0.0, "timings": "24 Hours open (Only hotel guests/boat trips)", "budget_category": "Luxury", "is_trending": True,
        "attractions": [{"name": "City Palace Udaipur Museum", "distance": "0.5 km (by boat)"}, {"name": "Jag Mandir Island", "distance": "1.2 km"}]
    },
    # === HIMACHAL PRADESH ===
    {
        "name": "Shimla Ridge Promenade", "state": "Himachal Pradesh", "city": "Shimla", "category": "Hill Stations",
        "description": "A wide open pedestrian street in the center of Shimla, acting as a cultural hub with pine-wood views and old colonial buildings.",
        "best_months": "October, November, December, January, February, March, April", "latitude": 31.1049, "longitude": 77.1735,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Mall Road Shops", "distance": "0.1 km"}, {"name": "Jakhoo Monkey Temple Peak", "distance": "2 km trek"}]
    },
    # === JAMMU & KASHMIR ===
    {
        "name": "Dal Lake Shikara Boat", "state": "Jammu & Kashmir", "city": "Srinagar", "category": "Hill Stations",
        "description": "The jewel water body of Srinagar, famous for traditional wooden Shikara boat rides, floating markets, and wooden houseboats.",
        "best_months": "April, May, June, July, August, September, October", "latitude": 34.0900, "longitude": 74.8400,
        "entry_fee": 0.0, "timings": "24 Hours open (Boat cruises till 8PM)", "budget_category": "Mid-range", "is_trending": True,
        "attractions": [{"name": "Shalimar Bagh Mughal Garden", "distance": "6 km"}, {"name": "Hazratbal Shrine Mosque", "distance": "8 km"}]
    },
    # === MAHARASHTRA ===
    {
        "name": "Gateway of India Monument", "state": "Maharashtra", "city": "Mumbai", "category": "Heritage",
        "description": "An iconic basalt stone arch monument built in 1924 overlooking the Mumbai harbor, symbolizing the city's historical heritage.",
        "best_months": "October, November, December, January, February, March", "latitude": 18.9220, "longitude": 72.8347,
        "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Taj Mahal Palace Hotel", "distance": "0.1 km"}, {"name": "Elephanta Caves Boat Ride", "distance": "10 km (by ferry)"}]
    },
    # === UTTARAKHAND ===
    {
        "name": "Kedarnath Temple Mountain Shrine", "state": "Uttarakhand", "city": "Kedarnath", "category": "Spiritual",
        "description": "A historic Shiva temple located near Mandakini River in the high snow peaks of Himalayas, requiring a 16 km trek from Gaurikund.",
        "best_months": "May, June, September, October, November", "latitude": 30.7352, "longitude": 79.0669,
        "entry_fee": 0.0, "timings": "6:00 AM - 2:00 PM, 5:00 PM - 8:30 PM (Winter Closed)", "budget_category": "Mid-range", "is_trending": True,
        "attractions": [{"name": "Bhairav Temple Kedarnath", "distance": "1 km climb"}, {"name": "Chorabari Glacial Lake", "distance": "4 km trek"}]
    },
    # === ANDHRA PRADESH ===
    {
        "name": "Kailasagiri Hill Viewpoint", "state": "Andhra Pradesh", "city": "Visakhapatnam", "category": "Hill Stations",
        "description": "A beautiful hilltop park offering panoramic views of the Vizag beach coast, featuring massive Shiva-Parvati statues and a toy train.",
        "best_months": "October, November, December, January, February", "latitude": 17.7497, "longitude": 83.3421,
        "entry_fee": 20.0, "timings": "10:00 AM - 8:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "INS Kursura Museum Beach", "distance": "4 km"}, {"name": "Rishikonda Beach", "distance": "6 km"}]
    },
    # === TELANGANA ===
    {
        "name": "Ramappa Lake Leisure Park", "state": "Telangana", "city": "Mulugu", "category": "Wildlife",
        "description": "A vast, ancient lake constructed during the Kakatiya era, popular for boating, sunset walks, and bird watching.",
        "best_months": "September, October, November, December, January", "latitude": 18.2520, "longitude": 79.9321,
        "entry_fee": 20.0, "timings": "9:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Ramappa Temple", "distance": "1 km"}, {"name": "Laknavaram Forest Lake", "distance": "30 km"}]
    },
    # === GUJARAT ===
    {
        "name": "Sun Temple Modhera Pool", "state": "Gujarat", "city": "Modhera", "category": "Heritage",
        "description": "The Modhera Sun Temple features a spectacular stepped tank (Suryakund) adorned with 108 miniature shrines.",
        "best_months": "October, November, December, January, February", "latitude": 23.5830, "longitude": 72.1383,
        "entry_fee": 25.0, "timings": "7:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Sun Temple Sabha Mandapa", "distance": "0.1 km"}, {"name": "Modhera Art Museum", "distance": "0.2 km"}]
    },
    # === WEST BENGAL ===
    {
        "name": "Sundarbans Tiger Reserve Sajnekhali", "state": "West Bengal", "city": "Sajnekhali", "category": "Wildlife",
        "description": "A key tiger preservation zone within Sundarbans Mangroves, hosting a turtle hatchery, museum, and wildlife watchtower.",
        "best_months": "November, December, January, February", "latitude": 21.9498, "longitude": 89.1834,
        "entry_fee": 150.0, "timings": "8:30 AM - 4:00 PM", "budget_category": "Luxury", "is_trending": False,
        "attractions": [{"name": "Sajnekhali Bird Sanctuary Watchtower", "distance": "0.1 km"}, {"name": "Sudhanyakhali Mangrove Point", "distance": "8 km (by boat)"}]
    },
    # === ODISHA ===
    {
        "name": "Puri Golden Beach Coast", "state": "Odisha", "city": "Puri", "category": "Beaches",
        "description": "A clean, golden-sand beach certified as Blue Flag, offering safe bathing waters, sunset craft stalls, and temple visits.",
        "best_months": "October, November, December, January, February", "latitude": 19.7997, "longitude": 85.8221,
        "entry_fee": 20.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": True,
        "attractions": [{"name": "Jagannath Temple Puri", "distance": "1.5 km"}, {"name": "Swargadwar Cremation Ghat Beach", "distance": "2 km"}]
    },
    # === ASSAM ===
    {
        "name": "Umananda River Island Temple", "state": "Assam", "city": "Guwahati", "category": "Spiritual",
        "description": "The smallest inhabited river island in the world, set on the Brahmaputra River, housing an ancient Shiva temple.",
        "best_months": "October, November, December, January, February", "latitude": 26.1958, "longitude": 91.7458,
        "entry_fee": 0.0, "timings": "6:00 AM - 5:00 PM (Ferry tickets apply)", "budget_category": "Budget", "is_trending": False,
        "attractions": [{"name": "Brahmaputra River Ferry Terminal", "distance": "0.1 km"}, {"name": "Kamakhya Temple Shrine", "distance": "8 km"}]
    }
]

# Additional filler data to ensure we have well over 100+ unique places across these 15 states.
extra_destinations = [
    # Tamil Nadu
    {"name": "Hodaikanal Coaker's Walk Trail", "state": "Tamil Nadu", "city": "Kodaikanal", "category": "Hill Stations", "description": "Paved pathway edge along mountain slopes offering valley views.", "best_months": "October, November, December", "latitude": 10.2316, "longitude": 77.4933, "entry_fee": 10.0, "timings": "7:00 AM - 7:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Bryant Park", "distance": "0.3 km"}]},
    {"name": "Marina Sandy Beach Walks", "state": "Tamil Nadu", "city": "Chennai", "category": "Beaches", "description": "Urban beach shore along the Bay of Bengal, famous for evening food stalls.", "best_months": "November, December, January", "latitude": 13.0501, "longitude": 80.2825, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "San Thome Cathedral Basilica", "distance": "2 km"}]},
    {"name": "Ooty Botanical Garden Lawns", "state": "Tamil Nadu", "city": "Ooty", "category": "Hill Stations", "description": "Lush terraced gardens featuring rare plants and fossilized trees.", "best_months": "October, November, March, April", "latitude": 11.4168, "longitude": 76.7112, "entry_fee": 40.0, "timings": "7:00 AM - 6:30 PM", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Doddabetta Peak View", "distance": "7 km"}]},

    # Kerala
    {"name": "Munnar Tea Valley walk", "state": "Kerala", "city": "Munnar", "category": "Hill Stations", "description": "Slopes of tea gardens with misty mountain walking pathways.", "best_months": "September, October, November", "latitude": 10.0890, "longitude": 77.0596, "entry_fee": 20.0, "timings": "8:30 AM - 4:30 PM", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Eravikulam Park", "distance": "8 km"}]},
    {"name": "Alleppey Houseboat Canal Cruise", "state": "Kerala", "city": "Alleppey", "category": "Beaches", "description": "Palm-fringed backwater channels toured by traditional houseboats.", "best_months": "October, November, December", "latitude": 9.4982, "longitude": 76.3389, "entry_fee": 1000.0, "timings": "24 Hours open", "budget_category": "Luxury", "is_trending": False, "attractions": [{"name": "Alleppey Shore Beach", "distance": "4.5 km"}]},
    {"name": "Kovalam Beach Lighthouse", "state": "Kerala", "city": "Kovalam", "category": "Beaches", "description": "Crescent beach curve with a striped red-and-white lighthouse tower.", "best_months": "November, December, January", "latitude": 8.4005, "longitude": 76.9788, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Hawa Beach Coast", "distance": "0.3 km"}]},

    # Karnataka
    {"name": "Virupaksha Temple Hampi", "state": "Karnataka", "city": "Hampi", "category": "Heritage", "description": "Historic active temple complex dedicated to Shiva, dating to 7th century AD.", "best_months": "October, November, December", "latitude": 15.3351, "longitude": 76.4601, "entry_fee": 0.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Hampi Stone Chariot", "distance": "3 km"}]},
    {"name": "Mysore Palace Durbar Hall", "state": "Karnataka", "city": "Mysore", "category": "Heritage", "description": "Magnificent royal palace architecture of the Wadiyar dynasty.", "best_months": "October, November, December", "latitude": 12.3052, "longitude": 76.6552, "entry_fee": 70.0, "timings": "10:00 AM - 5:30 PM", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Chamundi Hills Temple", "distance": "12 km"}]},
    {"name": "Gokarna Kudle Beach Path", "state": "Karnataka", "city": "Gokarna", "category": "Beaches", "description": "Quiet beach bay offering sandy shoreline walks and seaside cafes.", "best_months": "October, November, December", "latitude": 14.5220, "longitude": 74.3162, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Om Beach Gokarna", "distance": "2 km"}]},

    # Goa
    {"name": "Dudhsagar Milk Fall View", "state": "Goa", "city": "Sanguem", "category": "Wildlife", "description": "Four-tiered waterfall on Mandovi river looking like a sea of milk.", "best_months": "June, July, August, September", "latitude": 15.3186, "longitude": 74.3139, "entry_fee": 400.0, "timings": "9:00 AM - 5:00 PM", "budget_category": "Luxury", "is_trending": False, "attractions": [{"name": "Bhagwan Mahavir Sanctuary", "distance": "2 km"}]},
    {"name": "Baga Beach Shacks and Clubs", "state": "Goa", "city": "Calangute", "category": "Beaches", "description": "Lively shoreline shacks and night clubs on Baga beach coast.", "best_months": "November, December, January", "latitude": 15.5583, "longitude": 73.7512, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Calangute Beach Coast", "distance": "1.5 km"}]},
    {"name": "Fort Aguada Stone Citadel", "state": "Goa", "city": "Sinquerim", "category": "Heritage", "description": "Portuguese fort and lighthouse built in 1612 to protect coastlines.", "best_months": "October, November, December", "latitude": 15.4927, "longitude": 73.7736, "entry_fee": 25.0, "timings": "9:30 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Sinquerim Beach Rocks", "distance": "1 km"}]},

    # Rajasthan
    {"name": "Amber Palace Fort Hall", "state": "Rajasthan", "city": "Jaipur", "category": "Heritage", "description": "Hilltop palace fort built in 1592 by Raja Man Singh featuring sheesh mahal.", "best_months": "October, November, December", "latitude": 26.9856, "longitude": 75.8514, "entry_fee": 100.0, "timings": "8:00 AM - 5:30 PM", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Jaigarh Fort Castle", "distance": "1.5 km"}]},
    {"name": "Jaisalmer Fort Golden Citadel", "state": "Rajasthan", "city": "Jaisalmer", "category": "Heritage", "description": "One of the largest living forts in Thar desert, built in 1156 AD.", "best_months": "October, November, December", "latitude": 26.9125, "longitude": 70.9131, "entry_fee": 50.0, "timings": "9:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Patwon Ki Haveli Mansions", "distance": "0.5 km"}]},
    {"name": "Ranthambore Fort Tiger Park", "state": "Rajasthan", "city": "Sawai Madhopur", "category": "Wildlife", "description": "Bengal tiger park set around a historic 10th century fort.", "best_months": "October, November, December", "latitude": 25.8673, "longitude": 76.3015, "entry_fee": 1200.0, "timings": "6:00 AM - 9:30 AM", "budget_category": "Luxury", "is_trending": False, "attractions": [{"name": "Ranthambore Fort Ruins", "distance": "5 km"}]},

    # Himachal Pradesh
    {"name": "Solang Valley Adventure Slopes", "state": "Himachal Pradesh", "city": "Manali", "category": "Hill Stations", "description": "Adventure sports arena for paragliding, zorbing, and winter skiing.", "best_months": "October, November, December", "latitude": 32.3168, "longitude": 77.1668, "entry_fee": 0.0, "timings": "9:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Anjani Mahadev Cave Temple", "distance": "2 km"}]},
    {"name": "McLeod Ganj Tsuglagkhang Monastery", "state": "Himachal Pradesh", "city": "Dharamshala", "category": "Spiritual", "description": "Spiritual home of Dalai Lama and a center for Tibetan arts.", "best_months": "September, October, November", "latitude": 32.2427, "longitude": 77.3214, "entry_fee": 0.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Bhagsunag Falls", "distance": "2 km"}]},
    {"name": "Kasol Parvati River Valley", "state": "Himachal Pradesh", "city": "Kasol", "category": "Hill Stations", "description": "Scenic alpine village set along the roaring Parvati River.", "best_months": "October, November, April, May", "latitude": 32.0098, "longitude": 77.3152, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Manikaran Hot Springs", "distance": "4 km"}]},

    # Jammu & Kashmir
    {"name": "Pahalgam Valley Meadows", "state": "Jammu & Kashmir", "city": "Pahalgam", "category": "Hill Stations", "description": "Lush pine forests, rivers, and alpine meadows in Lidder Valley.", "best_months": "April, May, June, September, October", "latitude": 34.0162, "longitude": 75.3154, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Betaab Valley Park", "distance": "7 km"}]},
    {"name": "Sonamarg Glacial Valley", "state": "Jammu & Kashmir", "city": "Sonamarg", "category": "Hill Stations", "description": "Meadow of Gold offering treks to Thajiwas glacier and mountains.", "best_months": "April, May, June, September, October", "latitude": 34.3054, "longitude": 75.2931, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Thajiwas Glacier View", "distance": "3 km trek"}]},
    {"name": "Shankaracharya Temple Hill", "state": "Jammu & Kashmir", "city": "Srinagar", "category": "Spiritual", "description": "Ancient Shiva temple built on a hilltop overlooking Srinagar city.", "best_months": "April, May, June, September, October", "latitude": 34.0784, "longitude": 74.8451, "entry_fee": 0.0, "timings": "7:00 AM - 8:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Dal Lake Shore", "distance": "3 km"}]},

    # Maharashtra
    {"name": "Ellora Rock Cut Temples", "state": "Maharashtra", "city": "Aurangabad", "category": "Heritage", "description": "Stunning rock-cut caves showcasing the monolithic Kailash Temple.", "best_months": "October, November, December", "latitude": 20.0258, "longitude": 75.1784, "entry_fee": 40.0, "timings": "9:00 AM - 5:30 PM (Closed on Tuesdays)", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Kailash Cave 16", "distance": "0.1 km"}]},
    {"name": "Lonavala Bhushi Dam Lake", "state": "Maharashtra", "city": "Lonavala", "category": "Hill Stations", "description": "Scenic masonry dam popular during heavy monsoon rainfall.", "best_months": "June, July, August, September", "latitude": 18.7300, "longitude": 73.3480, "entry_fee": 0.0, "timings": "9:00 AM - 5:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Tiger's Leap Cliff", "distance": "4 km"}]},
    {"name": "Mahabaleshwar Kate's Point View", "state": "Maharashtra", "city": "Mahabaleshwar", "category": "Hill Stations", "description": "Cliff viewpoint overlooking the Balakwasli reservoir lake.", "best_months": "October, November, December, January", "latitude": 17.9254, "longitude": 73.6651, "entry_fee": 0.0, "timings": "6:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Arthur's Seat Peak", "distance": "8 km"}]},

    # Uttarakhand
    {"name": "Rishikesh Laxman Jhula Bridge", "state": "Uttarakhand", "city": "Rishikesh", "category": "Spiritual", "description": "Famous iron suspension bridge across the Ganges River.", "best_months": "October, November, December", "latitude": 30.1362, "longitude": 78.3312, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Triveni Ghat Aarti", "distance": "4 km"}]},
    {"name": "Nainital Naini Lake boating", "state": "Uttarakhand", "city": "Nainital", "category": "Hill Stations", "description": "Pear-shaped lake offering yachting, boating, and scenic shore walks.", "best_months": "October, November, March, April", "latitude": 29.3884, "longitude": 79.4651, "entry_fee": 100.0, "timings": "9:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Naina Devi Temple", "distance": "0.1 km"}]},
    {"name": "Mussoorie Kempty Waterfalls", "state": "Uttarakhand", "city": "Mussoorie", "category": "Hill Stations", "description": "Popular waterfalls cascading down mountain rocks into bathing pools.", "best_months": "October, November, March, April", "latitude": 30.4583, "longitude": 78.0784, "entry_fee": 0.0, "timings": "8:00 AM - 5:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Lal Tibba Viewpoint", "distance": "12 km"}]},

    # Andhra Pradesh
    {"name": "Simhachalam Varaha Temple", "state": "Andhra Pradesh", "city": "Visakhapatnam", "category": "Spiritual", "description": "Ornate hilltop temple dedicated to Lord Narasimha, dating back to 11th century AD.", "best_months": "October, November, December, January", "latitude": 17.7669, "longitude": 83.2500, "entry_fee": 0.0, "timings": "7:00 AM - 9:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "INS Kursura Museum", "distance": "16 km"}]},
    {"name": "Bhimunipatnam Sandy Coastline", "state": "Andhra Pradesh", "city": "Bheemili", "category": "Beaches", "description": "Quiet beach near Gosthani river mouth, showing Dutch graveyard ruins.", "best_months": "October, November, December", "latitude": 17.8902, "longitude": 83.4431, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Bheemili Dutch Cemetery", "distance": "0.5 km"}]},
    {"name": "Horsley Hills Hill Station", "state": "Andhra Pradesh", "city": "Madanapalle", "category": "Hill Stations", "description": "Lush green hills with pleasant climate conditions and forest views.", "best_months": "November, December, January, February", "latitude": 13.6495, "longitude": 78.3991, "entry_fee": 20.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Gali Banda Windy Rock", "distance": "1 km"}]},
    {"name": "Kondapalli Fort Ruins", "state": "Andhra Pradesh", "city": "Vijayawada", "category": "Heritage", "description": "14th-century hill fortress famous for producing traditional Kondapalli toys.", "best_months": "October, November, December", "latitude": 16.6183, "longitude": 80.5372, "entry_fee": 10.0, "timings": "10:00 AM - 5:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Kondapalli Toy Village", "distance": "1 km"}]},

    # Telangana
    {"name": "Warangal Fort Stone Arches", "state": "Telangana", "city": "Warangal", "category": "Heritage", "description": "Historic fort ruins with iconic Kakatiya Torana stone archways.", "best_months": "October, November, December", "latitude": 17.9732, "longitude": 79.6200, "entry_fee": 25.0, "timings": "9:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Thousand Pillar Temple", "distance": "6 km"}]},
    {"name": "Bhongir Fort Monolith Castle", "state": "Telangana", "city": "Bhongir", "category": "Heritage", "description": "Fort built on a single massive egg-shaped monolithic rock hill.", "best_months": "October, November, December", "latitude": 17.5113, "longitude": 78.8876, "entry_fee": 10.0, "timings": "9:00 AM - 5:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Bhongir Rock Climbing Area", "distance": "0.1 km"}]},
    {"name": "Yadadri Lakshmi Narasimha Temple", "state": "Telangana", "city": "Yadagirigutta", "category": "Spiritual", "description": "Major newly reconstructed gold-plated stone temple shrine.", "best_months": "October, November, December, January", "latitude": 17.5883, "longitude": 78.9431, "entry_fee": 0.0, "timings": "4:00 AM - 9:30 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Surendrapuri Mythology Museum", "distance": "4 km"}]},
    {"name": "Pocharam Wildlife Sanctuary Lake", "state": "Telangana", "city": "Medak", "category": "Wildlife", "description": "Sanctuary around a scenic reservoir, home to waterbirds and deer.", "best_months": "October, November, December", "latitude": 18.0667, "longitude": 78.1667, "entry_fee": 20.0, "timings": "9:00 AM - 5:30 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Medak Cathedral Church", "distance": "15 km"}]},

    # Gujarat
    {"name": "Adalaj Stepwell Monument", "state": "Gujarat", "city": "Gandhinagar", "category": "Heritage", "description": "Intricately carved five-story deep stone stepwell built in 1498.", "best_months": "October, November, December", "latitude": 23.1669, "longitude": 72.5800, "entry_fee": 25.0, "timings": "8:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Akshardham Temple Gandhinagar", "distance": "12 km"}]},
    {"name": "Rani Ki Vav Stepwell", "state": "Gujarat", "city": "Patan", "category": "Heritage", "description": "UNESCO World Heritage stepped well adorned with sculptures of Vishnu.", "best_months": "October, November, December", "latitude": 23.8584, "longitude": 72.1021, "entry_fee": 40.0, "timings": "8:00 AM - 6:00 PM", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Patan Patola Silk Museum", "distance": "1.5 km"}]},
    {"name": "Somnath Beach Walks", "state": "Gujarat", "city": "Veraval", "category": "Beaches", "description": "Beach shore adjacent to the Jyotirlinga temple, offering sea breezes.", "best_months": "October, November, December", "latitude": 20.8872, "longitude": 70.4022, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Somnath Temple Shrine", "distance": "0.1 km"}]},
    {"name": "Girnar Hill Pilgrimage Trail", "state": "Gujarat", "city": "Junagadh", "category": "Spiritual", "description": "Sacred mountain containing hundreds of temples along stone stairs.", "best_months": "October, November, December, January", "latitude": 21.5284, "longitude": 70.5213, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Girnar Ropeway Ride", "distance": "0.5 km"}]},

    # West Bengal
    {"name": "Dakshineswar River Ghats", "state": "West Bengal", "city": "Kolkata", "category": "Spiritual", "description": "River ghats on the Hooghly river adjacent to the Kali temple.", "best_months": "October, November, December", "latitude": 22.6550, "longitude": 88.3580, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Dakshineswar Temple", "distance": "0.1 km"}]},
    {"name": "Mirik Lake Hill Station", "state": "West Bengal", "city": "Mirik", "category": "Hill Stations", "description": "Picturesque lake surrounded by pine trees, cardamoms, and tea gardens.", "best_months": "October, November, April, May", "latitude": 26.8876, "longitude": 88.1812, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Sumendu Lake Arch Bridge", "distance": "0.1 km"}]},
    {"name": "Darjeeling Peace Pagoda Dome", "state": "West Bengal", "city": "Darjeeling", "category": "Spiritual", "description": "Beautiful Buddhist Peace Pagoda offering panoramic views of hills.", "best_months": "October, November, April, May", "latitude": 27.0294, "longitude": 88.2612, "entry_fee": 0.0, "timings": "4:30 AM - 7:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Darjeeling Toy Train Station", "distance": "3 km"}]},
    {"name": "Digha Marine Drive Coastline", "state": "West Bengal", "city": "Digha", "category": "Beaches", "description": "Coastal road connecting Digha to Mandarmani beaches along the sea.", "best_months": "October, November, December", "latitude": 21.6384, "longitude": 87.5584, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Mandarmani Beach Shacks", "distance": "22 km"}]},

    # Odisha
    {"name": "Puri Jagannath Temple Corridor", "state": "Odisha", "city": "Puri", "category": "Spiritual", "description": "Grand heritage corridor path surrounding the historic Jagannath Temple.", "best_months": "October, November, December", "latitude": 19.8050, "longitude": 85.8180, "entry_fee": 0.0, "timings": "5:30 AM - 10:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Puri Golden Beach", "distance": "1.5 km"}]},
    {"name": "Konark Chandrabhaga Sandy Coast", "state": "Odisha", "city": "Konark", "category": "Beaches", "description": "Beautiful ocean beach near the Sun temple, famous for sunsets.", "best_months": "October, November, December", "latitude": 19.8900, "longitude": 86.1121, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Konark Sun Temple", "distance": "3.5 km"}]},
    {"name": "Khandagiri Jain Cave Temple", "state": "Odisha", "city": "Bhubaneswar", "category": "Heritage", "description": "Historic Jain rock caves on Khandagiri hills with stone carvings.", "best_months": "October, November, December", "latitude": 20.2590, "longitude": 85.7870, "entry_fee": 25.0, "timings": "9:00 AM - 5:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Udayagiri Caves", "distance": "0.2 km"}]},
    {"name": "Nandankanan Zoological Park", "state": "Odisha", "city": "Bhubaneswar", "category": "Wildlife", "description": "Renowned zoo and sanctuary famous for breeding white tigers.", "best_months": "October, November, December, January", "latitude": 20.3994, "longitude": 85.8232, "entry_fee": 50.0, "timings": "7:30 AM - 5:30 PM (Closed on Mondays)", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Kanjia Lake boating", "distance": "0.5 km"}]},

    # Assam
    {"name": "Guwahati Brahmaputra Riverfront Park", "state": "Assam", "city": "Guwahati", "category": "Hill Stations", "description": "Scenic walk paths along the Brahmaputra River in Guwahati.", "best_months": "October, November, December", "latitude": 26.1884, "longitude": 91.7432, "entry_fee": 20.0, "timings": "9:00 AM - 7:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Umananda Island Temple", "distance": "1 km (by boat)"}]},
    {"name": "Kamakhya Nilachal Hill Trail", "state": "Assam", "city": "Guwahati", "category": "Spiritual", "description": "Hill road and walking tracks leading up to Kamakhya temple.", "best_months": "October, November, December", "latitude": 26.1650, "longitude": 91.7050, "entry_fee": 0.0, "timings": "24 Hours open", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Kamakhya Temple Shrine", "distance": "0.1 km"}]},
    {"name": "Pobitora Wildlife Sanctuary Trail", "state": "Assam", "city": "Morigaon", "category": "Wildlife", "description": "Dense grass sanctuary boasting the highest density of one-horned rhinos.", "best_months": "November, December, January, February", "latitude": 26.2497, "longitude": 92.0512, "entry_fee": 100.0, "timings": "7:30 AM - 3:00 PM", "budget_category": "Mid-range", "is_trending": False, "attractions": [{"name": "Brahmaputra River Shore", "distance": "5 km"}]},
    {"name": "Tezpur Agnigarh Hill Park", "state": "Assam", "city": "Tezpur", "category": "Heritage", "description": "Clifftop park associated with mythological romance stories, offering river views.", "best_months": "October, November, December", "latitude": 26.6232, "longitude": 92.8058, "entry_fee": 20.0, "timings": "9:00 AM - 6:00 PM", "budget_category": "Budget", "is_trending": False, "attractions": [{"name": "Bhairabi Temple", "distance": "2 km"}]}
]

# Combine datasets
all_destinations = destinations_data + extra_destinations

def main():
    db = SessionLocal()
    try:
        # Load categories mapping
        categories = db.query(Category).all()
        categories_map = {cat.name: cat.id for cat in categories}

        if not categories_map:
            print("Error: No categories found in database. Seed categories first.")
            return

        # Fetch existing destination names to avoid duplicates
        existing_dests = db.query(Destination).all()
        existing_names = {dest.name.lower().strip() for dest in existing_dests}

        inserted_count = 0
        skipped_count = 0

        for dest in all_destinations:
            name_lower = dest["name"].lower().strip()
            if name_lower in existing_names:
                skipped_count += 1
                continue

            # Get category ID
            category_name = dest["category"]
            if category_name not in categories_map:
                continue
            category_id = categories_map[category_name]

            # Select random images from category list
            imgs = category_images.get(category_name, [])
            selected_images = ",".join(random.sample(imgs, min(len(imgs), 2)))

            # Format nearby attractions
            nearby_attractions_formatted = []
            for attr in dest.get("attractions", []):
                nearby_attractions_formatted.append({
                    "name": attr["name"],
                    "distance": attr["distance"],
                    "description": f"A notable place located {attr['distance']} away from {dest['name']}."
                })

            # Generate nearby services data shifted slightly from coordinate
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

            # Construct Destination model instance
            db_destination = Destination(
                category_id=category_id,
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
            existing_names.add(name_lower)
            inserted_count += 1

        db.commit()
        print(f"Number of new destinations inserted: {inserted_count}")
        print(f"Duplicate destinations skipped: {skipped_count}")

    finally:
        db.close()

if __name__ == "__main__":
    main()
