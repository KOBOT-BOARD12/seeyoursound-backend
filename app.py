from fastapi import FastAPI
from router.register_keywords import ws_router
from manager import firebase_manager

app = FastAPI()

app.include_router(ws_router)

@app.get("/")
def read_root():
   return {"Hello": "World"}