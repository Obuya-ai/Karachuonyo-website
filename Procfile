# Procfile for Render deployment
# Defines how to run the Karachuonyo website backend

web: cd backend && gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app