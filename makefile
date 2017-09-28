export PATH := env/bin:$(PATH)
settings = --settings=api.settings.local

local-all: local-requirements

local-data: local-migrations
	cd api; \
	python manage.py loaddata fixtures/initial.json $(settings)

local-migrations: local-all
	cd api; \
	python manage.py migrate $(settings)

local-venv:
	pip install virtualenv
	test -d env || virtualenv env
	. env/bin/activate

local-requirements: local-venv
	pip install -Ur requirements/dev.txt

local-test: local-migrations
	cd api; \
	python manage.py test $(settings)

local-run: local-data
	cd api; \
	python manage.py runserver $(settings)

docker-migrations: docker-requirements
	docker-compose run web python manage.py migrate

docker-data: docker-migrations
	docker-compose run web python manage.py loaddata fixtures/initial.json

docker-requirements:
	docker-compose build

docker-test: docker-requirements
	docker-compose run web python manage.py test

docker-run: docker-data
	docker-compose up