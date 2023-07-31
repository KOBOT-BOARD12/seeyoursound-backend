from fastapi import FastAPI
from router.streaming import ws_router
from router.check_keywords import existing_keyword_router

app = FastAPI()

app.include_router(ws_router)
app.include_router(existing_keyword_router)