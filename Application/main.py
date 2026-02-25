from fastapi import FastAPI
from Application.APIs.routers import api_router

app = FastAPI(title="CleverCookin")

app.include_router(api_router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "CleverCookin API is running"}