#!/usr/bin/env python3
#
# Copyright 2016-2017 Luke Horwell <code@horwell.me>
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

"""
A utility to diagnose and output useful information about the application
index used by Software Boutique.
"""

import os
import sys
import glob
import json

# Variables
watched_arch = ["i386", "amd64", "armhf"]
watched_releases = ["xenial", "artful"]
watched_methods = ["snap"]

# Output functions
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

def print_colour_only(color, string):
    return("\033[9{0}m{1}\033[0m".format(str(color), string))

def list_to_string(list_data):
    return ', '.join(map(str, list_data))

# Populate indexes
print_msg(3, "Reading indexes...")
os.chdir(os.path.join(os.path.dirname(__file__), "..", "apps"))
categories = glob.glob("*")
indexes = []

for category in categories:
    app_category_paths = glob.glob(category + "/*")
    for path in app_category_paths:
        try:
            json_path = os.path.join(path, "metadata.json")
            with open(json_path) as data_file:
                index = json.load(data_file)
            indexes.append(index)
        except Exception:
            print_msg(1, "Unable to read index: " + path)

# Begin output of stats
print_msg(7, "\nSoftware Boutique Index Inspector")
print_msg(7, "======================================================")
print_msg(3, "There are {0} applications indexed.".format(len(indexes)))

count_open_source = 0
count_proprietary = 0
count_32_bit_apps = 0
for index in indexes:
    if index["proprietary"] == True:
        count_proprietary += 1
    else:
        count_open_source += 1

    try:
        for codename in index["apt"]:
            if index["apt"][codename]["enable-i386"] == True:
                count_32_bit_apps += 1
    except KeyError:
        pass

print("  - Open Source: {0}".format(str(count_open_source)))
print("  - Proprietary: {0}".format(str(count_proprietary)))
print("  - 32-bit apps: {0}".format(str(count_32_bit_apps)))
print("\n")

# How many are marked as unlisted?
unlisted = []
for index in indexes:
    if index["listed"] == False:
        unlisted.append(index["name"])

if len(unlisted) == 0:
    print_msg(2, "There are no unlisted applications.\n")
else:
    print_msg(1, "There are {0} unlisted applications:".format(len(unlisted)))
    for name in unlisted:
        print("  - " + name)
    print("\n")

# Are there any apps unavailable for specific releases?
for release in watched_releases:
    not_present = []
    for index in indexes:
        if not release in index["releases"]:
            not_present.append([index["name"], list_to_string(index["releases"])])

    if len(not_present) == 0:
        print_msg(2, "All applications support '{0}'.\n".format(release))
    else:
        print_msg(3, "These applications are not available for '{0}':".format(release))
        for app in not_present:
            print("  - {0} - {1}".format(app[0], print_colour_only(4, app[1])))
        print("\n")

# Are there any apps unavailable for specific architectures?
for arch in watched_arch:
    not_present = []
    for index in indexes:
        if not arch in index["arch"]:
            not_present.append([index["name"], list_to_string(index["arch"])])

    if len(not_present) == 0:
        print_msg(2, "All applications support '{0}'.\n".format(arch))
    else:
        print_msg(3, "These applications are not available for '{0}':".format(arch))
        for app in not_present:
            print("  - {0} - {1}".format(app[0], print_colour_only(4, app[1])))
        print("\n")

# List how each app is installed
for method in watched_methods:
    matches = []
    for index in indexes:
        if method in index["methods"]:
            matches.append(index["name"])

    if len(matches) == 0:
        print_msg(1, "No applications install via '{0}'.\n".format(method))
    else:
        print_msg(3, "These applications install via '{0}':".format(method))
        for app in matches:
            print("  - {0}".format(app))
        print("\n")

# List apps that support multiple installs
matches = []
for index in indexes:
    if len(index["methods"]) > 1:
        matches.append([index["name"], index["methods"]])

if len(matches) == 0:
    print_msg(2, "All applications only support one installation method.\n")
else:
    print_msg(3, "These applications support multiple installation methods:")
    for app in matches:
        print("  - {0} - {1}".format(app[0], print_colour_only(4, list_to_string(app[1]))))
    print("\n")


# List apps that install differently per release
matches = []
for index in indexes:
    if len(index["apt"].keys()) > 1:
        matches.append([index["name"], list(index["apt"].keys())])

if len(matches) == 0:
    print_msg(2, "All applications install the same way in every release.\n")
else:
    print_msg(3, "These applications have different install instructions:")
    for app in matches:
        print("  - {0} - {1}".format(app[0], print_colour_only(4, list_to_string(app[1]))))
    print("\n")

# List apps that have no icon or screenshot
missing_icons = []
missing_screenshots = []

for category in categories:
    app_category_paths = glob.glob(category + "/*")
    for path in app_category_paths:
        app_name = os.path.basename(path)
        if not os.path.exists(os.path.join(path, "icon.png")):
            missing_icons.append(app_name)
        if len(glob.glob(os.path.join(path, "screenshot*"))) == 0:
            missing_screenshots.append(app_name)

if len(missing_icons) == 0:
    print_msg(2, "All applications have an icon.\n")
else:
    print_msg(1, "These applications are missing an icon:")
    for app in missing_icons:
        print("  - {0}".format(app))
    print("\n")

if len(missing_screenshots) == 0:
    print_msg(2, "All applications have at least one screenshot.\n")
else:
    print_msg(3, "These applications are missing a screenshot:")
    for app in missing_screenshots:
        print("  - {0}".format(app))
    print("\n")
