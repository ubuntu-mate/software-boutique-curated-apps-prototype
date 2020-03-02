## Software Boutique Curated Index Format

| Version   | Last Modified |
| --------- | ------------- |
| 5         | June 2017     |
| 7         | March 2020    |

The **revision number** is the amount of commits made in this repository.

Each application is stored in its own subfolder inside the category folder, for
example:

* `./apps/accessories/gparted/`
* `./apps/multimedia/vlc/`
* `./apps/system/virtualbox/`

Each folder is expected to have:

* [`metadata.json`](#metadata.json)
* `icon.png` - 64x64 PNG icon
* `screenshot-1.jpg` - Optional. Screenshot of the application. More can be added by incrementing the number prefix.


### metadata.json

* Standard JSON rules apply (Watch out for commas)
* Non-required values should be `null`.

| Key           | Data Type | Required? | Description                          |
| ------------- | --------- | --------- | ------------------------------------ |
| listed        | boolean   | Yes       | `true` to show this application in Boutique, or `false` to omit.
| name          | string    | Yes       | Name of the application as displayed to the user.
| summary       | string    | Yes       | A brief one-liner that describes the application.
| description   | string    | Yes       | A more in-depth description of the application.
| developer-name| string    | Yes       | Author's name, whether it's an individual or company.
| developer-url | string    | Yes       | Website for the author or company.
| launch-cmd    | string    | No        | Command to launch the installed program.
| alternate-to  | string    | No        | Mention the app is similar to another product.
| proprietary   | boolean   | Yes       | Is this non-free software?
| urls          | dict      | Yes
| -- info       | string    | Yes       | URL to the web page for more information.
| -- android-app| string    | No        | URL if there is an associated Android app.
| -- ios-app    | string    | No        | URL if there is an associated iOS app.
| arch          | list      | Yes       | Architectures to show for this app. E.g. `i386`, `amd64`, `armhf`, `arm64`.
| releases      | list      | Yes       | Versions of Ubuntu MATE to show this application. E.g. `xenial`, `bionic`, `focal`.
| methods       | list      | Yes       | Ways of installed that are supported, e.g. `apt`, `snap`.
| apt           | dict      | No        | See **Apt Installs** below.
| snap          | dict      | No        | See **Snap Installs** below.


#### Apt Installs

For applications distributed as:

* A package in the Ubuntu repositories.
* A package avaliable via a trusted PPA.
* A package via a third party repository (file) server.

Under the `apt` dict are dictionaries that describe the instructions per release,
with `default` being the fallback. Alternate instructions can be specified by
adding additional keys for each codename, for example:

```
"apt": {
    "default": { ... },
    "xenial": { ... }
    "cosmic": { ... }
}
```

Nested under the `default` or `<codename>` dict:

| Key               | Data Type | Required? | Description                          |
| ----------------- | --------- | --------- | ------------------------------------ |
| source            | string    | Yes       | One of: "main", "universe", "restricted", "multiverse", "partner", "ppa:XXX/YYY", "manual"
| main-package      | string    | Yes       | The package used to check whether it's installed.
| install-packages  | string    | Yes       | The packages that will be installed.
| remove-packages   | string    | Yes       | The packages that will be uninstalled.
| enable-i386       | boolean   | No        | `true` enables the i386 architecture for i386 packages. Only for Steam/Wine.

If a `manual` source is specified, these additional keys are required:

| Key               | Data Type | Description                                  |
| ----------------- | --------- | -------------------------------------------- |
| list-file         | string    | The source file name that is written at `/etc/apt/sources.d/`, including the extension (.list)
| list-contents     | string    | The contents of the source.list file, e.g. `deb https://example.com/debian stable xenial`
| list-key-url      | string    | Retrieve the signing key from URL.
| list-key-server   | list      | **OR** retrieve the signing key from a keyserver: `[<server>, <key>]`. E.g. `["keyserver.ubuntu.com", "ABC12345"]`

Only one `list-key-url` or `list-key-server` must be specified, with the other `null`.


**Placeholders**

For the `list-file` and `list-contents` keys, you may use these strings as
placeholders:

| String        | Replaced with                 | Example           |
| ------------- | ----------------------------- | ----------------- |
| CODENAME      | Current Ubuntu release        | `xenial`
| OSVERSION     | Current Ubuntu version        | `16.04`


#### Snap Installs

If the software is distributed via Snapcraft, this data is required under the `snap` key:

| Key               | Data Type | Required? | Description                          |
| ----------------- | --------- | --------- | ------------------------------------ |
| name              | string    | Yes       | Name of the snap.
