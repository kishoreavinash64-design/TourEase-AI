# TourEase AI - Smart Tourism Information System

TourEase AI is a single-platform Smart Tourism Information System built for the **Smart India Hackathon (SIH)**. The platform enables travelers to discover places, view local amenities (hotels, restaurants, hospitals, and transit hubs) on interactive Leaflet maps, generate custom travel itineraries using Gemini 1.5, chat with a travel chatbot, and manage their trips. Secured admin panels offer stats, destination editing, and downloadable CSV reports.

---

## 🌟 Key Features
- **Smart Place Discovery**: Search and filter places by State, Category, Budget, and Season.
- **Interactive OpenStreetMap**: Render color-coded Leaflet pins for local services (hospitals, hotels, etc.) with SVG route paths.
- **AI Itinerary Planner**: Connects to Google Gemini 1.5 to draft daily plans and accommodations within a custom budget.
- **AI Travel Assistant Chatbot**: Interactive chatbot answering travel guidelines, customs, and safety questions.
- **Emergency Helpline Directory**: View toll-free national services or filter state-specific emergency numbers.
- **Admin Analytics & Management**: Dashboards listing database records, CRUD forms, and downloadable CSV logs of users, reviews, and places.
- **Multi-Language Support**: Switch the entire UI seamlessly between English and Hindi.
- **Dark Mode Support**: Sleek, eye-friendly travel dashboard theme.

---

## 📁 System Architecture & Folder Layout

```
C:/subash/
├── backend/
│   ├── app/
│   │   ├── config.py         # Config reader using Pydantic Settings
│   │   ├── database.py       # SQL database session generator
│   │   ├── models.py         # 8 SQLAlchemy Database models
│   │   ├── schemas.py        # Pydantic v2 validation models
│   │   ├── auth.py           # password hashing & JWT security layers
│   │   ├── ai.py             # Gemini API Integration + fallback mocks
│   │   ├── seed.py           # Idempotent DB seeder
│   │   └── routers/          # Modular API routers
│   ├── .env.example
│   └── requirements.txt
└── frontend/                 # React client built on Vite & Tailwind
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── index.html
    └── src/
        ├── context/          # Auth, Theme, and Language context states
        ├── components/       # Custom MapComponent, Nav, and Footer
        └── pages/            # Page layouts (Dashboard, Explore, Admin, details...)
```

---

## 🚀 Local Setup Instructions

### 1. Backend Server Setup
Ensure Python 3.10+ is installed on your computer.

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
# Activate virtual environment (Windows)
venv\Scripts\activate
# Activate virtual environment (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
copy .env.example .env
```

Open the created `.env` file. To enable live Gemini AI integration, insert your Google Gemini API Key:
```env
DATABASE_URL=sqlite:///./tourease.db
SECRET_KEY=localdevsecretkeyforfastapijwttokenauthentication123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```
*Note: If no Gemini key is provided, the application will automatically fall back to intelligent pre-constructed mock responses so that the planner and chatbot work seamlessly!*

```bash
# Seed the database with default destinations, emergency contacts, and test credentials
python app/seed.py

# Start the FastAPI web server
uvicorn app.main:app --reload
```
The backend server runs at **`http://localhost:8000`**. You can visit **`http://localhost:8000/docs`** to view the interactive Swagger API documentation.

### 2. Frontend React Setup
Ensure Node.js 18+ is installed.

```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install Node dependencies
npm install

# Start the client development server
npm run dev
```
The React frontend client will start at **`http://localhost:5173`**.

---

## 🔑 Test Accounts & Logins
Seeding the database creates two test profiles with default data:

### Standard Tourist Account
- **Email**: `user@tourease.com`
- **Password**: `UserPassword123`
- **Privileges**: Create AI plans, chat, save favorites, write reviews.

### Administrative Control Account
- **Email**: `admin@tourease.com`
- **Password**: `AdminPassword123`
- **Privileges**: Full access, CRUD operations, delete reviews, download CSV stats.

---

## ☁️ Deployment Guide

### Database (Neon PostgreSQL)
1. Sign up at [Neon.tech](https://neon.tech) and create a free PostgreSQL database.
2. Copy the database connection string (URI).
3. Replace the local `DATABASE_URL` in your `.env` settings:
   `DATABASE_URL=postgresql://user:password@endpoint-pooler.neon.tech/neondb?sslmode=require`

### Backend Server (Railway or Render)
1. Link your GitHub repository to Railway or Render.
2. Set the root directory to `backend`.
3. Add the following environment variables:
   - `DATABASE_URL` (your Neon PostgreSQL URL)
   - `SECRET_KEY` (a secure random string)
   - `GEMINI_API_KEY` (your Google Gemini API key)
4. Set the build command to: `pip install -r requirements.txt`
5. Set the start command to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend Client (Vercel)
1. Install the Vercel CLI or connect your Git repo on Vercel's dashboard.
2. Choose **Vite** as the framework template.
3. Set the root directory to `frontend`.
4. Leave build/install commands as default.
5. In `frontend/src/context/AuthContext.jsx`, ensure the default Axios base URL points to your deployed backend URL:
   `axios.defaults.baseURL = 'https://your-backend-url.railway.app';`
6. Deploy the client!
