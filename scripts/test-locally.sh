#!/bin/bash
#
# Builds and hosts a web server for testing locally.
#

cd "$(dirname $0)"
local_cache="~/.cache/software-boutique"

# (1) Build the index first.
echo -e "\033[93mBuilding index...\033[0m"
python3 ./build-index.py
if [ ! $? == 0 ]; then exit 1; fi

# (2) Prepare what will appear on the web server
echo -e "\033[93mPacking for distribution...\033[0m"
./post-build.sh
if [ ! $? == 0 ]; then exit 1; fi

# (3) Ensure Welcome "downloads" the local server copy.
if [ -d "$local_cache" ]; then
    rm -rf "$local_cache"
fi

# (4) Ready to host the web server for testing.
if [ "$1" == "--build-only" ]; then
    exit 0
else
    cd ../dist/
    touch /tmp/boutique-dev.lock
    python3 -m http.server 8000
fi
