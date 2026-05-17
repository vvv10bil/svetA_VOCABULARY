# Trilingual Automobile Industry Dictionary

Coursework project. A single-page website that turns a curated
**Ukrainian / English / German** glossary of automobile-industry
terminology into a searchable mini-dictionary.

The glossary itself is the deliverable that gets uploaded to Google
Drive; the website is the deliverable that demonstrates how a
linguist-prepared dataset is turned into a digital tool.

## What is in this repository

```
.
├── index.html              # single-page dictionary site
├── assets/
│   ├── styles.css
│   └── script.js           # search logic (vanilla JS, no frameworks)
├── data/
│   ├── glossary.xlsx       # primary glossary (Excel, required by brief)
│   ├── glossary.json       # generated export used by the website
│   └── glossary.csv        # generated export for portability
├── scripts/
│   └── build_glossary.py   # regenerates the three glossary files
└── docs/
    └── prompts.md          # AI-prompt iterations (required by brief)
```

## The glossary

- **Theme:** Automobile Industry.
- **Languages:** Ukrainian (source) → English → German.
- **Size:** 123 entries (the brief requires at least 100).
- **Columns:** `ID`, `Ukrainian`, `English`, `German`, `Notes`.
- **Notes column** records context, register, regional variants
  (`US 'gasoline'` vs `UK 'petrol'`), gendered forms where relevant,
  and standard abbreviations (`ABS`, `ECU`, `FWD`, `PKW`, ...).

To regenerate the three glossary files from the source list of entries:

```sh
pip install openpyxl
python3 scripts/build_glossary.py
```

The script writes `data/glossary.xlsx`, `data/glossary.json` and
`data/glossary.csv` from a single Python list, so the three files cannot
drift out of sync.

## The website

A single page (`index.html`) with no frameworks and no build step. It
loads `data/glossary.json` at startup and provides search across all
three languages.

Features required by the brief (section 8.3):

- search by a word in any of the three languages,
- displays the corresponding entries in the other languages,
- a dedicated "nothing matched" state when the query has no hits,
- the author's name is shown in the hero and the footer.

Additional behaviours:

- case-insensitive search,
- diacritic-insensitive search (`Tschuss` finds `Tschüss`,
  `Motoroel` finds `Motoröl`),
- partial-substring matching (one query fragment matches every entry
  that contains it, useful for inflected languages),
- per-language filter pills (Any / Ukrainian / English / German),
- matched substrings are highlighted with `<mark>` in the result cards,
- keyboard shortcuts: `/` to focus the search box, `Escape` to clear.

## Running the site locally

The page fetches `data/glossary.json`, so it must be served over HTTP —
opening `index.html` directly from the file system will trigger a
browser-level fetch error (the page itself shows an explanatory
message). Use any static server, for example:

```sh
python3 -m http.server 8000
# then open http://localhost:8000 in the browser
```

## AI prompts

The course brief requires a record of how the AI prompts evolved while
building the project. See [`docs/prompts.md`](docs/prompts.md) for the
three prompts (initial site structure, search-only, refined search) and
a discussion of the linguistic decisions that each iteration forced into
the open.

## Author

**Svitlana Boloshyna**, group ФЛПЛ-12 — coursework, 2026.
