import httpx
from app.utils.constants import HTTPMethods, JSONType
from typing import Optional, Dict, Type, TypeVar
from pydantic import BaseModel


# For Generic Type
T = TypeVar("T", bound=BaseModel)


# HTTP Client for Reusability
class HTTPClient:

    async def request(
        self,
        url: str,
        method: HTTPMethods,
        headers: dict = None,
        params: dict = None,
        json: JSONType = None,
        content: str = None,
        response_model: Optional[Type[T]] = None,
    ):
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers or {},
                params=params or {},
                json=json,
                content=content,
            )

        # Raise HTTP errors FIRST so callers get a clean exception
        response.raise_for_status()

        # Parse JSON — gracefully handle empty or non-JSON bodies
        try:
            data = response.json()
        except Exception:
            data = {}

        if response_model is None:
            return data

        return response_model.model_validate(data)