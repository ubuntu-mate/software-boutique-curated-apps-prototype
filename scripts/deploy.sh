#!/bin/bash

for HOST in man yor; do
    echo "Deploying to: ${HOST}"
    rsync -a -e "ssh -o StrictHostKeyChecking=no" --progress --delete dist/ matey@${HOST}.ubuntu-mate.net:ubuntu-mate.software/
done
