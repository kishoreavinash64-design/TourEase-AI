from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/api/emergency", tags=["Emergency Contacts"])

@router.get("", response_model=List[schemas.EmergencyContactResponse])
def get_all_emergency_contacts(db: Session = Depends(get_db)):
    return db.query(models.EmergencyContact).all()

@router.get("/{state}", response_model=schemas.EmergencyContactResponse)
def get_emergency_contacts_by_state(state: str, db: Session = Depends(get_db)):
    contact = db.query(models.EmergencyContact).filter(
        models.EmergencyContact.state.ilike(state)
    ).first()
    
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Emergency contacts for state '{state}' not found."
        )
    return contact
