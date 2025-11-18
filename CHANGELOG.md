# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.12.0] - 2025-11-18

### Added - Web Authentication System

#### Backend
- **New API endpoints** (`/api/v1/auth-web`):
  - `POST /register` - Email/Password registration
  - `POST /login` - Email/Password login
  - `POST /google` - Google OAuth (optional)
  - `GET /me` - Get current user profile
- **Enhanced User model** with web auth support:
  - `email` field (unique, indexed)
  - `email_verified` flag
  - `password_hash` (bcrypt with 12 rounds)
  - `auth_provider` enum (EMAIL, GOOGLE, TELEGRAM)
  - `oauth_provider_id` for external OAuth
- **Security enhancements**:
  - Password strength validation (8+ chars, uppercase, lowercase, digit, special char)
  - bcrypt password hashing
  - JWT tokens for web sessions
- **Pydantic schemas** (`auth_web.py`):
  - RegisterRequest, LoginRequest, LoginResponse
  - UserProfile, GoogleOAuthRequest/Response

#### Frontend
- **Authentication pages**:
  - LoginPage - Email/Password login form
  - RegisterPage - User registration form
- **Zustand store** (`authStore.ts`):
  - Email/Password registration
  - Email/Password login
  - Google OAuth integration
  - Persistent auth state (localStorage)
- **API client** (`authWeb.ts`):
  - Axios-based client with JWT interceptors
  - Type-safe API methods
- **Auth hook** (`useAuth.ts`):
  - Auto-login logic for Telegram WebApp
  - Dev mode support (manual login)
  - Computed values (hasCredits, canUseFreemium, hasActiveSubscription)

#### Database
- **Migration**: Updated `auth_provider_enum` to uppercase values
- **Backward compatibility**: Existing Telegram users preserved

### Fixed

1. **Missing email-validator package**
   - Installed `email-validator` for Pydantic EmailStr support

2. **Pydantic forward reference error**
   - Added `from __future__ import annotations`
   - Moved `UserProfile` class to top of file

3. **Missing auth routes (404)**
   - Added LoginPage and RegisterPage routes to App.tsx

4. **API endpoint mismatch**
   - Updated frontend API client to use `/api/v1/auth-web/` prefix

5. **Router prefix mismatch**
   - Changed backend router prefix from `/auth` to `/auth-web`

6. **AuthProvider enum mismatch**
   - Synchronized Python enum and database enum to uppercase
   - Updated database enum: `email` → `EMAIL`, etc.

7. **Cached statement error**
   - Added documentation about backend restart after schema changes

8. **useAuth hook errors**
   - Fixed method names: `login` → `loginWithEmail`, etc.
   - Added dev mode auto-login skip logic

### Tested
- ✅ E2E testing with Playwright MCP
- ✅ Email/Password registration flow
- ✅ Email/Password login flow
- ✅ JWT token persistence
- ✅ Protected routes with authentication
- ✅ Password hashing and validation

### Documentation
- Created comprehensive implementation report: `docs/WEB_AUTH_IMPLEMENTATION.md`
- Updated README.md with web auth information
- Added troubleshooting guide for common issues

---

## [0.11.3] - 2025-11-17

### Fixed - Cache Busting for Telegram WebApp

#### Frontend
- Implemented cache busting for production builds
- Added version query parameter to asset URLs
- Updated nginx configuration for proper cache control

#### Deployment
- Updated deployment scripts with cache busting support
- Added version tracking in deployment process

---

## [0.11.0] - 2025-11-15

### Added - Initial Release

#### Core Features
- Virtual clothing try-on with AI
- AI-powered image editing with chat assistant
- Freemium model (10 actions/month with watermark)
- Subscription system (Basic, Pro, Premium)
- Credit purchase system
- Referral program (+10 credits per referral)

#### Backend
- FastAPI async backend
- PostgreSQL database with SQLAlchemy ORM
- Celery + Redis for async tasks
- Alembic migrations
- kie.ai integration (Nano Banana)
- OpenRouter integration (Claude Haiku)
- YuKassa payment integration
- Telegram WebApp authentication

#### Frontend
- React 18 with TypeScript
- Vite build system
- Tailwind CSS styling
- Zustand state management
- Telegram WebApp SDK integration
- Responsive design
- Progressive Web App features

#### Security
- HMAC SHA-256 validation for Telegram initData
- JWT tokens for API sessions
- File validation (MIME + magic bytes)
- Rate limiting (10 req/min/user)
- SQL injection protection via ORM
- XSS sanitization
- GDPR compliance (auto-delete files)

---

## Version History

- **0.12.0** (2025-11-18) - Web Authentication System
- **0.11.3** (2025-11-17) - Cache Busting Fix
- **0.11.0** (2025-11-15) - Initial Release

---

**Note**: For detailed technical documentation of version 0.12.0, see [docs/WEB_AUTH_IMPLEMENTATION.md](docs/WEB_AUTH_IMPLEMENTATION.md)
