#!/bin/bash
#
# Prepares the contents on the server by compressing them for distribution.
#
# This will be used by the CI or for a local test web server.
#   => dist/
#

cd "$(dirname '$0')"/../

# Initialise a new folder for deployment
if [ -d dist/ ]; then
    rm -r dist/
fi
mkdir dist/
cd dist/

# Add the number
git rev-list --count master > latest_revision

# Compress indexes
cp ../compiled/*.json .
gzip *.json

# Compress application data
cd ../compiled/
tar -cf - icons/ screenshots/ | xz -9 -e > ../dist/application-data.tar.xz     # 8.9 MB
cd ../dist/

# Generate SHA256SUMS for client to verify
sha256sum * > SHA256SUMS

# Sign the SHA256SUMS so client knows it's by us.
# FIXME: Sign SHA256SUMS automatically!
