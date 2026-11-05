# aktujo catalog

The official catalog of [aktujo](https://aktujo.dev): **templates of kinds of documents**. aktujo itself knows no
kinds – a space has the kinds its people define, for letters, sheet music, research papers, the books of a collection
or anything else. A template is a set of such kinds, taken over into a space in one step and changed there as the
space needs. None is needed.

aktujo ships none of it. Anyone can propose a template by pull request (CONTRIBUTING.md); the aktujo team reviews it
(REVIEW.md) before it is merged. You can also run a catalog of your own (FORKING.md).

## Templates

| Template | Kinds |
|---|---|
| [`aktujo/paperwork`](templates/aktujo/paperwork/template.json) | letter, contract, official notice, invoice, receipt, insurance policy, payslip – who sent it, when, a reference, an amount; words in German, English, French, Italian, Spanish and Dutch |
| [`aktujo/library`](templates/aktujo/library/template.json) | book – title, author, publisher, year, ISBN, read |
| [`aktujo/research`](templates/aktujo/research/template.json) | research paper – authors, journal, DOI, arXiv identifier, date of publication |

These are general on purpose. A trade's own kinds – accounting in depth, sheet music – come with the programs of that
trade, which build aktujo in.

## Layout

```
catalog.json                          generated – the one file aktujo reads to browse this source
source.toml                           name and description of this source, allowed licences
tags.toml                             the tags templates may use
templates/<author>/<name>/
  template.json                       a template: who, licence, names, description, tags, kinds – data only
tools/catalog.py                      checks everything and writes catalog.json
.github/                              CI (the same check) and the pull request checklist
```

`<author>` is the GitHub name of whoever submitted it (`aktujo` for the team's). The folder is its identity: a
template's ID is `<author>.<name>`.

## Using a template

- **Web app:** *Kinds* → *Import template …* → choose a `template.json`.
- **Terminal:** `K`, then the path of the file.
- **API:** `POST /api/v1/spaces/{space}/kind-import` with the file as the body.

A kind with the same identity as one in the space replaces it; the others stay. *Export kinds* writes the kinds of a
space in the same form. OPEN: browsing this catalog from within aktujo.

## `template.json`

```json
{
  "author": "aktujo",
  "license": "MIT",
  "name": "Library",
  "names": { "de": "Bibliothek" },
  "description": "The books of a collection.",
  "tags": ["books", "collection"],
  "kinds": [
    {
      "id": "book",
      "name": "Book",
      "names": { "de": "Buch" },
      "fields": [
        { "key": "author", "name": "Author", "type": "text", "find": [{ "way": "label", "labels": ["author", "by"] }] },
        { "key": "isbn", "name": "ISBN", "type": "text", "code": true, "find": [{ "way": "label", "labels": ["isbn"] }] }
      ],
      "words": [{ "word": "isbn", "weight": 6 }],
      "title": [["author"]]
    }
  ]
}
```

The kinds are exactly the JSON of a kind in aktujo – the same as in the events of a space
([RFC 0005](https://github.com/aktujo/aktujo/blob/main/docs/rfc/0005-pure-core.md)):

- **`id`, `key`:** `a-z`, `0-9`, `.`, `-`, `_`, at most 64 characters. An identity of a kind is in one template of
  this catalog only.
- **`names`, `descriptions`:** optional, by language tag.
- **`type`:** `text`, `date`, `money`, `number` or `flag`.
- **`find`:** the ways to find a field in the text, tried in order – `label` (the value after one of the labels),
  `largest` (the largest value after any of them), `first` (the first value of the type on the first page), `sender`
  (the name in the letterhead with one of the markers, else the topmost line), `present` (yes, if a phrase occurs).
  `code: true` keeps only the first word with a digit – a number or reference.
- **`words`:** words and phrases that speak for the kind, matched as whole words in any case, with whole weights; a
  kind is suggested from a sum of 6.
- **`title`:** the fields a suggested title is made of after the kind's name – the first with a value of each group.

Every suggestion is only that: a person confirms it.

## Licence

The tools and the team's templates: MIT ([LICENSE](LICENSE)). Every template names its own licence; REUSE compliant.
