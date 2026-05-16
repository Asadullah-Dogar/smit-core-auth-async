# Advanced Asynchronous Backend System 🚀

> **Enterprise-Grade Authentication Engine** with Zero-Trust Security, Asynchronous Non-Blocking I/O, and Dual-Token JWT Authorization

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI/CD: GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)](https://github.com/features/actions)

---

## 📋 Project Overview

The **Advanced Asynchronous Backend System** is a production-ready FastAPI microservice that demonstrates enterprise-grade authentication and authorization patterns. Built with **100% asynchronous execution**, it showcases industry best practices for secure, scalable, and maintainable backend systems.

### Key Highlights

✨ **Zero-Trust Architecture**: Every protected endpoint validates Bearer tokens against a Redis blacklist  
⚡ **Non-Blocking I/O**: All database and cache operations use async/await (no thread blocking)  
🔐 **Dual-Token System**: Access tokens (short-lived) + Refresh tokens (long-lived) for robust session management  
📦 **Production-Ready**: Tested, documented, and CI/CD enforced with automated security scanning  
🎯 **Beginner-Friendly**: Run locally without Docker, Postgres, or external Redis—everything just works!

---

## 🛠 Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | Modern async web framework with auto-generated OpenAPI docs |
| **ORM** | [SQLAlchemy 2.0](https://docs.sqlalchemy.org/) | Async-native SQL toolkit with declarative ORM |
| **Database Driver** | [aiosqlite](https://aiosqlite.omnilib.dev/) (dev) / [asyncpg](https://magicstack.github.io/asyncpg/) (prod) | Non-blocking async database I/O |
| **Migrations** | [Alembic](https://alembic.sqlalchemy.org/) | Version-controlled schema migrations |
| **Authentication** | [PyJWT](https://pyjwt.readthedocs.io/) | JWT token creation and validation |
| **Password Hashing** | [passlib](https://passlib.readthedocs.io/) + PBKDF2-SHA256 | Industry-standard password hashing (100k+ rounds) |
| **Cache / Blacklist** | [redis-asyncio](https://github.com/redis/redis-py) / [fakeredis](https://github.com/cunla/fakeredis) | Token revocation + session state |
| **Validation** | [Pydantic v2](https://docs.pydantic.dev/) | Strict runtime data validation with auto-generated docs |
| **Testing** | [pytest](https://docs.pytest.org/) + [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) | Comprehensive E2E and unit tests |
| **Linting** | [Ruff](https://docs.astral.sh/ruff/) | Lightning-fast Python linter |
| **Security Scanning** | [Bandit](https://bandit.readthedocs.io/) | OWASP security audit for hardcoded credentials & crypto weaknesses |

---

## 🚀 Frictionless Local Setup

### The Beauty of This Project 🎁

**No external dependencies needed!**  
This project is designed for immediate local development:

- 🗄️ **SQLite** (not Postgres) for local dev—comes with Python  
- 🚫 **No Docker required**—just Python and pip  
- 💨 **Fake Redis** with `fakeredis`—zero external services to manage  
- ⏱️ **Full test suite passes locally**—verify immediately  

### Installation & Setup (5 minutes)

#### 1. **Clone the Repository**

```bash
git clone https://github.com/Asadullah-Dogar/smit-core-auth-async.git
cd smit-core-auth-async
```

#### 2. **Create and Activate Virtual Environment**

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux (bash/zsh):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. **Install Dependencies**

```bash
pip install --upgrade pip
pip install -e .
```

This installs all project dependencies from `pyproject.toml`.

#### 4. **Configure Environment**

The `.env` file is already configured for local dev:

```bash
# .env (already present)
DATABASE_URL=sqlite+aiosqlite:///./dev.db
REDIS_URL=redis://localhost:6379/0
ACCESS_TOKEN_SECRET=dev-access-secret-key-change-in-production
REFRESH_TOKEN_SECRET=dev-refresh-secret-key-change-in-production
```

No changes needed—everything is ready! 🎉

#### 5. **Run Database Migrations**

```bash
alembic upgrade head
```

Creates the user table in `dev.db`.

#### 6. **Start the Development Server**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Server running!** Open your browser:  
🌐 http://localhost:8000/docs (interactive API documentation)

---

## 📡 API Endpoints

### Public Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Server health check |
| `POST` | `/auth/register` | Create a new user account |
| `POST` | `/auth/login` | Authenticate and receive dual tokens |

### Protected Routes (Require Bearer Token)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/users/me` | Retrieve authenticated user profile |
| `POST` | `/tokens/refresh` | Rotate access token using refresh token |
| `POST` | `/tokens/logout` | Revoke all tokens (logout) |

### Example Usage

#### Register a User

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePassword123!"
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "john@example.com",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2026-05-16T10:38:57"
}
```

#### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePassword123!"
  }'
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Access Protected Route

```bash
curl -X GET http://localhost:8000/users/me \
  -H "Authorization: Bearer <your_access_token>"
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "john@example.com",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2026-05-16T10:38:57"
}
```

---

## ✅ Testing

### Run All Tests

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_auth_flow.py -v
```

### What Gets Tested? 🎯

The automated test suite verifies the **complete authentication flow**:

1. ✓ User registration with email validation
2. ✓ Secure password hashing verification
3. ✓ User login and dual-token generation
4. ✓ Protected route access with Bearer tokens
5. ✓ Token refresh (rotation) mechanism
6. ✓ Logout and token blacklisting
7. ✓ Zero-Trust validation (blacklist checks on every request)

### Test Environment Setup

Tests automatically:
- Use an **in-memory SQLite database** (`test.db`)
- Mock Redis with **fakeredis** (no external services)
- Create/destroy test data per test (isolated execution)
- Validate response schemas against Pydantic models

---

## 🔄 Enterprise CI/CD Pipeline

Every push to `main` triggers an automated GitHub Actions workflow:

### Pipeline Stages

#### 1. **Checkout & Environment Setup**
- Clone repository
- Set up Python 3.11
- Spin up PostgreSQL 15 service
- Spin up Redis 7 service

#### 2. **Linter Engine (Ruff)** 🔍
```bash
ruff check app/ tests/
```
Enforces PEP 8 compliance and code quality standards.

#### 3. **Static Security Audit (Bandit)** 🛡️
```bash
bandit -r app/ --skip B104,B105
```
Scans for hardcoded credentials, weak crypto, and security weaknesses.

#### 4. **Integration Test Suite (Pytest)** ✅
```bash
pytest -v
```
Runs complete E2E authentication flow against live PostgreSQL and Redis.

### Status Badge

Add this to your GitHub profile or project board:

```markdown
[![CI/CD Pipeline](https://github.com/Asadullah-Dogar/smit-core-auth-async/actions/workflows/ci.yml/badge.svg)](https://github.com/Asadullah-Dogar/smit-core-auth-async/actions)
```

---

## 🏗 Architecture

### Layered Design

```
┌─────────────────────────────────────────┐
│  API Layer (Routes)                     │
│  - /auth/register, /auth/login          │
│  - /users/me, /tokens/refresh           │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│  Service Layer (Business Logic)         │
│  - jwt.py (token creation/validation)   │
│  - auth.py (password hashing)           │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│  Data Layer (Database & Cache)          │
│  - SQLAlchemy async engine              │
│  - Redis blacklist (or fakeredis)       │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│  Storage (SQLite dev / Postgres prod)   │
└─────────────────────────────────────────┘
```

### Project Structure

```
app/
├── main.py                    # FastAPI app + lifespan management
├── config.py                  # Pydantic settings from .env
├── database.py                # SQLAlchemy engine & session
├── redis.py                   # Redis client initialization
├── dependencies.py            # Dependency injection (get_current_user)
├── routers/
│   ├── auth.py               # POST /auth/register, /auth/login
│   ├── tokens.py             # POST /tokens/refresh, /tokens/logout
│   └── user.py               # GET /users/me
├── services/
│   ├── jwt.py                # JWT creation & decoding
│   └── auth.py               # Password hashing & verification
├── models/
│   └── user.py               # SQLAlchemy User model
└── schemas/
    ├── auth.py               # Request/response Pydantic models
    └── user.py               # User schemas

alembic/                      # Database migrations
├── env.py
├── versions/
│   └── *_*.py               # Migration files

tests/
├── conftest.py              # Pytest fixtures & setup
└── test_auth_flow.py        # End-to-end auth tests

.env                          # Local dev config
pyproject.toml               # Dependencies & project metadata
alembic.ini                  # Alembic configuration
.github/workflows/ci.yml     # GitHub Actions pipeline
```

---

## 🔐 Security Features

### Password Security
- ✓ **PBKDF2-SHA256** hashing with 100,000+ iterations (NIST-approved)
- ✓ Passwords never stored as plaintext
- ✓ Salted hashes prevent rainbow table attacks

### Token Security
- ✓ **JWT HS256** signing with strong secret keys
- ✓ Access tokens: **15-minute expiration** (short-lived)
- ✓ Refresh tokens: **7-day expiration** (long-lived)
- ✓ Token revocation: Blacklist in Redis with TTL matching expiration
- ✓ **Zero-Trust validation**: Every request validates against blacklist

### Input Validation
- ✓ **Pydantic v2** strict mode for all request bodies
- ✓ Email validation via `email-validator` package
- ✓ Password strength enforcement
- ✓ No SQL injection vulnerabilities (SQLAlchemy parameterized queries)

### Deployment Security Checklist

For production deployment:
- [ ] Change `ACCESS_TOKEN_SECRET` and `REFRESH_TOKEN_SECRET` in `.env`
- [ ] Switch `DATABASE_URL` to PostgreSQL with SSL
- [ ] Use managed Redis cluster (not local/fakeredis)
- [ ] Enable HTTPS/TLS on all endpoints
- [ ] Set up rate limiting on auth endpoints
- [ ] Configure CORS for your domain
- [ ] Enable request logging and monitoring
- [ ] Run Bandit & Ruff in CI/CD (already done! ✓)

---

## 📚 Learning Resources

### For Beginners

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [JWT Authentication Explained](https://jwt.io/introduction)
- [Pydantic Data Validation](https://docs.pydantic.dev/)

### For Advanced Topics

- [Zero-Trust Security Model](https://en.wikipedia.org/wiki/Zero_trust_security_model)
- [Token-Based Authentication](https://tools.ietf.org/html/rfc6749)
- [Async Python Best Practices](https://docs.python.org/3/library/asyncio.html)
- [Password Hashing Standards](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** and test them (`pytest -v`)
4. **Commit with a message** (`git commit -m 'feat: add amazing feature'`)
5. **Push to your branch** (`git push origin feature/amazing-feature`)
6. **Open a Pull Request** with a clear description

### Code Standards

- Follow **PEP 8** (enforced by Ruff)
- Pass **Bandit** security scan
- Write async-first code (no blocking calls in async functions)
- Add tests for new features
- Update documentation

---

## 📄 License

This project is licensed under the **MIT License**—feel free to use it in your own projects!

See [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Asad Ullah Dogar**  
Senior Backend Engineer | Async Python Specialist  
GitHub: [@Asadullah-Dogar](https://github.com/Asadullah-Dogar)

---

## 🎯 Next Steps

1. **Clone and run locally** (5 minutes)
   ```bash
   git clone https://github.com/Asadullah-Dogar/smit-core-auth-async.git
   cd smit-core-auth-async
   python -m venv .venv
   source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows
   pip install -e .
   alembic upgrade head
   uvicorn app.main:app --reload
   ```

2. **Explore the API**  
   Open http://localhost:8000/docs in your browser

3. **Run the test suite**  
   ```bash
   pytest -v
   ```

4. **Review the code**  
   Start with `app/main.py`, then explore `app/routers/` and `app/services/`

5. **Deploy to production** (when ready)  
   Switch to PostgreSQL, enable HTTPS, configure environment secrets

---

## ❓ FAQ

**Q: Do I need Docker to run this locally?**  
A: No! It uses SQLite and fakeredis by default. Just clone, install, and run.

**Q: Can I use this in production?**  
A: Absolutely! Just update `.env` to use PostgreSQL and real Redis, enable HTTPS, and configure secrets.

**Q: How do I switch from SQLite to PostgreSQL?**  
A: Update `DATABASE_URL=postgresql+asyncpg://user:pass@host/db` in `.env` and ensure Alembic migrations are applied.

**Q: Is this suitable for beginners?**  
A: Yes! The code is well-documented, and the architecture is clean. Start with `app/main.py` and trace through to understand async FastAPI patterns.

**Q: How do I extend the authentication system?**  
A: Add new fields to the `User` model in `app/models/user.py`, create a migration with Alembic, update the Pydantic schemas, and add routes in `app/routers/`.

---

## 📞 Support

Have questions or issues? Please open a GitHub issue!

**Happy coding!** 🚀
