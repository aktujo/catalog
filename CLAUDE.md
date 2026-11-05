# CLAUDE.md – aktujo catalog

`aktujo/catalog`: the official catalog of aktujo – templates of kinds of documents – and the template for other
catalogs. This file is public: nothing personal goes here. aktujo itself lives in `aktujo/aktujo`, checked out next to
this one as `../aktujo`; the design of kinds as data is its `docs/rfc/0005-pure-core.md`.

- **English** in files and commits; talk to the maintainer in German. Commits signed off (`git commit -s`).
- **The format is an interface.** `catalog.json` (`format` 1), the layout `templates/<author>/<name>/template.json`
  and its members; the kinds in exactly the JSON of `aktujo_doc::Kind` (`../aktujo/crates/aktujo-doc/src/kinds.rs`).
  Change them only together with aktujo, and raise `FORMAT` in `tools/catalog.py` for changes an older aktujo would
  misread.
- **After every change:** `python3 tools/catalog.py` and commit `catalog.json` with it; `--check` must pass.
- **General cases only:** a household, a collection, research. A trade's own kinds (accounting, sheet music …) come
  with the programs of that trade, not here. An identity of a kind is in one template only.
- **Never delete (your own actions):** move files to `_to_delete/` (git-ignored) instead.
- **Verified before claimed:** mark what is not verified as `OPEN`. Licence MIT, REUSE compliant.
