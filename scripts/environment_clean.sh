#!/bin/sh

set -eu -o pipefail # Fail on error , debug all lines

cd $(dirname $0)/.. && {
    rm -rf ./app/storage_reports
    rm -rf ./app/media/uploads
    rm -rf ./app/db/petereport.sqlite3
}