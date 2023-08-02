from fastapi import FastAPI
from manager import firebase_manager
from router.streaming import ws_router
from router.keyword_router import register_keyword_router, existing_keyword_router, delete_keywords_router
from router.model_router import upload_model_router

app = FastAPI()

app.include_router(ws_router)
app.include_router(register_keyword_router)
app.include_router(existing_keyword_router)
app.include_router(delete_keywords_router)
app.include_router(upload_model_router)