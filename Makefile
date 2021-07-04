install:
	pip install -r requirements/dev.txt

run:
	python manage.py runserver --settings=base.settings.dev

docker:
	docker build -t find-city-api:dev .
	docker tag find-city-api:dev tjdntjr123/find-city-api:dev
	docker push tjdntjr123/find-city-api:dev

