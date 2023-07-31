from fastapi import APIRouter, File, UploadFile, Form
from manager.firebase_manager import storage, bucket
from pydantic import BaseModel
from os.path import os

upload_model_router = APIRouter()

class Data(BaseModel):
    user_inherent_id: str

@upload_model_router.post("/upload_model")
async def upload_model(user_inherent_id: str = Form(...), keyword_modeling: UploadFile = File(...)):
    content = await keyword_modeling.read()
    
    object_name = f"{user_inherent_id}"
    
    bucket_name = os.getenv("STORAGE_BUCKET_URL")
    bucket = storage.bucket(bucket_name)
    
    blob = bucket.blob(object_name)
    blob.upload_from_string(content, content_type="application/json")