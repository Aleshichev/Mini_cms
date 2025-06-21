from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}