#!/bin/sh

set -eu -o pipefail # Fail on error , debug all lines

cd $(dirname $0)/.. && {
    backup="$(pwd)/backups/petereport_environment.backup.$(date +"%Y-%m-%dT%H:%M:%S%z").tgz"
    tar -cvzf ${backup} ./app/storage_reports ./app/media/uploads ./app/db/petereport.sqlite3
    ls -lh ${backup}
    echo "Backup [OK]"
}