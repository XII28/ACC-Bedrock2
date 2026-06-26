from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Favorite
from routers.fridge import get_current_user_id

router = APIRouter()

class FavoriteRequest(BaseModel):
    recipe_id: str
    recipe_name: str
    recipe_image: str = ""

@router.get("")
def get_favorites(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()

@router.post("")
def add_favorite(req: FavoriteRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    favorite = Favorite(user_id=user_id, **req.dict())
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite

@router.delete("/{favorite_id}")
def delete_favorite(favorite_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    item = db.query(Favorite).filter(Favorite.id == favorite_id, Favorite.user_id == user_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="즐겨찾기를 찾을 수 없습니다.")
    db.delete(item)
    db.commit()
    return {"ok": True}