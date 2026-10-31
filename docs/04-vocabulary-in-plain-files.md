# Vocabulary in Plain Files

Flashcard apps are great — until they shut down, get bought, lose your
export, or ask for an account you'll never use again. This chapter keeps
your vocabulary the way you'd keep your savings: **somewhere you actually
control.**

Everything here is plain text files in one folder, plus one small Python
program (`scripts/vocab.py`) that does the scheduling for you. No accounts,
no cloud, no subscription. If the tool vanished, your vocabulary survives
in files you can read with Notepad.

## The two files

**1. `vocab.csv`** — one row per word, five plain columns:

| Column | Meaning | Example |
|---|---|---|
| `word` | the word or phrase | `manzana` |
| `meaning` | your meaning line, your language | `apple` |
| `due` | date you should see it next | `2026-10-30` |
| `box` | memory strength 0–7 | `3` |
| `note` | anything — example, trap, source | `fruta fresca` |

You can open, edit, back up, and email this file. That's the point.

**2. `phrases-[topic].md`** — your phrase lists (chapter 6 templates have
the format). Full sentences you want to *steal and keep*, organized by real
situations: airport, pharmacy, small talk at a children's party. Words live
in `vocab.csv`; the sentences that make words useful live here.

A starter pair is included: `vocab/sample-vocab.csv` and
`templates/phrase-list-template.md`. Copy both into your practice folder.

## How the schedule works

`vocab.py` runs a simple box system — the same idea behind every flashcard
app, visible in a spreadsheet you can read:

- A word starts in **box 0**, due tomorrow.
- When you recall it correctly, it moves **up one box**, and the wait
  grows to match the box: 1, 2, 4, 8, 16, 32, 64 days — until a word in
  box 7 comes back about every two months.
- When you forget it, it sits right back at **box 1** (or stays at 0 if
  it never lifted off) — due again tomorrow, not banished for good.
- Sessions stay small: the program shows no more than 12 cards a day by
  default, so "due" never snowballs into a 45-minute guilt pile.

Why this interval pattern works (and how to tune it if you like) is
covered gently in the sister guide's chapter 3, *Spaced Review* — here we
care mostly that it's automated and you can see the mechanism.

## Using `vocab.py`

You need Python 3 (already on every Mac and Linux machine; a two-minute
install on Windows). Every command ends with what happened, in writing.

```bash
# from your practice folder
python3 scripts/vocab.py --file my-vocab.csv add manzana apple "la fruta"
python3 scripts/vocab.py --file my-vocab.csv due          # today's shortlist
python3 scripts/vocab.py --file my-vocab.csv review       # the 5-minute session
python3 scripts/vocab.py --file my-vocab.csv stats        # how the boxes look
```

- `add WORD MEANING "NOTE"` — puts a word in the pile, box 0, due tomorrow.
- `due` — shows what's due today and what's coming; run it when you don't
  want a full session.
- `review` — the actual drill. It shows the word, you say the meaning
  **out loud** (this matters — chapter 2), press Enter to check, then
  grade yourself honestly: `y` (knew it) or `n` (didn't).
- `stats` — words per box, next due, anything due today. Your scoreboard,
  judgment-free.

One flag matters: `--max 8` makes a session shorter. `--max 20` longer.

## Grading honestly (the whole game)

The program believes you. That's the strength and the danger. When your
tongue hesitates for four unhurried seconds before the word comes, the
truthful grade is **"knew it with effort" = `y`, but keep the honest rule:
did you say it out loud, unprompted, within ten seconds?** Anything less is
`n`, and `n` is a good answer — it feeds the word back while you still care.

Fifty shed cards loved at `n` beat one hundred lost cards politely passed
as `y`.

## Where AI fits in this chapter

Two jobs, both from the partner in chapter 2:

**Make the cards.** Paste your CORRECTIONS TABLE from chapter 3 and ask:

> From this session's corrections table, pick the 3 items I'll use most
> this month. Give each as: word/phrase, plain meaning, one natural
> example sentence in context.

Then add those by hand — typing each one deliberately. (You'll also find
drills already throw vocabulary worth keeping.)

**Review words through context.** Once a week, run the due words through
the partner:

> Using only these words — [paste 8 words from vocab.csv] — write a four-
> line mini story in [LANGUAGE] at my level, where each word appears once
> and every gap between words is one I could fill in.

Reading-and-filling your own words in context is worth more reviews than
the same card ten times.

## Backups that don't blink

Plain files back up by copying. Two habits:

- Put your practice folder in whatever automatic backup you already have
  (cloud sync at home, USB stick on payday, whatever). A folder of
  `.csv`/`.md` files syncs in milliseconds.
- Or simply: once a month, copy the whole folder to one other place.

That's it. Your election to move to a fancy app later can happen at any
time — and taking the CSV with you will be trivial, because it's a CSV.
