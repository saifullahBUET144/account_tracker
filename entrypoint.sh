#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Start Gunicorn server for production
echo "Starting Gunicorn server..."
exec gunicorn account_log.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 4 \
    --worker-class=gthread

