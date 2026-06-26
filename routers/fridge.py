from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import FridgeItem
from routers.auth import JWT_SECRET
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        return int(payload["sub"])
    except JWTError:
        raise HTTPException(status_code=401, detail="인증이 필요합니다.")

class FridgeItemRequest(BaseModel):
    name: str
    quantity: float = 0
    unit: str = ""
    category: str = ""
    expiry_date: str = ""

@router.get("")
def get_fridge(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return db.query(FridgeItem).filter(FridgeItem.user_id == user_id).all()

@router.post("")
def add_item(req: FridgeItemRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    item = FridgeItem(user_id=user_id, **req.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}")
def delete_item(item_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    item = db.query(FridgeItem).filter(FridgeItem.id == item_id, FridgeItem.user_id == user_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="항목을 찾을 수 없습니다.")
    db.delete(item)
    db.commit()
    return {"ok": True}