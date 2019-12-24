web: gunicorn textile.wsgi
release: python manage.py makemigrations
release: python manage.py migrate
release: python heroku_init.py
