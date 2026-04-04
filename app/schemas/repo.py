from pydantic import BaseModel
from typing import Optional


class RepoResponse(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    html_url: Optional[str] = None
    description: Optional[str] = None
    fork: Optional[bool] = None
    language: Optional[str] = None
    stargazers_count: Optional[int] = None
    forks_count: Optional[int] = None
    open_issues_count: Optional[int] = None
    default_branch: Optional[str] = None
