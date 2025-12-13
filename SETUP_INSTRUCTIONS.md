# Setup Instructions - Authentication & API Key Management

## Branch

All changes are in the `feat/auth-and-api-keys` branch.

## Quick Start

### Backend Setup

```bash
# Navigate to backend
cd project/backend

# Install dependencies (if not already installed)
pip install djangorestframework

# Update database
python manage.py migrate

# Create superuser (optional, for Django admin)
python manage.py createsuperuser

# Start development server
python manage.py runserver 0.0.0.0:8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
yarn install

# Create environment file
cp .env.example .env.local

# Edit .env.local if needed
# VITE_API_BASE_URL=http://localhost:8000

# Start development server
yarn dev
```

## Access the Application

- **Frontend**: http://localhost:5173/
- **Backend API**: http://localhost:8000/api/v1/
- **Django Admin**: http://localhost:8000/admin/

## First Time Setup

1. **Register a new account**:
   - Go to http://localhost:5173/#/register
   - Enter email and password
   - You'll be automatically logged in

2. **Generate an API Key**:
   - Click "Generate API Key" on the dashboard
   - Copy the key (shown once)
   - Save it securely

3. **Test the Tagger**:
   - Go to "Tagger Playground"
   - Enter an image URL
   - Select tagging mode
   - Click "Tag Image"

4. **View Usage**:
   - Go to "Usage History"
   - See your request statistics

## API Endpoints

### Authentication (Session-based)

**Register**
```
POST /api/v1/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123",
  "password2": "securepass123"
}
```

**Login**
```
POST /api/v1/auth/login/
Content-Type: application/json
Cookie: sessionid=...

{
  "email": "user@example.com",
  "password": "securepass123"
}
```

**Get Current User**
```
GET /api/v1/auth/me/
Cookie: sessionid=...
```

**Logout**
```
POST /api/v1/auth/logout/
Cookie: sessionid=...
```

### API Key Management

**List Keys**
```
GET /api/v1/keys/
Cookie: sessionid=...

Response:
[
  {
    "id": 1,
    "masked_key": "fk_live_****abcd",
    "created_at": "2025-12-13T10:00:00Z",
    "last_used_at": "2025-12-13T11:30:00Z"
  }
]
```

**Generate Key**
```
POST /api/v1/keys/
Content-Type: application/json
Cookie: sessionid=...

Response:
{
  "id": 1,
  "key": "fk_live_xY9Z8k2M7qP3R5tU9vW",
  "masked_key": "fk_live_****P3R5tU9vW",
  "created_at": "2025-12-13T10:00:00Z"
}
```

**Revoke Key**
```
DELETE /api/v1/keys/{id}/
Cookie: sessionid=...

Response: 204 No Content
```

### Image Tagging (API Key Auth)

```
POST /api/v1/tag/
Authorization: Api-Key fk_live_xY9Z8k2M7qP3R5tU9vW
Content-Type: application/json

{
  "image_url": "https://example.com/image.jpg",
  "mode": "fast"
}

Response:
{
  "image_url": "https://example.com/image.jpg",
  "tags": { ... }
}
```

## File Structure

### Backend

```
project/backend/
├── accounts/
│   ├── migrations/
│   ├── services/
│   │   └── api_key.py          (Key generation & hashing)
│   ├── authentication.py        (APIKeyAuthentication class)
│   ├── models.py               (User, APIKey models)
│   ├── serializers.py          (Auth & key serializers)
│   ├── views.py                (Auth & key views)
│   └── urls.py                 (Auth & key routes)
├── backend/
│   ├── settings.py             (Updated with auth config)
│   └── urls.py                 (Updated with auth routes)
└── manage.py
```

### Frontend

```
frontend/src/
├── lib/
│   └── api.ts                  (Centralized API client)
├── stores/
│   ├── auth.ts                 (Session auth state)
│   └── apiKeys.ts              (API keys state)
├── types/
│   └── api.ts                  (TypeScript interfaces)
├── pages/
│   ├── LoginPage.svelte        (Login with email/password)
│   ├── RegisterPage.svelte     (Registration form)
│   ├── Dashboard.svelte        (Main dashboard with keys)
│   ├── Tagger.svelte           (Image tagging playground)
│   └── Usage.svelte            (Usage history)
├── components/
│   ├── Sidebar.svelte          (Navigation & user menu)
│   ├── APIKeyCard.svelte       (Display individual keys)
│   └── ...
└── app.svelte                  (Router configuration)
```

## Troubleshooting

### CORS Error

If you see CORS errors, ensure:
- Backend is running on `http://localhost:8000`
- Frontend is running on `http://localhost:5173`
- `CORS_ALLOWED_ORIGINS` in settings includes both

### Session Cookie Not Set

If login doesn't persist:
- Check browser DevTools → Application → Cookies
- Look for `sessionid` cookie
- Verify `credentials: 'include'` in API client

### API Key Not Working

When using API key for `/api/v1/tag/`:
- Format: `Authorization: Api-Key <key>`
- Not: `Authorization: Bearer <key>`
- Key must be complete (includes prefix)

### Database Issues

```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Production Considerations

1. **Settings.py**: Update to production values
   - `DEBUG = False`
   - `SECRET_KEY` from environment
   - `SESSION_COOKIE_SECURE = True`
   - `ALLOWED_HOSTS` for your domain

2. **Database**: Use PostgreSQL instead of SQLite
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'image_tagging',
           'USER': 'postgres',
           'PASSWORD': 'password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Frontend**: Build for production
   ```bash
   yarn build
   # Deploy dist/ folder
   ```

4. **SSL/HTTPS**: Enable in production

## Need Help?

Refer to:
- `IMPLEMENTATION_GUIDE.md` - Detailed architecture and features
- Django docs: https://docs.djangoproject.com/
- DRF docs: https://www.django-rest-framework.org/
- Svelte docs: https://svelte.dev/
