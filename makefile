NAME ?= teste

code-convention:
	flake8
	pycodestyle

create-venv:
	virtualenv -p /usr/bin/python3.10 .venv

install:
	python3 -m pip install --upgrade pip
	pip install -r infra/libs/requirements.txt

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +

run:
	python3 "app/run.py"

run-migration:
	python3 "infra/data/db_migration/gen_data.py"

compose-example:
	docker compose -f infra/dockerfiles/docker-compose-example.yaml up -d