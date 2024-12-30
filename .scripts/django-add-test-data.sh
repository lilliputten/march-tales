#!/bin/sh

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`
utilsPath="$rootPath/.utils"

test -f "$utilsPath/check-python-env.sh" && . "$utilsPath/check-python-env.sh"

SITE_YAML="site-real.yaml"
if [[ "$*" =~ .*--local.* ]]; then
  SITE_YAML="site-local.yaml"
fi

echo "Using SITE_YAML:" $SITE_YAML

$PYTHON_RUNTIME manage.py loaddata $SITE_YAML test-users.yaml test-membership.yaml
