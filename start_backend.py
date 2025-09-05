#!/usr/bin/env python3
"""
Karachuonyo Website Backend Startup Script
Simplified script to start the backend server with proper configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_dependencies():
    """Install required dependencies"""
    requirements_file = Path('backend/requirements.txt')
    
    if not requirements_file.exists():
        print("Error: requirements.txt not found in backend directory")
        return False
    
    print("Installing dependencies...")
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
        ], check=True)
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('backend/.env')
    env_example = Path('backend/.env.example')
    
    if env_file.exists():
        print(".env file already exists")
        return True
    
    if not env_example.exists():
        print("Warning: .env.example not found")
        return True
    
    print("Creating .env file from .env.example...")
    try:
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            content = src.read()
            # Set development defaults
            content = content.replace('your-secret-key-here-change-in-production', 'karachuonyo-dev-key-2024')
            content = content.replace('your-app-password-here', 'dev-password-change-me')
            dst.write(content)
        
        print(".env file created successfully!")
        print("\nIMPORTANT: Please edit backend/.env file with your actual email credentials")
        return True
    except Exception as e:
        print(f"Error creating .env file: {e}")
        return False

def start_backend_server():
    """Start the Flask backend server"""
    backend_dir = Path('backend')
    app_file = backend_dir / 'app.py'
    
    if not app_file.exists():
        print("Error: backend/app.py not found")
        return False
    
    print("Starting Karachuonyo Backend Server...")
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to backend directory and run the app
        os.chdir(backend_dir)
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("Karachuonyo Website Backend Startup")
    print("====================================")
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Check if we're in the right directory
    if not Path('backend').exists():
        print("Error: backend directory not found")
        print("Please run this script from the project root directory")
        return 1
    
    # Install dependencies
    print("\n1. Checking dependencies...")
    if not install_dependencies():
        return 1
    
    # Create .env file
    print("\n2. Setting up configuration...")
    if not create_env_file():
        return 1
    
    # Start server
    print("\n3. Starting backend server...")
    if not start_backend_server():
        return 1
    
    return 0

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nStartup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)