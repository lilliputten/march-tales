#!/bin/sh

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`
utilsPath="$rootPath/.utils"

# Import config variables...
test -f "$utilsPath/config.sh" && . "$utilsPath/config.sh"
test -f "$utilsPath/check-python-env.sh" && . "$utilsPath/check-python-env.sh"

echo "Cleaning all the migrations..."
$RMCMD -Rf "$rootPath/$DJANGO_APP/migrations/__pycache__"
$FINDCMD . -path "$rootPath/$DJANGO_APP/migrations/*.py" -not -name "__init__.py" -delete
$FINDCMD . -path "$rootPath/$DJANGO_APP/migrations/*.pyc" -delete

if [ -f "$rootPath/db.sqlite3" ]; then
  TIMETAG=`$DATECMD +%y%m%d-%H%M`
  echo "Backing up sqlite database..."
  mv -vf "$rootPath/db.sqlite3" "$rootPath/db-backup-${TIMETAG}.sqlite3"
fi

# TODO: DELETE FROM django_migrations WHERE app = $DJANGO_APP
"$scriptsPath/django-makemigrations.sh" \
&& echo "All migrations and database has been successfuly cleared"

