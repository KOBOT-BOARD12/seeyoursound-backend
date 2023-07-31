from fastapi import APIRouter, HTTPException
from manager.firebase_manager import firestore, db
from pydantic import BaseModel

existing_keyword_router = APIRouter()

class UserData(BaseModel):
    user_inherent_id: str
    
@existing_keyword_router.post("/return_keyword")
async def return_keyword(user_data: UserData):
    user_ref = db.collection("Users").document(user_data.user_inherent_id)
    doc = user_ref.get()
    if doc.exists:
        existing_keywords = doc.to_dict().get("keywords", [])
        return {"keywords": existing_keywords}
    else:
        raise HTTPException(status_code=400, detail="등록돼 있지 않은 사용자입니다.")
