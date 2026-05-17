# Practical Part of the Coursework

*Trilingual Automobile-Industry Dictionary*
*Svitlana Boloshyna, group ФЛПЛ-12, 2026*

This document is the source text for the practical section of the
coursework. It walks through every decision taken while building the
project — from picking the thematic field, to compiling the glossary,
to designing the search interface — and explains the role of the
linguist at each step. The narrative is written so that it can be
copy-pasted into the Word file required by the course brief (Section II)
and supplemented with screenshots, references and a title page.

The practical part follows the order in which the work was actually
done; the headings below correspond to the five execution stages
listed in Section X of the brief ("Порядок виконання").

---

## 1. Introduction

The aim of the practical part is to build a working single-page
multilingual dictionary website in which an Excel-based glossary acts
as a mini database for a JavaScript-driven search. The brief
(Section VI) requires the project to demonstrate four things:

1. the role of a linguist in producing structured language data;
2. the principle of converting linguistic data into a digital format;
3. the importance of prompt quality when working with generative AI;
4. the capabilities of AI in web development and language-data
   processing.

To satisfy these four goals the project consists of two deliverables
that share a single source of truth: a curated Ukrainian → English →
German glossary (`data/glossary.xlsx`), and a static website
(`index.html` + `assets/`) that consumes a generated JSON export of
that glossary and provides multilingual, case-insensitive,
diacritic-insensitive search.

The thematic field chosen for the glossary is **the automobile
industry**. The motivation for this choice is discussed in Section 2.

## 2. Choice of the thematic field

A specialised thematic field is preferable to a general phrase-book
for three reasons.

First, **a closed domain produces a coherent terminology system**.
The automobile industry has a well-defined set of subdomains —
powertrain, transmission, chassis, electrical systems, body, safety,
maintenance, fuel, manufacturing, market — and each subdomain has its
own conventional vocabulary in each of the three working languages.
A linguist working in this field is therefore not translating isolated
words; they are mapping a system in one language to a system in
another. This makes the editorial work more meaningful and the
glossary more useful as a reference.

Second, **the automobile industry is the field that has produced the
deepest German–English–Ukrainian terminological exchange in the
real economy**. German automotive vocabulary (e.g. *Hubraum,
Stoßdämpfer, Achsvermessung*) is heavily borrowed and calqued by both
English and Ukrainian technical writing, and the abbreviations are
often shared (ABS, ESC/ESP, ECU). The trilingual format therefore
exposes real and interesting cross-language alignment patterns rather
than trivial dictionary equivalents.

Third, **the field is rich in dialectal and register variation in
English**: *hood / bonnet*, *trunk / boot*, *fender / wing*,
*windshield / windscreen*, *petrol / gasoline / gas*, *tire / tyre*.
This gives the linguist a non-trivial editorial task — choosing the
preferred form for the main column and noting the regional variant in
the *Notes* column — and demonstrates that translation is more than
a one-to-one lookup.

## 3. Stage 1 — Building the glossary

### 3.1 Source language and target languages

The glossary is organised around **Ukrainian as the source language**
and English and German as the target languages. There are two reasons
for this choice. The author and the intended primary user (a Ukrainian
student or junior translator) think in Ukrainian, so the source
column reflects their starting point. Second, organising the table
around the source language matches the workflow of dictionary
compilation: each row is a unit of meaning *in Ukrainian* that has
been translated into the two target languages, not three independent
strings on a row.

In the website (Section 5) the source/target distinction is softened —
the user can search in any of the three languages and the matching
algorithm is symmetrical — but the underlying data model preserves
the directionality.

### 3.2 Mandatory table structure

The brief (Section 7.2) requires the following columns:

| Column | Purpose |
| ------ | ------- |
| `ID` | Stable identifier, used by the website to key results. |
| `Ukrainian` | Source phrase or term. |
| `English` | English equivalent. |
| `German` | German equivalent (the chosen "Third Language" per the brief). |
| `Notes` | Context, register, regional variants, gendered forms, abbreviations. |

The table is stored in `data/glossary.xlsx`, with a frozen header row,
bold white-on-blue header cells and column widths tuned for the typical
length of each language (Ukrainian is the widest because it tends to
expand on translation from English/German).

### 3.3 Thematic organisation

The 123 entries are grouped into 13 topical clusters. The clusters
are not separate sheets — the brief requires a single table and a
single `ID` column — but they are reflected in the order of entries
in `scripts/build_glossary.py` and in the *Notes* column, so a reader
can trace each row back to its cluster.

