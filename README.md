# Ubuntu MATE's Curated Applications

This repository stores the index used by Software Boutique. Each application is
individually stored in `apps/` in their relevant category.

## Structure

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

In future, this process can be automated by fetching data from upstream sources,
such as AppStream to avoid duplication. As the data is index stored centrally,
think of this repository serving more as a "cache".


### Translations

Localised index data for each application can be found in `sources/locales/`.

* There is a **POT** file for each application.
* When building the index, the **PO** will be used if available.

Transifex is not yet set up.


### Dependencies

To compile POT translations you will need:

* `translate-toolkit` (to provide `json2po`)
* `gettext` (to provide `pygettext`)
