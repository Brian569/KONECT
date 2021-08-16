serve:
	python3 manage.py runserver

migrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

static:
	python3 manage.py collectstatic

user:
	python3 manage.py createsuperuser

freeze:
	pip freeze > requirements.txt


