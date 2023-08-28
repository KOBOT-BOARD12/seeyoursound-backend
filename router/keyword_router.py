from fastapi import APIRouter, HTTPException
from manager.firebase_manager import firestore, db
from firebase_admin.firestore import ArrayUnion
from pydantic import BaseModel
from phonemizer import phonemize
import re

keyword_router = APIRouter()

def convert_to_ipa(korean_text):
    ipa_text = phonemize(korean_text, language="ko", backend="espeak")
    return ipa_text

class Register(BaseModel):
    user_id: str
    keyword: str

class ReturnKeyword(BaseModel):
    user_id: str

class DeleteKeyword(BaseModel):
    user_id: str
    keyword: str

def validate_keyword(keyword: str):
    if not keyword:
        raise HTTPException(status_code=400, detail="키워드를 입력해 주세요.")
    if len(keyword) > 5:
        raise HTTPException(status_code=400, detail="키워드는 다섯 글자 이하로 입력해 주셔야 합니다.")
    if not re.match(r'^[가-힣]+$', keyword):
        raise HTTPException(status_code=400, detail="키워드는 한글로만 입력이 가능합니다.")

@keyword_router.post("/register_keyword")
async def receive_data(data: Register):
    validate_keyword(data.keyword)
    user_id = data.user_id
    keyword = data.keyword
    keywords_ref = db.collection("Users").document(user_id)
    doc = keywords_ref.get()
    if doc.exists:
        existing_keywords = doc.to_dict().get("keywords", {})
        if keyword in existing_keywords:
            raise HTTPException(status_code=400, detail="이미 존재하는 키워드입니다.")
        if len(existing_keywords) >= 3:
            raise HTTPException(status_code=400, detail="키워드는 최대 세 개까지만 추가할 수 있습니다.")
    else:
        existing_keywords = {}
    ipa_of_keyword = convert_to_ipa(keyword).replace(' ', '')
    existing_keywords[keyword] = ipa_of_keyword
    keywords_ref.set({
        "keywords": existing_keywords
    })
    return {"message": "키워드가 성공적으로 추가되었습니다."}

@keyword_router.post("/return_keyword")
async def return_keyword(data: ReturnKeyword):
    user_id = data.user_id
    user_ref = db.collection("Users").document(user_id)
    doc = user_ref.get()
    if doc.exists:
        existing_keywords = doc.to_dict().get("keywords", [])
        return {"keywords": list(existing_keywords.keys())}
    else:
        raise HTTPException(status_code=400, detail="등록돼 있지 않은 사용자입니다.")

@keyword_router.post("/delete_keyword")
async def delete_data(data: DeleteKeyword):
    user_id = data.user_id
    keyword = data.keyword
    user_ref = db.collection("Users").document(user_id)
    doc = user_ref.get()
    if doc.exists:
        existing_keywords = doc.to_dict().get("keywords", [])
        if keyword in existing_keywords:
            existing_keywords.pop(keyword)
            user_ref.update({"keywords": existing_keywords})
            raise HTTPException(status_code=200, detail="해당 키워드를 성공적으로 삭제하였습니다.")
        else:
            raise HTTPException(status_code=400, detail="사용자 키워드 리스트에 존재하지 않는 키워드입니다.")
    else:
        raise HTTPException(status_code=400, detail="등록돼 있지 않은 사용자입니다.")
