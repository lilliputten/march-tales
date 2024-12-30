#!/bin/sh

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
# rootPath=`dirname "$scriptsPath"`
# utilsPath="$rootPath/.utils"

. "$scriptsPath/django-clear-migrations.sh"
. "$scriptsPath/django-add-test-data.sh" $*
