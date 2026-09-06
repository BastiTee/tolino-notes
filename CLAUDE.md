# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Tolino Notes is a Python CLI that parses the `notes.txt` file produced by Tolino e-readers (highlights, notes, bookmarks — mixed across books, in one of six device languages) and converts it into per-book Markdown or JSON files.

## Commands

Built with Poetry; `make` targets are the primary interface (see `Makefile`):

- `make venv` — create/refresh the local `.venv` and install dependencies (`poetry install`)
- `make test` — run the test suite (`poetry run py.test tests`)
- `make mypy` — type-check `tolino_notes` and `tests`
- `make isort` / `make isort-apply` — check / fix import order
- `make black` — format code (`skip-string-normalization = true`, so single quotes are preserved)
- `make lint` — flake8 (max line length 88, matching black; docstrings required via flake8-docstrings)
- `make build` — runs test → mypy → isort → black → lint, then `poetry build`
- `make` (no target) — clean, create venv, build (the full default pipeline; mirrors CI)
- `make clean` — remove venv, caches, build/dist artifacts

Run a single test: `poetry run py.test tests/test_tolino_note.py::TestCode::test_lang_de_marker_note`

Run the CLI locally: `poetry run tolino-notes --input-file notes.txt --output-dir output --format md`

CI (`.github/workflows/main.yml`) runs `make` across Python 3.9–3.13 on every push to `main` and `feature/*`.

## Architecture

The pipeline has three stages, each in its own module:

1. **`__main__.py`** — CLI entry point (Click). Reads the raw `notes.txt`, splits it into individual raw note blocks on lines of 10+ dashes, and feeds each block to `TolinoNote.from_unparsed_content`. Groups parsed notes by `book_title`, then derives a filesystem-safe filename per book (lowercased, non-`[a-z0-9äöü-]` chars collapsed to `-`) and dispatches to the writer for the requested format.

2. **`tolino_note.py`** — parsing core. `LANGS` maps each supported device language (en/de/es/nl/it/fr) to the regex prefixes and date format Tolino uses for that language (e.g. `"Added on "` vs `"Hinzugefügt am "`). `TolinoNote.from_unparsed_content` is the key method: given one raw note block, it identifies the book title (first line), detects language and parses the creation date from the last line, then classifies the block as a `NoteType.HIGHLIGHT`, `NOTE`, or `BOOKMARK` based on which language-specific prefix matches. Because the raw format has no reliable structural markers, note-vs-highlight separation for `NOTE` type is a heuristic based on quote positions (see the comments in that branch) — this is the fragile, best-guess part of the codebase; if you touch it, run the full test suite and check edge cases in `tests/test_tolino_note.py`.

3. **`notes_writer.py`** — output formatting. `write_to_markdown` sorts notes by `(page, cdate)`, skips bookmarks, and writes one Markdown file per book (notes rendered as a quoted highlight followed by a blockquoted user comment). `write_to_json` sorts the same way but serializes all note types including bookmarks.

Language support is added by extending the `LANGS` dict with a new entry (prefixes + `date_format`) — no other code changes are needed for a new language, provided the raw format follows the existing pattern.

Tests (`tests/test_tolino_note.py`) are table-driven per language/note-type combination and construct raw note blocks inline as multi-line strings mimicking the actual `notes.txt` format — use these as reference when adding language or format-edge-case coverage.
