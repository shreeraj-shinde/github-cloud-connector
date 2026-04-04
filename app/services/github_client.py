from app.utils.client import HTTPClient
from app.utils.constants import HTTPMethods


class GitHubClient:

    # Base API URL
    GITHUB_API_URL = "https://api.github.com"

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        self._client = HTTPClient()

    def _url(self, path: str) -> str:
        return f"{self.GITHUB_API_URL}/{path}"

    # ── User ─────────────────────────────────────────────────────────────────

    async def get_authenticated_user(self) -> dict:
        return await self._client.request(
            url=self._url("user"),
            method=HTTPMethods.GET,
            headers=self.headers,
        )

    # ── Repositories ─────────────────────────────────────────────────────────

    async def list_repos(self, per_page: int = 30, page: int = 1) -> list:
        return await self._client.request(
            url=self._url("user/repos"),
            method=HTTPMethods.GET,
            headers=self.headers,
            params={"per_page": per_page, "page": page},
        )

    async def get_repo(self, owner: str, repo: str) -> dict:
        return await self._client.request(
            url=self._url(f"repos/{owner}/{repo}"),
            method=HTTPMethods.GET,
            headers=self.headers,
        )

    # ── Issues ────────────────────────────────────────────────────────────────

    async def list_issues(self, owner: str, repo: str, state: str = "open") -> list:
        return await self._client.request(
            url=self._url(f"repos/{owner}/{repo}/issues"),
            method=HTTPMethods.GET,
            headers=self.headers,
            params={"state": state},
        )

    async def get_issue(self, owner: str, repo: str, issue_number: int) -> dict:
        return await self._client.request(
            url=self._url(f"repos/{owner}/{repo}/issues/{issue_number}"),
            method=HTTPMethods.GET,
            headers=self.headers,
        )

    async def create_issue(self, owner: str, repo: str, payload: dict) -> dict:
        return await self._client.request(
            url=self._url(f"repos/{owner}/{repo}/issues"),
            method=HTTPMethods.POST,
            headers=self.headers,
            json=payload,
        )

    async def update_issue(self, owner: str, repo: str, issue_number: int, payload: dict) -> dict:
        return await self._client.request(
            url=self._url(f"repos/{owner}/{repo}/issues/{issue_number}"),
            method=HTTPMethods.PATCH,
            headers=self.headers,
            json=payload,
        )

    # ── Pull Requests ─────────────────────────────────────────────────────────

    async def create_pull_request(self, owner: str, repo: str, payload: dict) -> dict:
        return await self._client.request(
            url=self._url(f"repos/{owner}/{repo}/pulls"),
            method=HTTPMethods.POST,
            headers=self.headers,
            json=payload,
        )

    async def list_pull_requests(self, owner: str, repo: str, state: str = "open") -> list:
        return await self._client.request(
            url=self._url(f"repos/{owner}/{repo}/pulls"),
            method=HTTPMethods.GET,
            headers=self.headers,
            params={"state": state},
        )

    async def get_pull_request(self, owner: str, repo: str, pull_number: int) -> dict:
        return await self._client.request(
            url=self._url(f"repos/{owner}/{repo}/pulls/{pull_number}"),
            method=HTTPMethods.GET,
            headers=self.headers,
        )




