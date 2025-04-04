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

"$scriptsPath/django-local-db-backup.sh"

echo "Starting migrate and add test data..." \
&& . "$scriptsPath/django-migrate.sh" \
&& . "$scriptsPath/django-add-test-data.sh" $* \
&& touch "$rootPath/index.wsgi" \
&& echo "Done"
