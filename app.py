from fastapi import FastAPI
from router.streaming import ws_router
from router.delete_keywords import delete_keywords_router

app = FastAPI()

app.include_router(ws_router)
app.include_router(delete_keywords_router)
