# Your AI Practice Partner

Before the drills: what kind of AI you want, and how to set it up so it
never laughs at you and never expensive-fails you.

## What "practice partner" means

A practice partner is a person you *converse* with, at your level, without
judgment. What it is not:

- A teacher with a curriculum. You don't need one yet.
- A translation machine. Translation converts; practice *converses*.
- An authority on grammar rules (chapter 5 explains where rules live — in
  real sources, checked by you).

The magic of an AI partner is **unlimited patience at your exact level**.
You will make the same mistake fourteen times. Your partner waits for the
fifteenth without a sigh.

## Option A — a local model (free, private, offline)

A local model runs entirely on your own computer. Your stumbles in Spanish
never leave the machine, and everything still works when the Wi-Fi is down —
nice if you practice on a commute or in a breakroom basement.

The easiest free and private way to do this is **Ollama** (ollama.com),
which handles the install in one step on Windows, macOS, and Linux. After
installing, download a small general-purpose model, for example:

```bash
ollama run llama3.2:3b
```

(Choose the largest model your machine runs comfortably; small models of
3–8 billion parameters are usually good enough to *converse* in the major
languages, which is all we need.) In the first session of each day, you give
it the partner instructions from *chapter 3* and afterwards use
`ollama run` again to reopen it, because a local chat forgets between runs.

What lives on your machine: the model (a few GB), your pasted session text,
your plain files (chapters 4–6). Nothing is broadcast anywhere. If you want
the free directory of local options, see the sister repo
`free-local-models-directory` in the same series.

## Option B — free hosted chat

If your machine is too old or you don't want to install anything, a free
hosted AI chat works nearly as well. Every exercise in this guide works over
plain typing. Two honest trade-offs:

- You'll re-paste the *partner instructions* from chapter 3 at the start of
  each session (or save them in one note you keep open).
- Privacy: hosted chats go over someone else's servers. Fine for "I'd like
  two apples and a loaf of bread" — think twice about the parts of your
  life you'd rather keep local (chapter 4 and chapter 6 keep *your* data in
  *your* files either way).

## Option C — your phone, your voice

Speaking is the goal, eventually. Whichever AI you use will likely have a
voice mode on their phone app — use it during weeks 5+ (chapter 1 upgrade
path). Until then, typing plus *saying your typed answer aloud* is honest
enough practice. The mouth learns when the mouth works.

## The session template that makes it a *partner*, not a chatbot

Whatever the tool, each session gets the same four-line introduction. This
is what turns a generic chat into a patient practice partner:

> I am learning [LANGUAGE], roughly [A1/A2/B1] level. For this session you
> are my conversation partner. Three rules:
> 1. Keep everything in [LANGUAGE] except my corrections.
> 2. Never switch to English unless I ask — guessing is part of practice.
> 3. At the end of the session, list my 5 most useful mistakes in a table:
>    what I said | a more natural way to say it | why.
> Today's drill: [THE DRILL FROM CHAPTER 3, PASTED].

Save it once as `partner-instructions.txt` and re-paste or re-type it each
time. Different chat apps remember it differently; "I pasted it again" is
faster than trusting memory.

## Sessions end better than they start

When the timer says fifteen minutes are up, end with the correction table —
even if you type `Session over; corrections table, please.` That table is
the actual lesson. Copy its best line into your phrase list or vocab file
(chapter 4), then close the laptop. Done. Partner says goodnight, whether
it's a local model or a website.

## One version habit

Keep everything in one folder, e.g.

```text
language-practice/
  partner-instructions.txt
  phrases-restaurant.md        (chapter 6 templates)
  vocab.csv                    (chapter 4)
  week-cards.md                (chapter 1 cards)
```

Whatever tool you use and however many sessions you abandon, the folder is
the school, and it's all yours.
