lint:
	isort .
	black . --config myproject.toml
	flake8

install:
	pip install -r requirements/dev.txt

run:
	python manage.py runserver --settings=base.settings.dev

docker:
	docker build -t mingle-api:dev .
	docker tag mingle-api:dev tjdntjr123/mingle-api:dev
	docker push tjdntjr123/mingle-api:dev

m1:
	python manage.py makemigrations

m2:
	python manage.py migrate

reset_db:
	./manage.py reset_db


test_user:
	python manage.py test user

test_box:
	python manage.py test box
