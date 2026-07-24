---
name: coding-question
description: Turn a YouTube coding-challenge video into a new solved coding question under ./coding-questions. Use when the user provides a YouTube URL (e.g. a CodeSignal/LeetCode explainer) and wants the problem scaffolded with a description, implementation, and unit tests. Invoke with the video URL as the argument.
argument-hint: <youtube-url>
---

# Coding question

Given a YouTube URL for a coding-challenge video, create a new self-contained
coding-question folder under `./coding-questions/` containing a single `impl.py`
with the problem description, an implementation, and passing unit tests.

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
     edge/boundary cases, ending with:
     ```python
     if __name__ == '__main__':
         unittest.main()
     ```

4. **Match the local style.** Follow the repo conventions in `CLAUDE.md`
   (notably: 2-space Python indentation, and `snake_case` identifiers — rename
   camelCase names from the source problem, e.g. `inputString` → `input_string`).

5. **Verify.** Run `python3 ./coding-questions/<name>/impl.py` and confirm the tests
   report `OK`. Fix until green.

6. **Report** the folder created, the one-line problem summary, and the test
   result. Do not commit or open a PR unless the user asks.
