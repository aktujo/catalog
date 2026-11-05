# Reviewing a template

What the aktujo team checks before a template is merged. CI (`tools/catalog.py --check`) covers the form – every
member, identities, types, ways, weights, titles, unique identities of kinds, licences and tags; everything else is a
reviewer's judgement. A template is merged when two things hold: we would use it ourselves, and it gives people
something the catalog does not have yet.

Templates are **data**: nothing in them runs. aktujo reads them as it reads kinds a person defines.

- [ ] The folder is `templates/<author>/<name>/`, `author` is the submitter's GitHub name, `template.json` its only
      file.
- [ ] It is general: useful to many people, not one organisation's forms; a trade's own kinds belong to its programs.
- [ ] The kinds and fields are what people look for; names are clear, in English, with other languages under
      `names`.
- [ ] Words tell its kinds apart from each other and from the kinds of the other templates; no word every document
      has; weights that suggest a kind only for clear cases.
- [ ] Labels are as they stand on real documents; `code` for numbers and references.
- [ ] The title is made of fields that tell two documents of the kind apart (who, when).
- [ ] Tried in aktujo with real documents (the pull request says how).
- [ ] No personal data in labels, words or examples; no names of real people or customers.
- [ ] The licence is one of `source.toml`'s, and it is the submitter's to share.
- [ ] `catalog.json` is up to date.
