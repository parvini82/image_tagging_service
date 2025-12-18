# Deployment Guide - Image Tagging Service on Hamravesh

This guide provides step-by-step instructions to deploy the Image Tagging Service on Hamravesh.

## Prerequisites

- Hamravesh account ([hamravesh.com](https://hamravesh.com))
- GitHub account with access to this repository
- Docker knowledge (basic understanding)
- PostgreSQL database (or use Hamravesh's managed database)

## Pre-Deployment Changes (COMPLETED)

The following production-ready configurations have been committed to the repository:

### ✅ Files Updated

1. **`.env.production`** - Production environment variables template
   - Contains all necessary environment variables
   - Includes security settings (HSTS, SSL redirect, etc.)
   - Replace placeholder values with your actual settings

2. **`docker-compose.yml`** - Updated for production
   - Uses environment variables for configuration
   - Includes PostgreSQL database service (optional, with `local-db` profile)
   - Added networking and restart policies
   - Proper volume management and logging

3. **`Dockerfile`** - Production optimizations
   - Multi-stage build for smaller image size
   - Non-root user for security
   - Static file collection with error handling
   - Enhanced health checks
   - PostgreSQL client support
   - Optimized gunicorn configuration

4. **`requirements.txt`** - Added production dependencies
   - `psycopg2-binary` - PostgreSQL database driver
   - `gunicorn` - Production WSGI server
   - `python-decouple` - Environment variable management
   - `dj-database-url` - Database URL parsing

## Hamravesh Deployment Steps

### Step 1: Create Hamravesh Account & Project

1. Sign up at [hamravesh.com](https://hamravesh.com)
2. Go to پنل کاربری (User Panel)
3. Click ایجاد اپلیکیشن جدید (Create New Application)
4. Select Docker deployment method

### Step 2: Connect GitHub Repository

1. Click "Connect GitHub" or select repository source
2. Authorize Hamravesh to access your GitHub account
3. Select repository: `parvini82/image_tagging_service`
4. Select branch: `main`
5. Choose deployment path: `/` (root)

### Step 3: Configure Environment Variables

In Hamravesh dashboard, set these critical variables:

#### Security Settings
```
DEBUG=False
SECRET_KEY=<generate-secure-key-e.g.-with-django-shell>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

#### Domain Configuration
```
ALLOWED_HOSTS=your-domain.hamravesh.ir,your-domain.com,www.your-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.hamravesh.ir,https://your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.hamravesh.ir,https://your-domain.com
API_BASE_URL=https://your-api-domain.hamravesh.ir
```

#### Database Configuration
```
DATABASE_URL=postgresql://username:password@hostname:5432/database_name
```

#### Logging
```
LOG_LEVEL=INFO
```

### Step 4: Generate Django Secret Key

Generate a secure SECRET_KEY by running:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Or use online generators (not recommended for production):
https://djecrety.ir/

### Step 5: Database Setup

#### Option A: Use Hamravesh Managed Database

1. In Hamravesh dashboard, go to "Add-ons" or "Services"
2. Add PostgreSQL database
3. Hamravesh provides connection string automatically
4. Use provided DATABASE_URL

#### Option B: Use External PostgreSQL Database

1. Create PostgreSQL database on external provider (AWS RDS, DigitalOcean, etc.)
2. Format DATABASE_URL:
   ```
   postgresql://username:password@hostname:5432/database_name
   ```
3. Ensure database is accessible from Hamravesh IP addresses

### Step 6: Configure Application

1. Set application name
2. Choose plan (start with basic plan)
3. Set port: `8000` (default)
4. Click "Deploy"

### Step 7: Monitor Deployment

1. Watch build logs in real-time
2. Check for any build errors
3. Verify migrations run successfully
4. Monitor startup logs

### Step 8: Post-Deployment Verification

#### Check Health Endpoint
```bash
curl https://your-api-domain.hamravesh.ir/api/v1/auth/me/
```

#### Check Logs
- View application logs in Hamravesh dashboard
- Look for any migration errors
- Verify database connections

#### Database Migrations
If migrations didn't run automatically:
1. SSH into container (if available)
2. Run: `python manage.py migrate`

### Step 9: Custom Domain Setup (Optional)

1. Add custom domain in Hamravesh settings
2. Update DNS records at your domain registrar
3. Point to Hamravesh nameservers or CNAME record
4. Wait for DNS propagation (up to 48 hours)

### Step 10: Frontend Deployment

Deploy frontend separately or alongside backend:

1. Build frontend separately on Hamravesh or
2. Include in docker-compose with separate service
3. Update `VITE_API_BASE_URL` to point to backend domain
4. Deploy to production CDN or Hamravesh

## Troubleshooting

### Common Issues

#### "Connection refused" error
- Check DATABASE_URL format
- Verify database credentials
- Ensure database is accessible
- Check firewall rules

#### "Migration errors"
- Run migrations manually in container
- Check migration files in `project/backend/migrations/`
- Verify database permissions

#### "Static files not serving"
- Ensure `collectstatic` runs successfully
- Check static file paths in Django settings
- Verify `/staticfiles/` directory exists

#### "CORS errors in frontend"
- Update `CORS_ALLOWED_ORIGINS` with correct frontend domain
- Update `CSRF_TRUSTED_ORIGINS` with same value
- Clear browser cache

#### "503 Service Unavailable"
- Check application logs
- Verify health check endpoint
- Ensure sufficient resources allocated
- Check gunicorn worker count

## Performance Optimization

### Gunicorn Workers
In `docker-compose.yml`, adjust workers based on CPU cores:
```bash
--workers=4  # For 2 CPU cores, use: CPU_cores * 2 + 1
```

### Database Connections
```
CONNS_MAX_AGE=600  # Add to Django settings
```

### Caching
Consider implementing Redis for caching:
```
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis-host:6379/1',
    }
}
```

## Monitoring & Logs

### Access Logs
View in Hamravesh dashboard:
- Application logs
- Build logs
- Error logs

### Database Monitoring
- Monitor connection count
- Check query performance
- Set up alerts for errors

## Security Checklist

- [ ] Set `DEBUG=False`
- [ ] Generate secure `SECRET_KEY`
- [ ] Use HTTPS only (`SECURE_SSL_REDIRECT=True`)
- [ ] Enable HSTS
- [ ] Set `ALLOWED_HOSTS` correctly
- [ ] Configure CORS properly
- [ ] Use strong database password
- [ ] Enable SSL on database connection
- [ ] Set up regular backups
- [ ] Monitor for security updates

## Maintenance

### Regular Tasks
1. Monitor application health
2. Review error logs
3. Update dependencies
4. Backup database
5. Update Django security patches

### Scaling
When you need to scale:
1. Increase Hamravesh plan
2. Adjust gunicorn workers
3. Implement caching (Redis)
4. Use CDN for static files
5. Consider load balancing

## Support

- Hamravesh Documentation: https://hamravesh.com/docs
- Django Documentation: https://docs.djangoproject.com/
- Docker Documentation: https://docs.docker.com/

## Version Information

- Python: 3.11
- Django: 5.0+
- Node.js: 18 (for frontend build)
- PostgreSQL: 16 (recommended)
- Gunicorn: 21.0+

---

For questions or issues, refer to the repository's issue tracker or Hamravesh support.
