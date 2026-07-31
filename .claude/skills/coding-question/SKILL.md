---
name: coding-question
description: Turn a YouTube coding-challenge video OR an existing local implementation into a coding question under ./knowledge/coding-questions, authored as four files (impl.py skeleton, meta.json difficulty/tags/hint, solution.py full solution, tests.py). Use when the user gives a YouTube URL (e.g. a CodeSignal/LeetCode explainer) or a local path to an existing solution file. Invoke with the video URL or local path as the argument.
argument-hint: <youtube-url-or-local-path>
---

# Coding question

Given either a **YouTube URL** for a coding-challenge video or a **local path**
to an existing implementation already in this repo, create a new folder under
`./knowledge/coding-questions/<name>/` containing four files:

- **`impl.py`** — the skeleton the user starts with in the editor: the
  problem-description comment block (title, optional `# Source:`, statement,
  examples — **no** Difficulty/Tags/Approach), any input data-structure classes
  (e.g. `Node`), and the primary function **stubbed** with `raise NotImplementedError`.
- **`meta.json`** — `{ "difficulty": "<easy|medium|hard>", "tags": ["tag1", ...],
  "hint": "<one-line approach>" }`. Difficulty, tags, and the solution hint live
  here (not in the impl.py comment); `hint` is `""` when there's no useful nudge.
- **`solution.py`** — the full working solution: the same input classes + the
  implemented primary function (+ any private helpers or alternate variants).
- **`tests.py`** — `import unittest`, any test-only helper functions (e.g.
  `build_list`/`to_list`), and the `unittest.TestCase`, ending with the
  `if __name__ == '__main__':\n  unittest.main()` guard.

The app runs the user's edited `impl.py` **concatenated with `tests.py`**, so
the tests must build their inputs from the classes in `impl.py`. The reference
exemplar to mirror is `knowledge/coding-questions/CTCI/2.5-sum-lists/`.

The catalog is stored in a database (not a JSON file); after creating or editing
a problem you re-import it — see step 9.

The two input modes differ only in how you recover the problem (step 1) and a
move-and-cleanup step for local sources (step 7).

## Steps

1. **Identify the problem.** A URL on a `youtube.com` / `youtu.be` host is video
   mode; anything that resolves to a file or directory in this repo is
   local-path mode.

   **Video mode.** The raw watch page is mostly footer junk, so don't WebFetch
   it. Instead:
   - Get title/channel via oEmbed:
     `curl -s "https://www.youtube.com/oembed?url=<VIDEO_URL>&format=json"`
   - If the title alone doesn't pin down the exact statement, WebSearch it
     (usually a known CodeSignal/LeetCode/HackerRank problem) to recover the
     precise statement, constraints, and canonical examples.
   - You do not need to watch the video — the goal is the problem definition;
     derive the solution yourself.

   **Local-path mode.** The argument points at an existing solution (a file like
   `graph/island-count.go`, or a folder). Read every source file there; they
   usually carry a description comment and a working implementation. Recover the
   exact statement, constraints, and examples. Note the language: a Go source is
   **ported** to Python for `solution.py` (step 4) — the repo stores only the
   three Python files, so there is no `.go` file in the new folder.

2. **Pick a folder name.** Short, descriptive kebab-case matching the problem's
   real name (e.g. `century-from-year`). In local-path mode, name it after the
   problem, not the source filename. If a folder for the same problem already
   exists, tell the user and ask before overwriting.

3. **Write `impl.py` and `meta.json`** — the skeleton plus metadata:

   - **Problem-description comment block** at the top of `impl.py`:
     - **Title** on line 1 — just the title (`# Century From Year`, not
       `# Century From Year (CodeSignal)`).
     - `# Source: <url>` — **only if the input carries a reference link**; omit
       otherwise. Preserve every genuine reference URL (the YouTube URL in video
       mode; any Coursera/YouTube/GeeksforGeeks/LeetCode link in a local source's
       comments/README). One `# Source:` line per URL. Keep them out of the title.
     - A **faithful problem statement** the way a clean interview/LeetCode prompt
       reads: address the reader ("You are given...", "Return..."), state input
       and required output precisely, list constraints (size bounds, value
       ranges, guarantees). Strip cutesy narrative (mascots, character names,
       gift-giving framings) — state the underlying task plainly. Then 2-4
       concrete examples (include the tricky boundary cases).
     - **Do NOT put difficulty, tags, or the approach/hint in this comment** —
       they go in `meta.json`.

   - **`meta.json`** in the same folder:
     `{ "difficulty": "<easy|medium|hard>", "tags": ["tag1", ...], "hint": "..." }`
     - `hint`: a one-line **approach** nudge (shown as a collapsible hint in the
       app), or `""` when there's no useful nudge.
     - `tags`: techniques/data-structures/topics. **Reuse existing tags — don't
       invent near-duplicates.** First list what's used:
       ```
       python3 -c "import json,glob,collections as c; print(c.Counter(t for f in glob.glob('knowledge/coding-questions/**/meta.json',recursive=True) for t in json.load(open(f)).get('tags',[])).most_common())"
       ```
       Normalize: lowercase, kebab-case for multi-word (`two-pointers`,
       `dynamic-programming`); name the technique/structure/topic; every tag must
       carry real signal (avoid vague catch-alls like `implementation`,
       `simulation`, `logic`). Do NOT tag the language. Store tags **without** the
       leading `#`.

   - **Input classes.** If the inputs are a data structure (linked list, tree,
     grid wrapper, …), define the class(es) the tests need to construct inputs
     (e.g. `class Node`). Copy them **verbatim into `solution.py`** too. Most
     array/string/number problems need no class.

   - **Stubbed primary function.** One clearly-named function — signature only,
     body replaced with:
     ```python
     def some_function(args):
       # TODO: implement
       raise NotImplementedError
     ```

   Do **not** put `import unittest`, helper functions, alternates, or tests in
   `impl.py`.

