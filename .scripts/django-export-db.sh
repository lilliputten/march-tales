#!/bin/sh

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`
utilsPath="$rootPath/.utils"

# Import config variables...
test -f "$utilsPath/config.sh" && . "$utilsPath/config.sh"
test -f "$utilsPath/config-local.sh" && . "$utilsPath/config-local.sh"

test -f "$utilsPath/check-python-env.sh" && . "$utilsPath/check-python-env.sh"

FILE_NAME=".temp/exported-db.yaml"
mkdir -p .temp
$PYTHON_RUNTIME manage.py dumpdata | json2yaml > "$FILE_NAME"
echo "See exported file: $FILE_NAME"
