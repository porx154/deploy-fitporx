#!/bin/bash
echo "Installing requirements..."
pip install -r requirements.txt --break-system-packages

echo "Collecting static files..."
python3.12 manage.py collectstatic --noinput --clear