release: python manage.py makemigrations
release: python manage.py migrate
release: python manage.py init_db
web: gunicorn --pythonpath purbeurre_project purbeurre_project.wsgi
