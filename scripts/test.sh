#!/bin/bash
#
# Runs a suite of tests to check the integrity of the index.
#
# This can be completed automatically (mainly CI) and follow a series of rules.
#

cd $(dirname "$0")/../tests/
success=true

for test in $(ls *.py)
do
    echo "---------- $test ----------"
    ./$test
    if [ ! $? == 0 ]; then
        success=false
        echo -e "FAILED!\n"
    else
        echo -e "PASSED!\n"
    fi
done
