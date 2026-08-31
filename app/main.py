from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.submissions import router as submissions_router
from app.core.database import engine, Base
from app.core.limiter import limiter

app = FastAPI(
    title="Embeddable Widget Platform API",
    version="1.0.0",
    description="Backend engine for widget configuration and submission processing."
)

# Set rate limiter state and exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(submissions_router)

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "ok", "service": "Widget Platform API"}