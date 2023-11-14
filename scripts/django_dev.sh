#!/bin/sh

set -x

pipenv run ./app/manage.py makemigrations
pipenv run ./app/manage.py migrate
pipenv run ./app/manage.py createfts
pipenv run ./app/manage.py loaddata ./app/config/cwe-list.json
pipenv run ./app/manage.py loaddata ./app/config/cwe-default.json
pipenv run ./app/manage.py loaddata ./app/config/owasp-list.json
pipenv run ./app/manage.py loaddata ./app/config/owasp-default.json
pipenv run ./app/manage.py loaddata ./app/config/cspn-evaluation-stage-list.json
pipenv run ./app/manage.py loaddata ./app/config/cspn-evaluation-stage-default.json
pipenv run ./app/manage.py loaddata ./app/config/data-test.json

set +x
