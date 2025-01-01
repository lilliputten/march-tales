#!/bin/sh
# Call:
# sh .scripts/django-reset-db.sh
# sh .scripts/django-reset-db.sh --local

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`
# utilsPath="$rootPath/.utils"

echo "Starting reset and re-create db and schemas..." \
&& . "$scriptsPath/django-clear-migrations.sh" \
&& . "$scriptsPath/django-add-test-data.sh" $* \
&& touch "$rootPath/index.wsgi" \
&& echo "Done"
