from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/destinations", tags=["Destinations"])

@router.get("/categories", response_model=List[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

@router.get("", response_model=List[schemas.DestinationResponse])
def get_destinations(
    state: Optional[str] = Query(None, description="Filter by state name"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    budget: Optional[str] = Query(None, description="Filter by budget (Budget, Mid-range, Luxury)"),
    season: Optional[str] = Query(None, description="Filter by month/season (e.g. October)"),
    search: Optional[str] = Query(None, description="Search keyword in name or description"),
    trending: Optional[bool] = Query(None, description="Filter by trending status"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Destination)
    
    if state:
        query = query.filter(models.Destination.state.ilike(f"%{state}%"))
    if category_id:
        query = query.filter(models.Destination.category_id == category_id)
    if budget:
        query = query.filter(models.Destination.budget_category == budget)
    if season:
        query = query.filter(models.Destination.best_months.ilike(f"%{season}%"))
    if search:
        query = query.filter(
            models.Destination.name.ilike(f"%{search}%") | 
            models.Destination.description.ilike(f"%{search}%")
        )
    if trending is not None:
        query = query.filter(models.Destination.is_trending == trending)
        
    destinations = query.all()
    
    # Calculate average rating for each destination
    response_data = []
    for dest in destinations:
        # Calculate average rating
        avg_rating_query = db.query(func.avg(models.Review.rating)).filter(
            models.Review.destination_id == dest.id
        ).scalar()
        
        avg_rating = round(float(avg_rating_query), 1) if avg_rating_query else 0.0
        
        # Build the schema response manually or set the dynamic attribute
        dest.rating = avg_rating
        response_data.append(dest)
        
    return response_data

@router.get("/{dest_id}", response_model=schemas.DestinationResponse)
def get_destination_by_id(dest_id: int, db: Session = Depends(get_db)):
    dest = db.query(models.Destination).filter(models.Destination.id == dest_id).first()
    if not dest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
        
    # Calculate average rating
    avg_rating_query = db.query(func.avg(models.Review.rating)).filter(
        models.Review.destination_id == dest.id
    ).scalar()
    
    dest.rating = round(float(avg_rating_query), 1) if avg_rating_query else 0.0
    return dest
