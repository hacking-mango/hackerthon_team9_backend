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

docker-asgi:
	docker build -t mingle-api-asgi:dev .
	docker tag mingle-api-asgi:dev tjdntjr123/mingle-api-asgi:dev
	docker push tjdntjr123/mingle-api-asgi:dev

m1:
	python manage.py makemigrations

m2:
	python manage.py migrate

reset_db:
	./manage.py reset_db

create:
	python manage.py createsuperuser --settings=base.settings.dev


test_user:
	python manage.py test user

test_box:
	python manage.py test box
