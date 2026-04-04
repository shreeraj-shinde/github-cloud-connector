from pydantic import BaseModel
from typing import Optional


class IssueCreate(BaseModel):
    title: str
    body: Optional[str] = None
    labels: Optional[list[str]] = None


class IssueUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    state: Optional[str] = None   # "open" | "closed"
    labels: Optional[list[str]] = None


class IssueResponse(BaseModel):
    id: int
    number: int
    title: str
    state: str
    body: Optional[str] = None
    html_url: Optional[str] = None
    labels: Optional[list] = None
    user: Optional[dict] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
