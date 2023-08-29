from fastapi import APIRouter, HTTPException
from manager.firebase_manager import db
from pydantic import BaseModel
from typing import Dict

class_router = APIRouter()

class SoundClass(BaseModel):
    class_config: Dict[int, bool]

class ClassSetting(BaseModel):
    user_id: str
    sound_class: SoundClass

@class_router.post("/select_class")
async def select_class(data: ClassSetting):
    try:
        user_id = data.user_id
        class_config = data.sound_class.class_config
        class_config_str_keys = {str(key): value for key, value in class_config.items()}
        user_doc_ref = db.collection("Users").document(user_id)
        user_doc = user_doc_ref.get()
        if user_doc.exists:
            existing_class_config = user_doc.to_dict().get("class_config", {})
            existing_class_config.update(class_config_str_keys)
            user_doc_ref.update({"class_config": existing_class_config})
        else:
            user_doc_ref.set({"class_config": class_config_str_keys})

    except Exception as e:
        print(e)