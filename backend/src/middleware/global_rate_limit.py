from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.core.cache_service import redis_client


GLOBAL_LIMIT = 50
GLOBAL_KEY = "global_api_requests"


class GlobalRateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        current = await redis_client.incr(GLOBAL_KEY)

        if current == 1:
            await redis_client.expire(
                GLOBAL_KEY,
                86400
            )

        if current > GLOBAL_LIMIT:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Global API limit exceeded"
                }
            )

        return await call_next(request)