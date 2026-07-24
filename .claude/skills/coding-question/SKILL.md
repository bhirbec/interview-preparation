---
name: coding-question
description: Turn a YouTube coding-challenge video into a new solved coding question under ./coding-questions. Use when the user provides a YouTube URL (e.g. a CodeSignal/LeetCode explainer) and wants the problem scaffolded with a description, implementation, and unit tests. Invoke with the video URL as the argument.
argument-hint: <youtube-url>
---

# Coding question

Given a YouTube URL for a coding-challenge video, create a new self-contained
coding-question folder under `./coding-questions/` containing two files:

- `impl.py` — the problem description, a working implementation, and passing
  unit tests.
- `impl_empty.py` — a practice copy for the user to solve: byte-for-byte
  identical to `impl.py` except the function body is replaced with a stub, so
  the user can fill it in themselves.

## Steps

1. **Identify the problem from the URL.** The raw YouTube watch page is mostly
   footer junk when fetched, so don't rely on WebFetch of the watch URL. Instead:
   - Get the title and channel reliably via the oEmbed endpoint:
     ```
     curl -s "https://www.youtube.com/oembed?url=<VIDEO_URL>&format=json"
     ```
   - If the title alone doesn't fully pin down the exact problem statement,
     use WebSearch on the video title (these are usually well-known
     CodeSignal / LeetCode / HackerRank problems) to recover the precise
     statement, constraints, and canonical examples.
   - You do not need to watch the video or extract frames. The goal is the
     problem definition, not the presenter's specific solution — derive the
     solution yourself.

2. **Pick a folder name.** Use a short, descriptive kebab-case name that matches
   the problem's actual name (e.g. `century-from-year`, not a paraphrase).
   If a folder for the same problem already exists under `./coding-questions/`,
   tell the user and ask before overwriting rather than silently clobbering it.

