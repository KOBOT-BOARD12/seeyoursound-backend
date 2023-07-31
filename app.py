from fastapi import FastAPI
from router.streaming import ws_router
from router.check_keywords import exi_router

app = FastAPI()

app.include_router(ws_router)
app.include_router(exi_router)
