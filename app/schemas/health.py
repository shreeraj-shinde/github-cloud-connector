from pydantic import BaseModel


class HealthResponse(BaseModel):
    success: bool
    status_code: int
    message: str