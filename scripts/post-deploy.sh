#!/bin/sh
set -eu

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Building Tailwind CSS..."
python manage.py tailwind build

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Post-deploy tasks completed."
