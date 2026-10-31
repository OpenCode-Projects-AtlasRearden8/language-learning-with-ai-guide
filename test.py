#!/usr/bin/env python3
"""Test suite for Learning a Language with AI.

Covers:
  - scripts/vocab.py: add/due/review/stats logic, grading rules,
    duplicate handling, malformed rows, CLI behavior (including the
    piped-input/EOF path).
  - build.py: --check build verification (structure, links, content).

Zero dependencies. Run:
    python3 test.py
Exit code 0 = everything passes.
"""

import datetime
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))

import vocab  # noqa: E402

SAMPLE = ROOT / "vocab" / "sample-vocab.csv"
BUILD = ROOT / "build.py"
SCRIPT = ROOT / "scripts" / "vocab.py"

T = datetime.date(2026, 10, 31)  # fixed "today" for deterministic tests


def run_cli(args, stdin=None, csv_file=None):
    cmd = [sys.executable, str(SCRIPT), "--file", str(csv_file or SAMPLE),
           *args]
    return subprocess.run(cmd, input=stdin, capture_output=True,
                          text=True, timeout=60)


class GradeLogic(unittest.TestCase):
    def test_correct_climbs_boxes(self):
        card = {"word": "perro", "meaning": "dog", "box": 0,
                "due": T, "note": ""}
        # first correct recall -> box 1, still seen tomorrow
        self.assertEqual(vocab.grade(card, True, T), T + datetime.timedelta(1))
        self.assertEqual(card["box"], 1)
        for expected_box, wait in ((2, 2), (3, 4), (4, 8), (5, 16),
                                   (6, 32), (7, 64), (7, 64)):
            vocab.grade(card, True, T)
            self.assertEqual(card["box"], expected_box)
            self.assertEqual(card["due"], T + datetime.timedelta(wait))

    def test_miss_drops_to_box1_and_tomorrow(self):
        card = {"word": "x", "meaning": "y", "box": 4, "due": T, "note": ""}
        vocab.grade(card, False, T)
        self.assertEqual(card["box"], 1)
        self.assertEqual(card["due"], T + datetime.timedelta(1))
        vocab.grade(card, False, T)  # already low: stays at box 1
        self.assertEqual(card["box"], 1)
        self.assertEqual(card["due"], T + datetime.timedelta(1))
        new_card = {"word": "x", "meaning": "y", "box": 0, "due": T,
                    "note": ""}
        vocab.grade(new_card, False, T)  # never lifted off: stays at 0
        self.assertEqual(new_card["box"], 0)

    def test_grade_disabled_peak(self):
        card = {"word": "x", "meaning": "y", "box": 7, "due": T, "note": ""}
        for _ in range(3):
            vocab.grade(card, True, T)
        self.assertEqual(card["box"], 7)


class AddLogic(unittest.TestCase):
    def test_add_defaults_and_duplicate(self):
        cards = []
        cards, msg = vocab.add_card(cards, "mesa", "table", today=T)
        self.assertIn("added 'mesa'", msg)
        self.assertEqual(cards[0]["box"], 0)
        self.assertEqual(cards[0]["due"], T + datetime.timedelta(1))
        cards2, msg2 = vocab.add_card(cards, "MESA", "second", today=T)
        self.assertIn("not added twice", msg2)
        self.assertEqual(len(cards2), 1)

    def test_add_requires_word_and_meaning(self):
        with self.assertRaises(vocab.VocabError):
            vocab.add_card([], "", "meaning", today=T)
        with self.assertRaises(vocab.VocabError):
            vocab.add_card([], "word", "", today=T)


