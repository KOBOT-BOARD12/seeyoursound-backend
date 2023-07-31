from fastapi import APIRouter, HTTPException
from manager.firebase_manager import firestore, db
from firebase_admin.firestore import ArrayUnion
from pydantic import BaseModel
import re

router = APIRouter()

class UserData(BaseModel):
    user_inherent_id: str
    user_new_keyword: str

def validate_user_data(user_data: UserData):
    if not user_data.user_new_keyword:
        raise HTTPException(status_code=400, detail="키워드를 입력해 주세요.")
    if len(user_data.user_new_keyword) > 5:
        raise HTTPException(status_code=400, detail="키워드는 다섯 글자 이하로 입력해 주셔야 합니다.")
    if not re.match(r'^[가-힣]+$', user_data.user_new_keyword):
        raise HTTPException(status_code=400, detail="키워드는 한글로만 입력이 가능합니다.")

@router.post("/receive_data")
async def receive_data(user_data: UserData):
        validate_user_data(user_data)
        keywords_ref = db.collection("Users").document(user_data.user_inherent_id)
        doc = keywords_ref.get()
        if doc.exists: # 사용자의 고유 아이디 컬렉션이 존재하는 경우
            existing_keywords = doc.to_dict().get("keywords", []) # 사용자의 고유 아이디 컬렉션에서 이미 존재하고 있는 키워드 가져오기

            if user_data.user_new_keyword in existing_keywords:
                raise HTTPException(status_code=400, detail="이미 존재하는 키워드입니다.")

            if len(existing_keywords) >= 5:
                raise HTTPException(status_code=400, detail="키워드는 최대 다섯 개까지만 추가할 수 있습니다.")

            keywords_ref.update({
                "keywords": firestore.ArrayUnion([user_data.user_new_keyword])
            })
        else:
            keywords_ref.set({
                "keywords": [user_data.user_new_keyword]
            })
        return {"message": "키워드가 성공적으로 추가되었습니다."}