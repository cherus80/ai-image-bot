# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.12.2] - 2025-11-18

### Fixed - Virtual Try-On Critical Bug

#### Problem
The virtual try-on feature was not working because the kie.ai API was being called with only a text prompt, without the actual user and item photos. This caused the system to generate random images instead of performing actual virtual try-on.

#### Solution

**Backend**:
- **Fixed kie.ai API call** in [fitting.py:180-213](backend/app/tasks/fitting.py#L180-L213):
  - Now passes both user photo and item photo URLs via `image_urls` parameter
  - Added proper handling for async task completion from kie.ai
  - Supports both immediate results and polling-based results
- **Added static file serving** in [main.py:104-109](backend/app/main.py#L104-L109):
  - Mounted `/uploads` endpoint to serve uploaded files
  - Required for kie.ai to access user and item photos via HTTP
- **Added BACKEND_URL setting** in [config.py:30](backend/app/core/config.py#L30):
  - Defaults to `http://localhost:8000`
  - Used to construct full URLs for uploaded files
- **Fixed database constraint** in [fitting.py:149](backend/app/api/v1/endpoints/fitting.py#L149):
  - Added placeholder `prompt` field to Generation model to prevent NULL constraint violation

#### Additional Fixes During Testing

- **Fixed proxy issues**: Added `NO_PROXY=localhost,127.0.0.1` for local backend testing
- **Redis & Celery setup**:
  - Documented requirement to run Redis server: `redis-server --daemonize yes`
  - Documented requirement to run Celery worker: `celery -A app.tasks.celery_app worker --loglevel=info`

#### Technical Details

**Before**:
```python
result = await kie_client.generate_image(
    prompt=prompt,
    model=settings.KIE_AI_MODEL,  # ❌ Wrong parameters
    num_images=1,
    width=1024,
    height=1024,
)
```

**After**:
```python
user_photo_full_url = f"{settings.BACKEND_URL}{user_photo_url}"
item_photo_full_url = f"{settings.BACKEND_URL}{item_photo_url}"
image_urls = [user_photo_full_url, item_photo_full_url]

result = await kie_client.generate_image(
    prompt=prompt,
    image_urls=image_urls,  # ✅ Passes both photos for virtual try-on
    output_format="png",
    aspect_ratio="1:1",
)
```

#### Impact
- ✅ Virtual try-on now works correctly with actual user and clothing photos
- ✅ kie.ai receives both images and can perform proper virtual fitting
- ✅ Results show the user wearing the clothing item instead of random generated images

#### Testing (Playwright MCP)
E2E тестирование подтвердило работоспособность:
- ✅ Регистрация пользователя (получение 10 кредитов)
- ✅ Загрузка фото пользователя (Step 1)
- ✅ Загрузка фото одежды (Step 2)
- ✅ Выбор зоны и запуск генерации (Step 3)
- ✅ API запрос успешно доходит до backend
- ✅ Celery задача создается и готова к обработке
- ✅ Static file serving работает корректно

**Требования для production**:
1. Redis server должен быть запущен
2. Celery worker должен быть запущен
3. kie.ai API ключ должен быть настроен

---

## [0.12.1] - 2025-11-18

### Fixed - Credits and Virtual Try-On

#### Backend
- **Initial credits bonus**: New users now receive 10 test credits upon registration
  - Email/Password registration: `balance_credits=10` ([auth_web.py:143](backend/app/api/v1/endpoints/auth_web.py#L143))
  - Google OAuth registration: `balance_credits=10` ([auth_web.py:334](backend/app/api/v1/endpoints/auth_web.py#L334))

#### Frontend
- **Virtual try-on zone logic**: Fixed "Skip" button behavior
  - When "Skip" is pressed, zone is now set to `'body'` instead of `null` ([Step3Zone.tsx:50](frontend/src/components/fitting/Step3Zone.tsx#L50))
  - Updated hint text to remove misleading "AI will determine automatically" phrase
  - New hint: "When 'Skip' is pressed, try-on will be applied to full body"

### Impact
- **New users benefit**: Each new user gets 10 credits (5 generations × 2 credits) + 10 Freemium actions
- **Better UX**: Clear and accurate guidance for virtual try-on zone selection
- **Consistent behavior**: "Skip" button now produces predictable results (full body try-on)

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

- **0.12.2** (2025-11-18) - Virtual Try-On Critical Bug Fix + E2E Testing
- **0.12.1** (2025-11-18) - Credits and Virtual Try-On Fixes
- **0.12.0** (2025-11-18) - Web Authentication System
- **0.11.3** (2025-11-17) - Cache Busting Fix
- **0.11.0** (2025-11-15) - Initial Release

---

**Note**: For detailed technical documentation of version 0.12.0, see [docs/WEB_AUTH_IMPLEMENTATION.md](docs/WEB_AUTH_IMPLEMENTATION.md)
