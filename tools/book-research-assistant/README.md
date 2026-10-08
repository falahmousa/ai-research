# Book Research Helper

A small, human-reviewed command-line tool for finding **public bibliographic metadata** from [Open Library](https://openlibrary.org/developers/api). Built as an optional addition to [Books & Evidence](../../books-evidence/README.md).

It does **not** access Blinkist, copy book summaries, download book texts, assess whether claims are true, or upload information about its users. Records are explicitly marked **Unverified** until checked. Requires Python 3.9 or later; no third-party packages.

## Usage

Run locally (network required for a search):

```sh
python book_research.py "democracy elections" --limit 5
python book_research.py "democracy elections" --limit 5 --csv research_books.csv
```

Generate an offline worksheet, no network needed:

```sh
python book_research.py --blank-template evidence_review.csv
```

Run unit tests using a simulated network response:

```sh
python -m unittest discover -s tools/book-research-assistant -v
```

The public search endpoint is rate-limited by the provider. Use one user-invoked request at a time, do not batch or scrape, verify edition and publisher data, and consult [Open Library API use guidance](https://openlibrary.org/developers/api) before building a commercial service.

## Related services

The software is offered as a research aid. Tailored source checks and comparative briefs are commissioned separately through [falahmousa.com](https://falahmousa.com/contact/).

Copyright 2026 Falah Mousa. No licence for redistribution is granted at present; prospective contributors should request permission.
