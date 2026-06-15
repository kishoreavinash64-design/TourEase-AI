from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas, auth, ai

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])

@router.post("", response_model=schemas.ChatResponse)
async def chat_with_bot(
    chat_in: schemas.ChatMessageRequest,
    lang: str = Query("en", description="Preferred language (en or hi)"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Retrieve last 10 chat history items for context
    history_items = db.query(models.ChatHistory).filter(
        models.ChatHistory.user_id == current_user.id
    ).order_by(models.ChatHistory.created_at.asc()).all()
    
    # Format for Gemini context
    history_context = [
        {"sender": item.sender, "message": item.message}
        for item in history_items[-10:]
    ]
    
    # Get reply from Gemini / Fallback
    try:
        reply = await ai.get_chatbot_reply_ai(
            user_message=chat_in.message,
            chat_history=history_context,
            language=lang
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate AI reply: {str(e)}"
        )
        
    # Save User message
    user_msg = models.ChatHistory(
        user_id=current_user.id,
        sender="user",
        message=chat_in.message
    )
    db.add(user_msg)
    
    # Save AI message
    ai_msg = models.ChatHistory(
        user_id=current_user.id,
        sender="ai",
        message=reply
    )
    db.add(ai_msg)
    db.commit()
    
    # Return reply and updated history
    updated_history = db.query(models.ChatHistory).filter(
        models.ChatHistory.user_id == current_user.id
    ).order_by(models.ChatHistory.created_at.asc()).all()
    
    return {
        "reply": reply,
        "history": updated_history
    }

@router.get("/history", response_model=List[schemas.ChatHistoryResponse])
def get_chat_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    history = db.query(models.ChatHistory).filter(
        models.ChatHistory.user_id == current_user.id
    ).order_by(models.ChatHistory.created_at.asc()).all()
    return history

@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
def clear_chat_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db.query(models.ChatHistory).filter(models.ChatHistory.user_id == current_user.id).delete()
    db.commit()
    return None
