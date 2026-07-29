#!/usr/bin/env python3
"""Build a JSON catalog of coding questions for the web UI.

Scans ../coding-questions/<name>/impl.py, splits each file into its problem
description, reference solution, unit tests, and a stubbed starter, and writes
the result to ../app/public/problems.json.

Each impl.py follows a fixed shape:

    # Title
    # Difficulty: <level>
    # Source: <url>            (optional, zero or more)
    # Tags: #tag1 #tag2
    #
    # <problem statement, examples, approach...>

    import unittest

    def primary(...): ...      (first top-level def == the function to solve)
    def alt(...): ...          (optional extra reference variants)

    class TestX(unittest.TestCase): ...

    if __name__ == '__main__':
      unittest.main()

The starter keeps the primary function's signature and replaces its body with a
TODO stub, so the UI can offer a LeetCode-style "fill in the blank" experience.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
QUESTIONS_DIR = os.path.join(ROOT, "coding-questions")
OUTPUT = os.path.join(ROOT, "app", "public", "problems.json")


def split_sections(lines):
  """Return (comment_lines, solution_lines, test_lines)."""
  comment_lines = []
  i = 0
  while i < len(lines) and lines[i].startswith("#"):
    comment_lines.append(lines[i])
    i += 1

  first_def = next(i for i, ln in enumerate(lines) if ln.startswith("def "))
  test_start = next(i for i, ln in enumerate(lines) if ln.startswith("class ")
                    and "unittest.TestCase" in ln)
  guard = next((i for i, ln in enumerate(lines)
                if ln.startswith("if __name__")), len(lines))

  solution = lines[first_def:test_start]
  tests = lines[test_start:guard]
  return comment_lines, _strip_trailing_blanks(solution), _strip_trailing_blanks(tests)


def _strip_trailing_blanks(block):
  while block and block[-1].strip() == "":
    block.pop()
  return block


def parse_metadata(comment_lines):
  """Pull title/difficulty/source/tags/description out of the comment block."""
  title = comment_lines[0].lstrip("#").strip()
  difficulty = ""
  sources = []
  tags = []
  description = []

  for ln in comment_lines[1:]:
    text = ln.lstrip("#")
    text = text[1:] if text.startswith(" ") else text  # drop one leading space
    stripped = text.strip()
    if stripped.startswith("Difficulty:"):
      difficulty = stripped.split(":", 1)[1].strip()
    elif stripped.startswith("Source:"):
      sources.append(stripped.split(":", 1)[1].strip())
    elif stripped.startswith("Tags:"):
      tags = re.findall(r"#([a-z0-9-]+)", stripped)
    else:
      description.append(text.rstrip())

  # Trim leading/trailing blank description lines.
  while description and description[0].strip() == "":
    description.pop(0)
  while description and description[-1].strip() == "":
    description.pop()

  return {
      "title": title,
      "difficulty": difficulty,
      "sources": sources,
      "tags": tags,
      "description": "\n".join(description),
  }


def make_starter(solution_lines):
  """Keep the primary (first) function's signature; stub out its body."""
  # Capture the signature, which may span multiple lines until it ends with ':'.
  sig = []
  i = 0
  for i, ln in enumerate(solution_lines):
    sig.append(ln)
    if ln.rstrip().endswith(":"):
      break

  name = re.match(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)", solution_lines[0]).group(1)
  starter = "\n".join(sig) + "\n  # TODO: implement\n  pass\n"
  return name, starter


def build_problem(slug, path):
  with open(path) as f:
    lines = f.read().splitlines()

  comment_lines, solution_lines, test_lines = split_sections(lines)
  meta = parse_metadata(comment_lines)
  primary, starter = make_starter(solution_lines)

  return {
      "slug": slug,
      "title": meta["title"],
      "difficulty": meta["difficulty"],
      "tags": meta["tags"],
      "sources": meta["sources"],
      "description": meta["description"],
      "primaryFunction": primary,
      "starter": starter,
      "solution": "\n".join(solution_lines) + "\n",
      "tests": "\n".join(test_lines) + "\n",
  }


def main():
  problems = []
  for slug in sorted(os.listdir(QUESTIONS_DIR)):
    impl = os.path.join(QUESTIONS_DIR, slug, "impl.py")
    if os.path.isfile(impl):
      problems.append(build_problem(slug, impl))

  os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
  with open(OUTPUT, "w") as f:
    json.dump(problems, f, indent=2)
    f.write("\n")

  print(f"Wrote {len(problems)} problems to {os.path.relpath(OUTPUT, ROOT)}")


if __name__ == "__main__":
  main()
