#!/usr/bin/env bash
set -e
. .env
echo "from django.contrib.auth.models import User; User.objects.filter(username='${DEFAULT_SUPERUSER_NAME}').delete()" | python manage.py shell
echo "from django.contrib.auth.models import User; User.objects.create_superuser('${DEFAULT_SUPERUSER_NAME}', '${DEFAULT_SUPERUSER_EMAIL}', '${DEFAULT_SUPERUSER_PASSWORD}')" | python manage.py shell
