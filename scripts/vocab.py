#!/usr/bin/env python3
"""vocab.py — spaced vocabulary review over a plain CSV file.

Part of *Learning a Language with AI* (Asdale Dynamics, LLC).
Local-first, zero dependencies: Python 3 standard library only.

The vocabulary file is a five-column CSV (readable in any text editor
or spreadsheet):

    word,meaning,due,box,note

  word    the word or phrase to learn
  meaning plain meaning in your own words
  due     ISO date the word should next be reviewed (YYYY-MM-DD)
  box     memory strength, 0..7 (a simple Leitner box system)
  note    anything: example, trap, source; may be empty

Correctly recalled words move up one box (wait doubles, up to 128
days); forgotten words fall back to box 1 (or stay at 0) and come back
tomorrow. Sessions cap at --max cards so "due" never snowballs.

Usage:
    python3 vocab.py [--file FILE] add WORD MEANING [NOTE]
    python3 vocab.py [--file FILE] due
    python3 vocab.py [--file FILE] review [--max N]
    python3 vocab.py [--file FILE] stats [--max N]

If --file is omitted, defaults to vocab/sample-vocab.csv next to the
script, so the tool works out of the box.
"""

import argparse
import csv
import datetime
import sys
from pathlib import Path

FIELDS = ["word", "meaning", "due", "box", "note"]
DEFAULT_FILE = Path(__file__).resolve().parent.parent / "vocab" / "sample-vocab.csv"

# days to wait after a correct recall, indexed by the box you land in
# (box 0 is new: due tomorrow; box 7 is the top: about every two months)
BOX_TO_WAIT = {0: 1, 1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32, 7: 64}
MAX_BOX = 7


class VocabError(Exception):
    """User-facing error; printed cleanly, no traceback."""


# --------------------------------------------------------------- file I/O

def load(file_path: Path) -> list[dict]:
    """Load the CSV, returning a list of card dicts (skipping junk rows)."""
    if not file_path.exists():
        return []
    cards = []
    with file_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        rows = list(reader)
    if rows and [c.strip().lower() for c in rows[0]] == FIELDS:
        rows = rows[1:]
    for lineno, row in enumerate(rows, start=2):
        if not row or all(not c.strip() for c in row):
            continue
        word = row[0].strip()
        meaning = row[1].strip() if len(row) > 1 else ""
        if not word or not meaning:
            print(f"warning: line {lineno} skipped "
                  "(needs a word and a meaning)", file=sys.stderr)
            continue
        due = row[2].strip() if len(row) > 2 else ""
        box_raw = row[3].strip() if len(row) > 3 else ""
        note = row[4].strip() if len(row) > 4 else ""
        try:
            due_date = datetime.date.fromisoformat(due)
        except ValueError:
            due_date = datetime.date.today()  # bad/missing due: due now
        try:
            box = max(0, min(MAX_BOX, int(box_raw)))
        except ValueError:
            box = 0
        cards.append(
            {"word": word, "meaning": meaning,
             "due": due_date, "box": box, "note": note})
    return cards


