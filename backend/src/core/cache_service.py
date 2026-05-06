import os
import json
from dotenv import load_dotenv
from redis.asyncio import Redis

load_dotenv()
HOST = os.getenv("REDIS_HOST", "localhost")
PORT = int(os.getenv("REDIS_PORT", 6379))
if not HOST or PORT:
    raise ValueError("REDIS environment variable not set")

CACHE_TTL = 86400

redis_client = Redis(
    host=HOST,
    port=PORT,
    decode_responses=True
)

def cache_key(query: str) -> str:
    normalized = query.strip().lower()
    return f"search_place:{normalized}"

async def get_cache(query: str):
    key = cache_key(query)
    cached = await redis_client.getex(key, ex=CACHE_TTL)
    if cached:
        payload = json.loads(cached)
        return payload
    return None

async def set_cache(query:str, result):
    key = cache_key(query)
    if isinstance(result, list):
        serializable = []
        for item in result:
            if hasattr(item, "model_dump"):
                serializable.append(item.model_dump())
            else:
                serializable.append(item)
    elif hasattr(result, "model_dump"):
        serializable = result.model_dump()
    else:
        serializable = result

    await redis_client.set(key, json.dumps(serializable), ex=CACHE_TTL)

