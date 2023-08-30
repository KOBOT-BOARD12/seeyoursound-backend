from fastapi import FastAPI
from manager import firebase_manager
from router.websocket import ws_router
from router.keyword_router import keyword_router
from router.model_router import upload_model_router
from router.class_router import class_router, return_class_router

app = FastAPI()

app.include_router(ws_router)
app.include_router(keyword_router)
app.include_router(upload_model_router)
app.include_router(class_router)
app.include_router(return_class_router)