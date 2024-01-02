deploy:
	git pull origin main
	pip install -r requirements.txt
	python manage.py migrate
	python manage.py collectstatic --no-input
	sass ./scss/styles.scss ./staticfiles/css/styles.css

install:
	pip install -r requirements.txt
	python manage.py migrate
	python manage.py loaddata fixtures/easytribute.json
	python manage.py createsuperuser
	sass ./scss/styles.scss ./static/css/styles.css

runserver:
	python manage.py runserver

sass-watch:
	sass --watch ./scss/styles.scss ./static/css/styles.css