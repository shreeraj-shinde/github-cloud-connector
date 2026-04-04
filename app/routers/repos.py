from fastapi import APIRouter, Depends
from app.services.github_service import GitHubService
from app.dependencies.git_middleware import get_github_service

router = APIRouter(prefix="/repos", tags=["Repos"])


@router.get("/")
async def list_repos(
    per_page: int = 30,
    page: int = 1,
    service: GitHubService = Depends(get_github_service),
):
    return await service.list_repos(per_page=per_page, page=page)


@router.get("/{owner}/{repo}")
async def get_repo(
    owner: str,
    repo: str,
    service: GitHubService = Depends(get_github_service),
):
    return await service.get_repo(owner=owner, repo=repo)
