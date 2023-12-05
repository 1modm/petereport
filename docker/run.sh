#!/bin/sh

cd /opt/petereport && {
    mkdir -p ./app/storage_reports/{custom,html,images,jupyter,markdown,pdf,pandoc} &&
    mkdir -p ./app/media/uploads &&
    pipenv install --deploy --ignore-pipfile --python 3.11 &&
    pip freeze &&
    pipenv run ./app/manage.py makemigrations &&
    pipenv run ./app/manage.py migrate &&
    pipenv run ./app/manage.py createfts &&
    pipenv run ./app/manage.py loaddata ./app/config/cwe-list.json &&
    pipenv run ./app/manage.py loaddata ./app/config/cwe-default.json &&
    pipenv run ./app/manage.py loaddata ./app/config/owasp-list.json &&
    pipenv run ./app/manage.py loaddata ./app/config/owasp-default.json &&
    pipenv run ./app/manage.py loaddata ./app/config/cspn-evaluation-stage-list.json &&
    pipenv run ./app/manage.py loaddata ./app/config/cspn-evaluation-stage-default.json &&
    pipenv run gunicorn --chdir ./app petereport.wsgi:application --timeout 550 --graceful-timeout 60 --bind 127.0.0.1:8000 --workers 2 --threads 2
}