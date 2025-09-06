# Karachuonyo Website Deployment Guide

This guide provides step-by-step instructions for deploying the Karachuonyo website on Render.

## Prerequisites

- GitHub repository with the website code
- Render account (free tier available)
- Email account for contact form functionality (Gmail recommended)

## Deployment Architecture

The website consists of two main components:
1. **Frontend**: Static HTML/CSS/JS files served by Render's static site service
2. **Backend**: Flask API server for contact forms, newsletter, and dynamic functionality
3. **Database**: PostgreSQL database for storing submissions and user data

## Step 1: Prepare Your Repository

1. Ensure all files are committed to your GitHub repository
2. Verify the following files exist:
   - `render.yaml` (Blueprint configuration)
   - `Procfile` (Process definition)
   - `build.sh` (Build script)
   - `backend/requirements.txt` (Python dependencies)
   - `backend/.env.example` (Environment variables template)

## Step 2: Deploy on Render

### Option A: Using Render Blueprint (Recommended)

1. Log in to your Render dashboard
2. Click "New" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Review the services that will be created:
   - `karachuonyo-backend` (Web Service)
   - `karachuonyo-frontend` (Static Site)
   - `karachuonyo-db` (PostgreSQL Database)
6. Click "Apply" to start deployment

### Option B: Manual Service Creation

If you prefer to create services manually:

#### Backend Web Service
1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `karachuonyo-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Plan**: Free (or paid for better performance)

#### Frontend Static Site
1. Click "New" → "Static Site"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `karachuonyo-frontend`
   - **Build Command**: `./build.sh`
   - **Publish Directory**: `.`

#### Database
1. Click "New" → "PostgreSQL"
2. Configure:
   - **Name**: `karachuonyo-db`
   - **Plan**: Free (or paid for production)

## Step 3: Configure Environment Variables

Set the following environment variables in your backend web service:

### Required Variables
```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key-here
PORT=10000

# Email Configuration (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Database (automatically set by Render)
DATABASE_URL=postgresql://...

# CORS Origins
CORS_ORIGINS=https://your-frontend-url.onrender.com,https://karachuonyofirst.com

# Admin Configuration
ADMIN_EMAIL=admin@karachuonyofirst.com
ADMIN_PASSWORD=secure-admin-password
```

### Setting Up Gmail App Password

1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account settings → Security → App passwords
3. Generate a new app password for "Mail"
4. Use this password in the `MAIL_PASSWORD` environment variable

## Step 4: Update Frontend API URLs

The build script automatically updates API endpoints, but verify:

1. Check that HTML files reference the correct backend URL
2. Update any hardcoded localhost URLs to your Render backend URL
3. Format: `https://karachuonyo-backend.onrender.com`

## Step 5: Custom Domain (Optional)

### For Frontend
1. In Render dashboard, go to your static site
2. Click "Settings" → "Custom Domains"
3. Add your domain (e.g., `karachuonyofirst.com`)
4. Update your DNS records as instructed

### For Backend API
1. In Render dashboard, go to your web service
2. Click "Settings" → "Custom Domains"
3. Add API subdomain (e.g., `api.karachuonyofirst.com`)
4. Update CORS_ORIGINS environment variable

## Step 6: Monitoring and Maintenance

### Health Checks
- Backend health endpoint: `https://your-backend-url.onrender.com/health`
- Monitor service logs in Render dashboard

### Database Management
- Access database via Render dashboard
- Use provided connection string for external tools
- Regular backups recommended for production

### Performance Optimization
- Consider upgrading to paid plans for better performance
- Enable CDN for static assets
- Monitor response times and error rates

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check build logs in Render dashboard
   - Verify all dependencies in requirements.txt
   - Ensure Python version compatibility

2. **Email Not Working**
   - Verify Gmail app password is correct
   - Check MAIL_USERNAME and MAIL_PASSWORD variables
   - Test with health check endpoint

3. **CORS Errors**
   - Update CORS_ORIGINS with correct frontend URL
   - Ensure both HTTP and HTTPS URLs are included

4. **Database Connection Issues**
   - Verify DATABASE_URL is set correctly
   - Check database service is running
   - Review connection logs

### Support Resources

- Render Documentation: https://render.com/docs
- Flask Documentation: https://flask.palletsprojects.com/
- Contact: admin@karachuonyofirst.com

## Security Considerations

1. **Environment Variables**: Never commit sensitive data to repository
2. **HTTPS**: Always use HTTPS in production
3. **CORS**: Restrict origins to your domains only
4. **Database**: Use strong passwords and regular backups
5. **Rate Limiting**: Monitor and adjust rate limits as needed

## Cost Estimation

### Free Tier
- Static Site: Free
- Web Service: 750 hours/month free
- PostgreSQL: 1GB storage free
- Custom domains: Free

### Paid Plans
- Web Service: $7/month for better performance
- Database: $7/month for 1GB+ storage
- Additional features and support available

---

**Note**: This deployment guide assumes you're using the free tier. For production websites with high traffic, consider upgrading to paid plans for better performance and reliability.