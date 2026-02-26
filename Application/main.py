from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from Application.APIs.routers import router

app = FastAPI()

app.mount("/static", StaticFiles(directory="Application/Static"), name="static")

app.include_router(router)