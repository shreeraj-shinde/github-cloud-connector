# GitHub Cloud Connector

A robust, production-ready FastAPI-based cloud connector to the GitHub API. This application provides a clean REST interface for retrieving and managing GitHub resources like repositories, issues, and pull requests securely with OAuth 2.0 authentication.

---

## 📑 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture & Design](#architecture--design)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Configuration (.env)](#configuration-env)
- [Running the Application](#running-the-application)
- [Authentication Deep Dive](#authentication-deep-dive)
- [API Endpoints](#api-endpoints)
- [Testing the API](#testing-the-api)
- [Error Handling](#error-handling)

---

## ✨ Features

- 🔐 **Secure Authentication**: Supports both **GitHub OAuth 2.0 flow** and **Personal Access Tokens (PAT)** seamlessly via Bearer HTTP headers.
- 🔒 **Token Encryption**: OAuth tokens are **JWT-encrypted** before being stored limitings exposure. Tokens support explicit expiration.
- 📦 **Repositories**: Browse and fetch details of public and private repositories.
- 🐛 **Issue Management**: Full CRUD lifecycle support—list, fetch, create, update, and close issues.
- 🎁 **Pull Requests**: Easily list, fetch, and create pull requests between branches.
- 👤 **Users**: Fetch the currently authenticated user's profile information.
- ✅ **Structured Validation**: End-to-end request/response validation using `Pydantic`.
- 🚥 **Custom Middleware**: Robust error handling, comprehensive logging, and smart fallback authentication mechanisms.

---

## 🛠️ Tech Stack

- **Language**: Python 3.13
- **Framework**: FastAPI
- **HTTP Client**: `httpx` (Fully Asynchronous)
- **Security/Auth**: `python-jose` (JWT), GitHub OAuth 2.0
- **Configuration**: Pydantic Settings
- **Package Manager**: `uv`

---

## 🧱 Architecture & Design

The application follows a clean layered architectural pattern ensuring separation of concerns:

1. **Routers (`app/routers/`)**: Defines the API endpoints and injects dependencies. Maps incoming HTTP requests to Service layer calls.
2. **Middleware (`app/dependencies/git_middleware.py`)**: Intercepts requests, validates the `Authorization` header, decrypts JWTs securely, and gracefully falls back to explicit PATs if decoded incorrectly. Injects the initialized `GitHubService` instance.
3. **Business Logic (`app/services/github_service.py`)**: Validates business rules, acts as an abstraction layer to the underlying client, and formats the output.
4. **API Client (`app/services/github_client.py`)**: Low-level integration with the `api.github.com` endpoints handling strict HTTP verb calling.

---

## 📋 Prerequisites

To run this application locally, you need:
- Python 3.13+ installed.
- `uv` package manager installed (`pip install uv`).
- A registered GitHub OAuth Application (optional, if using PAT only).

---

## 🚀 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/shreeraj-shinde/github-cloud-connector.git
cd github-cloud-connector
```

### 2. Create a GitHub OAuth App (For OAuth Flow)

1. Go to **GitHub → Settings → Developer Settings → OAuth Apps → New OAuth App**
2. Name the application and set the **Authorization callback URL** exactly to:
   ```
   http://localhost:8000/auth/callback
   ```
3. Save and copy your **Client ID** and **Client Secret**.

### 3. Configure Virtual Environment & Dependencies

```bash
# Using uv (fastest & recommended)
uv sync

# Or if you freeze requirements via `uv pip freeze > requirements.txt`
pip install -r requirements.txt
```

---

## ⚙️ Configuration (.env)

Create a `.env` file in the root directory (you can copy from `.env.example`).

```env
PORT=8000
APP_ENV=development

# GitHub OAuth Credentials
GIT_CLIENT_ID=your_github_client_id
GIT_CLIENT_SECRET=your_github_client_secret

# Security Settings
SECRET=your_secure_random_string_for_jwt
ALGORITHM=HS256
TOKEN_EXPIRE_HOURS=8

# CORS Configuration
# Comma-separated allowed origins (e.g., https://app.example.com) or * for dev
CORS_ORIGINS=*
```

> **Security Note:** Never commit your `.env` file. Keep your `SECRET` and GitHub app credentials private.

---

## 🏃 Running the Application

Start the FastAPI server:

```bash
# Recommended with uv
uv run main.py

# Alternatively via classic Python
python main.py

# Or directly with uvicorn (with hot reload enabled)
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
```

- **Server starts at:** `http://localhost:8000`
- **Interactive Swagger UI Docs:** `http://localhost:8000/docs`

---

## 🔐 Authentication Deep Dive

The connector utilizes smart fallback middleware that supports two modes sequentially without requiring API consumer modifications:

### 1. OAuth 2.0 Web Flow (Recommended)
1. User hits `GET /auth/login`.
2. Backend redirects user to GitHub Authorization page.
3. User accepts and GitHub redirects back to `GET /auth/callback?code=...`.
4. Server grabs access token from GitHub API behind the scenes.
5. Server **symmetric-encrypts** the raw token into a JWT using `SECRET` and sets an expiry.
6. The user receives the Encrypted JWT which they use as their Bearer Token. At every subsequent request, the middleware decrypts it into the raw payload to communicate with GitHub.

### 2. Personal Access Token (PAT) Fallback
If you do not wish to go through the Web Flow. Generate a PAT from **GitHub → Settings → Developer Settings → Personal Access Tokens**.
The middleware explicitly intercepts tokens. If decoding as a JWT fails, it elegantly falls back and treats the input as a raw personal access token.

```http
Authorization: Bearer <your_raw_ghp_token>
```

---

## 📡 API Endpoints

### System & Authentication

| Method | Endpoint          | Description                                |
|--------|-------------------|--------------------------------------------|
| GET    | `/health`         | Validates if the local server is operating |
| GET    | `/auth/login`     | Redirect payload to GitHub OAuth process   |
| GET    | `/auth/callback`  | OAuth callback URL triggered by GitHub     |

---

**Note:** All remaining endpoints below represent protected routes and explicitly **require** an `Authorization` header passed by the API client.

### Users

| Method | Endpoint     | Description                    |
|--------|--------------|--------------------------------|
| GET    | `/users/me`  | Gets authenticated user profile |

### Repositories

| Method | Endpoint                 | Description              | Query Constraints    |
|--------|--------------------------|--------------------------|----------------------|
| GET    | `/repos/`                | List user's repositories | `per_page`, `page`   |
| GET    | `/repos/{owner}/{repo}`  | Get a single repository  | —                    |

### Issues

| Method | Endpoint                                        | Description       |
|--------|-------------------------------------------------|-------------------|
| GET    | `/repos/{owner}/{repo}/issues`                  | List issues       |
| GET    | `/repos/{owner}/{repo}/issues/{number}`         | Get single issue  |
| POST   | `/repos/{owner}/{repo}/issues`                  | Create an issue   |
| PATCH  | `/repos/{owner}/{repo}/issues/{number}`         | Update an issue   |
| PATCH  | `/repos/{owner}/{repo}/issues/{number}/close`   | Close an issue    |

#### Create Issue Example Payload
```json
{
  "title": "Bug: Authentication loop fails",
  "body": "System stuck in redirect loop on Safari.",
  "labels": ["bug", "priority-high"]
}
```

### Pull Requests

| Method | Endpoint                                  | Description            |
|--------|-------------------------------------------|------------------------|
| GET    | `/repos/{owner}/{repo}/pulls`             | List pull requests     |
| GET    | `/repos/{owner}/{repo}/pulls/{number}`    | Get a single PR        |
| POST   | `/repos/{owner}/{repo}/pulls`             | Create a pull request  |

#### Create PR Example Payload

```json
{
  "title": "Add JWT Decryption Middleware mapping",
  "head": "feature/jwt-support",
  "base": "main",
  "body": "Implements the auth service bindings directly inside the router schema middleware.",
  "draft": false
}
```
*(Validation Note: The `head` branch must be explicitly ahead of the `base` branch to not receive an unprocessable entity error from GitHub).*

---

## 🧪 Testing the API

### Method 1: Using Swagger Docs (Easiest)

1. Open `http://localhost:8000/docs`.
2. Locate the **Authorize** lock icon `🔒` at the top right of the page.
3. Paste either your **OAuth JWT string** or your **raw GitHub PAT** inside the value field. *(Do not include the word 'Bearer' here, Swagger does it).*
4. Click **Authorize** and easily execute protected endpoints via the UI.

### Method 2: Using CURL / PowerShell

```powershell
# Fetch current user profile
Invoke-WebRequest -Uri "http://localhost:8000/users/me" `
  -Headers @{"Authorization" = "Bearer gho_YOUR_TOKEN_STRING"} `
  -UseBasicParsing | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

---

## ⚠️ Error Handling

All generic exceptions, API integration errors, and business rule collisions will return a standardized structured JSON error to easily map on frontend services:

```json
{ "error": "Description of what went wrong" }
```

| HTTP Status                   | Scenario Indicator                                    |
|-------------------------------|-------------------------------------------------------|
| `401 Unauthorized`            | Missing Bearer token, Tampered JWT, or Invalid Token. |
| `400 Bad Request`             | Structural validation failed directly via GitHub API. |
| `422 Unprocessable Entity`    | Missing required fields handled natively by Pydantic. |
| `500 Internal Server Error`   | Underlying code crash, missing attributes handling.   |
