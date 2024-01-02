deploy:
	git pull origin main
	pip install -r requirements.txt
	python manage.py migrate
	python manage.py collectstatic --no-input

install:
	pip install -r requirements.txt
	python manage.py migrate
	python manage.py loaddata fixtures/easytribute.json
	python manage.py createsuperuser

runserver:
	python manage.py runserver

sass-watch:
	sass --watch ./scss/styles.scss ./static/css/styles.css