class DueAndFiles(unittest.TestCase):
    def test_due_sorted_and_filtered(self):
        cards = [
            {"word": "c", "meaning": "3", "box": 0, "due": T, "note": ""},
            {"word": "b", "meaning": "2", "box": 1,
             "due": T - datetime.timedelta(2), "note": ""},
            {"word": "a", "meaning": "1", "box": 2, "due": T, "note": ""},
            {"word": "z", "meaning": "9", "box": 1,
             "due": T + datetime.timedelta(5), "note": ""},
        ]
        due = vocab.due_cards(cards, T)
        self.assertEqual([c["word"] for c in due], ["b", "a", "c"])
        soon = vocab.upcoming(cards, T)
        self.assertEqual([c["word"] for c in soon], ["z"])

    def test_save_load_roundtrip_and_junk_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "out.csv"
            cards = [
                {"word": "hola", "meaning": "hello", "box": 2,
                 "due": T, "note": "first"},
                {"word": "qué tal", "meaning": "how's it going", "box": 0,
                 "due": T - datetime.timedelta(1), "note": ""},
            ]
            vocab.save(f, cards)
            loaded = vocab.load(f)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0]["word"], "hola")
            self.assertEqual(loaded[0]["due"], T)
            # malformed file: junk lines skipped, bad dates reset to today
            junk = Path(tmp) / "junk.csv"
            junk.write_text(
                "word,meaning,due,box,note\n"
                "uno,dos,bad-date,notanumber,ignored values\n"
                "badrow\n"
                ",,2026-01-01,0,\n",
                encoding="utf-8")
            loaded = vocab.load(junk)
            self.assertEqual(len(loaded), 1)
            self.assertEqual(loaded[0]["word"], "uno")
            self.assertEqual(loaded[0]["due"], datetime.date.today())
            self.assertEqual(loaded[0]["box"], 0)


class CLI(unittest.TestCase):
    def test_due_on_sample(self):
        r = run_cli(["due"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("due today or overdue", r.stdout)
        self.assertIn("gracias", r.stdout)

    def test_stats_on_sample(self):
        r = run_cli(["stats"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("words", r.stdout)
        self.assertIn("box 0", r.stdout)

    def test_add_and_duplicate_message(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "cli.csv"
            r1 = run_cli(["add", "mesa", "table", "wood"], csv_file=f)
            self.assertEqual(r1.returncode, 0, r1.stderr)
            self.assertIn("added 'mesa'", r1.stdout)
            self.assertTrue(f.exists())
            r2 = run_cli(["add", "MESA", "again"], csv_file=f)
            self.assertEqual(r2.returncode, 0, r2.stderr)
            self.assertIn("not added twice", r2.stdout)

    def test_add_missing_meaning_fails_cleanly(self):
        r = run_cli(["add", "justword"])
        self.assertEqual(r.returncode, 2)
        self.assertIn("error:", r.stderr)

    def test_review_piped_input_grades_and_saves(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "review.csv"
            f.write_text(SAMPLE.read_text(encoding="utf-8"),
                         encoding="utf-8")
            stdin = "\ny\ny\nn\ny\ny\ny\n"
            r = run_cli(["review", "--max", "6"], stdin=stdin, csv_file=f)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("session done", r.stdout)
            self.assertIn("input ended", r.stdout)  # stdin ran out
            text = f.read_text(encoding="utf-8")
            self.assertIn("gracias", text)
            # gracias graded correct: box should be 4 now
            row = [ln for ln in text.splitlines()
                   if ln.startswith("gracias")][0]
            self.assertIn(",4,", row)

    def test_review_eof_only_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "msd.csv"
            f.write_text(SAMPLE.read_text(encoding="utf-8"),
                         encoding="utf-8")
            r = run_cli(["review"], stdin="", csv_file=f)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(f.read_text(encoding="utf-8"),
                             SAMPLE.read_text(encoding="utf-8"))

    def test_review_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "empty.csv"
            f.write_text("", encoding="utf-8")
            r = run_cli(["review"], stdin="", csv_file=f)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("empty", r.stdout)

    def test_due_of_empty_file_suggests_add(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "e.csv"
            f.write_text("", encoding="utf-8")
            r = run_cli(["due"], csv_file=f)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("empty", r.stdout)
            self.assertIn("add", r.stdout)


class Build(unittest.TestCase):
    def test_build_check(self):
        r = subprocess.run([sys.executable, str(BUILD), "--check"],
                           capture_output=True, text=True, timeout=120)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Check passed", r.stdout)

    def test_raw_copyables_match_sources(self):
        for rel in ("templates/weekly-plan-cards.md",
                    "templates/phrase-list-template.md",
                    "templates/phrases-starter.md"):
            src = ROOT / rel
            dst = ROOT / "site" / "templates" / "files" / src.name
            self.assertTrue(src.exists(), f"missing source {rel}")
            self.assertTrue(dst.exists(),
                            f"run build.py first: missing {dst}")
            self.assertEqual(src.read_text(encoding="utf-8"),
                             dst.read_text(encoding="utf-8"))
        self.assertTrue((ROOT / "site" / "templates" / "files" /
                         "sample-vocab.csv").exists())


if __name__ == "__main__":
    failures = 0
    suite = unittest.defaultTestLoader.discover(
        ".", pattern="test.py")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    failures = len(result.failures) + len(result.errors)
    sys.exit(1 if failures else 0)
