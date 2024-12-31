#!/bin/sh

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`
utilsPath="$rootPath/.utils"

test -f "$utilsPath/check-python-env.sh" && . "$utilsPath/check-python-env.sh"

$PYTHON_RUNTIME manage.py shell
