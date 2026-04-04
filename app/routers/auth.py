from fastapi import APIRouter
from app.services.github_service import GitHubService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/login")
async def connect_github():
    return await GitHubService.login()

    
@router.get("/callback")
async def process_callback(code:str):
    return await GitHubService.get_access_token(code)


