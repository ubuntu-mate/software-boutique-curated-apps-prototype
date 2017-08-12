# Ubuntu MATE Software

This repository stores data used by the Software Boutique application.

[![Build Status](https://travis-ci.org/ubuntu-mate/ubuntu-mate.software.svg?branch=master)](https://travis-ci.org/ubuntu-mate/ubuntu-mate.software)

### Sources

Contains the curvated applications to be used by Software Boutique, stored in `sources/apps`.

Every application requires:

* `metadata.json` - As described in `docs/metadata.json.txt`
* `icon.png` - Application's icon that is PNG and exactly 64x64.
* `screenshot-1.jpg` - Screenshot of this application. More can be added by incrementing the number prefix.

However, in future, there will be scripts that will fetch the data from upstream sources, such as AppStream
to avoid duplication of data.

### Distribution

The data used for Software Boutique is stored on this server so that the application
only needs one source for our picks.

The web folder will include:

* `applications-LOCALE.json.gz` contains the compiled metadata, compressed.
* `application-data.tar.gz` contains the icons and screenshots, compressed.
* `latest_revision` contains a number indicating the latest revision.
* `SHA256SUMS` to ensure data integrity.
    * In future, there will be a GPG key for signing and validating its signed by us.
