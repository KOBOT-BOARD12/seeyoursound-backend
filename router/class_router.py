from fastapi import APIRouter, HTTPException
from manager.firebase_manager import db
from pydantic import BaseModel
from typing import Dict

class_router = APIRouter()


class ClassData(BaseModel):
    user_id: str
    sound_class: Dict[int, bool]


class ReturnData(BaseModel):
    user_id: str


@class_router.post("/update_class")
async def update_class(data: ClassData):
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


@class_router.post("/return_class")
async def return_class(data: ReturnData):
    user_id = data.user_id
    user_doc_ref = db.collection("Users").document(user_id)
    user_info = user_doc_ref.get()

    if user_info.exists and user_info.to_dict().get("current_class"):
        existing_current_class = user_info.to_dict()["current_class"]
        return existing_current_class
    else:
        initial_value = {str(key): True for key in range(5)}
        existing_data = user_info.to_dict() if user_info.exists else {}
        existing_data["current_class"] = initial_value
        user_doc_ref.set(existing_data)
        return initial_value
