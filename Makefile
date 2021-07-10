help: ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

SUPERUSER_NAME=admin
SUPERUSER_EMAIL=admin@test.com
SUPERUSER_PASSWORD=admin

superuser:
	scripts/create_super_user.sh

build-deps:
	pip install pip==21.1.3 setuptools==57.1.0

install:build-deps
	pip install -r requirements.txt

install-dev:build-deps
	pip install -r requirements-dev.txt

reqs:
	pip-compile requirements.in --generate-hashes

reqs-dev:
	pip-compile requirements-dev.in --generate-hashes

reqs-all:
	make reqs
	make reqs-dev

reqs-upgrade:
	pip-compile -U requirements.in

reqs-dev-upgrade:
	pip-compile -U requirements-dev.in


reqs-upgrade-all:
	make reqs-upgrade
	make reqs-dev-upgrade

run:
	python manage.py runserver

reset-migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./venv/*" -delete -print

regenerate-migrations:
	rm db.sqlite3
	make reset-migrations
	make migrations
	make migrate
	make superuser

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

dbschema:
	python manage.py graph_models -a -o "db_schema_$(shell date  +%Y%m%d%H%M%S).png"

shell_plus:
	python manage.py shell_plus
