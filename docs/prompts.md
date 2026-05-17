# AI Prompt Iterations

This document records the prompts that were given to a code-generation AI
(Google AI for Developers / Gemini family of models) while building this
project, and shows how the output changed as the prompts were refined.
It satisfies section **IX. Робота з Google AI for Developers** of the
course brief.

The course brief asks for three artefacts:

1. an **initial prompt** for the structure of the site,
2. a **separate prompt** for generating the search code over the
   Excel / JSON / CSV file,
3. a **refined prompt** that adds details about search logic,
   case-insensitivity and error handling.

For each step we record the prompt verbatim, summarise the AI output and
note which linguistic aspects had to be clarified.

---

## Step 1 — Initial prompt: site structure

> **Prompt 1 (initial, deliberately under-specified)**
>
> *Generate the HTML and CSS for a single-page website that is a
> trilingual dictionary for the automobile industry. The languages are
> Ukrainian, English and German.*

**What the AI produced.** A generic three-column HTML table with a
heading and a flat CSS stylesheet. The page was usable but had several
issues:

- no search box at all — the user could only scroll;
- no author credit (mandatory per section 8.3 of the brief);
- no theme indication or entry count;
- the three languages were treated symmetrically, with no visual cues to
  tell them apart, which makes the page harder to scan;
- mobile layout broke because the table did not collapse.

**Linguistic observations.** Because the prompt did not say which
language is the *source* and which are *targets*, the AI produced a
table where every column was equivalent. For a dictionary aimed at a
Ukrainian-speaking user, the source language (Ukrainian) should be
visually anchored. This is a typical case where a missing linguistic
detail produces flat, undifferentiated output.

---

## Step 2 — Separate prompt: search over Excel / JSON / CSV

> **Prompt 2 (search-only, still under-specified)**
>
> *Write JavaScript that loads `data/glossary.json` (an array of objects
> with `ukrainian`, `english`, `german`, `notes` fields) and lets the
> user search for a word.*

**What the AI produced.** A working function that does
`entries.filter(e => e.ukrainian === query || e.english === query || e.german === query)`
and prints matches to the console.

Problems with this output:

- the comparison is **strict equality**, so `"engine"` would not match
  the entry whose English value is `"Internal combustion engine"`;
- the comparison is **case-sensitive**, so `"Engine"` works but
  `"engine"` does not when the data is capitalised, and vice versa;
- there is **no normalisation of diacritics**: `"Tschuss"` will not find
  `"Tschüss"`, `"motoroel"` will not find `"Motoröl"`, and Ukrainian
  apostrophe variants (`'`, `’`) silently mismatch;
- there is **no rendering**: matches go to `console.log`, so the user
  never sees a result;
- there is **no behaviour for the empty query or for zero matches** —
  the page just stays blank, which the user cannot distinguish from
  "still loading" or "broken".

**Linguistic observations.** This step made the importance of
*normalisation* concrete: it is not enough to lowercase strings, you
have to decide what counts as "the same character". Concretely we have
to handle

- **case** — `Engine` vs `engine` (English uppercase nouns at the start
  of dictionary entries vs lowercase queries);
- **diacritics** — `ö ü ß` in German, `і ї є` in Ukrainian — a German
  speaker using a US keyboard will type `Stossstange`, not `Stoßstange`;
- **partial matches vs whole-word matches** — for a learner-facing
  dictionary, partial matches are far more useful, because users often
  remember only a fragment of the word and because Ukrainian and German
  are heavily inflected, so a single citation form will not match every
  surface form the user types;
- **morphological variation** is out of scope for this project (we are
  not doing lemmatisation), but it is the reason partial matching is the
  safer default.

---

## Step 3 — Refined prompt: full search behaviour

> **Prompt 3 (refined and explicit)**
>
> *Write a vanilla-JavaScript module (no frameworks) that:*
>
> 1. *fetches `data/glossary.json` and stores the entry list in memory;*
> 2. *exposes a search input that filters the entries as the user
>    types, with a short debounce so we do not re-render on every
>    keystroke;*
> 3. *matches by **partial substring**, not exact equality;*
> 4. *is **case-insensitive** — `engine`, `Engine` and `ENGINE` must
>    behave the same;*
> 5. *is **diacritic-insensitive** — `Tschuss` matches `Tschüss`,
>    `Motoroel` matches `Motoröl`, by NFD-normalising and stripping
>    combining marks before comparison;*
> 6. *lets the user **restrict the search to one language** (Ukrainian,
>    English, German) or search across all three;*
> 7. *shows a dedicated **"nothing matched"** state that names the
>    query and suggests trying a shorter substring or the "any
>    language" filter, instead of silently rendering an empty page;*
> 8. *handles the **fetch failure** case (e.g. when the page is opened
>    via `file://` rather than `http://`) with an actionable error
>    message that tells the user to start a local web server;*
> 9. *renders each result as a card that **highlights** the matched
>    substring with `<mark>`, while keeping the original casing of the
>    data;*
> 10. *escapes the highlighted text so that malformed glossary content
>     cannot inject HTML.*

**What the AI produced.** The code shipped as `assets/script.js`. The
behaviours requested in the prompt map onto the code as follows:

| Requirement                | Where it lives in `assets/script.js`       |
| -------------------------- | ------------------------------------------ |
| fetch + in-memory cache    | `loadGlossary()`                           |
| debounced filtering        | `debounce()` + `onInput` handler           |
| partial-substring matching | `search()` using `String.prototype.includes` |
| case-insensitivity         | `normalise()` calls `.toLowerCase()`       |
| diacritic-insensitivity    | `normalise()` strips `̀-ͯ`       |
| per-language filtering     | `state.lang`, `.filter` buttons            |
| "nothing matched" state    | `renderEmptyState()`                       |
| fetch-failure message      | `catch` block of `loadGlossary()`         |
| highlighted matches        | `highlight()` + `<mark>` in the CSS        |
| HTML-escaping              | `escapeHtml()`                             |

**Linguistic observations.** The refined prompt forced us to name every
behaviour we wanted, instead of leaving the AI to choose defaults that
happen to make sense for English-only data. The biggest payoff was
diacritic normalisation: without it, a non-trivial fraction of the
German entries and several Ukrainian entries would be effectively
unsearchable for any user without the right keyboard layout.

---

## Take-aways

1. **The first prompt is almost never enough.** The model produces
   technically correct but linguistically naive output until you tell it
   what "the same word" means in your data.
2. **Linguistic decisions are product decisions.** Whether to do exact
   match vs substring match, whether to fold diacritics, whether to
   collapse the apostrophe variants `'` / `’` / `ʼ` in Ukrainian — these
   are choices about who the dictionary is for, and they have to be
   stated explicitly in the prompt.
3. **Error states are part of the linguistics, too.** A blank page is
   not the same as "no matches", and "no matches" is not the same as "I
   could not load the data". The third prompt explicitly asks for both
   states, which is why the final UI is usable in both cases.
