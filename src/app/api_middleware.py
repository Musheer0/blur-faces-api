from fastapi import Header, HTTPException
import os


async def apiMiddleware(
    x_api_key: str | None = Header(default=None)
):
    expected_key = os.environ.get("API_KEY")

    if x_api_key != expected_key:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )