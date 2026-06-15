import json
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..database import get_db
from .. import models, schemas, auth, ai

router = APIRouter(prefix="/api/itineraries", tags=["Itineraries"])

@router.post("/generate", response_model=Dict[str, Any])
async def generate_itinerary(
    req: schemas.ItineraryGenerateRequest,
    lang: str = Query("en", description="Preferred language (en or hi)"),
    current_user: models.User = Depends(auth.get_current_user)
):
    try:
        # Call Gemini or fallback
        itinerary = await ai.generate_itinerary_ai(
            destination=req.destination_name,
            num_days=req.num_days,
            budget=req.budget,
            language=lang
        )
        return itinerary
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate itinerary: {str(e)}"
        )

@router.post("/save", response_model=schemas.ItineraryResponse)
def save_itinerary(
    itinerary_in: schemas.ItineraryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Create the itinerary in db
    new_itinerary = models.Itinerary(
        user_id=current_user.id,
        destination_name=itinerary_in.destination_name,
        num_days=itinerary_in.num_days,
        budget=itinerary_in.budget,
        day_wise_details=itinerary_in.day_wise_details
    )
    db.add(new_itinerary)
    db.commit()
    db.refresh(new_itinerary)
    return new_itinerary

@router.get("", response_model=List[schemas.ItineraryResponse])
def get_my_itineraries(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    itineraries = db.query(models.Itinerary).filter(
        models.Itinerary.user_id == current_user.id
    ).order_by(models.Itinerary.created_at.desc()).all()
    return itineraries

@router.delete("/{itinerary_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_itinerary(
    itinerary_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    itinerary = db.query(models.Itinerary).filter(
        models.Itinerary.id == itinerary_id,
        models.Itinerary.user_id == current_user.id
    ).first()
    
    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Itinerary not found in history"
        )
        
    db.delete(itinerary)
    db.commit()
    return None
