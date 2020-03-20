python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py run_huey &
#gunicorn new_shows.wsgi:application -w 2 -b :8000
python manage.py runserver
exec "$@"