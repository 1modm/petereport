#!/bin/sh

set -eu -o pipefail # Fail on error , debug all lines

export PIPENV_VERBOSITY=-1

pipenv run ./app/manage.py makemigrations
pipenv run ./app/manage.py migrate
pipenv run ./app/manage.py createfts
pipenv run ./app/manage.py loaddata ./app/config/cwe-list.json
pipenv run ./app/manage.py loaddata ./app/config/cwe-default.json
pipenv run ./app/manage.py loaddata ./app/config/owasp-list.json
pipenv run ./app/manage.py loaddata ./app/config/owasp-default.json
pipenv run ./app/manage.py loaddata ./app/config/cspn-evaluation-stage-list.json
pipenv run ./app/manage.py loaddata ./app/config/cspn-evaluation-stage-default.json
if [ $# -ge 1 ] && [ -n "$1" ] && [ "$1" = "dev" ]; then
    pipenv run ./app/manage.py loaddata ./app/config/data-test.json
fi

cd $(dirname $0)/.. && {
    mkdir -p ./app/storage_reports/{custom,html,images,jupyter,markdown,pdf,pandoc} &&
    mkdir -p ./app/media/uploads
}