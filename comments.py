from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Comment
from schemas import CommentCreate, CommentOut
from auth import get_current_user
from models import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{ad_id}/comments")
def add_comment(ad_id: int, comment: CommentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_comment = Comment(content=comment.content, ad_id=ad_id, author_id=user.id)
    db.add(db_comment)
    db.commit()
    return {"status": "added"}

@router.get("/{ad_id}/comments", response_model=dict)
def get_comments(ad_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.ad_id == ad_id).all()
    return {"comments": [CommentOut.from_orm(c) for c in comments]}

@router.patch("/{ad_id}/comments/{comment_id}")
def update_comment(ad_id: int, comment_id: int, comment: CommentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_comment = db.query(Comment).filter(Comment.id == comment_id, Comment.author_id == user.id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db_comment.content = comment.content
    db.commit()
    return {"status": "updated"}

@router.delete("/{ad_id}/comments/{comment_id}")
def delete_comment(ad_id: int, comment_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_comment = db.query(Comment).filter(Comment.id == comment_id, Comment.author_id == user.id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(db_comment)
    db.commit()
    return {"status": "deleted"}
