from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from Application.APIs.routers import api_router
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from Application.Database.base import Base
from Application.Database.session import engine_write
from Application.APIs.users import router as users_router

Base.metadata.create_all(bind=engine_write)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="Application/Static"), name="static")

templates = Jinja2Templates(directory="Application/Templates")

app.include_router(api_router)
app.include_router(users_router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})