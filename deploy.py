#!/usr/bin/env python3
"""
Karachuonyo Website Deployment Preparation Script
Prepares the website for deployment on Render
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*50)
    print(f" {title}")
    print("="*50)

def print_step(step, description):
    """Print a formatted step"""
    print(f"\n[{step}] {description}")

def check_requirements():
    """Check if all required files exist"""
    print_step("1", "Checking deployment requirements...")
    
    required_files = [
        "render.yaml",
        "Procfile",
        "build.sh",
        "backend/app.py",
        "backend/requirements.txt",
        "backend/config.py",
        "index.html"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✓ {file_path}")
    
    if missing_files:
        print("\n❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("\n✅ All required files present")
    return True

def update_api_endpoints():
    """Update API endpoints in HTML files for production"""
    print_step("2", "Updating API endpoints for production...")
    
    # Production API URL (will be updated after deployment)
    prod_api_url = "https://karachuonyo-backend.onrender.com"
    dev_api_url = "http://localhost:5000"
    
    html_files = ["index.html", "news-article.html"]
    
    for html_file in html_files:
        if os.path.exists(html_file):
            print(f"Updating {html_file}...")
            
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace localhost URLs with production URLs
            updated_content = content.replace(dev_api_url, prod_api_url)
            updated_content = updated_content.replace("http://127.0.0.1:5000", prod_api_url)
            
            # Create backup
            backup_file = f"{html_file}.backup"
            shutil.copy2(html_file, backup_file)
            print(f"   Backup created: {backup_file}")
            
            # Write updated content
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"   ✓ {html_file} updated")
        else:
            print(f"   ⚠️  {html_file} not found")

def validate_backend():
    """Validate backend configuration"""
    print_step("3", "Validating backend configuration...")
    
    # Check Python dependencies
    try:
        with open("backend/requirements.txt", 'r') as f:
            requirements = f.read()
            
        essential_packages = ['Flask', 'gunicorn', 'Flask-CORS', 'Flask-Mail']
        for package in essential_packages:
            if package.lower() in requirements.lower():
                print(f"✓ {package} found in requirements.txt")
            else:
                print(f"❌ {package} missing from requirements.txt")
                
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False
    
    # Check if config.py exists and is importable
    try:
        sys.path.insert(0, 'backend')
        import config
        print("✓ config.py is valid")
    except ImportError as e:
        print(f"❌ config.py import error: {e}")
        return False
    
    return True

def create_env_template():
    """Create environment variables template for Render"""
    print_step("4", "Creating environment variables template...")
    
    env_template = """
# Environment Variables for Render Deployment
# Copy these to your Render service environment variables

# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key-here-generate-new-one
PORT=10000

# Email Configuration (Gmail recommended)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

# Database (automatically provided by Render PostgreSQL)
DATABASE_URL=postgresql://...

# CORS Origins (update with your actual frontend URL)
CORS_ORIGINS=https://karachuonyo-frontend.onrender.com,https://karachuonyofirst.com

# Admin Configuration
ADMIN_EMAIL=admin@karachuonyofirst.com
ADMIN_PASSWORD=secure-admin-password-here

# Rate Limiting
RATE_LIMIT_CONTACT_FORM=5 per minute
RATE_LIMIT_NEWSLETTER=3 per minute
"""
    
    with open("render-env-vars.txt", 'w') as f:
        f.write(env_template)
    
    print("✓ Environment variables template created: render-env-vars.txt")
    print("   Please update the values and set them in your Render service")

def generate_deployment_checklist():
    """Generate deployment checklist"""
    print_step("5", "Generating deployment checklist...")
    
    checklist = """
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
"""
    
    with open("deployment-checklist.md", 'w') as f:
        f.write(checklist)
    
    print("✓ Deployment checklist created: deployment-checklist.md")

def main():
    """Main deployment preparation function"""
    print_header("Karachuonyo Website Deployment Preparation")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    success = True
    
    # Run preparation steps
    if not check_requirements():
        success = False
    
    if success:
        update_api_endpoints()
        
    if success and not validate_backend():
        success = False
    
    if success:
        create_env_template()
        generate_deployment_checklist()
    
    # Final summary
    print_header("Deployment Preparation Summary")
    
    if success:
        print("✅ Deployment preparation completed successfully!")
        print("\nNext steps:")
        print("1. Review and update render-env-vars.txt with your actual values")
        print("2. Push all changes to your GitHub repository")
        print("3. Create a new Blueprint deployment on Render")
        print("4. Set environment variables in Render dashboard")
        print("5. Follow the deployment-checklist.md for verification")
        print("\nFor detailed instructions, see DEPLOYMENT.md")
    else:
        print("❌ Deployment preparation failed!")
        print("Please fix the issues above and run the script again.")
        sys.exit(1)

if __name__ == "__main__":
    main()