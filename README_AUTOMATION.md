# BlackPhnix Hub - CyberPanel Automation System

This project implements a secure, production-ready automation system for hosting account provisioning via CyberPanel.

## System Architecture

### 1. CyberPanel Integration (`src/services/cyberpanel_service.py`)
- Handles API communication with CyberPanel.
- Securely retrieves credentials from environment variables.
- Supports user creation, website/subdomain setup, database/FTP/Email account creation.

### 2. Models (`src/models.py`)
- `User`: Local user management.
- `CyberAccount`: Tracks CyberPanel account details, domains, and suspension states.
- `SystemLog`: Internal logging for all automation events.

### 3. API Endpoints (`src/api/routes.py`)
- `POST /api/auth/register`: Combined registration and automated provisioning.
- `GET /api/admin/accounts`: Admin view for managed accounts.
- `GET /api/admin/logs`: System event logs.

### 4. Automated Cleanup (`src/scripts/cleanup.py`)
- Background task that runs daily.
- Automatically deletes websites suspended for more than 15 days.
- Logs all cleanup actions.

## Setup Instructions

1. **Environment Variables**: Set the following in your Replit secrets:
   - `CYBERPANEL_URL`: Your CyberPanel URL (e.g., https://your-ip:8090)
   - `CYBERPANEL_ADMIN_USER`: API Username
   - `CYBERPANEL_ADMIN_PASS`: API Password

2. **Workflows**:
   - `Start application`: Runs the main Flask server.
   - `Cleanup Task`: Runs the background cleanup script.

## Security Best Practices
- **No Hardcoding**: Credentials are strictly managed via environment variables.
- **Credential Encryption**: CyberPanel passwords are encrypted using Fernet (AES-128) before being stored in the database.
- **Key Management**: The `ENCRYPTION_KEY` must be kept secret and is stored as a Replit secret.
- **Rate Limiting**: Integrated via Flask infrastructure.