3. **Write `./coding-questions/<name>/impl.py`** with these parts, in this order:
   - **Problem description** as a top-of-file comment block, in this order:
     - The problem title on line 1. Just the title — do not append the source
       (e.g. write `# Century From Year`, not `# Century From Year (CodeSignal)`).
     - A **metadata** block with two fields:
       - `# Difficulty: <easy|medium|hard>`
       - `# Tags: #tag1 #tag2 ...` — hashtags describing the techniques, data
         structures, and topics the problem involves. There is no fixed list:
         choose whatever tags genuinely fit the content. The leading `#` makes
         them greppable, e.g. `grep -rl '#hashtable' coding-questions/`.

         **Reuse existing tags — don't invent near-duplicates.** Before picking
         tags, list the ones already used across coding questions and prefer an
         existing tag whenever it means the same thing (so we never end up with
         `#hashtable` vs `#hash-table` vs `#hashmap` for one concept):

         ```
         grep -rhoE '#[a-z0-9-]+' coding-questions/ | sort | uniq -c | sort -rn
         ```

         Only coin a new tag when nothing existing fits. Normalize every tag:
         - lowercase, kebab-case for multi-word (`#two-pointers`,
           `#dynamic-programming`, `#binary-search`)
         - name the technique/data-structure/topic (`#sorting`, `#hashtable`,
           `#math`, `#greedy`, `#recursion`, `#string`) — these are examples,
           not an allow-list
         - every tag must carry real signal that distinguishes this problem
           from others. Do NOT use vague catch-all tags that could apply to
           almost any question — `#implementation`, `#simulation`, `#easy`,
           `#logic`, `#coding` say nothing useful when grepping. If the best
           you can do for a problem is a generic tag, prefer a more specific
           one (`#matrix`, `#prefix-sum`, `#counting`) or just fewer tags.
         - do NOT tag the implementation language: every solution here is
           Python, so `#python` adds no search value
     - A faithful statement of the problem, written the way a real interview
       question or a clean LeetCode-style prompt would read: address the reader
       directly ("You are given...", "Return..."), describe the input and the
       required output precisely, and list the constraints (input size bounds,
       value ranges, guarantees like distinctness). Do NOT copy the source's
       flavor narrative — strip cutesy backstories (mascots, character names,
       gift-giving framings) and state the underlying task in plain, precise
       terms. Then give 2-4 concrete examples (include the tricky boundary
       cases), and a one-line note on the approach.
   - **Imports**: all imports go at the top of the file, immediately after the
     problem-description comment block and before the implementation (e.g.
     `import unittest`). Do not scatter imports lower down next to the tests.
   - **Implementation**: a single clearly-named function. Prefer integer/exact
     arithmetic over floating point where it matters.
   - **Unit tests**: a `unittest.TestCase` covering the video's examples plus
     a thorough set of edge/boundary cases, ending with:
     ```python
     if __name__ == '__main__':
         unittest.main()
     ```

     Aim for genuinely thorough coverage — the video's examples are a starting
     point, not the finish line. Derive edge cases from the problem's own
     constraints and structure, not just from the examples shown. Before
     finalizing the tests, walk this checklist and add a test for each item
     that applies to this problem (skip the ones that don't — e.g. don't test
     an empty array when the constraints guarantee `len >= 1`):
     - **Smallest valid input**: single element, single-char string, `1x1`
       matrix, or whatever the lower size bound allows.
     - **Empty input**, but only if the constraints actually permit it.
     - **Boundary values**: the minimum and maximum allowed values, and inputs
       at the upper size bound where behavior could differ.
     - **Uniformity**: all elements identical / all duplicates; all the same
       length; a single distinct value.
     - **Special numeric cases where relevant**: zero, negatives, the number
       that trips off-by-one errors, values that would overflow float precision.
     - **Ordering**: already sorted, reverse sorted, and unsorted inputs when
       order matters to the logic.
     - **Position of the "interesting" element**: at the start, in the middle,
       and at the end of the input (a bug at index 0 or the last index is
       common and easy to miss).
     - **Every branch of the intended solution**: pick inputs so that each
       distinct code path / rule in the problem is exercised at least once,
       including the case where a rule does NOT fire.
     - **The problem's designed trap**: the specific boundary the question is
       built to catch (e.g. a `0` that blocks the rest of a column, ties for a
       maximum, wrap-around) — test it head-on.

     Give each test a descriptive `snake_case` name stating the scenario it
     covers, and make each test target a distinct scenario rather than
     re-checking the same path with different numbers.

4. **Write `./coding-questions/<name>/impl_empty.py`.** This is the user's
   practice copy. It must be identical to `impl.py` in every respect — same
   problem-description comment block, same imports, same function name and
   signature, and the exact same `unittest.TestCase` (same test names, same
   assertions) — with only ONE difference: the function body is replaced by a
   stub so the tests fail until the user solves it. Use:
   ```python
   def some_function(args):
     # TODO: implement
     raise NotImplementedError
   ```
   Do not weaken or remove any tests in `impl_empty.py`; the whole point is that
   the user's future solution is judged against the same tests that `impl.py`
   passes. If you later refine the tests in `impl.py`, mirror the change into
   `impl_empty.py` so the two stay in sync.

5. **Match the local style.** Follow the repo conventions in `CLAUDE.md`
   (notably: 2-space Python indentation, and `snake_case` identifiers — rename
   camelCase names from the source problem, e.g. `inputString` → `input_string`).

6. **Verify.** Run `python3 ./coding-questions/<name>/impl.py` and confirm the
   tests report `OK`; fix until green. Then run
   `python3 ./coding-questions/<name>/impl_empty.py` and confirm it instead
   FAILS (every test erroring with `NotImplementedError`) — this proves the
   tests actually exercise the function and that the practice stub is empty.

7. **Report** the folder created, the one-line problem summary, and the test
   results for both files. Do not commit or open a PR unless the user asks.
