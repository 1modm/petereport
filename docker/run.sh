#!/bin/sh

cd /opt/petereport && {
    mkdir -p ./app/storage_reports/html &&
    mkdir -p ./app/storage_reports/images &&
    mkdir -p ./app/storage_reports/jupyter &&
    mkdir -p ./app/storage_reports/markdown &&
    mkdir -p ./app/storage_reports/pdf &&
    pipenv install --deploy --ignore-pipfile --python 3.9 &&
    pip freeze &&
    pipenv run ./app/manage.py makemigrations &&
    pipenv run ./app/manage.py migrate &&
    pipenv run ./app/manage.py createfts &&
    pipenv run ./app/manage.py loaddata ./app/config/cwe-list.json &&
    pipenv run ./app/manage.py loaddata ./app/config/cwe-default.json &&
    pipenv run ./app/manage.py loaddata ./app/config/owasp-list.json &&
    pipenv run ./app/manage.py loaddata ./app/config/owasp-default.json &&
    pipenv run gunicorn --chdir ./app petereport.wsgi:application --timeout 120 --graceful-timeout 60 --bind 127.0.0.1:8000
}