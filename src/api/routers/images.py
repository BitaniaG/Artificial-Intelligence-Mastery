from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.database import get_db

router = APIRouter(prefix="/image-detections", tags=["Image Detections"])

@router.get("/")
def get_detections(db: Session = Depends(get_db)):
    query = """
        SELECT *
        FROM public_marts.fct_image_detections
        ORDER BY confidence DESC
    """
    return db.execute(query).mappings().all()