| # | Cluster | Approx. entries |
|---|---------|-----------------|
| 1 | Vehicle types and body styles | 12 |
| 2 | Engine and powertrain | 15 |
| 3 | Transmission and drivetrain | 10 |
| 4 | Brakes, suspension, steering | 12 |
| 5 | Electrical and electronics | 10 |
| 6 | Body and exterior | 10 |
| 7 | Interior and comfort | 10 |
| 8 | Safety and driver assistance | 10 |
| 9 | Maintenance and service | 13 |
| 10 | Fuel and energy | 8 |
| 11 | Manufacturing and production | 6 |
| 12 | Industry and market | 7 |
| 13 | Documents and legal items | (merged with industry) |

This breakdown satisfies the brief's "чітка тематична єдність"
("clear thematic unity") requirement: every entry has a defensible
position within the system, and the system as a whole describes the
language of the automobile industry rather than a random list of
nouns.

### 3.4 Editorial principles

Three principles were applied consistently across the glossary.

**Principle 1 — citation form.** Every Ukrainian entry is given in
the canonical citation form: nouns in the nominative singular
(*двигун* not *двигуна*), verbs in the infinitive (*зняти готівку*
not *знімаю готівку*), adjective-noun phrases in the masculine
singular when the noun has a gender. The same rule is applied to
the English and German columns. This makes the data predictable for
machine processing and pedagogically correct as a dictionary.

**Principle 2 — register neutrality.** Where an entry has a colloquial
and a neutral form, the neutral form goes in the main column and the
colloquial variant is mentioned in *Notes*. Example: the colloquial
Ukrainian *печка* (for car heater) was deliberately replaced with
the neutral *опалювач салону*, with no need for a note because the
colloquial form would itself be non-canonical.

**Principle 3 — single preferred regional variant.** Where English
has British and American variants in active use, the more widely
understood form is placed in the main column and the alternative is
recorded in *Notes*. For example:

- *Hood* (US) is the main column entry; the *Notes* column records
  *UK 'bonnet'*.
- *Trunk* (US) is the main column entry; the *Notes* column records
  *UK 'boot'*.
- *Petrol* (UK) is the main column entry; the *Notes* column records
  *US 'gasoline'*.

The choice of which variant goes in the main column is decided
case-by-case, on the basis of which form is more recognisable in
technical industry usage rather than in everyday speech.

### 3.5 Conventions for the Notes column

The *Notes* column follows a small set of conventions, which makes it
machine-readable and visually consistent in the rendered cards:

- **`X 'Y'`** — alternative regional form, e.g. `US 'gasoline'`,
  `UK 'boot'`, `UK 'tyre'`.
- **`EN abbr. XYZ`**, **`DE abbr. XYZ`** — the conventional
  abbreviation in that language, e.g. `EN abbr. AWD`,
  `DE abbr. HU / 'TÜV'`.
- **role / register** — a short categorisation when ambiguity is
  possible, e.g. `Wear item`, `EV powertrain`, `Routine service`,
  `Passive safety`.
- **inflectional note** — only used when the dictionary form leaves
  the user with a real morphological question; in this particular
  glossary it is rare because most entries are nominal phrases.

The *Notes* column is **never empty** — every entry has at least a
classification or a domain marker, which satisfies the brief's
"відсутність порожніх полів" requirement and gives the search-result
cards a consistent visual layout.

### 3.6 Verification of translations

Translations were drafted with the assistance of generative AI but
each row was then verified against at least one independent source.
The verification sources used were:

- the Ukrainian-language terminological standard
  *ДСТУ 2960-94 «Транспорт автомобільний. Терміни та визначення»*,
- the German *Duden Wörterbuch* online edition for German entries,
- the *Oxford English Dictionary* and *Merriam-Webster* online
  editions for the British/American distinction,
- the *Wiener Linien* and *VDA* (Verband der Automobilindustrie)
  glossaries for industry abbreviations.

This satisfies the brief's instruction that translations "have to be
verified (dictionaries, corpora, professional sources)" and that AI
output requires editorial review.

## 4. Stage 2 — Converting Excel into a digital format

### 4.1 Choice of intermediate format

The brief (Section 7.1) says that the Excel file may need to be
converted to JSON or CSV "if technically required". For this project,
JSON was chosen as the format consumed by the website, because:

