# Authentication & API Key Management Implementation

## ✅ Status: FULLY IMPLEMENTED

All backend and frontend code is complete and ready to run.

---

## Quick Start (5 minutes)

### 1. Backend Setup

```bash
cd project/backend

# Install dependencies (if needed)
pip install djangorestframework

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver 0.0.0.0:8000
```

Backend running at: **http://localhost:8000**

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
yarn install

# Start dev server
yarn dev
```

Frontend running at: **http://localhost:5173**

---

## First Time Users

1. **Go to http://localhost:5173**
2. **Click "Register"** and create an account
3. **Login** with your email/password
4. **Generate API Key** on the dashboard
5. **Copy and save** the key securely
6. **Test Tagger** with the generated key

---

## Architecture

### Two Separate Auth Systems

**System 1: UI Authentication (Session-based)**
```
User Registration → Email + Password → Login → Django Session Cookie
```
- Used for dashboard access
- Session cookie automatically included in requests
- Logout clears session

**System 2: API Key Authentication (Token-based)**
```
Generate Key → Stored Hashed → Use in API Calls → Authorization: Api-Key <token>
```
- Used for `/api/v1/tag/` endpoint only
- Shows raw key once, then masked display
- Rate limited per user

### Key Security Features

✅ **API Keys**:
- Stored as SHA256 hashes
- Masked display: `fk_live_****abcd`
- Raw key shown only once on creation
- Revokable at any time

✅ **Sessions**:
- `SESSION_COOKIE_HTTPONLY = True` (can't access via JS)
- `SESSION_COOKIE_SAMESITE = 'Lax'` (CSRF protection)
- Automatic in browser cookies

---

## API Endpoints

### Authentication

**Register**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "password2": "password123"
  }'
```

**Login**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**Get Me**
```bash
curl http://localhost:8000/api/v1/auth/me/ \
  -b cookies.txt
```

**Logout**
```bash
curl -X POST http://localhost:8000/api/v1/auth/logout/ \
  -b cookies.txt
```

### API Key Management

**List Keys**
```bash
curl http://localhost:8000/api/v1/keys/ \
  -b cookies.txt
```

**Generate Key**
```bash
curl -X POST http://localhost:8000/api/v1/keys/ \
  -H "Content-Type: application/json" \
  -b cookies.txt

# Response:
# {
#   "id": 1,
#   "key": "fk_live_xY9Z8k2M7qP3...",  # ← Save this!
#   "masked_key": "fk_live_****...",
#   "created_at": "2025-12-13T..."
# }
```

**Revoke Key**
```bash
curl -X DELETE http://localhost:8000/api/v1/keys/1/ \
  -b cookies.txt
```

### Image Tagging (with API Key)

```bash
curl -X POST http://localhost:8000/api/v1/tag/ \
  -H "Authorization: Api-Key fk_live_xY9Z8k2M7qP3..." \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/image.jpg",
    "mode": "fast"
  }'
```

---

## File Structure

### Backend

```
project/backend/
├── accounts/
│   ├── migrations/
│   ├── services/
│   │   ├── __init__.py
│   │   └── api_key.py          ← Key generation & hashing
│   ├── authentication.py         ← APIKeyAuthentication
│   ├── models.py                ← User, APIKey models
│   ├── serializers.py           ← DRF serializers (NEW)
│   ├── views.py                 ← Auth views (NEW)
│   ├── urls.py                  ← Auth routes (NEW)
│   └── apps.py
├── backend/
│   ├── settings.py              ← Updated for auth
│   └── urls.py                  ← Added auth routes
└── manage.py
```

### Frontend

```
frontend/src/
├── lib/
│   └── api.ts                   ← Centralized API client (NEW)
├── stores/
│   ├── auth.ts                  ← Session auth state (NEW)
│   └── apiKeys.ts               ← API keys state (NEW)
├── types/
│   └── api.ts                   ← TypeScript types (NEW)
├── pages/
│   ├── LoginPage.svelte         ← Login form (NEW)
│   ├── RegisterPage.svelte      ← Registration (NEW)
│   ├── Dashboard.svelte         ← Main dashboard (NEW)
│   ├── Tagger.svelte            ← Tagging playground (UPDATED)
│   └── Usage.svelte             ← Usage history (NEW)
├── components/
│   ├── Sidebar.svelte           ← Navigation (NEW)
│   └── APIKeyCard.svelte        ← Key display (NEW)
└── app.svelte                   ← Router (UPDATED)
```

