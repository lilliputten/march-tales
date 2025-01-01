#!/bin/sh
# Export current data to a yaml file (npm's json2yaml is used)

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`
utilsPath="$rootPath/.utils"

# Import config variables...
test -f "$utilsPath/config.sh" && . "$utilsPath/config.sh"
test -f "$utilsPath/config-local.sh" && . "$utilsPath/config-local.sh"

test -f "$utilsPath/check-python-env.sh" && . "$utilsPath/check-python-env.sh"

DATA_FOLDER=".data"
DATE_ID=`date "+%y%m%d-%H%M"`
FILE_NAME="$DATA_FOLDER/exported-db-$DATE_ID.yaml"
mkdir -p "$DATA_FOLDER"
$PYTHON_RUNTIME manage.py dumpdata | json2yaml > "$FILE_NAME"
echo "See exported file: $FILE_NAME"
