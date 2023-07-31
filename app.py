from fastapi import FastAPI
from router.register_keywords import router
from manager import firebase_manager
from router.streaming import ws_router

app = FastAPI()

app.include_router(ws_router)
app.include_router(router)