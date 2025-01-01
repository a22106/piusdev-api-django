release: python manage.py migrate
web: python manage.py collectstatic --no-input && gunicorn core.wsgi --log-file -