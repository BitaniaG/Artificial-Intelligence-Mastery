from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.database import get_db

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.get("/")
def get_messages(limit: int = 100, db: Session = Depends(get_db)):
    query = f"""
        SELECT message_pk, channel_pk, message_text, message_date
        FROM public_marts.fact_messages
        ORDER BY message_date DESC
        LIMIT {limit}
    """
    return db.execute(query).mappings().all()
