deploy:
	git pull origin main
	pip install -r requirements.txt
	python manage.py migrate
	python manage.py collectstatic --no-input

install:
	pip install -r requirements.txt
	python manage.py migrate
	python manage.py loaddata fixtures/easytribute.json
	python manage.py createsuperuser --user admin --email admin@example.com

migrate:
	python manage.py migrate

run:
	python manage.py runserver

sass-watch:
	sass --watch ./scss/styles.scss ./static/css/styles.css --style compressed

make workon-venv:
	workon easytribute-virtualenv