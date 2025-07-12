#!/bin/bash
set -e

echo "📦 Activating migrate.."
python manage.py migrate --noinput

echo "🗃️ Collecting static files.."
python manage.py collectstatic --noinput

echo "🛠️ Creating superuser, if he is exist... "
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if all([username, email, password]):
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print("✅ Super user create.")
    else:
        print("ℹ️ Super user already exist.")
    
else:
    print("❌ DJANGO_SUPERUSER*. Environment not set - user not created.")
EOF

echo "🚀 Starting Gunincorn..."
exec gunicorn Resume.wsgi:application -b 0.0.0.0:8000
exec "$@"