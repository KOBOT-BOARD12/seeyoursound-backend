from fastapi import FastAPI
from manager import firebase_manager
from router.streaming import ws_router
from router.register_keywords import register_keyword_router

app = FastAPI()

app.include_router(ws_router)
app.include_router(register_keyword_router)