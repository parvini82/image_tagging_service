# 🚀 Hamravesh Quick Start Guide

**Time to Deploy**: ~15 minutes

---

## Step 1: Generate Django Secret Key (2 min)

Run this command locally:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

**Copy the output** - you'll need it in Step 5.

---

## Step 2: Prepare Your Values (3 min)

Gather these values before starting:

```
SECRET_KEY: [output from Step 1]

Your Hamravesh Domain: (will get this after creating app)
Example: your-app.hamravesh.ir

Database URL: (choose one)
Option A: Use Hamravesh PostgreSQL add-on
Option B: External database connection string
Format: postgresql://user:password@host:5432/dbname

Frontend Domain: (if deploying frontend separately)
Example: your-frontend.hamravesh.ir
```

---

## Step 3: Create Application on Hamravesh (2 min)

1. Go to [hamravesh.com](https://hamravesh.com)
2. پنل کاربری (User Panel) → ایجاد اپلیکیشن جدید (Create New Application)
3. Select: **Docker** deployment
4. Repository Source: **GitHub**
5. Authorize and select: `parvini82/image_tagging_service`
6. Branch: `main`
7. Deployment Path: `/`
8. Click: **Next** or **Continue**

---

## Step 4: Add Environment Variables (5 min)

In Hamravesh dashboard, add these variables:

### Copy-Paste These Values:

```
DEBUG=False
SECRET_KEY=[YOUR_SECRET_KEY_FROM_STEP_1]
ALLOWED_HOSTS=your-app.hamravesh.ir
CORS_ALLOWED_ORIGINS=https://your-app.hamravesh.ir
CSRF_TRUSTED_ORIGINS=https://your-app.hamravesh.ir
API_BASE_URL=https://your-app.hamravesh.ir
DATABASE_URL=[YOUR_DATABASE_URL]
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
LOG_LEVEL=INFO
```

### Replace These:
- `[YOUR_SECRET_KEY_FROM_STEP_1]` → Paste your secret key
- `your-app.hamravesh.ir` → Your actual app domain (from Hamravesh)
- `[YOUR_DATABASE_URL]` → Your PostgreSQL connection string

---

## Step 5: Configure Database (2 min)

### Option A: Hamravesh PostgreSQL (Recommended)

1. Go to **Add-ons** in Hamravesh dashboard
2. Click **Add** PostgreSQL
3. Copy the connection string provided
4. Paste in `DATABASE_URL` environment variable
5. Done!

### Option B: External Database

1. Create PostgreSQL database externally:
   - AWS RDS
   - DigitalOcean
   - Any provider
2. Get connection string
3. Paste in `DATABASE_URL` environment variable
4. Make sure database is accessible from Hamravesh

---

## Step 6: Deploy (1 min)

1. Review all settings
2. Click **Deploy** or **استقرار** (Persian)
3. Watch the build logs
4. Wait for deployment to complete (~3-5 minutes)

---

## Step 7: Verify Deployment (1 min)

After deployment completes:

### Check Logs
- Look for "Successfully" messages
- Check for any errors
- Verify database migrations ran

### Test Health Endpoint

```bash
curl https://your-app.hamravesh.ir/api/v1/auth/me/
```

### Expected Response
You should get a 401 (Unauthorized) or similar response.
This means the API is working!

---

## 💨 Troubleshooting Quick Fixes

### "502 Bad Gateway" Error
- Check logs in Hamravesh dashboard
- Verify all environment variables are set
- Ensure database connection is correct
- Wait 2-3 minutes for full startup

### "Connection Refused"
- Check DATABASE_URL is correct
- Verify database credentials
- Ensure database is accessible
- Check firewall rules

### "CORS Errors"
- Verify CORS_ALLOWED_ORIGINS matches your domain
- Verify CSRF_TRUSTED_ORIGINS matches
- Clear browser cache

### Application Won't Start
- Check all environment variables are set
- Verify SECRET_KEY is valid
- Check database migrations in logs
- Ensure no typos in environment variable names

---

## 🔍 View Logs

1. Go to your application on Hamravesh
2. Click **Logs** or **گزارشات**
3. View real-time deployment and error logs
4. Look for key information:
   - Build status
   - Startup messages
   - Database connections
   - Migration status

---

## ✅ Success Checklist

If you see these, your deployment is successful:

- [ ] Application started without errors
- [ ] Health endpoint responds (curl works)
- [ ] Logs show migrations completed
- [ ] Database connection successful
- [ ] No 502/503 errors
- [ ] Can access at your domain

---

## 📚 Full Documentation

For more details, see:

- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Complete guide (10 steps)
- **[DEPLOYMENT_SUMMARY.md](./DEPLOYMENT_SUMMARY.md)** - Summary & checklist
- **[PRODUCTION_READY_CHECKLIST.md](./PRODUCTION_READY_CHECKLIST.md)** - Detailed verification
- **[.hamravesh.env](./.hamravesh.env)** - Environment variables reference

---

## 🌏 What's Deployed

- ✅ Django backend API
- ✅ PostgreSQL database support
- ✅ Security hardening
- ✅ Health checks
- ✅ Static file serving
- ✅ CORS configuration
- ✅ SSL/TLS ready
- ✅ Logging configured

---

## 📐 Environment Variables Reference

| Variable | Value | Required |
|----------|-------|----------|
| `DEBUG` | `False` | Yes |
| `SECRET_KEY` | Your generated key | Yes |
| `ALLOWED_HOSTS` | Your domain | Yes |
| `DATABASE_URL` | PostgreSQL connection | Yes |
| `CORS_ALLOWED_ORIGINS` | Frontend URL | Yes |
| `CSRF_TRUSTED_ORIGINS` | Same as CORS | Yes |
| `SECURE_SSL_REDIRECT` | `True` | Recommended |
| `SESSION_COOKIE_SECURE` | `True` | Recommended |
| `LOG_LEVEL` | `INFO` | Optional |

---

## 🤔 FAQ

**Q: Can I deploy frontend too?**
A: Yes! Deploy separately or as part of docker-compose. Set `VITE_API_BASE_URL` to backend domain.

**Q: How long does deployment take?**
A: 3-5 minutes typically. First deployment may take longer.

**Q: Can I rollback?**
A: Yes! Hamravesh keeps previous deployments. You can revert in dashboard.

**Q: How do I update my app?**
A: Just push to main branch. Hamravesh auto-redeploys.

**Q: Can I scale later?**
A: Yes! Hamravesh lets you upgrade plan and adjust workers.

---

## 🏁 Quick Commands

```bash
# Generate secret key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Test health endpoint (after deployment)
curl https://your-app.hamravesh.ir/api/v1/auth/me/

# Run locally with docker (for testing)
cp .env.example .env
docker-compose up

# Run with PostgreSQL locally
docker-compose --profile local-db up
```

---

## 🗐️ Notes

- Keep your SECRET_KEY private!
- Don't commit `.env` files with real secrets
- Database credentials should be strong
- Monitor application after deployment
- Check logs regularly for errors
- Update dependencies regularly

---

## 📞 Support

- **Hamravesh**: https://hamravesh.com (Persian support available)
- **Django Docs**: https://docs.djangoproject.com/
- **Docker Docs**: https://docs.docker.com/
- **Repository Issues**: GitHub issues tab

---

## ✅ You're Ready!

Your application is production-ready. Follow the 7 steps above to deploy on Hamravesh.

**Questions?** See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed information.

**Happy deploying!** 🚀
