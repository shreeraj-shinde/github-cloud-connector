from fastapi import APIRouter, Depends
from app.services.github_service import GitHubService
from app.dependencies.git_middleware import get_github_service
from app.schemas.pull_request import PullRequestCreate

router = APIRouter(prefix="/repos", tags=["Pull Requests"])


@router.get("/{owner}/{repo}/pulls")
async def list_pull_requests(
    owner: str,
    repo: str,
    state: str = "open",
    service: GitHubService = Depends(get_github_service),
):
    return await service.list_pull_requests(owner=owner, repo=repo, state=state)


@router.get("/{owner}/{repo}/pulls/{pull_number}")
async def get_pull_request(
    owner: str,
    repo: str,
    pull_number: int,
    service: GitHubService = Depends(get_github_service),
):
    return await service.get_pull_request(owner=owner, repo=repo, pull_number=pull_number)


@router.post("/{owner}/{repo}/pulls")
async def create_pull_request(
    owner: str,
    repo: str,
    body: PullRequestCreate,
    service: GitHubService = Depends(get_github_service),
):
    return await service.create_pull_request(
        owner=owner,
        repo=repo,
        payload=body.model_dump(exclude_none=True),
    )
