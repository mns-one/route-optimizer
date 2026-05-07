from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from .api import register_routes
from src.core.rate_limiter import limiter
from src.core.cache_service import redis_client
from src.middleware.global_rate_limit import GlobalRateLimitMiddleware

load_dotenv()
FRONTEND_URL = os.getenv("FRONTEND_URL")
if not FRONTEND_URL:
    raise ValueError("FRONTEND_URL environment variable is not set")

origins = [
    "http://localhost:8501"
]

if FRONTEND_URL:
    origins.append(FRONTEND_URL)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GlobalRateLimitMiddleware)

register_routes(app)

@app.on_event("startup")
async def startup():
    try:
        await redis_client.ping()
        print("Redis connected")

    except Exception as e:
        print(f"Redis connection failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown():
    await redis_client.close()
    print("Redis connection closed")

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded, _rate_limit_exceeded_handler
)
app.add_middleware(SlowAPIMiddleware)

