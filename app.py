from fastapi import FastAPI
from manager import firebase_manager
from router.streaming import ws_router
from router.check_keywords import existing_keyword_router
from router.register_keywords import register_keyword_router
from router.model_router.upload_model import upload_model_router

app = FastAPI()

app.include_router(ws_router)
app.include_router(register_keyword_router)
app.include_router(upload_model_router)
app.include_router(existing_keyword_router)
app.include_router(register_keyword_router)