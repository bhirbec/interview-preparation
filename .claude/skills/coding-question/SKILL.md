---
name: coding-question
description: Turn a YouTube coding-challenge video OR an existing local implementation into a self-contained coding question under ./coding-questions. Use when the user provides a YouTube URL (e.g. a CodeSignal/LeetCode explainer) or a local path to an existing solution file (e.g. graph/island-count.go) and wants it scaffolded with a description, implementation, and unit tests. Invoke with the video URL or local path as the argument.
argument-hint: <youtube-url-or-local-path>
---

# Coding question

Given either a **YouTube URL** for a coding-challenge video or a **local path**
to an existing implementation already in this repo, create a self-contained
coding-question folder under `./coding-questions/` containing:

- `impl.py` — the problem description, a working Python implementation, and
  passing unit tests. **Always produced.**
- `impl.go` — a Go reference solution. **Only when the local source includes a
  Go implementation** — copy it into the folder (see step 4). Never invent one.
- `impl_empty.py` — a practice copy for the user to solve: byte-for-byte
  identical to `impl.py` except the function body is replaced with a stub.
  **Generated locally for practice, but NEVER committed** — the repo's
  `.gitignore` excludes `impl_empty.py`. Create it and verify it, but keep it
  out of any commit or PR.

The two input modes differ only in how you recover the problem (step 1), an
optional Go copy (step 4), and a move-and-cleanup step for local sources
(step 7). Everything else — the folder layout, the Python file, the tests — is
identical.

## Steps

1. **Identify the problem.** First decide which input you were given: a URL on a
   `youtube.com` / `youtu.be` host is the video mode; anything that resolves to a
   file or directory in this repo is the local-path mode.

   **Video mode (YouTube URL).** The raw YouTube watch page is mostly footer junk
   when fetched, so don't rely on WebFetch of the watch URL. Instead:
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

   **Local-path mode.** The argument points at an existing solution in the repo
   (a single file like `graph/island-count.go`, or a folder). Read every source
   file at that path. These files usually already carry a problem description in
   a leading comment and one or more working implementations — use them to
   recover the exact problem statement, constraints, and examples. If the
   description is thin, infer the precise statement from the code's behavior and,
   if it's a known problem, confirm details with WebSearch. Note the source
   language(s): if any file is Go (`.go`), you will copy it into the new folder
   as `impl.go` in step 4.

2. **Pick a folder name.** Use a short, descriptive kebab-case name that matches
   the problem's actual name (e.g. `century-from-year`, not a paraphrase). In
   local-path mode, name it after the problem, not the source filename (e.g.
   `graph/island-count.go` → `biggest-island`, not `island-count`, if that reads
   better — but keeping `island-count` is fine when it already describes the
   problem). If a folder for the same problem already exists under
   `./coding-questions/`, tell the user and ask before overwriting rather than
   silently clobbering it.

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
         - do NOT tag the implementation language. `impl.py` is always Python,
           so `#python` adds no search value; likewise don't add `#go` just
           because an `impl.go` reference is present — tag the problem, not the
           language.
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

4. **Copy the Go implementation (local-path mode only, and only if one exists).**
   If the local source included a `.go` file, copy it into the new folder as
   `./coding-questions/<name>/impl.go`, preserved essentially verbatim — it is a
   reference solution the user can read and copy, not something you rewrite to
   match Python conventions. You may drop a throwaway `main()` demo harness and
   fix the `package` line if needed, but keep the algorithm and its comments as
   the author wrote them. Skip this step entirely in video mode or when the
   source has no Go implementation; never write a Go file from scratch.

5. **Write `./coding-questions/<name>/impl_empty.py`.** This is the user's
   practice copy, for LOCAL USE ONLY — it is listed in `.gitignore` and must
   never be committed or included in a PR. It must be identical to `impl.py` in
   every respect — same problem-description comment block, same imports, same
   function name and signature, and the exact same `unittest.TestCase` (same
   test names, same assertions) — with only ONE difference: the function body is
   replaced by a stub so the tests fail until the user solves it. Use:
   ```python
   def some_function(args):
     # TODO: implement
     raise NotImplementedError
   ```
   Do not weaken or remove any tests in `impl_empty.py`; the whole point is that
   the user's future solution is judged against the same tests that `impl.py`
   passes. If you later refine the tests in `impl.py`, mirror the change into
   `impl_empty.py` so the two stay in sync.

6. **Match the local style.** Follow the repo conventions in `CLAUDE.md`
   (notably: 2-space Python indentation, and `snake_case` identifiers — rename
   camelCase names from the source problem, e.g. `inputString` → `input_string`).

7. **Move, don't copy (local-path mode only): remove the original source.** The
   goal of local-path mode is to relocate a scattered implementation into
   `./coding-questions/`, not to duplicate it. Once the new folder is written and
   its tests pass, delete the original source file(s) you read in step 1 (use
   `git rm` when they are tracked). If removing a file would leave an empty
   directory, remove the directory too. Keep an eye out for shared helpers: if
   the original file depends on a sibling you did not fold into the new folder
   (or vice-versa), do not delete that sibling — call it out in the report
   instead. Never touch anything outside the original source path.

8. **Verify.** Run `python3 ./coding-questions/<name>/impl.py` and confirm the
   tests report `OK`; fix until green. Then run
   `python3 ./coding-questions/<name>/impl_empty.py` and confirm it instead
   FAILS (every test erroring with `NotImplementedError`) — this proves the
   tests actually exercise the function and that the practice stub is empty. If
   an `impl.go` was copied and Go is available, `gofmt -l` it to confirm it
   still parses; do not block on Go being installed.

9. **Report** the folder created (and which of `impl.py` / `impl.go` /
   `impl_empty.py` it holds), the one-line problem summary, the test results,
   and — in local-path mode — exactly which original files you removed. Do not
   commit or open a PR unless the user asks. When you do commit, remember
   `impl_empty.py` is gitignored and stays out of the commit.
