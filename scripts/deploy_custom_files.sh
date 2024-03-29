#!/bin/sh

set -eu -o pipefail # Fail on error , debug all lines

if [ $# -ge 2 ] && [ -n "$1" ] && [ -n "$2" ] && [ "$2" = "local" ] || [ "$2" = "complete" ]; then
    
    tarfiles=$(mktemp)

    if [ "$1" = "deploy" ]; then
        cd $(dirname $0)/../deploy/custom \
        && tar -cf $tarfiles ./app/ \
        && cd ../.. \
        && tar -cf deploy/original/deploy.tar $(tar -tf $tarfiles|grep -e "[^/]$") \
        && tar -xvf $tarfiles
    fi

    if [ "$1" = "undeploy" ]; then
        cd $(dirname $0)/../ \
        && tar -xvf deploy/original/deploy.tar
    fi
    
    #rm -f $tarfiles
fi