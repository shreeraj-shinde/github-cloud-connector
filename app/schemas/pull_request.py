from pydantic import BaseModel
from typing import Optional


class PullRequestCreate(BaseModel):
    title: str
    head: str            # branch to merge FROM (e.g. "feature/my-branch")
    base: str            # branch to merge INTO (e.g. "main")
    body: Optional[str] = None
    draft: Optional[bool] = False


class PullRequestResponse(BaseModel):
    id: int
    number: int
    title: str
    state: str
    draft: Optional[bool] = None
    html_url: Optional[str] = None
    body: Optional[str] = None
    head: Optional[dict] = None
    base: Optional[dict] = None
    user: Optional[dict] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    merged_at: Optional[str] = None
    mergeable: Optional[bool] = None
