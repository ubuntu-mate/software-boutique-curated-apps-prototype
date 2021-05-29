#! /bin/bash

# Root of the folder hierarchy
ROOT=$(dirname ${0})/..

# If no locale was given on the command line, exit
if [ -z ${1} ]
then
    echo "Usage : ${0} locale"
    exit -1
fi

# Store the locale
LOCALE=${1}

# Iterate over every pacakge
for METADATA in $(find ${ROOT}/apps -type f -name "metadata.json")
do
    # If a .po doesn't exist for that app and that locale, create it
    PO=${ROOT}/locales/${APP}/${LOCALE}.po
    if [ ! -f ${PO} ]
    then
        APP=$(basename $(dirname ${METADATA}))
        mkdir -p ${ROOT}/locales/${APP}
        json2po --filter name,summary,description,developper-name ${METADATA} ${ROOT}/locales/${APP}/${LOCALE}.po
    fi
done
