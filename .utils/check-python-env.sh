#!/bin/sh
# @desc Check if run under .venv environment
# @changed 2024.12.21, 02:28

PYTHON_RUNTIME=`which python`

echo "$PYTHON_RUNTIME" | grep -q ".venv"

if [ $? = 1 ]; then
  # Is poetry exists?
  if which poetry > /dev/null 2>&1; then
    echo "check-python-env: Using poetry"
    PYTHON_RUNTIME="poetry run python"
  else
    echo "check-python-env: ERROR: No .venv or poetry found!"
    exit 1
  fi
else
  echo "check-python-env: Using .venv"
fi
