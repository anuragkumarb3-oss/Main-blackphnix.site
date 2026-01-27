# replit.md

## Overview

BlackPhnix Hub - A hosting services platform built as a Flask + React SPA. The frontend is a pre-built React application served from the `public/` directory, with a Flask backend providing API endpoints for hosting plans, orders, and support tickets.

**Recent Changes (Jan 2026):**
- Fixed SPA routing issues - all routes now work on refresh
- Updated service worker for network-first caching strategy
- Removed conflicting Flask static file handler
- Added proper cache-control headers for HTML

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

- **Framework**: Single-page application (SPA) - likely React based on the `<div id="root"></div>` mount point pattern
- **Build Tool**: Vite (inferred from asset file naming pattern `index-B403tFjw.js`)
- **Styling**: Tailwind CSS (evidenced by `--tw-border-spaci` prefix in CSS and utility-first approach)
- **Typography**: Custom font stack including Inter, JetBrains Mono, Orbitron, Architects Daughter, DM Sans, Fira Code, and Geist Mono

### Service Workers

- **Basic Service Worker** (`sw.js`): Minimal implementation that skips waiting on install - handles app caching/offline functionality
- **Ad Service Worker** (`sw_1768827361567.js`): Third-party service worker for Monetag ad network integration

### Build Output Structure

The production build outputs to:
- `index.html` - Entry point
- `assets/` - Bundled JavaScript and CSS with content hashing for cache busting

## External Dependencies

### Monetization Services

1. **Google AdSense**
   - Client ID: `ca-pub-2511974370329391`
   - Loaded asynchronously via `pagead2.googlesyndication.com`

2. **Monetag**
   - Verification tag: `b700f771347f37ec3c30ca6e5de25c7d`
   - Zone ID: `10486465`
   - Domain: `5gvci.com`
   - Implemented via dedicated service worker

### Font Services

- **Google Fonts**: Multiple font families loaded via `fonts.googleapis.com` and `fonts.gstatic.com`
  - Architects Daughter
  - DM Sans (variable weight)
  - Fira Code (variable weight)
  - Geist Mono (variable weight)
  - Inter (multiple weights)
  - JetBrains Mono
  - Orbitron (multiple weights)

### Development Configuration

- **Semgrep**: Security linting configured in `.config/replit/.semgrep/` for TypeScript security auditing, particularly CORS validation patterns