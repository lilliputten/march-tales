#!/bin/sh

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`
utilsPath="$rootPath/.utils"

# Import config variables...
test -f "$utilsPath/config.sh" && . "$utilsPath/config.sh"
test -f "$utilsPath/check-python-env.sh" && . "$utilsPath/check-python-env.sh"

SITE_YAML="site-real.yaml"
if [[ "$*" =~ .*--local.* ]]; then
  SITE_YAML="site-local.yaml"
fi

echo "Using SITE_YAML:" $SITE_YAML

echo "Adding test data..." \
&& $PYTHON_RUNTIME manage.py loaddata \
  $SITE_YAML \
  test-users.yaml \
  test-tracks.yaml \
  test-membership.yaml \
&& echo "Test data added"
