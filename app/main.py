from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .config import BASE_DIR
from .database import init_db
from .routes import router

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield

app = FastAPI(title="FitBuddy API", description="AI-powered 7-day fitness plans", version="1.0.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(router)

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}
