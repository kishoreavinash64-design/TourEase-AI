from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/api/favorites", tags=["Favorites"])

@router.post("/toggle", response_model=Dict[str, bool])
def toggle_favorite(
    fav_in: schemas.FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Check if destination exists
    destination = db.query(models.Destination).filter(models.Destination.id == fav_in.destination_id).first()
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found"
        )
        
    # Check if already favorited
    existing = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id,
        models.Favorite.destination_id == fav_in.destination_id
    ).first()
    
    if existing:
        # Remove it
        db.delete(existing)
        db.commit()
        return {"favorited": False}
    else:
        # Add it
        new_fav = models.Favorite(
            user_id=current_user.id,
            destination_id=fav_in.destination_id
        )
        db.add(new_fav)
        db.commit()
        return {"favorited": True}

@router.get("", response_model=List[schemas.FavoriteResponse])
def get_my_favorites(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    favorites = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.id
    ).all()
    return favorites
