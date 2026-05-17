/**
 * Trilingual Travel & Hospitality Dictionary
 *
 * Loads the glossary from data/glossary.json and provides a case-insensitive
 * partial-match search across Ukrainian, English and German. Optionally
 * restricts the search to a single language. Renders results as cards with
 * matched substrings highlighted.
 */

(function () {
  "use strict";

  const SEARCH_FIELDS = ["ukrainian", "english", "german"];
  const MAX_RESULTS = 60;
  const DATA_URL = "data/glossary.json";

  const els = {
    input: document.getElementById("search-input"),
    clear: document.getElementById("clear-button"),
    status: document.getElementById("status-line"),
    results: document.getElementById("results"),
    filters: document.querySelectorAll(".filter"),
    chips: document.querySelectorAll(".quick__chip"),
    template: document.getElementById("card-template"),
    emptyTemplate: document.getElementById("empty-template"),
  };

  const state = {
    entries: [],
    lang: "any",
    query: "",
  };

  // ---------- Normalisation ----------
  // Lowercase + strip diacritics so "Tschuss" matches "Tschüss",
  // "danke" matches "Danke", etc.
  function normalise(value) {
    if (value == null) return "";
    return String(value)
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .trim();
  }

  // ---------- Data loading ----------
  async function loadGlossary() {
    try {
      const response = await fetch(DATA_URL);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();
      state.entries = (data.entries || []).map((entry) => ({
        ...entry,
        _normalised: {
          ukrainian: normalise(entry.ukrainian),
          english: normalise(entry.english),
          german: normalise(entry.german),
        },
      }));
      render();
    } catch (err) {
      console.error("Failed to load glossary:", err);
      els.status.textContent =
        "Could not load the glossary. If you opened the page directly from the file system, please run a local web server (e.g. `python3 -m http.server`) so the browser can fetch data/glossary.json.";
      els.status.classList.add("status--error");
    }
  }

  // ---------- Search ----------
  function search(rawQuery, lang) {
    const query = normalise(rawQuery);
    if (!query) {
      return state.entries;
    }
    const fields = lang === "any" ? SEARCH_FIELDS : [lang];
    return state.entries.filter((entry) =>
      fields.some((field) => entry._normalised[field].includes(query))
    );
  }

  // ---------- Rendering ----------
  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  // Wraps every case-insensitive, diacritic-insensitive occurrence of
  // `query` inside `text` in <mark>...</mark>, preserving original casing.
  function highlight(text, query) {
    if (!query) return escapeHtml(text);

    const normText = normalise(text);
    const normQuery = normalise(query);
    if (!normQuery || !normText.includes(normQuery)) {
      return escapeHtml(text);
    }

    // Walk both strings in parallel: the normalised forms share length
    // (NFD-stripping diacritic marks does not change the count of base
    // characters for our languages), so indices in normText map 1:1 to
    // indices in text.
    if (normText.length !== text.length) {
      // Fallback: simple lowercase find without diacritic insensitivity.
      const lower = text.toLowerCase();
      const q = query.toLowerCase();
      let out = "";
      let i = 0;
      while (i < text.length) {
        const found = lower.indexOf(q, i);
        if (found === -1) {
          out += escapeHtml(text.slice(i));
          break;
        }
        out += escapeHtml(text.slice(i, found));
        out +=
          "<mark>" + escapeHtml(text.slice(found, found + q.length)) + "</mark>";
        i = found + q.length;
      }
      return out;
    }

    let out = "";
    let i = 0;
    while (i < text.length) {
      const found = normText.indexOf(normQuery, i);
      if (found === -1) {
        out += escapeHtml(text.slice(i));
        break;
      }
      out += escapeHtml(text.slice(i, found));
      out +=
        "<mark>" +
        escapeHtml(text.slice(found, found + normQuery.length)) +
        "</mark>";
      i = found + normQuery.length;
    }
    return out;
  }

  function renderEmptyState(query) {
    els.results.innerHTML = "";
    if (els.emptyTemplate) {
      const node = els.emptyTemplate.content.firstElementChild.cloneNode(true);
      node.querySelector(".results__empty-title").textContent =
        `Nothing matched “${query}”`;
      els.results.appendChild(node);
    } else {
      const safeQuery = escapeHtml(query);
      els.results.innerHTML = `
        <div class="results__empty">
          <strong>Nothing matched &ldquo;${safeQuery}&rdquo;</strong>
          Try a different spelling or switch the language filter to <em>Any language</em>.
        </div>
      `;
    }
  }

  function renderResults(matches, query) {
    els.results.innerHTML = "";

    if (matches.length === 0) {
      renderEmptyState(query);
      return;
    }

    const shown = matches.slice(0, MAX_RESULTS);
    const fragment = document.createDocumentFragment();

    for (const entry of shown) {
      const node = els.template.content.firstElementChild.cloneNode(true);
      node.querySelector(".card__id").textContent = `#${entry.id}`;
      node.querySelector(".card__notes").textContent = entry.notes || "";

      for (const field of SEARCH_FIELDS) {
        const valueEl = node.querySelector(`[data-field="${field}"]`);
        valueEl.innerHTML = highlight(entry[field], query);
      }

      fragment.appendChild(node);
    }

    els.results.appendChild(fragment);
  }

  function updateStatus(matches, query) {
    els.status.classList.remove("status--error");
    const total = state.entries.length;

    if (!query) {
      els.status.textContent = `Showing all ${total} entries.`;
      return;
    }

    const count = matches.length;
    const langLabel =
      state.lang === "any"
        ? "all languages"
        : state.lang.charAt(0).toUpperCase() + state.lang.slice(1);

    if (count === 0) {
      els.status.textContent = `No matches for "${query}" in ${langLabel}.`;
    } else if (count > MAX_RESULTS) {
      els.status.textContent = `${count} matches for "${query}" in ${langLabel} — showing first ${MAX_RESULTS}.`;
    } else {
      els.status.textContent = `${count} match${count === 1 ? "" : "es"} for "${query}" in ${langLabel}.`;
    }
  }

  function render() {
    const matches = search(state.query, state.lang);
    updateStatus(matches, state.query);
    renderResults(matches, state.query);
    els.clear.classList.toggle("is-visible", state.query.length > 0);
  }

  // ---------- Wiring ----------
  function debounce(fn, delay) {
    let t;
    return function (...args) {
      clearTimeout(t);
      t = setTimeout(() => fn.apply(this, args), delay);
    };
  }

  function bindEvents() {
    const onInput = debounce(() => {
      state.query = els.input.value;
      render();
    }, 80);

    els.input.addEventListener("input", onInput);

    els.clear.addEventListener("click", () => {
      els.input.value = "";
      state.query = "";
      render();
      els.input.focus();
    });

    els.chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        const q = chip.getAttribute("data-query") || "";
        els.input.value = q;
        state.query = q;
        render();
        els.input.focus();
      });
    });

    els.filters.forEach((btn) => {
      btn.addEventListener("click", () => {
        const lang = btn.getAttribute("data-lang");
        if (lang === state.lang) return;
        state.lang = lang;
        els.filters.forEach((b) => {
          const isActive = b === btn;
          b.classList.toggle("is-active", isActive);
          b.setAttribute("aria-checked", isActive ? "true" : "false");
        });
        render();
      });
    });

    // Press "/" to focus the search input.
    document.addEventListener("keydown", (e) => {
      if (e.key === "/" && document.activeElement !== els.input) {
        e.preventDefault();
        els.input.focus();
      }
      if (e.key === "Escape" && document.activeElement === els.input) {
        els.input.value = "";
        state.query = "";
        render();
      }
    });
  }

  // ---------- Init ----------
  bindEvents();
  loadGlossary();
})();
