#!/bin/sh
# vim: ft=sh
# @desc Config variables (common version -- stored in repository)
# @changed 2024.12.01, 02:46

IS_WINDOWS=`echo "${OS}" | grep -i windows`
IS_CYGWIN=`uname | grep -i "CYGWIN"`

APP_ID=`git ls-remote --get-url | xargs basename -s .git`

# Project structure setup
# BUILD_FOLDER="build"
# PUBLIC_FOLDER="public"
# PUBLISH_FOLDER="publish-${APP_ID}"
# PUBLISH_BRANCH="publish-${APP_ID}"
# DIST_REPO comes from the actual git configuration

# This file is a project-wide source of truth for version info
VERSION_FILE="project-version.txt"

# Misc generated files (see update-build-variables.sh)
PROJECT_INFO_FILE="static/project-info.txt"
# PROJECT_INFO_JSON_FILE="lib/project-info.json"

SRC_TAG_PREFIX="v" # "v" for default "v.X.Y.Z"

# Timezone for timestamps (GMT, Europe/Moscow, Asia/Bangkok, Asia/Tashkent, etc)
TIMEZONE="Europe/Moscow"

# TODO: To use generic `init-crossplatform-command-names.sh`?
PYTHON_RUNTIME="python"
FINDCMD="find"
SORTCMD="sort"
GREPCMD="grep"
RMCMD="rm"
# # Override posix commands for cygwin or/and windows (may be overrided in `config-local.sh`, see `config-local.sh.TEMPLATE`)...
if [ "$IS_CYGWIN" ]; then
    # Don't use windows' own native commands
    FINDCMD="find_"
    SORTCMD="sort_"
    GREPCMD="grep_"
fi
