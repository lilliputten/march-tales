#!/bin/sh

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`
utilsPath="$rootPath/.utils"

# Import config variables...
test -f "$utilsPath/config.sh" && . "$utilsPath/config.sh"
test -f "$utilsPath/check-python-env.sh" && . "$utilsPath/check-python-env.sh"

$PYTHON_RUNTIME manage.py makemessages \
  --ignore ".venv" \
  --ignore "node_modules" \
  --ignore "static" \
  --ignore "media" \
  --ignore "tales_django/templates/admin" \
  --extension html,txt,py,django \
  --all