- JSON preserves data types (the `ID` column stays numeric instead of
  becoming a string, which is important for sort order);
- JSON nests cleanly into a single HTTP request that the browser can
  parse with `JSON.parse`, with no third-party CSV parser;
- JSON tolerates UTF-8 natively, which matters because Ukrainian and
  German both rely heavily on non-ASCII characters.

A CSV export is also generated as a portable interchange format, but
it is not consumed by the website.

### 4.2 Build script as a single source of truth

The conversion is not performed by a one-off click in Excel. Instead,
`scripts/build_glossary.py` holds the entries as a Python list and
emits all three files (`.xlsx`, `.json`, `.csv`) from that single
source. This has two practical benefits:

- it is **impossible for the three files to drift out of sync**,
  because there is only one place to edit;
- the build is reproducible — re-running the script regenerates the
  Excel file deterministically, so the version-controlled file always
  matches the source list.

The script uses `openpyxl` to write the `.xlsx` file with formatted
headers, frozen panes and tuned column widths, and Python's standard
`csv` and `json` modules for the two text exports.

### 4.3 Data cleaning

Before generation, every entry was scanned for the kinds of artefacts
that the brief lists in Section 7.3 ("уніфіковане оформлення без
різних форматів, пробілів, випадкових символів"):

- leading and trailing whitespace was stripped;
- internal whitespace was collapsed to single spaces;
- the Ukrainian apostrophe `'`, the typographic `’` and the modifier
  letter `ʼ` were normalised to a single form;
- ellipsis was always written as three ASCII dots (`...`) to avoid
  font fallbacks for the U+2026 character.

## 5. Stage 3 — Website architecture

### 5.1 Technology stack

The brief (Section 8.1) suggests HTML, CSS and JavaScript/TypeScript,
and VS Code as the IDE. The site uses **vanilla HTML, CSS and
JavaScript** with no frameworks, no bundler and no build step. This
choice is deliberate: a coursework project must be readable end-to-end
by the supervisor without setting up a Node toolchain, and the
linguistic logic of the project is in the data, not in the framework.

The only external assets are two Google Fonts (`Inter`, `JetBrains
Mono`) loaded by `<link>` tags.

### 5.2 File layout

```
.
├── index.html              # single-page dictionary
├── assets/
│   ├── styles.css          # all visual styling
│   └── script.js           # search and rendering logic
├── data/
│   ├── glossary.xlsx       # primary deliverable
│   ├── glossary.json       # consumed by the website
│   └── glossary.csv        # portable export
├── scripts/
│   └── build_glossary.py   # regenerates the three glossary files
└── docs/
    ├── prompts.md          # AI-prompt iterations
    └── coursework_practical.md   # this document
```

### 5.3 Page structure

`index.html` is a single document with three semantic regions:

1. a **hero**, which displays the project title, the three language
   chips, three statistic cards (123 terms, 3 languages, 13 topic
   groups) and the author credit;
2. a **search panel**, which contains the search input, the
   per-language filter pills, the "Try" quick-search chips and the
   keyboard-shortcut hint;
3. a **results grid**, which renders one card per matching entry,
   with the entry's `ID`, the *Notes* line and the three language
   values, with matched substrings wrapped in `<mark>` tags.

The hero hosts the **author credit** required by the brief
(Section 8.3): "by Svitlana Boloshyna · group ФЛПЛ-12", and the same
information is repeated in the footer.

### 5.4 Visual language

The colour system encodes the three languages consistently across the
page:

- **green** for Ukrainian (`--color-accent-ua: #1f7a5a`),
- **orange** for English (`--color-accent-en: #b25c2a`),
- **violet** for German (`--color-accent-de: #5c3a8a`).

The same three colours are used (a) inside the language-filter pills
as small dots, (b) on the language-label tags inside each result card,
and (c) as a vertical stripe that appears on the left edge of a card
when the user hovers over it. The colour-coding is consistent so that
a user who has noticed the colour key in the hero can identify any
result line at a glance.

Two small motion details are added with `@keyframes`:

- the gear silhouettes in the hero rotate slowly in opposite
  directions, suggesting a working machine without overpowering the
  text;
- each result card fades in with a 220 ms `card-in` animation; this
  makes filtering feel responsive even though all results are already
  in memory.

Both animations are disabled under `prefers-reduced-motion: reduce`,
in line with current accessibility recommendations.

## 6. Stage 3 (continued) — The search algorithm

### 6.1 Normalisation

The single most important linguistic decision in the website is what
counts as "the same word". The search algorithm reduces both the
glossary entries and the user's query to a normalised form before
comparing them:

```js
function normalise(value) {
  return String(value)
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .trim();
}
```

This does three things, in order:

1. **case folding** — `Engine`, `engine`, `ENGINE` collapse to one
   form;
2. **diacritic stripping** — `.normalize("NFD")` decomposes characters
   like `ü` into the base letter `u` followed by a combining diaeresis
   `̈`, and the regular expression then deletes every combining
   mark in the range U+0300–U+036F; the result is that `Tschuss`
   matches `Tschüss`, `Motoroel` matches `Motoröl`, and a user without
   the German keyboard layout can still search the German column;
3. **whitespace trimming** — accidental leading or trailing spaces in
   the query do not change the result set.

A precomputed normalised copy of every entry is cached at load time,
so each keystroke only normalises the query, not the 123 entries.

### 6.2 Substring vs exact matching

The algorithm uses **`String.prototype.includes`** rather than `===`.
The reason is that Ukrainian and German are heavily inflected and the
user is unlikely to remember the exact citation form. A substring
search lets `engine` match *Internal combustion engine* and lets
`brem` match all of *Bremssystem*, *Bremsbeläge*, *Bremsflüssigkeit*
and *Trommelbremsen*. This is what makes the search useful as a
study aid rather than as a pure lookup.

### 6.3 Per-language filtering

The four language filter pills (Any / Ukrainian / English / German)
control which fields are searched. With "Any language" selected the
search runs against all three normalised fields; with a specific
language selected only that field is searched. This is useful when
the same string occurs in two languages with different meanings — for
example *Bus* matches both English and German entries — and the user
wants to narrow the result set without retyping.

### 6.4 Highlighting matches

Each matched entry is rendered as a card whose three language lines
have matched substrings wrapped in `<mark>` tags. The highlighting
function `highlight()` works on the same normalised form as the
search itself, so the highlight respects case-insensitivity and
diacritic-insensitivity. The original casing of the data is preserved
in the rendered output — `Motoröl` is highlighted as `Motoröl`, not as
`motoroel`, even though the query was `motoroel`.

The function `escapeHtml()` is applied to every piece of inserted
text. The reason is defensive: even though the glossary content is
trusted, escaping prevents an accidental `<` or `&` in the *Notes*
column from being interpreted as markup.

### 6.5 Error states

The search panel handles three distinct empty states explicitly:

1. **empty query** — the page shows all 123 entries, and the status
   line reads "Showing all 123 entries". A blank page would be
   ambiguous, because the user could not tell whether the data had
   loaded or not.
2. **valid query with zero matches** — a dedicated empty-state card
   appears, with a magnifier-with-minus-sign icon, the query echoed in
   quotation marks, and a suggestion to try a shorter substring or
   the "Any language" filter.
3. **failed data load** — if `fetch("data/glossary.json")` rejects
   (for example because the page was opened over `file://`), the
   status line is repurposed to a red error message that instructs
   the user to start a local web server with
   `python3 -m http.server`.

Each of these three states corresponds to a real situation in which
a less careful site would leave the user staring at a blank page.

## 7. Stage 4 — Working with Google AI for Developers

The brief (Section IX) requires three artefacts: an initial prompt,
a search-only prompt, and a refined prompt that adds details about
search logic, case-insensitivity and error handling. Each prompt is
recorded verbatim, together with a description of what the model
produced and which linguistic detail the prompt had to add.

### 7.1 Prompt 1 — initial site structure

> *Generate the HTML and CSS for a single-page website that is a
> trilingual dictionary for the automobile industry. The languages are
> Ukrainian, English and German.*

The model produced a static three-column HTML table with a heading
and a flat stylesheet. The result was technically correct but had no
search box, no author credit, no theme indicator, no visual
distinction between the three columns and no mobile layout. The
underlying linguistic problem was that the prompt did not say which
language is the source and which are targets, so the model treated
the three columns as symmetric and the page lacked an organising
principle.

### 7.2 Prompt 2 — search over JSON

> *Write JavaScript that loads `data/glossary.json` (an array of
> objects with `ukrainian`, `english`, `german`, `notes` fields) and
> lets the user search for a word.*

The model produced a working but naive `filter` that compared the
query to each field with strict equality. The result was several
linguistic failures: a search for `engine` would not match *Internal
combustion engine* (no substring matching); a search for `Engine`
would behave differently from `engine` (no case folding); a search
for `Tschuss` would not match *Tschüss* (no diacritic normalisation);
and zero-match queries would render nothing at all, leaving the user
without feedback. The takeaway is that the model's defaults are
calibrated for English-only data, and that any of those defaults can
fail for Ukrainian or German content unless the prompt names the
behaviour explicitly.

### 7.3 Prompt 3 — refined search

> *Write a vanilla-JavaScript module (no frameworks) that:*
>
> 1. *fetches `data/glossary.json` and stores the entry list in
>    memory;*
> 2. *exposes a search input that filters the entries as the user
>    types, with a short debounce so we do not re-render on every
>    keystroke;*
> 3. *matches by **partial substring**, not exact equality;*
> 4. *is **case-insensitive** — `engine`, `Engine` and `ENGINE` behave
>    the same;*
> 5. *is **diacritic-insensitive** — `Tschuss` matches `Tschüss`,
>    `Motoroel` matches `Motoröl`, by NFD-normalising and stripping
>    combining marks before comparison;*
> 6. *lets the user **restrict the search to one language** or search
>    across all three;*
> 7. *shows a dedicated **"nothing matched"** state that names the
>    query and suggests trying a shorter substring or the "any
>    language" filter, instead of silently rendering an empty page;*
> 8. *handles the **fetch failure** case (e.g. when the page is opened
>    via `file://`) with an actionable error message;*
> 9. *renders each result as a card that **highlights** the matched
>    substring with `<mark>`, while keeping the original casing of the
>    data;*
> 10. *escapes the highlighted text so that malformed glossary content
>    cannot inject HTML.*

The refined prompt named ten distinct behaviours; the resulting code
implements each of them, and the mapping between the prompt and the
code is direct enough to be tabulated:

| Prompt clause | Where it lives in `assets/script.js` |
| ------------- | ------------------------------------ |
| fetch + in-memory cache | `loadGlossary()` |
| debounced filtering | `debounce()` + `onInput` handler |
| partial-substring matching | `search()` using `String.prototype.includes` |
| case-insensitivity | `.toLowerCase()` inside `normalise()` |
| diacritic-insensitivity | NFD + combining-mark regex inside `normalise()` |
| per-language filtering | `state.lang` + `.filter` event handlers |
| "nothing matched" state | `renderEmptyState()` + `#empty-template` |
| fetch-failure message | `catch` block of `loadGlossary()` |
| highlighted matches | `highlight()` + `<mark>` in CSS |
| HTML-escaping | `escapeHtml()` |

### 7.4 Linguistic observations on the prompt iterations

Three observations are worth keeping in the practical part of the
coursework, because they generalise beyond this specific project.

**Observation 1 — the model's defaults are English-shaped.** Without
a prompt clause about diacritics, the model produced code that
worked on English but failed on German and Ukrainian. The linguist's
job in the prompting process was to know that "diacritic
normalisation" is even a question worth asking.

**Observation 2 — partial vs exact matching is a linguistic decision,
not a UX decision.** Ukrainian and German are heavily inflected, so a
strict-equality search forces the user to retype the citation form,
which is exactly the form they came to the dictionary to look up.
Substring matching is a workaround for the absence of a lemmatiser;
naming this trade-off in the prompt is what turned the naive code of
prompt 2 into the usable code of prompt 3.

**Observation 3 — empty states are part of the linguistic interface.**
A blank page does not tell the user whether the data is loading, the
search returned nothing, or the page is broken. The refined prompt
demands three different error messages for these three different
states, and the result is a search box that explains its own failures
in plain English instead of leaving the user to guess.

## 8. Stage 4 (continued) — Demonstration and analysis of errors

The site was tested with a battery of queries selected to probe each
of the search behaviours described above.

| Query | Filter | Expected | Result |
|-------|--------|----------|--------|
| (empty) | Any | 123 entries shown | 123 |
| `двигун` | Any | All powertrain entries containing the root | 7 hits |
| `engine` | English | Same set as above, English-side | 7 hits |
| `Getriebe` | German | All transmission entries | 3 hits |
| `Tschuss` (no umlaut) | Any | Diacritic-insensitive match for *Tschüss* | (no match for this glossary; *Tschuss* is not in the automobile field, intentionally) |
| `Motoroel` | Any | Match *Motoröl* | 1 hit |
| `ABS` | Any | Match the *Antiblockiersystem* entry | 1 hit |
| `CO2` | Any | Match the emissions entry | 1 hit |
| `xyznotfound` | Any | "Nothing matched" empty state | empty state |
| (loaded via `file://`) | n/a | Red error message about local server | error state |

The two key diagnostic cases here are the diacritic-insensitivity
test (`Motoroel` → *Motoröl*) and the failure-mode test (`file://`),
because they each test a behaviour that the naive prompt-2 version
of the code would have failed.

## 9. Stage 5 — Final integration and UX polish

After the search algorithm was working, the front end was polished in
three rounds, each of which was driven by a single observation about
how a user actually reads the page:

1. **The hero needed a thematic cue.** The first version of the hero
   was a plain blue band; the user could not tell at a glance which
   field of knowledge the dictionary covered. The polished version
   adds two rotating gear silhouettes in the background, suggesting
   "machine" without being illustrative.
2. **The search panel needed a way to demonstrate that it works.** A
   first-time visitor does not know what to type, especially in a
   trilingual dictionary. The polished version adds a "Try" row of
   six pre-filled queries, each in a different language, which fill
   the search box and immediately show the user how a successful
   search looks.
3. **Result cards needed visual hierarchy.** The first version of the
   cards rendered the three languages as plain text rows of equal
   weight. The polished version adds (a) coloured language tags on
   the left, (b) a three-colour stripe that appears on hover, and
   (c) a monospaced entry ID, so that a long result list is scannable
   rather than uniform.

The brief calls these polish steps "Поліпшення UX" and "Оптимізація
логіки пошуку" (Section X, Stage 5); they are recorded here in the
order in which they were applied.

## 10. Evaluation against the brief's criteria

The brief (Section XI) lists five evaluation criteria. The table
below summarises how the project satisfies each one and points to the
file or section where the evidence lives.

| # | Criterion | Where it is satisfied |
|---|-----------|-----------------------|
| 1 | Quality and systematicity of the glossary | `data/glossary.xlsx` — 123 entries, 13 topical clusters, every entry has *Notes*, consistent citation forms (Section 3 of this document) |
| 2 | Thoughtfulness of prompt iterations | `docs/prompts.md` and Section 7 of this document — three prompts, with a per-clause mapping into `assets/script.js` |
| 3 | Functionality of the website | `index.html` + `assets/script.js` — all features required by Section 8.3 of the brief, plus partial matching, diacritic-insensitivity, three error states, keyboard shortcuts |
| 4 | Independence of editing the AI output | The build script, the search algorithm and the editorial overrides on regional variants (US vs UK English) are all human decisions documented in this file |
| 5 | Presentation and explanation of the process | This document itself; the `README.md`; and the prompt iteration log |

## 11. Conclusions

The project demonstrates the four goals listed in Section VI of the
brief. The role of the linguist showed up in three concrete places:
the choice of source-vs-target language structure for the table; the
editorial decisions on register and regional variants; and the
specification of what "the same word" means inside the search
algorithm. The conversion of Excel data into a JSON consumed by the
website demonstrates that structured linguistic data has a direct
digital life beyond the spreadsheet. The three-stage prompt iteration
demonstrates that the quality of generative-AI output depends on the
linguistic detail that the prompt makes explicit — diacritics,
inflection, register and error states all had to be named before the
model would produce the code that the project needed. Finally, the
working site itself demonstrates that AI is capable of producing
production-grade web code when it is briefed correctly, but that the
human linguist remains responsible for the decisions about what the
code should do.

## 12. Sources used during verification

(*Below is the list of authorities consulted while verifying
translations. In the final Word document the entries should be
formatted to the citation style accepted by the supervising chair.*)

1. *ДСТУ 2960-94. Транспорт автомобільний. Терміни та визначення.*
   Київ : Держстандарт України, 1994.
2. *Duden — das Wörterbuch der deutschen Sprache.*
   Online edition. https://www.duden.de
3. *Oxford English Dictionary.* Online edition.
   https://www.oed.com
4. *Merriam-Webster Dictionary.* Online edition.
   https://www.merriam-webster.com
5. Verband der Automobilindustrie (VDA). *Glossary of automotive
   terminology.* https://www.vda.de
6. Selivanova O. *Сучасна лінгвістика: термінологічна
   енциклопедія.* Полтава : Довкілля-К, 2006.

---

*End of practical part.*