def save(file_path: Path, cards: list[dict]) -> None:
    """Write the CSV back; creates parent directories and a header."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(FIELDS)
        for c in cards:
            writer.writerow([c["word"], c["meaning"],
                             c["due"].isoformat(), c["box"], c["note"]])


# --------------------------------------------------------------- logic

def find_card(cards: list[dict], word: str) -> dict | None:
    """Case-insensitive duplicate lookup."""
    for c in cards:
        if c["word"].casefold() == word.casefold():
            return c
    return None


def add_card(cards: list[dict], word: str, meaning: str,
             note: str = "", today: datetime.date | None = None
             ) -> tuple[list[dict], str]:
    """Add a word (box 0, due tomorrow). Returns (cards, message)."""
    today = today or datetime.date.today()
    if not word or not meaning:
        raise VocabError("a card needs both a word and a meaning")
    existing = find_card(cards, word)
    if existing:
        return cards, (f"already in the file: '{existing['word']}' "
                       f"(box {existing['box']}) — not added twice")
    cards = cards + [{
        "word": word, "meaning": meaning,
        "due": today + datetime.timedelta(days=1), "box": 0, "note": note,
    }]
    return cards, (f"added '{word}' -> '{meaning}' (box 0, "
                   f"due {today + datetime.timedelta(days=1)})")


def grade(card: dict, known: bool, today: datetime.date | None = None
          ) -> datetime.date:
    """Apply one recall result in place; return the new due date."""
    today = today or datetime.date.today()
    if known:
        card["box"] = min(MAX_BOX, card["box"] + 1)
        wait = BOX_TO_WAIT[card["box"]]
    else:
        card["box"] = 0 if card["box"] <= 0 else 1
        wait = 1
    card["due"] = today + datetime.timedelta(days=wait)
    return card["due"]


def due_cards(cards: list[dict], today: datetime.date | None = None
              ) -> list[dict]:
    """Cards due today or overdue, oldest due first."""
    today = today or datetime.date.today()
    return sorted([c for c in cards if c["due"] <= today],
                  key=lambda c: (c["due"], c["word"].casefold()))


def upcoming(cards: list[dict], today: datetime.date | None = None,
             limit: int = 8) -> list[dict]:
    """Next cards to become due, soonest first."""
    today = today or datetime.date.today()
    not_due = [c for c in cards if c["due"] > today]
    return sorted(not_due, key=lambda c: (c["due"], c["word"].casefold()))[:limit]


# --------------------------------------------------------------- commands

def cmd_add(args, today: datetime.date) -> list[str]:
    cards = load(Path(args.file))
    cards, msg = add_card(cards, args.word, args.meaning,
                          note=args.note or "", today=today)
    save(Path(args.file), cards)
    return [msg]


def cmd_due(args, today: datetime.date) -> list[str]:
    cards = load(Path(args.file))
    due = due_cards(cards, today)
    out = []
    if not cards:
        return ["the vocab file is empty — add a word with: "
                f"{Path(sys.argv[0]).name} add WORD MEANING"]
    out.append(f"{len(due)} due today or overdue, of {len(cards)} words:")
    for c in due:
        late = (today - c["due"]).days
        late_txt = f", {late} day{'s' if late != 1 else ''} late" if late else ""
        out.append(f"  [{c['box']}] {c['word']} — {c['meaning']}{late_txt}")
    nxt = upcoming(cards, today)
    if nxt:
        out.append("next up (not due yet):")
        for c in nxt:
            out.append(f"  [{c['box']}] {c['word']} "
                       f"(due {c['due'].isoformat()})")
    if due:
        out.append(f"run 'review' to work through today's {len(due)} "
                   "(or fewer with --max)")
    return out


def cmd_review(args, today: datetime.date) -> list[str]:
    """Interactive session. Prompts on stdin; results written back."""
    file_path = Path(args.file)
    cards = load(file_path)
    due = due_cards(cards, today)[: max(1, args.max)]
    out = []
    if not due:
        return ["nothing due today — the schedule rests, and so can you."
                if cards else "the vocab file is empty — nothing to review."]

    graded = 0
    halted = False
    for c in due:
        print(f"\n[{c['box']}]  {c['word']}")
        print("       (say it out loud, then press Enter to check)")
        if sys.stdin.readline() == "":
            halted = True
            break
        print(f"  -> {c['meaning']}" + (f"   ({c['note']})" if c["note"] else ""))
        print("  said it, unprompted, within ten seconds? [y/n/q]")
        while True:
            answer = sys.stdin.readline().strip().lower()
            if answer in ("y", "n", "q", ""):
                break
            print("  'y' knew it, 'n' missed it, 'q' stop the session")
        if answer in ("q", ""):
            out.append("input ended or session stopped — results saved so far.")
            break
        known = answer == "y"
        new_due = grade(c, known, today)
        graded += 1
        wait = (new_due - today).days
        verdict = (f"box {c['box']}, next in {wait} day"
                   f"{'s' if wait != 1 else ''}" if known
                   else "back to box 0, repeats tomorrow")
        print(f"  {c['word']}: {verdict}")
    if graded:
        save(file_path, cards)
    if halted:
        return ["input closed before any grading — nothing changed."]
    left = len(due_cards(cards, today))
    out.append(f"session done — {graded} card(s) graded, "
               f"{left} still due for next time." if left
               else f"session done — {graded} graded, "
               "pile cleared. Nicely held.")
    return out


def cmd_stats(args, today: datetime.date) -> list[str]:
    cards = load(Path(args.file))
    if not cards:
        return ["the vocab file is empty — nothing to score yet."]
    boxes: dict[int, int] = {}
    for c in cards:
        boxes[c["box"]] = boxes.get(c["box"], 0) + 1
    out = [f"{len(cards)} words, "
           f"{len(due_cards(cards, today))} due today."]
    for box in sorted(boxes):
        wait = BOX_TO_WAIT[box]
        out.append(f"  box {box}: {boxes[box]:>3} word(s) "
                   f"(wait ~{wait} day{'s' if wait != 1 else ''})")
    total_recalled = sum(v for k, v in boxes.items() if k >= 2)
    if total_recalled:
        out.append(f"  confidently known (box 2+): {total_recalled} — good tail.")
    return out


# --------------------------------------------------------------- main

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="vocab.py",
        description="Spaced vocabulary review over a plain CSV file.")
    parser.add_argument("--file", default=str(DEFAULT_FILE),
                        help="vocabulary CSV (default: vocab/sample-vocab.csv)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a word (box 0, due tomorrow)")
    p_add.add_argument("word")
    p_add.add_argument("meaning")
    p_add.add_argument("note", nargs="?", default="")

    for name, help_txt in (("due", "show today's due words and what's next"),
                           ("review", "interactive review session"),
                           ("stats", "words per box, simple scoreboard")):
        p = sub.add_parser(name, help=help_txt)
        if name != "due":
            p.add_argument("--max", type=int, default=12,
                           help="max cards this session (default 12)")

    args = parser.parse_args(argv)
    today = datetime.date.today()

    handlers = {"add": cmd_add, "due": cmd_due, "review": cmd_review,
                "stats": cmd_stats}
    handler = handlers[args.command]
    if args.command in ("review", "stats") and not hasattr(args, "max"):
        args.max = 12

    try:
        lines = handler(args, today)
    except VocabError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
