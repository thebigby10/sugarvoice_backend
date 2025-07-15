from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth_service.routes import router as auth_router
from glucose_tracker.routes import router as glucose_router
from core.database import init_db
from core.config import settings

app = FastAPI(title="Diabetes Tracker API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(glucose_router, prefix="/glucose", tags=["glucose"])

@app.get("/")
def read_root() ->str:
    return "Sugarvoice backend running."
