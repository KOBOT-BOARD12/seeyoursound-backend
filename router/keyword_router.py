from fastapi import APIRouter, HTTPException, Form
from manager.firebase_manager import firestore, db
from firebase_admin.firestore import ArrayUnion
from pydantic import BaseModel
import re

register_keyword_router = APIRouter()
existing_keyword_router = APIRouter()
delete_keywords_router = APIRouter()

def validate_user_data(user_inherent_id: str = Form(...), user_new_keyword: str = Form(...)):
    if not user_new_keyword:
        raise HTTPException(status_code=400, detail="키워드를 입력해 주세요.")
    if len(user_new_keyword) > 5:
        raise HTTPException(status_code=400, detail="키워드는 다섯 글자 이하로 입력해 주셔야 합니다.")
    if not re.match(r'^[가-힣]+$', user_new_keyword):
        raise HTTPException(status_code=400, detail="키워드는 한글로만 입력이 가능합니다.")

@register_keyword_router.post("/receive_data")
async def receive_data(user_inherent_id: str = Form(...), user_new_keyword: str = Form(...)):
        validate_user_data(user_inherent_id, user_new_keyword)
        keywords_ref = db.collection("Users").document(user_inherent_id)
        doc = keywords_ref.get()
        if doc.exists:
            existing_keywords = doc.to_dict().get("keywords", [])
            if user_new_keyword in existing_keywords:
                raise HTTPException(status_code=400, detail="이미 존재하는 키워드입니다.")

            if len(existing_keywords) >= 5:
                raise HTTPException(status_code=400, detail="키워드는 최대 다섯 개까지만 추가할 수 있습니다.")

            keywords_ref.update({
                "keywords": firestore.ArrayUnion([user_new_keyword])
            })
        else:
            keywords_ref.set({
                "keywords": [user_new_keyword]
            })
        return {"message": "키워드가 성공적으로 추가되었습니다."}

@existing_keyword_router.post("/return_keyword")
async def return_keyword(user_inherent_id: str = Form(...)):
    user_ref = db.collection("Users").document(user_inherent_id)
    doc = user_ref.get()
    if doc.exists:
        existing_keywords = doc.to_dict().get("keywords", [])
        return {"keywords": existing_keywords}
    else:
        raise HTTPException(status_code=400, detail="등록돼 있지 않은 사용자입니다.")


@delete_keywords_router.post("/delete_data")
async def delete_data(user_inherent_id: str = Form(...), user_deleting_keyword: str = Form(...)):
    user_ref = db.collection("Users").document(user_inherent_id)
    doc = user_ref.get()
    if doc.exists:
        existing_keywords = doc.to_dict().get("keywords", [])
        if user_deleting_keyword in existing_keywords:
            existing_keywords.remove(user_deleting_keyword)
            user_ref.update({"keywords": existing_keywords})
            raise HTTPException(status_code=200, detail="해당 키워드를 성공적으로 삭제하였습니다.")
        else:
            raise HTTPException(status_code=400, detail="사용자 키워드 리스트에 존재하지 않는 키워드입니다.")
    else:
        raise HTTPException(status_code=400, detail="등록돼 있지 않은 사용자입니다.")