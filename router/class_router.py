from fastapi import APIRouter, HTTPException
from manager.firebase_manager import db
from pydantic import BaseModel
from typing import Dict

class_router = APIRouter()

class ClassData(BaseModel):
    user_id: str
    sound_class: Dict[int, bool]

@class_router.post("/select_class")
async def select_class(data: ClassData):
    try:
        user_id = data.user_id
        current_class = data.sound_class

        new_class_dictionary = {str(key): value for key, value in current_class.items()}

        user_doc_ref = db.collection("Users").document(user_id)
        user_doc = user_doc_ref.get()

        if user_doc.exists:
            existing_class = user_doc.to_dict().get("current_class", {})
            existing_class.update(new_class_dictionary)
            user_doc_ref.update({"current_class": existing_class})
        else:
            user_doc_ref.set({"current_class": new_class_dictionary}) 

    except:
        raise HTTPException(status_code=400, detail="잘못된 요청이 들어왔습니다.")
