from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from Application.APIs.routers import api_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="Application/Static"), name="static")


app.include_router(api_router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "CleverCookin API is running"}
