# Deploying to Railway

This guide walks you through deploying the Image Tagging Service to [Railway](https://railway.app).

## Prerequisites

- Railway account (free tier available)
- GitHub account (repo connected to Railway)
- Git installed locally

## Step 1: Push to GitHub

Make sure all your code is committed and pushed to GitHub:

```bash
git checkout main
git pull origin main
git push origin main
```

## Step 2: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "GitHub Repo" (or connect your repo if first time)
4. Select your `image_tagging_service` repository
5. Railway will auto-detect it's a Python app and create a service

## Step 3: Configure Backend Service

### 3.1 Environment Variables

In Railway dashboard, go to your service → Variables tab, add:

```
DEBUG=False
SECRET_KEY=your-random-secret-key-here
ALLOWED_HOSTS=your-railway-domain.up.railway.app,yourdomain.com
CORS_ALLOWED_ORIGINS=https://your-railway-domain.up.railway.app,https://yourdomain.com
CSRF_TRUSTED_ORIGINS=https://your-railway-domain.up.railway.app,https://yourdomain.com
DATABASE_URL=postgresql://...
```

### 3.2 Generate SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Copy the output and use it in `SECRET_KEY` variable.

### 3.3 Set Python Version

In `project/backend/runtime.txt`:
```
python-3.11.7
```

### 3.4 Database Setup

**Option A: Use Railway PostgreSQL (Recommended)**

1. In Railway dashboard, click "+ Create"
2. Select "Database" → "PostgreSQL"
3. Railway will auto-populate `DATABASE_URL` environment variable
4. Your backend service will automatically connect

**Option B: Use SQLite (Not recommended for production)**

Skip database creation, SQLite will be used locally.

## Step 4: Configure Frontend Service

### 4.1 Create Frontend Service

1. In Railway dashboard, click "+ Create" 
2. Select "GitHub Repo" → your repo again
3. Configure as Node.js service

### 4.2 Environment Variables

```
VITE_API_BASE_URL=https://your-backend-railway-domain.up.railway.app
NODE_ENV=production
```

### 4.3 Build and Start Commands

**Build Command:**
```
cd frontend && yarn install && yarn build
```

**Start Command:**
```
cd frontend && yarn preview --host 0.0.0.0
```

## Step 5: Deploy

1. Railway will auto-deploy when you push to GitHub
2. Watch the deployment logs in the Railway dashboard
3. Once deployed, you'll get URLs for both services

## Step 6: Test the Deployment

1. Go to your frontend URL
2. Register a new account
3. Generate an API key
4. Check the API Documentation page
5. Test the API with curl:

```bash
curl -X POST https://your-backend-url/api/v1/tag/ \
  -H "Authorization: Api-Key YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/image.jpg",
    "mode": "fast"
  }'
```

## Step 7: Custom Domain (Optional)

1. In Railway dashboard, go to your service
2. Click "Domains" tab
3. Click "Generate Domain" or use your own domain
4. For custom domain, add CNAME records pointing to Railway

## Step 8: Configure HTTPS

Railway automatically provides free HTTPS certificates for Railway domains.

For custom domains, configure SSL in the Domains tab.

## Troubleshooting

### Deployment Failed

1. Check build logs in Railway dashboard
2. Verify `requirements.txt` exists in `project/backend/`
3. Ensure `Procfile` is in root directory
4. Check that Python version is compatible (3.11+)

### Database Connection Issues

1. Verify `DATABASE_URL` environment variable is set
2. Check PostgreSQL service is running
3. Run migrations: Click "Deploy" → "View Logs" to see migration output

### Frontend Not Loading

1. Check `VITE_API_BASE_URL` points to correct backend URL
2. Verify CORS settings in backend match frontend domain
3. Check browser console for CORS errors

### API Requests Failing

1. Verify API key is correct
2. Check Authorization header format: `Api-Key YOUR_KEY` (not Bearer)
3. Verify frontend and backend services are both running

## Production Checklist

- [ ] Generate and set strong `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure PostgreSQL database
- [ ] Set up CORS for your domain
- [ ] Configure CSRF_TRUSTED_ORIGINS
- [ ] Use custom domain with HTTPS
- [ ] Set up email for password reset (optional)
- [ ] Monitor logs and errors
- [ ] Set up backups for database
- [ ] Test API key generation and usage

## Scaling

### Increase Backend Workers

In your backend service, update the Procfile or environment:
```
--workers 8  # Default is 4
```

### Vertical Scaling

In Railway dashboard:
1. Go to your service
2. Click "Resources"
3. Increase CPU and RAM as needed
4. Service will auto-restart with new resources

## Monitoring

Railway provides:
- Live logs
- Deployment history
- Metrics (CPU, memory, requests)
- Alerts (optional)

Access these in the Railway dashboard for your services.

## Support

For Railway-specific issues:
- Check [Railway Docs](https://docs.railway.app)
- Join [Railway Discord](https://discord.gg/railway)

For application issues:
- Check application logs
- Review API documentation page
- Contact support

## Quick Reference

**Frontend URL:** https://your-frontend-railway-domain.up.railway.app  
**Backend URL:** https://your-backend-railway-domain.up.railway.app  
**API Base URL:** https://your-backend-railway-domain.up.railway.app/api/v1

### Common API Endpoints

```bash
# Register
POST /auth/register/

# Login
POST /auth/login/

# Get user info
GET /auth/me/

# Generate API key
POST /keys/

# Tag image (requires API key)
POST /tag/
```

## Cost Estimation

- **Free Tier:** Includes 5GB bandwidth, 512MB RAM per service
- **PostgreSQL:** $5/month for hobby tier (included in some plans)
- **Typical Setup:** $5-20/month depending on usage

Railway offers generous free tier for testing and small projects!

---

Happy deploying! 🚀
