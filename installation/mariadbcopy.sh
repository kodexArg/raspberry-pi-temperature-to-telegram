#!/bin/bash

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

#stop on failure
set -e

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCHE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"

function log_error {
    local readonly message "$1"
    log "ERROR" "$message"
}

function assert_is_installed {
    local readonly name="$1"

    if [[ ! $(command -v ${name}) ]]; then
        log_error "'$name' is required"
        exit 1
    fi
}

function log {
    local readonly level="$1"
    local readonly message="$2"
    local readonly timestamp=$(date +"%Y-%m-%d %H:%M:%S") >&2 echo -e "${timestamp} [${level}]"
}

function run {
    assert_is_installed "mariadb"
    assert_is_installed "mysqldump"
    assert_is_installed "gzip"
    assert_is_installed "aws"
}

function make_backup {
    local BAK="$(echo $HOME/mysql)"
    local MYSQL="$(which mysql)"
    local MYSQLDUMP="$(which mysqldump)"
    local GZIP="$(which gzip)"
    local NOW="$(date +"%d-%m-%Y")"
    #local BUCKET="fillmelater"

    USER="kodex"
    PASS=""
    HOST="localhost"
    DATABASE="rpi"

    [ ! -d "$BAK" ] && mkdir -p "$BAK"

    FILE=$BAK/$DATABASE.$NOW-$(date +"%T").gz

    local SECONDS=0

    $MYSQLDUMP -u $USER -h $HOST -p$PASS $DATABASE | $GZIP -9 > $FILE
    
    duration=$SECONDS

    echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."

    #aws s3 cp $BAK "s3://$BUCKET" --recursive
    
}

run
make_backup


