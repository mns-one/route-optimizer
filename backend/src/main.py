from fastapi import FastAPI
from .api import register_routes

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from src.core.rate_limiter import limiter
from src.core.cache_service import redis_client

app = FastAPI()

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

