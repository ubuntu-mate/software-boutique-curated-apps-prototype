#!/usr/bin/python3
#
# Validates and compiles the application index for use with Software Boutique.
#
# This script assembles the index and assets that will be used.
# Output dir: dist/
#
# Copyright 2018-2019 Luke Horwell <code@horwell.me>
#
# Software Boutique is free software: you can redistribute it and/or modify
# it under the temms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Software Boutique is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Software Boutique. If not, see <http://www.gnu.org/licenses/>.
#

import os
import glob
import inspect
import json
import shutil
import sys
import time
import subprocess

colours_supported = sys.stdout.isatty()
def print_msg(color, string):
    """
    color
        1 = Error (Red)
        2 = Success (Green)
        3 = Warning (Yellow)
        4 = Info (Blue)
    """
    if colours_supported:
        print("\033[9{0}m{1}\033[0m".format(str(color), string))
    else:
        print(string)


# Paths and Variables
repo_root = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()) + "/../"))
source_folder = os.path.join(repo_root, "apps/")
compiled_folder = os.path.join(repo_root, "dist/")
localised_folder = os.path.join(repo_root, "locales/")

# Determine locales that have been translated.
locale_dir = glob.glob(localised_folder + "/*/*.po")
raw_locales = []
for locale in locale_dir:
    locale_id = os.path.basename(locale.split("/")[-1][:-3])
    raw_locales.append(locale_id)

locales = []
print_msg(7, "Locales used:")
for locale in raw_locales:
  if locale not in locales:
    locales.append(locale)
    print_msg(4, "- " + locale)

# Perform validation prior to build.
print_msg(4, "\nValidating Index...")
validator = subprocess.Popen(os.path.join(repo_root, "tests", "auto", "validate-metadata.py"), shell=True, stdout=subprocess.PIPE)
validator.wait()
if not validator.returncode == 0:
    print_msg(1, "\nValidation Failed!")
    print_msg(1, "Please fix the index before building.")
    print_msg(1, "===========================================")
    print(validator.communicate()[0].decode("ascii"))
    print_msg(1, "===========================================\n")
    exit(1)
else:
    print_msg(2, "Validation OK!")

# Begin!
print_msg(4, "\nCompiling index...")
categories = os.listdir(source_folder)
categories.sort()
new_index = {}

# Clear the previous compiled state
if os.path.exists(compiled_folder):
    shutil.rmtree(compiled_folder)
os.mkdir(compiled_folder)
for folder in ["icons", "screenshots"]:
    os.mkdir(compiled_folder + folder)

# Add each application.
for category in categories:
    new_index[category] = {}
    apps = os.listdir(os.path.join(source_folder, category))
    apps.sort()

    for appid in apps:
        # Spaces are not allowed in app IDs.
        if appid.find(" ") != -1:
            print_msg(1, "{0}/{1} = Spaces are not allowed in app ID.".format(category, appid))
            continue

        # Is there config stored for this?
        json_path = os.path.join(source_folder, category, appid, "metadata.json")
        if not os.path.exists(json_path):
            print_msg(1, "{0}/{1} = Missing metadata.json!".format(category, appid))
            continue

        # Load JSON Index
        try:
            with open(json_path) as f:
                index = json.load(f)
        except Exception as e:
            print_msg(1, "{0}/{1} = Corrupt metadata.json! (Exception: {2})".format(category, appid, str(e)))
            continue

        # If unlisted, skip this.
        try:
            if index["listed"] == False:
                print_msg(3, "{0}/{1} = Marked as unlisted.".format(category, appid))
                continue
        except Exception:
            print_msg(1, "{0}/{1} = No 'listed' key.".format(category, appid))
            break

        # Add to compiled index
        new_index[category][appid] = index
        source_dir = os.path.join(source_folder, category, appid)
        shutil.copyfile(os.path.join(source_dir, "icon.png"), os.path.join(compiled_folder, "icons", appid + ".png"))
        file_list = os.listdir(os.path.join(source_dir))
        for filename in file_list:
            if filename.startswith("screenshot-"):
                screenshot_no = filename.split("-")[1][:1]
                shutil.copyfile(os.path.join(source_dir, filename), os.path.join(compiled_folder, "screenshots", appid + "-" + str(screenshot_no) + ".jpg"))

# Compile statistics
categories_no = 0
apps_no = 0
for category in new_index.keys():
    if category not in ["unlisted", "stats"]:
        categories_no += 1
        category_apps = new_index[category].keys()
        apps_no += len(category_apps)

new_index["stats"] = {
    "categories": categories_no,
    "apps": apps_no,
    "compiled": int(time.time())
}

# Save new index to file
new_index_path = os.path.join(compiled_folder, "applications-en.json")
with open(new_index_path, 'w') as f:
    json.dump(new_index, f, sort_keys=True)

# Now assemble translatable versions of the index.
print_msg(4, "\nCompiling localised indexes...")

def copy_original_index():
    with open(new_index_path) as f:
        data = json.load(f)
    return data

for locale in locales:
    print("=> " + locale, end=" : ")
    localised_index = copy_original_index()
    for category in categories:
        apps = os.listdir(os.path.join(source_folder, category))
        for appid in apps:
            try:
                # Only translate the app if a PO file exists for it.
                if os.path.exists(os.path.join(localised_folder, appid, locale + ".po")):
                    print(".", end="")
                    temp_json = "/tmp/" + appid + ".json"
                    # po2json "damages" the structure, so just take what we need.
                    os.system("po2json {0}/{1}/{2}.po -t {3}/{4}/{1}/metadata.json -o ".format(localised_folder, appid, locale, source_folder, category) + temp_json + " --progress none")
                    with open(temp_json) as f:
                        index = json.load(f)
                    os.remove(temp_json)
                    localised_index[category][appid]["name"] = index["name"]
                    localised_index[category][appid]["summary"] = index["summary"]
                    localised_index[category][appid]["description"] = index["description"]
                    localised_index[category][appid]["developer-name"] = index["developer-name"]
            except Exception:
                print_msg(1, "{0}/{1} = Failed to translate metadata!".format(category, appid))
                continue
    print("")

    # Save this localised index
    with open(os.path.join(compiled_folder, "applications-" + locale + ".json"), 'w') as f:
        json.dump(localised_index, f, sort_keys=True)

print_msg(2, "Index compiled.\n")
