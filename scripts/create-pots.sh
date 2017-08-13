#!/bin/bash
#
# Creates templates (.pot) for translating the index metadata.
#
# Uses locales specified in sources/locales/
#
repo_root=`realpath $(dirname $0)/../`

# Pre-checks - are these packages present?
bin_check="$(which json2po)"
if [ ! $? == 0 ]; then
    echo "Please install translate-toolkit"
    exit 1
fi

bin_check="$(which pygettext)"
if [ ! $? == 0 ]; then
    echo "Please install gettext"
    exit 1
fi

# Create POT files for each application
cd "$repo_root"
echo -e "Generating POTs for curated applications."
for category in $(ls source/apps/); do
    echo -n " -- $category : "
    for app in $(ls source/apps/$category/); do
        echo -n "."
        source="source/apps/$category/$app/"
        target="source/locales/$app/"
        mkdir -p $target
        json2po $source/metadata.json -P $target/$app.pot --filter name,summary,description,developer-name --progress none
    done
    echo ""
done

# Delete obsolete app locales
echo -e "Deleting any obsolete app locales..."
for app in $(ls source/locales/); do
    results=$(find source/apps/ -name "$app" | wc -l)
    if [ $results -eq 0 ]; then
        echo " -- Removed '$app'."
        rm -r "source/locales/$app"
    fi
done