4. **Write `solution.py`** — the full solution:
   - The **same input classes** as `impl.py` (verbatim).
   - The primary function **fully implemented**, plus any private helper
     functions it uses, plus any alternate reference variants. Prefer
     integer/exact arithmetic over floating point where it matters.
   - Any non-unittest imports the solution needs (e.g.
     `from collections import deque`).
   - No description comment, no `import unittest`, no tests.
   - **Porting a Go source:** don't re-derive from scratch — port the Go
     algorithm to idiomatic Python (same approach and complexity; Python data
     structures and `snake_case`; drop Go-isms like manual stacks / `interface{}`;
     `return` instead of print).

5. **Write `tests.py`** — the grader:
   - `import unittest` first, plus any non-unittest imports the tests need.
   - **Test-only helper functions** — the ones the TestCase calls to build/read
     inputs (e.g. `build_list`, `to_list`, `build_tree`). They may reference the
     input classes, which are supplied at run time from `impl.py`/`solution.py`;
     do **not** redefine the classes here.
   - A `unittest.TestCase` that exercises **only the primary function** — never
     an alternate variant or a private solution helper (those live in
     `solution.py`, so referencing them makes the user's run fail with a
     `NameError`). End the file with:
     ```python
     if __name__ == '__main__':
       unittest.main()
     ```

   Aim for genuinely thorough coverage. Derive edge cases from the problem's own
   constraints, not just the shown examples. Walk this checklist and add a test
   for each item that applies (skip ones that don't):
   - **Smallest valid input** (single element, single char, 1x1, …).
   - **Empty input**, only if the constraints permit it.
   - **Boundary values**: min/max allowed, and inputs at the upper size bound.
   - **Uniformity**: all identical / all duplicates / all same length.
   - **Special numerics**: zero, negatives, off-by-one triggers, float-precision.
   - **Ordering**: already sorted, reverse sorted, unsorted (when order matters).
   - **Position of the interesting element**: start, middle, and end.
   - **Every branch** of the intended solution, including where a rule does NOT
     fire.
   - **The problem's designed trap** (a `0` blocking a column, ties for a max,
     wrap-around) — test it head-on.

   Give each test a descriptive `snake_case` name; make each target a distinct
   scenario rather than re-checking one path with different numbers.

6. **Match the local style** (`CLAUDE.md`): 2-space Python indentation, and
   `snake_case` identifiers (rename camelCase from the source, e.g.
   `inputString` → `input_string`).

7. **Move, don't copy (local-path mode only): remove the original source.** Once
   the new folder is written and verified, delete the original file(s) you read
   in step 1 (`git rm` when tracked); remove a now-empty directory too. If the
   original depends on a sibling you didn't fold in (or vice-versa), don't delete
   that sibling — call it out. Never touch anything outside the original path.

8. **Verify by concatenation** (this is exactly how the app runs it — the user's
   `impl.py` plus `tests.py`):
   - `cat knowledge/coding-questions/<name>/solution.py knowledge/coding-questions/<name>/tests.py | python3`
     → must report `OK`. Fix until green.
   - `cat knowledge/coding-questions/<name>/impl.py knowledge/coding-questions/<name>/tests.py | python3`
     → must report `FAILED` with `NotImplementedError` and **no `NameError`**. A
     `NameError` means the tests reference a symbol not in `impl.py` — either the
     tests are grading an alternate/helper (fix the tests to grade only the
     primary) or a needed input class is missing from `impl.py` (add it there).

9. **Import into the catalog.** The catalog lives in the SQLite DB, imported by
   `backend/etl.py`. Re-run it so the app picks up the new/edited problem:
   ```
   docker compose exec api python etl.py
   ```
   If the containers aren't running, say so and tell the user to run it once
   they're up.

10. **Report** the folder and the four files created, the one-line problem
    summary, both verification results, whether the catalog was re-imported, and
    — in local-path mode — exactly which original files you removed. Do not
    commit or open a PR unless the user asks.
