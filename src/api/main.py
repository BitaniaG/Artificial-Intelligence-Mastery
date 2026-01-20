from fastapi import FastAPI
from src.api.routers import channels, messages, images

app = FastAPI(
    title="Medical Telegram Analytics API",
    version="1.0.0"
)

app.include_router(channels.router)
app.include_router(messages.router)
app.include_router(images.router)

@app.get("/")
def root():
    return {"status": "API is running"}
