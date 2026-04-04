from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.schemas.health import HealthResponse
from app.routers.users import router as user_router
from app.routers.auth import router as auth_router
from app.routers.repos import router as repo_router
from app.routers.issues import router as issues_router
from app.routers.pull_requests import router as pr_router

settings = get_settings()

app = FastAPI(
    title="GitHub Cloud Connector",
    description="A connector to the GitHub API with OAuth 2.0 authentication.",
    version="1.0.0",
)


origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")] if settings.CORS_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(repo_router)
app.include_router(issues_router)
app.include_router(pr_router)


#Health Check
@app.get("/health", response_model=HealthResponse)
def health_check():

    # Response Logic
    res = HealthResponse(
        success=True,
        status_code=200,
        message=f"Server Running at PORT {settings.PORT}"
    )

    return JSONResponse(content=res.model_dump(), status_code=200)
