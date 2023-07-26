from fastapi import FastAPI
from router.streaming import ws_router

app = FastAPI()

app.include_router(ws_router)