---

## What Was Changed

### Backend

✅ **New files**:
- `accounts/serializers.py`
- `accounts/views.py`
- `accounts/urls.py`
- `accounts/services/api_key.py`
- `accounts/services/__init__.py`

✅ **Modified files**:
- `backend/settings.py` - Added session, auth, CORS config
- `backend/urls.py` - Added auth routes
- `accounts/apps.py` - Added config

✅ **Preserved**:
- `accounts/models.py` - No changes to User/APIKey models
- `accounts/authentication.py` - No changes to API key auth
- All other apps and endpoints

### Frontend

✅ **New files**:
- `lib/api.ts`
- `stores/auth.ts`
- `stores/apiKeys.ts`
- `types/api.ts`
- `pages/LoginPage.svelte`
- `pages/RegisterPage.svelte`
- `pages/Dashboard.svelte`
- `pages/Usage.svelte`
- `components/Sidebar.svelte`
- `components/APIKeyCard.svelte`

✅ **Modified files**:
- `pages/Tagger.svelte` - Updated to use new auth
- `app.svelte` - Updated router

---

## Testing

### 1. Register & Login

```bash
# Open browser to http://localhost:5173
# Click Register
# Enter email: test@example.com
# Password: testpass123
# Submit
# → Should redirect to /dashboard
```

### 2. Generate API Key

```bash
# On dashboard, click "Generate API Key"
# Copy the key (shown in modal)
# Key should appear in the table below
```

### 3. Use API Key

```bash
# Go to Tagger Playground
# Enter image URL: https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png
# Select mode: fast
# Click "Tag Image"
# → Should show AI tags for the image
```

### 4. Revoke Key

```bash
# Back on Dashboard
# Click "Revoke" on the API key
# Confirm dialog
# Key should disappear from list
# Tagging with that key will now fail
```

---

## Troubleshooting

### Backend won't start

```bash
# Check Python version (3.9+)
python --version

# Install missing dependencies
pip install djangorestframework

# Clear database if needed
rm db.sqlite3
python manage.py migrate
```

### Frontend shows blank page

```bash
# Hard refresh browser: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows/Linux)
# Check browser console (F12) for errors
# Verify backend is running: http://localhost:8000/api/v1/auth/me/ (401 is OK)
```

### Session cookie not persisting

```bash
# Check DevTools → Application → Cookies
# Look for "sessionid" cookie
# Verify it's sent in requests: DevTools → Network → Headers
```

### API key not working

```bash
# Verify format: Authorization: Api-Key <full_key>
# Not: Authorization: Bearer <key>
# Include full key from generation, not masked version
```

---

## Production Deployment

### Backend

1. Update `settings.py`:
   ```python
   DEBUG = False
   SECRET_KEY = os.getenv('SECRET_KEY')
   ALLOWED_HOSTS = ['yourdomain.com']
   SESSION_COOKIE_SECURE = True  # HTTPS only
   ```

2. Switch to PostgreSQL:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'image_tagging',
           'USER': 'postgres',
           'PASSWORD': os.getenv('DB_PASSWORD'),
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. Use production WSGI server (Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn backend.wsgi:application
   ```

### Frontend

1. Update environment:
   ```
   VITE_API_BASE_URL=https://yourdomain.com
   ```

2. Build for production:
   ```bash
   yarn build
   ```

3. Deploy `dist/` folder to static hosting

---

## Next Steps

- [ ] Email verification on registration
- [ ] Password reset flow
- [ ] Multi-key support per user
- [ ] Key permissions/scopes
- [ ] Usage analytics dashboard
- [ ] Webhook notifications

---

## Support

Refer to:
- **SETUP_INSTRUCTIONS.md** - Detailed setup guide
- **IMPLEMENTATION_GUIDE.md** - Architecture & design
- **CHANGES_SUMMARY.md** - What changed overview

---

## Summary

✨ **Ready to use!**

- ✅ Session-based UI authentication
- ✅ API key management dashboard
- ✅ Secure API key hashing
- ✅ Backward compatible API
- ✅ Production-ready code
- ✅ Comprehensive documentation

Happy coding! 🚀
