from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.database import get_db

router = APIRouter(prefix="/channels", tags=["Channels"])

@router.get("/")
def get_channels(db: Session = Depends(get_db)):
    query = """
        SELECT channel_pk, channel_name
        FROM public_marts.dim_channels
        ORDER BY channel_name
    """
    return db.execute(query).mappings().all()
