from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Ad, Comment
from schemas import AdCreate, AdOut
from auth import get_current_user
from models import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict)
def create_ad(ad: AdCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_ad = Ad(**ad.dict(), user_id=user.id)
    db.add(new_ad)
    db.commit()
    db.refresh(new_ad)
    return {"id": new_ad.id}

@router.get("/{ad_id}", response_model=AdOut)
def get_ad(ad_id: int, db: Session = Depends(get_db)):
    ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    total_comments = db.query(Comment).filter(Comment.ad_id == ad.id).count()
    ad_data = AdOut.from_orm(ad)
    ad_data.total_comments = total_comments
    return ad_data

@router.patch("/{ad_id}")
def update_ad(ad_id: int, ad_data: AdCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ad = db.query(Ad).filter(Ad.id == ad_id, Ad.user_id == user.id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    for attr, value in ad_data.dict().items():
        setattr(ad, attr, value)
    db.commit()
    return {"status": "updated"}

@router.delete("/{ad_id}")
def delete_ad(ad_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ad = db.query(Ad).filter(Ad.id == ad_id, Ad.user_id == user.id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    db.delete(ad)
    db.commit()
    return {"status": "deleted"}
