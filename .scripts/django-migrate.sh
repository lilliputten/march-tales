#!/bin/sh

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`
utilsPath="$rootPath/.utils"

# Import config variables...
test -f "$utilsPath/config.sh" && . "$utilsPath/config.sh"
test -f "$utilsPath/check-python-env.sh" && . "$utilsPath/check-python-env.sh"

# TODO: DELETE FROM django_migrations WHERE app = $DJANGO_APP
echo "Migrate..." \
&& $PYTHON_RUNTIME manage.py migrate \
&& echo "Done"

