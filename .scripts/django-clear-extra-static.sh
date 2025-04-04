#!/bin/sh

scriptsPath=$(dirname "$(echo "$0" | sed -e 's,\\,/,g')")
rootPath=`dirname "$scriptsPath"`
utilsPath="$rootPath/.utils"

# Import config variables...
test -f "$utilsPath/config.sh" && . "$utilsPath/config.sh"

echo "Cleaning all the migrations..."
$RMCMD -Rf "$rootPath/static/CACHE"
$RMCMD -Rf "$rootPath/static/assets"
$RMCMD -Rf "$rootPath/static/samples"
$RMCMD -Rf "$rootPath/static/authors"
$RMCMD -Rf "$rootPath/static/tracks"
