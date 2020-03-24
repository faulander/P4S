python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py firstrun
celery -A new_shows worker --beat --scheduler django --loglevel=info &
#celery -A new_shows worker -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &
gunicorn new_shows.wsgi:application -w 2 -b :8000
#python manage.py runserver
exec "$@"