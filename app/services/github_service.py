from app.services.github_client import GitHubClient
from app.config import get_settings
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi import status
from app.utils.client import HTTPClient
from app.utils.constants import HTTPMethods
from app.utils.token_store import token_store
from app.services.auth_service import AuthService
from app.utils.logger import get_logger


settings = get_settings()
logger = get_logger(__name__)

class GitHubService:

    # Constant URLs
    GITHUB_AUTHORIZE = "https://github.com/login/oauth/authorize"
    GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"

    def __init__(self, client: GitHubClient):
        self.client = client  # Store the injected client (used after login)

    @staticmethod
    async def login():
        try:
            url = f"{GitHubService.GITHUB_AUTHORIZE}?client_id={settings.GIT_CLIENT_ID}&scope=repo,user"
            logger.info("Redirecting user to GitHub OAuth")
            return RedirectResponse(url)

        except Exception as e:
            logger.error(f"Login redirect failed: {e}")
            return JSONResponse(
                content={"error": "Server Error. Please try again later."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    async def get_access_token(code: str):
        try:
            # POST To Get Access Token
            client = HTTPClient()

            headers = {
                "Accept": "application/json"
            }

            payload = {
                "client_id": settings.GIT_CLIENT_ID,
                "client_secret": settings.GIT_CLIENT_SECRET,
                "code": code
            }

            data = await client.request(
                url=GitHubService.GITHUB_TOKEN_URL,
                method=HTTPMethods.POST,
                headers=headers,
                json=payload
            )

           
            access_token = data.get("access_token")
            if access_token:
                auth = AuthService(access_token)
                token_store["token"] = auth.encrypt(access_token)
                logger.info("Access token obtained and stored (encrypted)")
            else:
                return JSONResponse(
                    content={"error": data.get("error")},
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # Decrypt before returning so the response contains the raw token
            decrypted = auth.decrypt(token_store["token"])
            return JSONResponse(
                content={"token": decrypted},
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ── User ─────────────────────────────────────────────────────────────────

    async def get_user(self):
        try:
            data = await self.client.get_authenticated_user()
            return JSONResponse(content=data, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ── Repositories ─────────────────────────────────────────────────────────

    async def list_repos(self, per_page: int = 30, page: int = 1):
        try:
            data = await self.client.list_repos(per_page=per_page, page=page)
            return JSONResponse(content=data, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_repo(self, owner: str, repo: str):
        try:
            data = await self.client.get_repo(owner=owner, repo=repo)
            return JSONResponse(content=data, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ── Issues ────────────────────────────────────────────────────────────────

    async def list_issues(self, owner: str, repo: str, state: str = "open"):
        try:
            data = await self.client.list_issues(owner=owner, repo=repo, state=state)
            return JSONResponse(content=data, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_issue(self, owner: str, repo: str, issue_number: int):
        try:
            data = await self.client.get_issue(owner=owner, repo=repo, issue_number=issue_number)
            return JSONResponse(content=data, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def create_issue(self, owner: str, repo: str, payload: dict):
        try:
            data = await self.client.create_issue(owner=owner, repo=repo, payload=payload)
            return JSONResponse(content=data, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def update_issue(self, owner: str, repo: str, issue_number: int, payload: dict):
        try:
            data = await self.client.update_issue(owner=owner, repo=repo, issue_number=issue_number, payload=payload)
            return JSONResponse(content=data, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def close_issue(self, owner: str, repo: str, issue_number: int):
        try:
            data = await self.client.update_issue(
                owner=owner, repo=repo, issue_number=issue_number, payload={"state": "closed"}
            )
            return JSONResponse(content=data, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ── Pull Requests ─────────────────────────────────────────────────────────

    async def create_pull_request(self, owner: str, repo: str, payload: dict):
        try:
            data = await self.client.create_pull_request(owner=owner, repo=repo, payload=payload)
            return JSONResponse(content=data, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def list_pull_requests(self, owner: str, repo: str, state: str = "open"):
        try:
            data = await self.client.list_pull_requests(owner=owner, repo=repo, state=state)
            return JSONResponse(content=data, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def get_pull_request(self, owner: str, repo: str, pull_number: int):
        try:
            data = await self.client.get_pull_request(owner=owner, repo=repo, pull_number=pull_number)
            return JSONResponse(content=data, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
