#!/bin/bash
echo "Installing dependencies..."
python3 -m pip install -r requirements.txt --break-system-packages

echo "Running database migrations..."
python3 manage.py migrate --noinput

echo "Seeding database..."
python3 manage.py seed_db

echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "Build complete."
