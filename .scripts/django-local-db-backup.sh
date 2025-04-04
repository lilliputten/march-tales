#!/bin/sh
# @changed 2025.04.03, 01:47
# Call:
# sh .scripts/django-update-db.sh
# sh .scripts/django-update-db.sh --local

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`
utilsPath="$rootPath/.utils"

# Import config variables...
test -f "$utilsPath/config.sh" && . "$utilsPath/config.sh"

if [ -f "$rootPath/db.sqlite3" ]; then
  TIMETAG=`$DATECMD +%y%m%d-%H%M`
  cp -vf "$rootPath/db.sqlite3" "$rootPath/db-backup-${TIMETAG}.sqlite3"
fi
