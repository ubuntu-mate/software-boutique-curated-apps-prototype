#!/usr/bin/env python3
#
# Checks every JSON file (application metadata) and validate
# it contains the expected data types.
#

import os
import glob
import json

failed = False

accepted_arch = ["i386", "amd64", "armhf", "arm64"]
accepted_releases = ["xenial", "zesty", "artful"]
accepted_methods = ["dummy", "apt", "snap"]
accepted_sources = ["main", "universe", "restricted", "multiverse", "partner", "manual"] # + ppa*

def _check_data_type(path, index, key, expected_type, can_be_null=False):
    global failed
    if not type(index[key]) == expected_type:
        if can_be_null:
            return
        else:
            print("{0} : Expected {1} for key '{2}', but was {3}.".format(path, expected_type.__name__, key, type(index[key]).__name__))
            failed = True

def _check_if_string_empty(path, index, key):
    global failed
    if index[key] == "":
        print("{0} : Expected data for key '{1}', but was empty.".format(path, key))
        failed = True

os.chdir(os.path.join(os.path.dirname(__file__), "..", "..", "apps"))
categories = glob.glob("*")
for category in categories:
    app_category_paths = glob.glob(category + "/*")
    for path in app_category_paths:
        try:
            json_path = os.path.join(path, "metadata.json")
            with open(json_path) as data_file:
                index = json.load(data_file)

            _check_data_type(path, index, "listed", bool)
            _check_data_type(path, index, "name", str)
            _check_data_type(path, index, "summary", str)
            _check_data_type(path, index, "developer-name", str)
            _check_data_type(path, index, "developer-url", str)
            _check_data_type(path, index, "description", str)
            _check_data_type(path, index, "tags", str)
            _check_data_type(path, index, "launch-cmd", str, True)
            _check_data_type(path, index, "proprietary", bool)
            _check_data_type(path, index, "alternate-to", str, True)
            _check_data_type(path, index, "urls", dict)
            _check_data_type(path, index, "arch", list)
            _check_data_type(path, index, "releases", list)
            _check_data_type(path, index, "method", str)
            _check_data_type(path, index, "installation", dict)

            _check_if_string_empty(path, index, "name")
            _check_if_string_empty(path, index, "summary")
            _check_if_string_empty(path, index, "developer-name")
            _check_if_string_empty(path, index, "developer-url")
            _check_if_string_empty(path, index, "description")
            _check_if_string_empty(path, index, "tags")
            _check_if_string_empty(path, index, "method")

            # Check lists contain recognised data
            method = index["method"]
            if method not in accepted_methods:
                print("{0} : Unrecognised method: {1}".format(path, method))
                failed = True

            for arch in index["arch"]:
                if arch not in accepted_arch:
                    print("{0} : Unrecognised architecture: {1}".format(path, arch))
                    failed = True

            for release in index["releases"]:
                if release not in accepted_releases:
                    print("{0} : Unrecognised architecture: {1}".format(path, release))
                    failed = True

            # Depending on method, expect additional data.
            for installation in index["installation"].keys():
                i = index["installation"][installation]
                if method == "apt":
                    i["main-package"]
                    i["install-packages"]
                    i["remove-packages"]
                    source = i["source"]
                    if source not in accepted_sources:
                        if not source.startswith("ppa:"):
                            print("{0} : Unrecognised source: {1}".format(path, source))
                            failed = True

                    if source == "manual":
                        i["list-file"]
                        try:
                            i["list-key-url"]
                        except KeyError:
                            i["list-key-server"]
                        except:
                            print("{0} : Missing a list key URL or server address!".format(path))

                        # A source.list file is expected in the same directory
                        if not os.path.exists(os.path.join(path, "source.list")):
                            print("{0} : Missing a source.list file!".format(path))

                        # The "list-file" key should specify a .list extension
                        if not i["list-file"].endswith(".list"):
                            print("{0} : Missing '.list' extension for 'list-file' key.".format(path))

                elif method == "snap":
                    i["name"]

        except Exception as reason:
            print("{0} : {1}".format(path, reason))
            failed = True

if failed:
    exit(1)
else:
    exit(0)
