from fastapi import APIRouter, Depends
from app.services.github_service import GitHubService
from app.dependencies.git_middleware import get_github_service
from app.schemas.issue import IssueCreate, IssueUpdate

router = APIRouter(prefix="/repos", tags=["Issues"])


@router.get("/{owner}/{repo}/issues")
async def list_issues(
    owner: str,
    repo: str,
    state: str = "open",
    service: GitHubService = Depends(get_github_service),
):
    return await service.list_issues(owner=owner, repo=repo, state=state)


@router.get("/{owner}/{repo}/issues/{issue_number}")
async def get_issue(
    owner: str,
    repo: str,
    issue_number: int,
    service: GitHubService = Depends(get_github_service),
):
    return await service.get_issue(owner=owner, repo=repo, issue_number=issue_number)


@router.post("/{owner}/{repo}/issues")
async def create_issue(
    owner: str,
    repo: str,
    body: IssueCreate,
    service: GitHubService = Depends(get_github_service),
):
    return await service.create_issue(owner=owner, repo=repo, payload=body.model_dump(exclude_none=True))


@router.patch("/{owner}/{repo}/issues/{issue_number}")
async def update_issue(
    owner: str,
    repo: str,
    issue_number: int,
    body: IssueUpdate,
    service: GitHubService = Depends(get_github_service),
):
    return await service.update_issue(
        owner=owner, repo=repo, issue_number=issue_number,
        payload=body.model_dump(exclude_none=True)
    )


@router.patch("/{owner}/{repo}/issues/{issue_number}/close")
async def close_issue(
    owner: str,
    repo: str,
    issue_number: int,
    service: GitHubService = Depends(get_github_service),
):
    return await service.close_issue(owner=owner, repo=repo, issue_number=issue_number)
