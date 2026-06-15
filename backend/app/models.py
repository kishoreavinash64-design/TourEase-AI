import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), default="user") # 'user' or 'admin'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    itineraries = relationship("Itinerary", back_populates="user", cascade="all, delete-orphan")
    chat_history = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    destinations = relationship("Destination", back_populates="category", cascade="all, delete-orphan")

class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(100), index=True, nullable=False)
    state = Column(String(100), index=True, nullable=False)
    city = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=False)
    images = Column(Text, nullable=True)  # Comma-separated image URLs
    entry_fee = Column(Float, default=0.0)
    timings = Column(String(100), nullable=True)
    best_months = Column(String(255), nullable=True)  # Comma-separated months, e.g. "October, November, December"
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    nearby_attractions = Column(Text, nullable=True)  # JSON formatted string
    nearby_services = Column(Text, nullable=True)  # JSON formatted string (hotels, restaurants, hospitals, transport)
    is_trending = Column(Boolean, default=False)
    budget_category = Column(String(20), default="Mid-range")  # "Budget", "Mid-range", "Luxury"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="destinations")
    favorites = relationship("Favorite", back_populates="destination", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="destination", cascade="all, delete-orphan")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="favorites")
    destination = relationship("Destination", back_populates="favorites")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1 to 5 stars
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="reviews")
    destination = relationship("Destination", back_populates="reviews")

class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination_name = Column(String(100), nullable=False)
    num_days = Column(Integer, nullable=False)
    budget = Column(Float, nullable=False)
    day_wise_details = Column(Text, nullable=False)  # JSON formatted string representing day-by-day plan
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="itineraries")

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sender = Column(String(10), nullable=False)  # "user" or "ai"
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="chat_history")

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(String(100), unique=True, index=True, nullable=False)
    police_contact = Column(String(50), default="100")
    medical_contact = Column(String(50), default="102")
    fire_contact = Column(String(50), default="101")
    disaster_management = Column(String(50), default="1078")
    tourist_helpline = Column(String(50), default="1363")
