from fastapi import APIRouter, HTTPException
from manager.firebase_manager import firestore, db
from pydantic import BaseModel

delete_keywords_router = APIRouter()

class UserData(BaseModel):
    user_inherent_id: str
    user_deleting_keyword: str

@delete_keywords_router.post("/delete_data")
async def delete_data(user_data: UserData):
    user_ref = db.collection("Users").document(user_data.user_inherent_id)
    doc = user_ref.get()
    if doc.exists:
        existing_keywords = doc.to_dict().get("keywords", [])
        if user_data.user_deleting_keyword in existing_keywords:
            existing_keywords.remove(user_data.user_deleting_keyword)
            user_ref.update({"keywords": existing_keywords})
            raise HTTPException(status_code=200, detail="해당 키워드를 성공적으로 삭제하였습니다.")
        else:
            raise HTTPException(status_code=400, detail="사용자 키워드 리스트에 존재하지 않는 키워드입니다.")
        exit
    else:
        raise HTTPException(status_code=400, detail="등록돼 있지 않은 사용자입니다.")