import io
import csv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/api/admin", tags=["Admin Operations"], dependencies=[Depends(auth.get_admin_user)])

@router.get("/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_users = db.query(models.User).count()
    total_destinations = db.query(models.Destination).count()
    total_favorites = db.query(models.Favorite).count()
    total_reviews = db.query(models.Review).count()
    trending_count = db.query(models.Destination).filter(models.Destination.is_trending == True).count()
    
    # Group by category
    by_category_query = db.query(
        models.Category.name, func.count(models.Destination.id)
    ).join(models.Destination).group_by(models.Category.name).all()
    by_category = {name: count for name, count in by_category_query}
    
    # Group by state
    by_state_query = db.query(
        models.Destination.state, func.count(models.Destination.id)
    ).group_by(models.Destination.state).all()
    by_state = {state: count for state, count in by_state_query}
    
    return {
        "total_users": total_users,
        "total_destinations": total_destinations,
        "total_favorites": total_favorites,
        "total_reviews": total_reviews,
        "trending_count": trending_count,
        "by_category": by_category,
        "by_state": by_state
    }

# --- Destination CRUD ---
@router.post("/destinations", response_model=schemas.DestinationResponse, status_code=status.HTTP_201_CREATED)
def create_destination(dest_in: schemas.DestinationCreate, db: Session = Depends(get_db)):
    # Verify category exists
    category = db.query(models.Category).filter(models.Category.id == dest_in.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with ID {dest_in.category_id} does not exist."
        )
        
    destination = models.Destination(**dest_in.model_dump())
    db.add(destination)
    db.commit()
    db.refresh(destination)
    destination.rating = 0.0
    return destination

@router.put("/destinations/{dest_id}", response_model=schemas.DestinationResponse)
def update_destination(dest_id: int, dest_in: schemas.DestinationUpdate, db: Session = Depends(get_db)):
    destination = db.query(models.Destination).filter(models.Destination.id == dest_id).first()
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
        
    update_data = dest_in.model_dump(exclude_unset=True)
    
    if "category_id" in update_data:
        category = db.query(models.Category).filter(models.Category.id == update_data["category_id"]).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with ID {update_data['category_id']} does not exist."
            )
            
    for key, value in update_data.items():
        setattr(destination, key, value)
        
    db.commit()
    db.refresh(destination)
    
    # Calculate rating
    avg_rating_query = db.query(func.avg(models.Review.rating)).filter(
        models.Review.destination_id == destination.id
    ).scalar()
    destination.rating = round(float(avg_rating_query), 1) if avg_rating_query else 0.0
    return destination

@router.delete("/destinations/{dest_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_destination(dest_id: int, db: Session = Depends(get_db)):
    destination = db.query(models.Destination).filter(models.Destination.id == dest_id).first()
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
    db.delete(destination)
    db.commit()
    return None

# --- Feedback Moderation ---
@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    db.delete(review)
    db.commit()
    return None

# --- User Management ---
@router.get("/users", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.created_at.desc()).all()
    return users

# --- CSV Exports ---
@router.get("/export/users")
def export_users_csv(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Email", "Full Name", "Role", "Created At"])
    
    for u in users:
        writer.writerow([u.id, u.email, u.full_name, u.role, u.created_at])
        
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=users_report.csv"}
    )

@router.get("/export/destinations")
def export_destinations_csv(db: Session = Depends(get_db)):
    destinations = db.query(models.Destination).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Name", "State", "City", "Category ID", "Entry Fee", "Timings", 
        "Best Months", "Latitude", "Longitude", "Is Trending", "Budget Category"
    ])
    
    for d in destinations:
        writer.writerow([
            d.id, d.name, d.state, d.city, d.category_id, d.entry_fee, d.timings, 
            d.best_months, d.latitude, d.longitude, d.is_trending, d.budget_category
        ])
        
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=destinations_report.csv"}
    )

@router.get("/export/reviews")
def export_reviews_csv(db: Session = Depends(get_db)):
    reviews = db.query(models.Review).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Review ID", "User ID", "Destination ID", "Rating", "Comment", "Created At"])
    
    for r in reviews:
        writer.writerow([r.id, r.user_id, r.destination_id, r.rating, r.comment, r.created_at])
        
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=reviews_report.csv"}
    )
