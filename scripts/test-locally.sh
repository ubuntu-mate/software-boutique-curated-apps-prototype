#!/bin/bash
#
# Builds and hosts a web server for testing locally.
#

cd "$(dirname '$0')"
local_cache="~/.cache/software-boutique"

# (1) Build the index first.
echo "Building index..."
python3 ./build-index.py
if [ ! $? == 0 ]; then exit 1; fi

# (2) Prepare what will appear on the web server
echo "Preparing for distribution..."
./post-build.sh
if [ ! $? == 0 ]; then exit 1; fi

# (3) Ensure Welcome "downloads" the local server copy.
if [ -d "$local_cache" ]; then
    rm -rf "$local_cache"
fi

# (4) Host the web server for testing.
cd ../dist/
python -m SimpleHTTPServer 8000
