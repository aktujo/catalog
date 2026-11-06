#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check every template in this repository and write catalog.json – the one file aktujo reads to browse it.

  python3 tools/catalog.py           # check, then write catalog.json
  python3 tools/catalog.py --check   # check, and fail if catalog.json is not up to date (CI)

A template is checked as aktujo checks a kind before it takes it over (aktujo-doc, `Kind::check`): identities and keys
of a-z, 0-9, '.', '-', '_' (at most 64), names of 1 to 100 characters, each field once, a title made of the kind's own
fields, the known field types and ways to find a value, weights as whole numbers above 0. Beyond that: the folder is
templates/<author>/<name>/, `author` is the folder's, the licence is one of source.toml's, the tags are in tags.toml,
and an identity of a kind is in one template only – a space that takes over two templates must not have one replace
the other's kind.

Needs Python 3.11 or newer (tomllib) and nothing else. Without a recent Python: `nix run nixpkgs#python3 --
tools/catalog.py`. The output has no timestamps or commit hashes, so it only changes when something in here changes.
"""

import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "templates"
CATALOG = ROOT / "catalog.json"
# The form of catalog.json; raised for a change an older aktujo would misread.
FORMAT = 1

IDENTITY = re.compile(r"^[a-z0-9._-]{1,64}$")
FOLDER = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")
AUTHOR = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{0,38}$")
TYPES = {"text", "date", "money", "number", "flag"}
WAYS = {
    "label": "labels",
    "largest": "labels",
    "sender": "markers",
    "present": "phrases",
    "first": None,
    "tallest": None,
    "within": None,
}
# The ways that look in an area of the page: whether they need one.
AREA_WAYS = {"tallest": False, "within": True}


def area_ok(area):
    """A part of a page in thousandths: whole numbers 0 to 1000, the edges in order."""
    edges = ("left", "top", "right", "bottom")
    if not isinstance(area, dict) or set(area) != set(edges):
        return False
    if not all(isinstance(area[e], int) and not isinstance(area[e], bool) and 0 <= area[e] <= 1000 for e in edges):
        return False
    return area["left"] < area["right"] and area["top"] < area["bottom"]
TEMPLATE_KEYS = {"author", "license", "name", "names", "description", "descriptions", "tags", "homepage", "kinds"}
KIND_KEYS = {"id", "name", "names", "fields", "words", "title"}
FIELD_KEYS = {"key", "name", "names", "type", "code", "find"}


def name(value, where, errors):
    if not isinstance(value, str) or not 1 <= len(value.strip()) <= 100:
        errors.append(f"{where}: not a name: {value!r}")


def texts(value, where, errors, limit=100):
    if not isinstance(value, dict):
        errors.append(f"{where}: must be an object of language tag → text")
        return
    for language, text in value.items():
        if not re.fullmatch(r"[a-z]{2,3}", language):
            errors.append(f"{where}: not a language tag: {language!r}")
        if not isinstance(text, str) or not 1 <= len(text.strip()) <= limit:
            errors.append(f"{where}.{language}: not a text of 1 to {limit} characters")


def strings(value):
    return isinstance(value, list) and value and all(isinstance(s, str) and s.strip() for s in value)


def check_kind(kind, where, errors):
    for key in sorted(set(kind) - KIND_KEYS):
        errors.append(f"{where}: unknown member {key!r}")
    if not IDENTITY.match(str(kind.get("id", ""))):
        errors.append(f"{where}: not an identity: {kind.get('id')!r}")
    name(kind.get("name"), where, errors)
    texts(kind.get("names", {}), f"{where}.names", errors)
    keys = set()
    for field in kind.get("fields", []):
        at = f"{where}.{field.get('key')}"
        for key in sorted(set(field) - FIELD_KEYS):
            errors.append(f"{at}: unknown member {key!r}")
        if not IDENTITY.match(str(field.get("key", ""))):
            errors.append(f"{at}: not a key")
        if field.get("key") in keys:
            errors.append(f"{at}: the field is there twice")
        keys.add(field.get("key"))
        name(field.get("name"), at, errors)
        texts(field.get("names", {}), f"{at}.names", errors)
        if field.get("type") not in TYPES:
            errors.append(f"{at}: not a type: {field.get('type')!r}")
        for way in field.get("find", []):
            if way.get("way") not in WAYS:
                errors.append(f"{at}: not a way: {way.get('way')!r}")
                continue
            member = WAYS[way["way"]]
            if member and not strings(way.get(member)):
                errors.append(f"{at}: the way {way['way']} needs {member}")
            if way["way"] in AREA_WAYS and (AREA_WAYS[way["way"]] or "area" in way) and not area_ok(way.get("area")):
                errors.append(f"{at}: the way {way['way']} needs an area: left, top, right, bottom in thousandths")
    for word in kind.get("words", []):
        if not isinstance(word.get("weight"), int) or word["weight"] < 1 or not str(word.get("word", "")).strip():
            errors.append(f"{where}: not a word with a whole weight: {word!r}")
    for group in kind.get("title", []):
        for key in group:
            if key not in keys:
                errors.append(f"{where}: the title names the field {key!r}, which the kind does not have")


def main():
    check_only = "--check" in sys.argv[1:]
    errors = []
    source = tomllib.loads((ROOT / "source.toml").read_text(encoding="utf-8"))
    tags = tomllib.loads((ROOT / "tags.toml").read_text(encoding="utf-8")).get("tags", {})
    licences = set(source.get("licenses", []))
    entries, kinds_seen = [], {}
    for path in sorted(TEMPLATES.glob("*/*/template.json")):
        folder = path.parent
        author, folder_name = folder.parent.name, folder.name
        where = f"{author}/{folder_name}"
        if not AUTHOR.match(author) or not FOLDER.match(folder_name):
            errors.append(f"{where}: the folder must be templates/<author>/<name> (lowercase letters, digits, '-')")
        others = sorted(p.name for p in folder.iterdir() if p.name != "template.json")
        if others:
            errors.append(f"{where}: template.json is its only file, not {others}")
        raw = path.read_bytes()
        try:
            template = json.loads(raw)
        except json.JSONDecodeError as error:
            errors.append(f"{where}: not JSON: {error}")
            continue
        for key in sorted(set(template) - TEMPLATE_KEYS):
            errors.append(f"{where}: unknown member {key!r}")
        if template.get("author") != author:
            errors.append(f"{where}: author must be {author!r}, the folder's")
        if licences and template.get("license") not in licences:
            errors.append(f"{where}: the licence {template.get('license')!r} is not one of source.toml's")
        name(template.get("name"), where, errors)
        texts(template.get("names", {}), f"{where}.names", errors)
        if not isinstance(template.get("description"), str) or not template["description"].strip():
            errors.append(f"{where}: needs a description")
        texts(template.get("descriptions", {}), f"{where}.descriptions", errors, limit=500)
        for tag in template.get("tags", []):
            if tag not in tags:
                errors.append(f"{where}: the tag {tag!r} is not in tags.toml")
        kinds = template.get("kinds")
        if not isinstance(kinds, list) or not kinds:
            errors.append(f"{where}: needs kinds")
            kinds = []
        for kind in kinds:
            check_kind(kind, f"{where}:{kind.get('id')}", errors)
            if kind.get("id") in kinds_seen:
                errors.append(f"{where}: the kind {kind.get('id')!r} is also in {kinds_seen[kind['id']]}")
            kinds_seen[kind.get("id")] = where
        entry = {
            "id": f"{author}.{folder_name}",
            "author": author,
            "path": f"templates/{author}/{folder_name}/template.json",
            "sha256": hashlib.sha256(raw).hexdigest(),
            "license": template.get("license"),
            "name": template.get("name"),
            "names": template.get("names", {}),
            "description": template.get("description"),
            "descriptions": template.get("descriptions", {}),
            "tags": template.get("tags", []),
            "kinds": [{"id": k.get("id"), "name": k.get("name"), "names": k.get("names", {})} for k in kinds],
        }
        if "homepage" in template:
            entry["homepage"] = template["homepage"]
        entries.append(entry)

    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    catalog = {
        "format": FORMAT,
        "source": {k: source[k] for k in ("name", "description", "homepage") if k in source},
        "tags": tags,
        "templates": entries,
    }
    text = json.dumps(catalog, ensure_ascii=False, indent=2) + "\n"
    print(f"{len(entries)} templates, {len(kinds_seen)} kinds, {len(errors)} errors")
    if errors:
        sys.exit(1)
    if check_only:
        if not CATALOG.exists() or CATALOG.read_text(encoding="utf-8") != text:
            print("error: catalog.json is not up to date – run python3 tools/catalog.py", file=sys.stderr)
            sys.exit(1)
    else:
        CATALOG.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
