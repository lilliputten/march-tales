#!/bin/sh

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`
utilsPath="$rootPath/.utils"

# Import config variables...
test -f "$utilsPath/config.sh" && . "$utilsPath/config.sh"
test -f "$utilsPath/config-local.sh" && . "$utilsPath/config-local.sh"

test -f "$utilsPath/check-python-env.sh" && . "$utilsPath/check-python-env.sh"

$RMCMD -Rf "$rootPath/$DJANGO_APP/migrations/__pycache__"
$FINDCMD . -path "$rootPath/$DJANGO_APP/migrations/*.py" -not -name "__init__.py" -delete
$FINDCMD . -path "$rootPath/$DJANGO_APP/migrations/*.pyc" -delete

# TODO: DELETE FROM django_migrations WHERE app = $DJANGO_APP
$RMCMD -f $rootPath/db.* \
&& . "$scriptsPath/django-makemigrations.sh" \
&& echo "All migrations and database has been successfuly cleared"

