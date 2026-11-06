# Your own catalog

A catalog is a repository with a `catalog.json` and the templates next to it – nothing more. Use one of your own for
templates your team shares, for templates you do not want to publish, or to run a curated catalog of your own.

Templates from other catalogs are **not reviewed by the aktujo team**. They are data, nothing in them runs – but their
kinds replace kinds of the same identity in a space that takes them over.

## Option 1: fork this repository

You get everything: the official templates, the checks, the CI and the pull request checklist.

1. Fork `aktujo/catalog` on GitHub.
2. Edit `source.toml`: your source's `name`, `description` and `homepage`, and the `licenses` you accept.
3. Add templates under `templates/<author>/<name>/` (CONTRIBUTING.md) – remove the ones you do not want.
4. Run `python3 tools/catalog.py`, commit `catalog.json` with your changes, push.

To pick up new official templates, use GitHub's "Sync fork" (or `git pull upstream main`) and run the tool again.

## Option 2: a repository of your own

Start empty with this layout and copy `tools/catalog.py`:

```
catalog.json
source.toml         name = "…"  description = "…"  (homepage, licenses optional)
tags.toml           [tags] with the tags your templates use
templates/<author>/<name>/template.json
tools/catalog.py
```

In aktujo, add the source in *Settings → Sources of templates* with its address – `https://github.com/<you>/catalog`
(another branch: `…/tree/<branch>`), or any HTTPS address of the folder with `catalog.json`. Templates from it are
marked as not reviewed by the aktujo team.
