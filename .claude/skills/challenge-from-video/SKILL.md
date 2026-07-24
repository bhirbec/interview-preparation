---
name: challenge-from-video
description: Turn a YouTube coding-challenge video into a new solved challenge under ./challenges. Use when the user provides a YouTube URL (e.g. a CodeSignal/LeetCode explainer) and wants the problem scaffolded with a description, implementation, and unit tests. Invoke with the video URL as the argument.
argument-hint: <youtube-url>
---

# Challenge from video

Given a YouTube URL for a coding-challenge video, create a new self-contained
challenge folder under `./challenges/` containing a single `impl.py` with the
problem description, an implementation, and passing unit tests.

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
   If a folder for the same problem already exists under `./challenges/`, tell
   the user and ask before overwriting rather than silently clobbering it.

3. **Write `./challenges/<name>/impl.py`** with three parts, in this order:
   - **Problem description** as a top-of-file comment block, in this order:
     - The problem title (and source, e.g. CodeSignal / LeetCode) on line 1.
     - A **metadata** block with two fields:
       - `# Difficulty: <easy|medium|hard>`
       - `# Tags: #tag1 #tag2 ...` — one or more lowercase hashtags describing
         the techniques/topics (e.g. `#sorting`, `#hashtable`, `#math`,
         `#two-pointers`, `#dynamic-programming`, `#string`, `#greedy`,
         `#binary-search`, `#recursion`, `#implementation`). The leading `#`
         makes tags greppable, e.g. `grep -rl '#hashtable' challenges/`.
     - A faithful statement of the problem, 2-4 concrete examples (include the
       tricky boundary cases), and a one-line note on the approach.
   - **Implementation**: a single clearly-named function. Prefer integer/exact
     arithmetic over floating point where it matters.
   - **Unit tests**: a `unittest.TestCase` covering the video's examples plus
     edge/boundary cases, ending with:
     ```python
     if __name__ == '__main__':
         unittest.main()
     ```

4. **Match the local style.** Follow the repo conventions in `CLAUDE.md`
   (notably: 2-space Python indentation).

5. **Verify.** Run `python3 ./challenges/<name>/impl.py` and confirm the tests
   report `OK`. Fix until green.

6. **Report** the folder created, the one-line problem summary, and the test
   result. Do not commit or open a PR unless the user asks.
