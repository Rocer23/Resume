#!/bin/bash

echo "📦 Activating migrate.."
python manage.py migrate --noinput

echo "🗃️ Collecting static files.."
python manage.py collectstatic --noinput

echo "🛠️ Creating superuser, if he is exist... "
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("✅ Super user create.")
else:
    print("ℹ️ Super user already exist.")
EOF

echo "🚀 Starting Gunincorn..."
exec gunicorm Resume.wsgi:application -b 0.0.0.0:8000