#!/usr/bin/env python3
"""Import the coding-questions catalog into the database.

Recursively finds every coding-questions/**/impl.py (any depth), parses each
into its problem fields, and upserts them into the `problem` table. The problem
id is the folder path relative to coding-questions/ (e.g. "maximum-subarray" or
"CTCI/1.1-is-unique"), which is stable across runs.

Run it inside the api container (which has the DB + a read-only mount of
coding-questions):

    docker compose exec api python build.py

Each impl.py looks like:

    # Title
    # Difficulty: <level>
    # Source: <url>            (optional, zero or more)
    # Tags: #tag1 #tag2
    #
    # <problem statement...>

    import unittest
    <other imports>           (optional)

    class Node: ...           (optional helper class(es))
    def primary(...): ...     (first top-level def == the function to solve)
    ...

    class TestX(unittest.TestCase): ...

    if __name__ == '__main__':
      unittest.main()

The starter keeps only the primary function's signature with a stubbed body.
"""

import json
import os
import re

import db

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
QUESTIONS_DIR = os.environ.get(
    "QUESTIONS_DIR", os.path.join(ROOT, "coding-questions")
)


def find_impls(root):
  for dirpath, _dirnames, filenames in os.walk(root):
    if "impl.py" in filenames:
      yield os.path.join(dirpath, "impl.py")


def _strip_blanks(block):
  while block and block[0].strip() == "":
    block.pop(0)
  while block and block[-1].strip() == "":
    block.pop()
  return block


def parse_metadata(comment_lines):
  title = comment_lines[0].lstrip("#").strip()
  difficulty = ""
  sources = []
  tags = []
  description = []

  for ln in comment_lines[1:]:
    text = ln.lstrip("#").removeprefix(" ")
    stripped = text.strip()
    if stripped.startswith("Difficulty:"):
      difficulty = stripped.split(":", 1)[1].strip()
    elif stripped.startswith("Source:"):
      sources.append(stripped.split(":", 1)[1].strip())
    elif stripped.startswith("Tags:"):
      tags = re.findall(r"#([a-z0-9-]+)", stripped)
    else:
      description.append(text.rstrip())

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
  """Stub only the primary (first top-level) function's body, keeping everything
  else (helper classes like Node, needed imports, and test helpers) so the tests
  can still build their inputs.
  """
  start = next(
      (i for i, ln in enumerate(solution_lines) if ln.startswith("def ")), None
  )
  if start is None:
    return "", "\n".join(solution_lines) + "\n"

  name = re.match(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)", solution_lines[start]).group(1)

  # End of the (possibly multi-line) signature: the line ending with ":".
  sig_end = next(
      j for j in range(start, len(solution_lines))
      if solution_lines[j].rstrip().endswith(":")
  )

  # End of the function body: the next top-level (unindented, non-blank) line.
  body_end = len(solution_lines)
  for j in range(sig_end + 1, len(solution_lines)):
    ln = solution_lines[j]
    if ln.strip() and not ln[:1].isspace():
      body_end = j
      break

  stub = ["  # TODO: implement", "  raise NotImplementedError"]
  new_lines = solution_lines[:sig_end + 1] + stub
  trailing = solution_lines[body_end:]
  if trailing:
    new_lines += ["", ""] + trailing

  starter = "\n".join(new_lines).rstrip() + "\n"
  return name, starter


def build_problem(pid, path):
  with open(path) as f:
    lines = f.read().splitlines()

  comment = []
  i = 0
  while i < len(lines) and lines[i].startswith("#"):
    comment.append(lines[i])
    i += 1

  test_start = next(
      i for i, ln in enumerate(lines)
      if ln.startswith("class ") and "unittest.TestCase" in ln
  )
  guard = next(
      (i for i, ln in enumerate(lines) if ln.startswith("if __name__")), len(lines)
  )

  # Everything between the comment block and the test class is the solution
  # (helper classes, imports it needs, and the functions) minus `import unittest`.
  body = [ln for ln in lines[len(comment):test_start] if ln.strip() != "import unittest"]
  solution = _strip_blanks(body)
  tests = _strip_blanks(lines[test_start:guard])

  meta = parse_metadata(comment)
  primary, starter = make_starter(list(solution))

  return {
      "id": pid,
      "title": meta["title"],
      "difficulty": meta["difficulty"],
      "tags": meta["tags"],
      "sources": meta["sources"],
      "description": meta["description"],
      "primary_function": primary,
      "starter": starter,
      "solution": "\n".join(solution) + "\n",
      "tests": "\n".join(tests) + "\n",
  }


def natural_key(pid):
  # Zero-pad numbers so "1.10" sorts after "1.2".
  return re.sub(r"\d+", lambda m: m.group().zfill(6), pid)


def main():
  problems = []
  for path in find_impls(QUESTIONS_DIR):
    pid = os.path.relpath(os.path.dirname(path), QUESTIONS_DIR).replace(os.sep, "/")
    problems.append(build_problem(pid, path))

  problems.sort(key=lambda p: natural_key(p["id"]))

  db.init_db()
  ids = [p["id"] for p in problems]
  with db.connect() as conn:
    for position, p in enumerate(problems):
      conn.execute(
          """
          INSERT INTO problem
            (id, title, difficulty, tags, sources, description,
             primary_function, starter, solution, tests, position)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
          ON CONFLICT(id) DO UPDATE SET
            title=excluded.title, difficulty=excluded.difficulty,
            tags=excluded.tags, sources=excluded.sources,
            description=excluded.description,
            primary_function=excluded.primary_function,
            starter=excluded.starter, solution=excluded.solution,
            tests=excluded.tests, position=excluded.position
          """,
          (p["id"], p["title"], p["difficulty"], json.dumps(p["tags"]),
           json.dumps(p["sources"]), p["description"], p["primary_function"],
           p["starter"], p["solution"], p["tests"], position),
      )
    # Drop problems whose folder no longer exists.
    if ids:
      placeholders = ",".join("?" * len(ids))
      conn.execute(f"DELETE FROM problem WHERE id NOT IN ({placeholders})", ids)

  print(f"Imported {len(problems)} problems into the problem table.")


if __name__ == "__main__":
  main()
