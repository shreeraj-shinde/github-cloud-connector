from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.config import settings
from app.schemas.health import HealthResponse

app = FastAPI()


@app.get("/health", response_model=HealthResponse)
def health_check():

    # Response Logic
    res = HealthResponse(
        success=True,
        status_code=200,
        message=f"Server Running at PORT {settings.PORT}"
    )
    return JSONResponse(content=res.model_dump(), status_code=200)
