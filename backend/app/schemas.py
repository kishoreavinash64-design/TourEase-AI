from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    full_name: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Category Schemas ---
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# --- Destination Schemas ---
class DestinationBase(BaseModel):
    category_id: int
    name: str
    state: str
    city: str
    description: str
    images: Optional[str] = None  # Comma-separated URLs
    entry_fee: Optional[float] = 0.0
    timings: Optional[str] = None
    best_months: Optional[str] = None  # Comma-separated
    latitude: float
    longitude: float
    nearby_attractions: Optional[str] = None  # JSON string
    nearby_services: Optional[str] = None  # JSON string
    is_trending: Optional[bool] = False
    budget_category: Optional[str] = "Mid-range"  # Budget, Mid-range, Luxury

class DestinationCreate(DestinationBase):
    pass

class DestinationUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    description: Optional[str] = None
    images: Optional[str] = None
    entry_fee: Optional[float] = None
    timings: Optional[str] = None
    best_months: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    nearby_attractions: Optional[str] = None
    nearby_services: Optional[str] = None
    is_trending: Optional[bool] = None
    budget_category: Optional[str] = None

class DestinationSimpleResponse(BaseModel):
    id: int
    name: str
    state: str
    images: Optional[str] = None

    class Config:
        from_attributes = True

class DestinationResponse(DestinationBase):
    id: int
    created_at: datetime
    category: Optional[CategoryResponse] = None
    rating: Optional[float] = 0.0

    class Config:
        from_attributes = True

# --- Favorite Schemas ---
class FavoriteCreate(BaseModel):
    destination_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    destination_id: int
    created_at: datetime
    destination: DestinationSimpleResponse

    class Config:
        from_attributes = True

# --- Review Schemas ---
class ReviewCreate(BaseModel):
    destination_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    destination_id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime
    user_name: Optional[str] = None

    class Config:
        from_attributes = True

# --- Itinerary Schemas ---
class ItineraryGenerateRequest(BaseModel):
    destination_name: str
    num_days: int = Field(..., ge=1, le=14)
    budget: float = Field(..., ge=0)

class ItineraryCreate(ItineraryGenerateRequest):
    day_wise_details: str  # JSON formatted string

class ItineraryResponse(BaseModel):
    id: int
    user_id: int
    destination_name: str
    num_days: int
    budget: float
    day_wise_details: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Chat Schemas ---
class ChatMessageRequest(BaseModel):
    message: str

class ChatHistoryResponse(BaseModel):
    id: int
    user_id: int
    sender: str  # "user" or "ai"
    message: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    reply: str
    history: List[ChatHistoryResponse]

# --- Emergency Contact Schemas ---
class EmergencyContactBase(BaseModel):
    state: str
    police_contact: str = "100"
    medical_contact: str = "102"
    fire_contact: str = "101"
    disaster_management: str = "1078"
    tourist_helpline: str = "1363"

class EmergencyContactCreate(EmergencyContactBase):
    pass

class EmergencyContactResponse(EmergencyContactBase):
    id: int

    class Config:
        from_attributes = True

# --- Admin Dashboard Stats Schema ---
class DashboardStats(BaseModel):
    total_users: int
    total_destinations: int
    total_favorites: int
    total_reviews: int
    trending_count: int
    by_category: Dict[str, int]
    by_state: Dict[str, int]
