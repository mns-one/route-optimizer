from fastapi import FastAPI
from .api import register_routes
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

