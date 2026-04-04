from pydantic import BaseModel
from typing import Optional


class UserResponse(BaseModel):
    login: str
    id: int
    avatar_url: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    public_repos: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    html_url: Optional[str] = None
