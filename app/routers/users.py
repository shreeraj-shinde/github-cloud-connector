from fastapi import APIRouter, Depends
from app.services.github_service import GitHubService
from app.dependencies.git_middleware import get_github_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_authenticated_user(service: GitHubService = Depends(get_github_service)):
    return await service.get_user()