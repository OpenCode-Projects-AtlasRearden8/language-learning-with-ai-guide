# Learning a Language with AI

*AI as your patient practice partner — a manual of short, honest sessions
for real life.*

Written in the style of Dylan Asdale's *The Massive AI Manual* and the hub
site [dylanasdale.github.io](https://dylanasdale.github.io): plain English,
step by step, never condescending — like a friend explaining it over coffee.

**By Asdale Dynamics, LLC.** Beginner-friendly AI education, guides, and
practical tools.

## What this is

A complete guide for learning a language around a real life — work shifts,
kids, commutes — using AI as an endlessly patient conversation partner:

| Chapter | File | What you get |
|---|---|---|
| Start Here | `docs/00-start-here.md` | Orientation, chapter map, the five-finger summary |
| 1. Fifteen Minutes a Day | `docs/01-fifteen-minutes-a-day.md` | Daily plans that survive nurse-shift weeks; weekly rhythm |
| 2. Your AI Practice Partner | `docs/02-your-ai-practice-partner.md` | Local models (free, private, offline) + the session template |
| 3. Conversation Drills | `docs/03-conversation-drills.md` | Six drills and the correction loop that makes practice work |
| 4. Vocabulary in Plain Files | `docs/04-vocabulary-in-plain-files.md` | Spaced review over a plain CSV — no apps, no accounts, no cloud |
| 5. Check the Grammar | `docs/05-check-the-grammar.md` | Verifying AI grammar claims against real sources, rule of two |
| 6. Films, Songs, Labels | `docs/06-films-songs-labels.md` | The 20-minute scene, sticky-note lyrics, grocery-label immersion |
| 7. The Travel Countdown | `docs/07-travel-countdown.md` | A 10-day intensive driven by your actual itinerary |
| 8. Quitting Without Guilt | `docs/08-quitting-without-guilt.md` | The plateau protocol, good quits vs. rot, maintenance months |
| Glossary | `docs/glossary.md` | Every term in plain English |

Plus companion pieces:

- **`templates/`** — weekly plan cards (5 of them: word week, sentence week,
  listening week, rescue week, your own), the phrase-list template, a filled
  starter example, and a starter vocabulary file. Built into the site and
  copied to `site/templates/files/` as raw copy-paste files.
- **`scripts/vocab.py`** — a small, tested spaced-repetition program over a
  plain CSV file (add / due / review / stats). You own the file; the tool
  just schedules it.
- **`build.py`** — a dependency-free Python script that turns the docs and
  templates into a static HTML site in `site/`.

This guide pairs with **Study Smarter with AI** (study skills: notes into
quizzes, explain-it-back, catching hallucinations, spaced-review theory).
It builds on that guide without repeating it.

## How to run it

You need Python 3.8+ and nothing else.

```bash
python3 build.py          # build the site into site/
python3 build.py --check  # build + verify structure, links, content
python3 test.py           # run the test suite (17 tests, includes build check)
```

Then either open `site/index.html` directly in a browser, or serve it:

```bash
python3 -m http.server 8000 --directory site
# visit http://localhost:8000
```

To try the vocabulary tool:

```bash
python3 scripts/vocab.py due                       # see what's due today
python3 scripts/vocab.py stats                     # your boxes, at a glance
python3 scripts/vocab.py review                    # an interactive session
python3 scripts/vocab.py --file my-vocab.csv add perro dog "a common pet"
python3 scripts/vocab.py --help                    # all commands
```

Word data lives in whatever CSV you point `--file` at; a starter
(`vocab/sample-vocab.csv`) is included. Everything stays on your machine.

## Repository layout

```text
docs/       the manual, chapter by chapter (markdown)
templates/  weekly plan cards, phrase lists, starter vocab file
vocab/      starter vocabulary CSV consumed by scripts/vocab.py
scripts/    vocab.py (spaced review over plain CSV)
build.py    docs + templates -> static site
test.py     test suite for the tool and the build
site/       built static HTML (regenerate anytime)
```

## Local-first, private

No accounts, no tracking, no data leaves your machine. The AI choices in
chapter 2 favor a local model; all your vocabulary and phrases are plain
files you can read, edit, and back up yourself.

## License

MIT — see `LICENSE`. Copyright (c) 2026 Asdale Dynamics, LLC.

## About

From Dylan Asdale, author of *The Massive AI Manual* — AI explained "like a
friend would": plain English, step by step, never condescending. This guide
is part of a series of hands-on manuals by Asdale Dynamics, LLC.
