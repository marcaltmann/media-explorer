#!/bin/sh

npm run build
python manage.py collectstatic --noinput
python manage.py compilemessages
python manage.py migrate

exec "$@"
