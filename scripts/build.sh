#!/bin/bash
#
# Checks the environment and runs commands to build the index.
#
cd "$(dirname $0)"

# Check Git is installed
test=$(which git)
if [ $? != 0 ]; then
    echo "Please install 'git' and try again."
fi

# Does this git repository have a full history?
if [ "$(git rev-parse --is-shallow-repository)" != false ]; then
    echo "This is not a valid Git repository or does not contain the full Git history."
    exit 1
fi

# Build the actual index
cd ../
./scripts/build-index.py
