#!/bin/sh
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

echo "Starting migrate and add test data..." \
&& . "$scriptsPath/django-migrate.sh" \
&& . "$scriptsPath/django-add-test-data.sh" $* \
&& touch "$rootPath/index.wsgi" \
&& echo "Done"
