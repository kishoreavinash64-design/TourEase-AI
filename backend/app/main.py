from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from .database import engine, Base
from .routers import auth, destinations, favorites, itineraries, chat, reviews, admin, emergency

# Initialize Database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TourEase AI - Smart Tourism Information System API",
    description="Backend services for discovery, AI itinerary planning, interactive mapping, and chatbot assistant.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for Hackathon/Development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(destinations.router)
app.include_router(favorites.router)
app.include_router(itineraries.router)
app.include_router(chat.router)
app.include_router(reviews.router)
app.include_router(admin.router)
app.include_router(emergency.router)

@app.get("/", include_in_schema=False)
def root():
    # Redirect root visitors to Swagger interactive API documentation
    return RedirectResponse(url="/docs")

@app.get("/api/health", tags=["Health Check"])
def health_check():
    return {"status": "healthy", "service": "TourEase AI API", "version": "1.0.0"}
