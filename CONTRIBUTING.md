
## Software Boutique Curated Index Format

| Revision  | Last Modified |
| --------- | ------------- |
| 5         | June 2017     |

Each application is stored in its own subfolder inside the category folder, for
example:

* `./apps/accessories/gparted/`
* `./apps/multimedia/vlc/`
* `./apps/system/virtualbox/`

Each folder is expected to have:

* [`metadata.json` - See below.](#metadata.json)
* `icon.png` - 64x64 PNG icon
* `screenshot-1.jpg` - Optional. Screenshot of the application. More can be added by incrementing the number prefix.


### metadata.json

* Standard JSON rules apply (Watch out for commas)
* Non-required values should be `null`.

| Key           | Data Type | Required? | Description                          |
| ------------- | --------- | --------- | ------------------------------------ |
| listed        | boolean   | Yes       | `false` = Do not include in Boutique listings.
|               |           |           | `true` = Show this application in Boutique.
| name          | string    | Yes       | Name of the application as displayed to the user.
| summary       | string    | Yes       | A brief one-liner that describes the application.
| description   | string    | Yes       | A more in-depth description of the application.
| developer-name| string    | Yes       | Author's name, whether it's an individual or company.
| developer-url | string    | Yes       | Website for the author or company.
| tags          | string    | Yes       | Categories for this application and search key words. Comma separated. e.g. "texteditor", "System", "Office", "Application"
| launch-cmd    | string    | No        | Command to launch the installed program.
| alternate-to  | string    | No        | Mention the app is similar to another product.
| proprietary   | boolean   | Yes       | Is this non-free software?
| urls          | dict      | Yes
| -- info       | string    | Yes       | URL to the web page for more information.
| -- android-app| string    | No        | URL if there is an associated Android app.
| -- ios-app    | string    | No        | URL if there is an associated iOS app.
| arch          | list      | Yes       | Architectures to show for this app. E.g. `i386`, `amd64`, `armhf`, `arm64`.
| releases      | list      | Yes       | Versions of Ubuntu MATE to show this application. E.g. `xenial`, `bionic`, `focal`.


### Placeholders

    Where noted, these strings can be used and will be substituted:

    CODENAME        =   Current Ubuntu release, e.g. "xenial".
    OSVERSION       =   Current Ubuntu version, e.g "16.04".

