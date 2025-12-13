# Authentication & API Key Management Implementation Guide

## Overview

This implementation separates **UI authentication** (session-based) from **API authentication** (API key-based). Users login with username/password to access the dashboard, then manage API keys for programmatic access.

---

## Backend Changes

### 1. New Endpoints

#### Authentication (Session-based)
```
POST   /api/v1/auth/register/
POST   /api/v1/auth/login/
POST   /api/v1/auth/logout/
GET    /api/v1/auth/me/
```

#### API Key Management
```
GET    /api/v1/keys/          → List user's API keys
POST   /api/v1/keys/          → Generate new API key
DELETE /api/v1/keys/{id}/     → Revoke API key
```

### 2. Key Features

- **Session Cookies**: Authentication uses Django sessions (not JWT or tokens)
- **API Key Hashing**: Keys are hashed with SHA256 before storage
- **Masked Keys**: Users see only masked keys (prefix + last 4 chars) after creation
- **Full Key On Creation**: Raw key shown once when generated
- **One Key Per User**: (Can be extended to multiple keys)

### 3. Implementation Files

```
project/backend/accounts/
├── serializers.py          # DRF serializers for auth endpoints
├── views.py               # Auth & API key views
├── urls.py                # Auth & key management routes
├── authentication.py      # APIKeyAuthentication class
└── services/
    └── api_key.py         # Key generation & hashing
```

### 4. Settings Update

The `settings.py` includes:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'django.contrib.auth.backends.ModelBackend',      # Session auth
        'accounts.authentication.APIKeyAuthentication',   # API key auth
    ],
}

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CORS_ALLOW_CREDENTIALS = True
```

---

## Frontend Changes

### 1. New Pages

- `/login` - Login with email/password
- `/register` - Create new account
- `/dashboard` - Main dashboard with API key management
- `/dashboard/tagger` - Image tagging playground
- `/dashboard/usage` - Usage history (can be mocked)

### 2. Auth Flow

```
User Registration
  ↓
  POST /api/v1/auth/register/
  ↓
  Auto-login & set session cookie
  ↓
  Redirect to /dashboard
  ↓
User can now generate API keys
```

### 3. Key Files

```
frontend/src/
├── lib/
│   └── api.ts              # Centralized API client
├── stores/
│   ├── auth.ts             # Auth state management
│   └── apiKeys.ts          # API keys state management
├── types/
│   └── api.ts              # TypeScript types
├── pages/
│   ├── LoginPage.svelte
│   ├── RegisterPage.svelte
│   └── Dashboard.svelte
└── components/
    ├── Sidebar.svelte      # Navigation & logout
    ├── APIKeyCard.svelte   # Display individual keys
    └── ...
```

### 4. Critical Implementation Details

**API Client (`lib/api.ts`)**:
- Uses `credentials: 'include'` for session cookies
- Separates session endpoints from API key endpoints
- API key stored in auth store, NOT as authentication

**Auth Store (`stores/auth.ts`)**:
- Tracks logged-in user
- Does NOT store API key (separate concern)
- Updated by login/logout/register endpoints

**API Keys Store (`stores/apiKeys.ts`)**:
- Manages list of user's API keys
- Keys are only for display (masked version)
- Raw key only shown once on creation

---

## Migration Path

### Step 1: Database Migrations

```bash
cd project/backend
python manage.py migrate
```

This creates/updates:
- `accounts_user` (already exists, ensure email is unique)
- `accounts_apikey` (already exists, update to add `user` FK)

### Step 2: Install Dependencies

Backend (Django):
```bash
pip install djangorestframework python-decouple
```

Frontend (already in package.json):
```bash
cd frontend
yarn install
```

### Step 3: Update Django Settings

Use the provided `settings.py` or merge sections.

### Step 4: Update URLs

Ensure `backend/urls.py` includes:
```python
path('api/v1/auth/', include('accounts.urls')),
```

### Step 5: Start Backend

```bash
cd project/backend
python manage.py runserver 0.0.0.0:8000
```

### Step 6: Start Frontend

```bash
cd frontend
yarn dev
```

---

## Testing

### Register & Login

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"email": "user@example.com", "password": "securepass123"}'

# Get current user (verify session)
curl http://localhost:8000/api/v1/auth/me/ -b cookies.txt
```

### Generate API Key

```bash
# Generate key (requires session cookie)
curl -X POST http://localhost:8000/api/v1/keys/ \
  -H "Content-Type: application/json" \
  -b cookies.txt

# Response:
# {
#   "id": 1,
#   "key": "fk_live_xY9Z8k2M7qP3...",
#   "masked_key": "fk_live_****...7qP3",
#   "created_at": "2025-12-13T..."
# }
```

### Use API Key for Image Tagging

```bash
curl -X POST http://localhost:8000/api/v1/tag/ \
  -H "Authorization: Api-Key fk_live_xY9Z8k2M7qP3..." \
  -H "Content-Type: application/json" \
  -d '{"image_url": "https://..."}'
```

---

## Important Notes

### ✅ What Was Preserved

- Original `APIKey` model and hashing logic
- Original image tagging endpoint (`/api/v1/tag/`)
- API key authentication mechanism
- Rate limiting and quota system
- No changes to AI/LangGraph logic

### ✅ What Was Added

- Session-based UI authentication
- User registration
- API key management dashboard
- Separate auth stores (session vs API key)
- New serializers and views
- Frontend pages and components

### ⚠️ Breaking Changes

**For existing API users**:
- Still use API key auth (no breaking change)
- Format: `Authorization: Api-Key <key>`
- Rate limiting still enforced

**For UI access**:
- Old API key-based UI auth no longer works
- Must register/login first
- Then generate API key from dashboard

---

## Configuration

### Frontend `.env.local`

```env
VITE_API_BASE_URL=http://localhost:8000
```

### Backend `.env`

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## Next Steps

1. **Email Verification** (optional):
   - Add email confirmation after registration
   - Send confirmation link via email

2. **Password Reset** (optional):
   - Add `/api/v1/auth/password-reset/` endpoint
   - Send reset token via email

3. **Multiple API Keys** (optional):
   - Remove one-key-per-user restriction
   - Add key naming/description
   - Add key permissions/scopes

4. **Usage Analytics**:
   - Implement `/api/v1/keys/{id}/usage/` endpoint
   - Show daily/weekly usage charts

---

## Support

For issues or questions, refer to:
- `project/backend/` for backend implementation
- `frontend/src/` for frontend implementation
- Existing Django + DRF docs
- Svelte documentation
