# Karachuonyo Website - Production Deployment

## Overview

This repository contains the complete Karachuonyo political campaign website, ready for production deployment on Render. The website features a modern, responsive design with full backend functionality for contact forms, newsletter subscriptions, and content management.

## Architecture

### Frontend
- **Technology**: Static HTML5, CSS3, JavaScript
- **Features**: Responsive design, interactive components, optimized images
- **Deployment**: Render Static Site service

### Backend
- **Technology**: Python Flask with SQLite/PostgreSQL
- **Features**: Contact forms, newsletter, email notifications, admin panel
- **Deployment**: Render Web Service with Gunicorn

### Database
- **Development**: SQLite
- **Production**: PostgreSQL (Render managed)

## Quick Deployment

### Prerequisites
1. GitHub repository with this code
2. Render account (free tier available)
3. Gmail account for email functionality

### One-Click Deployment

1. **Fork/Clone this repository** to your GitHub account

2. **Run deployment preparation**:
   ```bash
   python deploy.py
   ```

3. **Deploy on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will detect `render.yaml` and create all services

4. **Configure Environment Variables**:
   - Use the generated `render-env-vars.txt` as a template
   - Set variables in Render dashboard for the backend service
   - Generate Gmail app password for email functionality

5. **Verify Deployment**:
   - Follow `deployment-checklist.md` for complete verification
   - Test all functionality before going live

## File Structure

```
karachuonyo-website/
├── 📁 backend/                 # Flask backend application
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Environment configurations
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment variables template
├── 📁 images/                 # Website images and assets
├── 📁 css/                    # Stylesheets
├── 📁 js/                     # JavaScript files
├── index.html                 # Main website page
├── news-article.html          # News article page
├── render.yaml               # Render deployment configuration
├── Procfile                  # Process definition for Render
├── build.sh                  # Build script
├── deploy.py                 # Deployment preparation script
├── DEPLOYMENT.md             # Detailed deployment guide
├── deployment-checklist.md   # Post-deployment verification
├── render-env-vars.txt       # Environment variables template
└── .gitignore               # Git ignore rules
```

## Key Features

### Frontend Features
- ✅ Responsive mobile-first design
- ✅ Interactive navigation and components
- ✅ Optimized image loading
- ✅ Contact form with validation
- ✅ Newsletter subscription
- ✅ Social media integration
- ✅ SEO optimized

### Backend Features
- ✅ RESTful API endpoints
- ✅ Email notifications (Gmail SMTP)
- ✅ Database integration
- ✅ Form validation and security
- ✅ Rate limiting
- ✅ Health monitoring
- ✅ CORS configuration
- ✅ Environment-based configuration

## Environment Variables

Required environment variables for production:

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key
PORT=10000

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Database (auto-provided by Render)
DATABASE_URL=postgresql://...

# CORS Origins
CORS_ORIGINS=https://your-frontend-url.onrender.com

# Admin Configuration
ADMIN_EMAIL=admin@karachuonyofirst.com
ADMIN_PASSWORD=secure-password
```

## API Endpoints

### Public Endpoints
- `GET /health` - Health check
- `POST /api/contact` - Contact form submission
- `POST /api/newsletter/subscribe` - Newsletter subscription
- `GET /api/newsletter/unsubscribe/<token>` - Newsletter unsubscribe

### Admin Endpoints (Future)
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/contacts` - View contact submissions
- `GET /admin/subscribers` - View newsletter subscribers

## Security Features

- ✅ HTTPS enforcement
- ✅ CORS protection
- ✅ Rate limiting
- ✅ Input validation
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Security headers
- ✅ Environment variable protection

## Performance Optimizations

- ✅ Optimized images (SVG preferred)
- ✅ Minified CSS/JS (production)
- ✅ Gzip compression
- ✅ CDN-ready assets
- ✅ Database connection pooling
- ✅ Efficient SQL queries

## Monitoring and Maintenance

### Health Monitoring
- Health check endpoint: `/health`
- Database connectivity verification
- Service status reporting

### Logging
- Application logs in Render dashboard
- Error tracking and alerting
- Performance metrics

### Backup Strategy
- Database backups (Render managed)
- Code repository (GitHub)
- Environment configuration documentation

## Cost Estimation

### Free Tier (Suitable for small campaigns)
- **Static Site**: Free
- **Web Service**: 750 hours/month free
- **PostgreSQL**: 1GB storage free
- **Total**: $0/month

### Paid Tier (Recommended for active campaigns)
- **Static Site**: Free
- **Web Service**: $7/month (better performance)
- **PostgreSQL**: $7/month (1GB+ storage)
- **Total**: ~$14/month

## Support and Maintenance

### Documentation
- `DEPLOYMENT.md` - Detailed deployment instructions
- `deployment-checklist.md` - Post-deployment verification
- This README - Production overview

### Getting Help
- Check Render documentation: https://render.com/docs
- Review application logs in Render dashboard
- Contact: admin@karachuonyofirst.com

## Development Workflow

1. **Local Development**:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   python app.py
   
   # Frontend (separate terminal)
   python -m http.server 8000
   ```

2. **Testing**:
   ```bash
   # Run deployment preparation
   python deploy.py
   
   # Test all functionality locally
   ```

3. **Deployment**:
   ```bash
   # Commit changes
   git add .
   git commit -m "Update for production"
   git push origin main
   
   # Render auto-deploys from main branch
   ```

## License

This project is created for the Karachuonyo political campaign. All rights reserved.

---

**Ready for Production Deployment** ✅

This website is fully configured and ready for deployment on Render. Follow the deployment guide and checklist for a smooth launch.