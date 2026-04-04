from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.services.github_client import GitHubClient
from app.services.github_service import GitHubService
from app.services.auth_service import AuthService
from app.utils.logger import get_logger

logger = get_logger(__name__)

bearer_scheme = HTTPBearer(auto_error=False)


def get_github_service(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> GitHubService:

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials  
    try:
        auth = AuthService(token)
        raw_token = auth.decrypt(token)
       
    except JWTError:
        # Not a JWT — assume it's a Personal Access Token (PAT) used directly
       
        raw_token = token

    client = GitHubClient(token=raw_token)
    return GitHubService(client=client)
