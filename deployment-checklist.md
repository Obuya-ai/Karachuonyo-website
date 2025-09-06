
# Karachuonyo Website Deployment Checklist

## Pre-Deployment
- [ ] All code committed to GitHub repository
- [ ] Environment variables configured (see render-env-vars.txt)
- [ ] Gmail app password generated for email functionality
- [ ] Domain name configured (if using custom domain)

## Render Setup
- [ ] Render account created
- [ ] GitHub repository connected to Render
- [ ] Blueprint deployment initiated (render.yaml)
- [ ] Environment variables set in Render dashboard
- [ ] Database service created and connected

## Post-Deployment
- [ ] Health check endpoint responding: /health
- [ ] Contact form functionality tested
- [ ] Newsletter subscription tested
- [ ] Email notifications working
- [ ] Frontend loading correctly
- [ ] All images displaying properly
- [ ] Custom domain configured (if applicable)
- [ ] SSL certificate active

## Monitoring
- [ ] Service logs reviewed for errors
- [ ] Performance metrics monitored
- [ ] Backup strategy implemented
- [ ] Error alerting configured

## URLs to Test
- Frontend: https://karachuonyo-frontend.onrender.com
- Backend Health: https://karachuonyo-backend.onrender.com/health
- Contact Form: Test form submission
- Newsletter: Test subscription
