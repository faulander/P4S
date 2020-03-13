python manage.py collectstatic --noinput
python manage.py run_huey &
gunicorn ADVOKAT.wsgi:application -w 2 -b :8000
exec "$@"