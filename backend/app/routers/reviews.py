from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/api/reviews", tags=["Reviews & Feedback"])

@router.post("", response_model=schemas.ReviewResponse)
def create_or_update_review(
    review_in: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Check if destination exists
    destination = db.query(models.Destination).filter(models.Destination.id == review_in.destination_id).first()
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
        
    # Check if already reviewed - if so, update
    existing = db.query(models.Review).filter(
        models.Review.user_id == current_user.id,
        models.Review.destination_id == review_in.destination_id
    ).first()
    
    if existing:
        existing.rating = review_in.rating
        existing.comment = review_in.comment
        db.commit()
        db.refresh(existing)
        review = existing
    else:
        # Create new review
        review = models.Review(
            user_id=current_user.id,
            destination_id=review_in.destination_id,
            rating=review_in.rating,
            comment=review_in.comment
        )
        db.add(review)
        db.commit()
        db.refresh(review)
        
    # Populate user name for response schema
    review.user_name = current_user.full_name
    return review

@router.get("/destination/{dest_id}", response_model=List[schemas.ReviewResponse])
def get_destination_reviews(dest_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(
        models.Review.destination_id == dest_id
    ).order_by(models.Review.created_at.desc()).all()
    
    # Populate user name for each review
    for review in reviews:
        review.user_name = review.user.full_name if review.user else "Anonymous"
        
    return reviews
