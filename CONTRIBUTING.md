# Contributing a template

1. Fork this repository and add yours in your GitHub name's folder: `templates/<you>/<name>/template.json` (names use
   lowercase letters, digits and `-`).
2. Write it (README.md, "`template.json`") and try it in aktujo: *Kinds* → *Import template …* in a space of its own,
   then add a few of your documents and look at what is suggested.
3. Run `python3 tools/catalog.py` and commit the updated `catalog.json` with it.
4. Open a pull request – one template per pull request – and fill in the checklist.

The aktujo team reviews it against REVIEW.md: does it work, is it general enough for many people, does it add
something the catalog does not have yet. Changes to a merged template go the same way; only its author or the team
change it.

## What makes a good template

- **General.** A household, a collection, a field of research – not one company's forms. A trade's own kinds come with
  the programs of that trade.
- **Kinds people recognise**, with the fields they look for, in the order they look for them.
- **Words that tell kinds apart**, weighted so that a kind is suggested only when its document is clearly one (from a
  sum of 6). A word every document has speaks for nothing.
- **Labels in the languages you know**, as they stand on real documents; names in other languages under `names`.
- **New identities.** An identity of a kind is in one template only (`tools/catalog.py` checks it); take one that says
  what it is (`sheet-music`, not `kind1`).

## Testing

`python3 tools/catalog.py` checks the form. Whether a template recognises documents only aktujo can tell: import it,
add documents, and look at the suggested kind and fields. With the source of aktujo,

```sh
cargo run --release -p aktujo-rules --example recognise -- <template.json> <file.pdf>
```

prints the kind and the fields it suggests for one file, with the line each came from.
