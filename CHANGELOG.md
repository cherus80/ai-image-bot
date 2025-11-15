# Changelog

All notable changes to the AI Image Generator Bot project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.11.0] - 2025-11-15

### Added
- Production deployment script `deploy-to-vps.sh` for automated deployment from local machine to VPS
- Root `.env` file for docker-compose production configuration
- Deployment report `DEPLOY_REPORT.md` with detailed deployment status
- CHANGELOG.md for tracking version history

### Fixed
- **Critical:** Frontend Docker build stability issues
  - Split npm dependency installation into separate RUN commands
  - Improved error handling for npm ci
  - Added fallback logic for installing build tools (python3/make/g++)
  - Fixed npm config commands (using `npm config set` instead of `npm set`)
  - Resolved exit code 1 errors during npm ci execution

### Changed
- Optimized `frontend/Dockerfile.prod` for better npm package installation reliability
- Updated deployment workflow to use SSH config alias instead of explicit parameters

### Deployment
- ✅ Successfully deployed to production VPS at https://ai-bot-media.mix4.ru
- ✅ Backend running (healthy) on port 8000
- ✅ Frontend running (healthy) on port 3000
- ✅ PostgreSQL, Redis, Celery Worker, Celery Beat all operational

### Known Issues
- ⚠️ Telegram Bot container restarting due to module import error (non-critical)
- ⚠️ Health endpoint not accessible through nginx (works locally on VPS)

---

## [0.10.0] - 2025-11-14

### Added
- Mock payment emulator for development testing
- Frontend debug page for localStorage and Telegram WebApp diagnostics
- Clear storage utility page
- MCP Playwright integration for automated frontend testing

### Fixed
- TypeScript errors in authStore mock data
- AuthGuard DEV mode implementation for testing without Telegram
- LoadingPage and ErrorPage UI improvements
- Telegram WebApp SDK integration issues

### Changed
- Improved development workflow with better debugging tools
- Enhanced error messages and user feedback

---

## [0.9.0] - 2025-11-13

### Added
- Complete frontend React application structure
- Authentication system with Telegram WebApp SDK
- State management with Zustand
- Routing with React Router
- Tailwind CSS styling
- Basic UI components (Button, Card, Input, etc.)

### Backend
- FastAPI application structure
- Database models (User, Generation, ChatHistory, Payment)
- API endpoints for auth, fitting, editing, payments
- Celery tasks for async image generation
- PostgreSQL database setup
- Redis for Celery broker

### Infrastructure
- Docker Compose setup for development and production
- Nginx configuration for reverse proxy
- VPS deployment scripts
- Database migration system (Alembic)

---

## [0.1.0] - 2025-11-01

### Added
- Initial project setup
- Project documentation (README.md, TODO.md, CLAUDE.md)
- Basic project structure
- Git repository initialization

---

## Deployment History

### Production Deployments

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 0.11.0 | 2025-11-15 | ✅ Success | Fixed Docker build issues, deployed to VPS |
| 0.10.0 | 2025-11-14 | ⏭️ Skipped | Development improvements only |
| 0.9.0 | 2025-11-13 | ⏭️ Skipped | Initial version, not deployed |

---

## Migration Notes

### Migrating from 0.10.0 to 0.11.0

1. **Docker Build Changes:**
   - No breaking changes
   - Frontend Dockerfile.prod optimized for better stability
   - Rebuild recommended: `docker-compose -f docker-compose.prod.yml build --no-cache`

2. **Environment Variables:**
   - New root `.env` file required for docker-compose
   - Copy from template or use existing backend/.env.production values

3. **Deployment:**
   - Use new `deploy-to-vps.sh` script for automated deployment
   - Ensure SSH config has `ai-bot-vps` alias configured

### Database Migrations

No database schema changes in this version.

---

## Contributors

- Claude Code (Anthropic) - AI Assistant
- Project Owner - Ruslan Cernov

---

## License

Proprietary - All rights reserved

---

## Links

- **Production:** https://ai-bot-media.mix4.ru
- **Repository:** https://github.com/cherus80/ai-image-bot
- **Documentation:** /docs

---

_Last updated: 2025-11-15_
