#!/bin/bash
# Karachuonyo Website Build Script for Render Deployment

set -e  # Exit on any error

echo "Starting Karachuonyo website build process..."

# Define production API URL
PROD_API_URL="https://karachuonyo-backend.onrender.com"
DEV_API_URL="http://localhost:5000"

# Function to update API endpoints in HTML files
update_api_endpoints() {
    echo "Updating API endpoints to production URLs..."
    
    # Update all HTML files to use production API URL
    find . -name "*.html" -not -path "./backend/*" -not -path "./build/*" | while read -r file; do
        if [ -f "$file" ]; then
            echo "Updating $file"
            # Replace localhost API calls with production URL
            sed -i "s|${DEV_API_URL}|${PROD_API_URL}|g" "$file"
            # Also handle any other localhost references
            sed -i "s|http://127.0.0.1:5000|${PROD_API_URL}|g" "$file"
        fi
    done
}

# Function to optimize images (if needed)
optimize_assets() {
    echo "Optimizing assets for production..."
    
    # Ensure images directory exists
    if [ ! -d "images" ]; then
        echo "Warning: images directory not found"
        return 1
    fi
    
    # Count images
    image_count=$(find images -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.svg" \) | wc -l)
    echo "Found $image_count images in images directory"
}

# Function to validate HTML files
validate_html() {
    echo "Validating HTML files..."
    
    # Check if main files exist
    required_files=("index.html" "news-article.html")
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            echo "Error: Required file $file not found"
            exit 1
        else
            echo "✓ $file found"
        fi
    done
}

# Function to create production environment file
create_prod_env() {
    echo "Creating production environment configuration..."
    
    # Create a production-ready .env file in backend
    cat > backend/.env.prod << EOF
# Production Environment Configuration
FLASK_ENV=production
SECRET_KEY=\${SECRET_KEY}
PORT=\${PORT}

# Email Configuration
MAIL_SERVER=\${MAIL_SERVER}
MAIL_PORT=\${MAIL_PORT}
MAIL_USERNAME=\${MAIL_USERNAME}
MAIL_PASSWORD=\${MAIL_PASSWORD}
MAIL_DEFAULT_SENDER=\${MAIL_DEFAULT_SENDER}

# Database
DATABASE_URL=\${DATABASE_URL}

# CORS
CORS_ORIGINS=\${CORS_ORIGINS}

# Admin
ADMIN_EMAIL=\${ADMIN_EMAIL}
ADMIN_PASSWORD=\${ADMIN_PASSWORD}
EOF

    echo "✓ Production environment file created"
}

# Main build process
main() {
    echo "========================================"
    echo "Karachuonyo Website Production Build"
    echo "========================================"
    
    # Validate files
    validate_html
    
    # Update API endpoints
    update_api_endpoints
    
    # Optimize assets
    optimize_assets
    
    # Create production environment
    create_prod_env
    
    echo "========================================"
    echo "Build completed successfully!"
    echo "Frontend ready for static deployment"
    echo "Backend ready for Python web service"
    echo "========================================"
}

# Run main function
main "$@"