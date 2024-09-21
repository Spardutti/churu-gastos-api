#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install --no-cache-dir -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate
