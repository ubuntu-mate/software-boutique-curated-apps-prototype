# Ubuntu MATE Software

This repository stores the index used by the Software Boutique application.

[![Build Status](https://travis-ci.org/ubuntu-mate/ubuntu-mate.software.svg?branch=master)](https://travis-ci.org/ubuntu-mate/ubuntu-mate.software)

### Sources

Contains the curated applications to be used by Software Boutique, stored in `sources/apps/`.

Every application requires:

* `metadata.json` - As described in `docs/metadata.json.txt`
* `icon.png` - Application's icon that is PNG and exactly 64x64.
* `screenshot-1.jpg` - Screenshot of this application. More can be added by incrementing the number prefix.

In future, this process can be automated by fetching data from upstream sources, such as AppStream
to avoid duplication. As the data is index stored centrally, think of this repository serving more as a "cache".


### Translations

Localised index data for each application can be found in `sources/locales/`.

* There is a **POT** file for each application.
* When building the index, the **PO** will be used if available.

Transifex is yet to be set up.


### Distribution

Software Boutique aims to downloads the curated picks from the central https://ubuntu-mate.software
server as quickly and securely as possible.

The web folder includes:

* `applications-LOCALE.json.gz` contains the compiled metadata, compressed.
* `application-data.tar.gz` contains the icons and screenshots, compressed.
* `latest_revision` contains a number indicating the latest revision.
* `SHA256SUMS` to ensure data integrity.
    * In future, there will be a GPG key for signing and validating its signed by us.


### Dependencies

To compile POT translations you will need:

* `translate-toolkit` (to provide `json2po`)
* `gettext` (to provide `pygettext`)
