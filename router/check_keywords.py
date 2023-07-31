from fastapi import APIRouter
from manager.firebase_manager import firestore, db
from pydantic import BaseModel

exi_router = APIRouter()

class UserData(BaseModel):
    user_inherent_id: str
@exi_router.post("/return_keyword")
async def return_keyword(user_data: UserData):
    user_ref = db.collection("Users").document(user_data.user_inherent_id)
    doc = user_ref.get()
    if doc.exists:
        existing_keywords = doc.to_dict().get("keywords", [])
        return existing_keywords
    else:
        return "등록돼 있지 않은 사용자입니다."