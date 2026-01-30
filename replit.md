# BlackPhnix Hub

## Overview

BlackPhnix Hub - A hosting services platform built as a Flask + React SPA. The frontend is a pre-built React application served from the `public/` directory, with a Flask backend providing API endpoints for hosting plans, orders, user management, and support tickets.

**Recent Changes (Jan 2026):**
- Cleaned up duplicate assets folders (kept only `public/assets/`)
- Removed attached_assets screenshots directory
- Updated .gitignore for Python projects
- Configured deployment with gunicorn

## Project Structure

```
├── main.py                 # Flask app entry point
├── server.py               # Alternative server entry
├── public/                 # Frontend static files
│   ├── index.html          # SPA entry point
│   ├── assets/             # Built JS/CSS assets
│   ├── sw.js               # Service worker
│   └── bot_script.js       # Bot automation script
├── src/
│   ├── api/
│   │   └── routes.py       # API endpoints
│   ├── models.py           # SQLAlchemy models
│   ├── services/
│   │   ├── ai_agent_service.py      # Gemini AI integration
│   │   ├── cyberpanel_service.py    # CyberPanel API
│   │   └── encryption_service.py    # Fernet encryption
│   └── scripts/
│       └── cleanup.py      # Cleanup utilities
├── requirements.txt        # Python dependencies
└── pyproject.toml          # Project metadata
```

## Technical Stack

### Backend
- **Framework**: Flask 3.x
- **Database**: SQLite (local), can use PostgreSQL
- **ORM**: SQLAlchemy / Flask-SQLAlchemy
- **CORS**: Flask-CORS enabled
- **Production Server**: Gunicorn

### Frontend
- **Framework**: React SPA (pre-built)
- **Build Tool**: Vite
- **Styling**: Tailwind CSS

### External Services
- **AI**: Google Gemini API (GEMINI_API_KEY)
- **Hosting**: CyberPanel API integration
- **Encryption**: Fernet (ENCRYPTION_KEY)
- **Ads**: Google AdSense, Monetag

## API Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/domain/claim` - Claim domain and provision hosting
- `GET/POST /api/hosting-plans/*` - CRUD for hosting plans
- `GET/POST /api/orders` - Order management
- `GET/POST /api/tickets` - Support tickets
- `GET /api/admin/bot/status` - Bot status
- `POST /api/admin/bot/analyze` - AI analysis

## Environment Variables (Optional)

- `GEMINI_API_KEY` - Google Gemini API key
- `CYBERPANEL_URL` - CyberPanel server URL
- `CYBERPANEL_ADMIN_USER` - CyberPanel admin username
- `CYBERPANEL_ADMIN_PASS` - CyberPanel admin password
- `ENCRYPTION_KEY` - Fernet encryption key

## Running the Project

Development: `python main.py`
Production: `gunicorn --bind=0.0.0.0:5000 --reuse-port main:app`
