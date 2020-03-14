python manage.py collectstatic --noinput
python manage.py process_tasks &
gunicorn new_shows.wsgi:application -w 2 -b :8000
exec "$@"