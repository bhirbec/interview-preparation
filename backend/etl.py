#!/usr/bin/env python3
"""ETL for the knowledge/ content: extract the coding-questions catalog and the
lessons, transform them, and load them into the SQLite database.

Each coding-question folder (under knowledge/coding-questions/) has four files:

    impl.py      # description comment + input classes + the STUBBED primary
    meta.json    # { difficulty, tags, hint }
    solution.py  # input classes + the full solution
    tests.py     # import unittest + test helpers + the unittest.TestCase

The problem id is the folder path relative to the coding-questions dir (e.g.
"maximum-subarray" or "CTCI/1.1-is-unique"). The stored `starter` is impl.py with
its leading description comment stripped (shown in its own panel); `tests` is
tests.py with its `if __name__ == '__main__'` guard stripped. Lessons
(knowledge/lessons/<slug>/ meta.json + lesson.md) load into the `lesson` table.

Run it inside the api container (which has the DB + read-only mounts of the
content):

    docker compose exec api python etl.py
"""

import json
import os
import re

import db

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
QUESTIONS_DIR = os.environ.get(
    "QUESTIONS_DIR", os.path.join(ROOT, "knowledge", "coding-questions")
)
LESSONS_DIR = os.environ.get(
    "LESSONS_DIR", os.path.join(ROOT, "knowledge", "lessons")
)


def find_problem_dirs(root):
  for dirpath, _dirnames, filenames in os.walk(root):
    if "impl.py" in filenames:
      yield dirpath


def _read(path):
  with open(path) as f:
    return f.read()


def _strip(text):
  return text.strip("\n") + "\n" if text.strip() else ""


def split_comment(text):
  """Return (comment_lines, code_str) splitting off the leading '#' comment."""
  lines = text.splitlines()
  i = 0
  comment = []
  while i < len(lines) and lines[i].startswith("#"):
    comment.append(lines[i])
    i += 1
  while i < len(lines) and lines[i].strip() == "":
    i += 1
  return comment, "\n".join(lines[i:])


def strip_guard(text):
  """Drop the `if __name__ == '__main__':` guard block from a test file."""
  out = []
  for ln in text.splitlines():
    if ln.startswith("if __name__"):
      break
    out.append(ln)
  return "\n".join(out)


def parse_metadata(comment_lines):
  title = comment_lines[0].lstrip("#").strip() if comment_lines else ""
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


def build_problem(pid, folder):
  impl = _read(os.path.join(folder, "impl.py"))
  comment, code = split_comment(impl)
  meta = parse_metadata(comment)  # title, sources, description (from impl.py)

  # difficulty / tags / hint live in meta.json (fall back to impl.py if absent).
  meta_path = os.path.join(folder, "meta.json")
  mj = json.loads(_read(meta_path)) if os.path.exists(meta_path) else {}

  solution = _read(os.path.join(folder, "solution.py"))
  tests = strip_guard(_read(os.path.join(folder, "tests.py")))

  primary = ""
  m = re.search(r"^def\s+([a-zA-Z_][a-zA-Z0-9_]*)", code, re.MULTILINE)
  if m:
    primary = m.group(1)

  return {
      "id": pid,
      "title": meta["title"],
      "difficulty": mj.get("difficulty", meta["difficulty"]),
      "tags": mj.get("tags", meta["tags"]),
      "sources": meta["sources"],
      "description": meta["description"],
      "hint": mj.get("hint", ""),
      "primary_function": primary,
      "starter": _strip(code),
      "solution": _strip(solution),
      "tests": _strip(tests),
  }


def natural_key(pid):
  return re.sub(r"\d+", lambda m: m.group().zfill(6), pid)


def import_lessons(conn, valid_ids):
  """Import lessons/<nn>-<slug>/ (meta.json + lesson.md) into the lesson table.
  Lesson id = folder slug without the numeric prefix; position = prefix. Warns
  about (but keeps) exercise ids not in the catalog."""
  if not os.path.isdir(LESSONS_DIR):
    return [], []
  imported = []
  missing = []
  for name in sorted(os.listdir(LESSONS_DIR)):
    folder = os.path.join(LESSONS_DIR, name)
    meta_path = os.path.join(folder, "meta.json")
    if not os.path.isfile(meta_path):
      continue
    m = re.match(r"(\d+)-(.+)", name)
    position = int(m.group(1)) if m else 0
    lid = m.group(2) if m else name
    meta = json.loads(_read(meta_path))
    body = _read(os.path.join(folder, "lesson.md"))
    exercises = meta.get("exercises", [])
    for ex in exercises:
      if ex not in valid_ids:
        missing.append((lid, ex))
    db.upsert_lesson(conn, lid, meta["title"], meta.get("topic", ""),
                     body, json.dumps(exercises), position)
    imported.append(lid)
  if imported:
    placeholders = ",".join("?" * len(imported))
    conn.execute(f"DELETE FROM lesson WHERE id NOT IN ({placeholders})", imported)
  return imported, missing


def main():
  problems = []
  skipped = []
  for folder in find_problem_dirs(QUESTIONS_DIR):
    pid = os.path.relpath(folder, QUESTIONS_DIR).replace(os.sep, "/")
    if not (os.path.exists(os.path.join(folder, "solution.py"))
            and os.path.exists(os.path.join(folder, "tests.py"))):
      skipped.append(pid)
      continue
    problems.append(build_problem(pid, folder))

  problems.sort(key=lambda p: natural_key(p["id"]))

  db.init_db()
  ids = [p["id"] for p in problems]
  with db.connect() as conn:
    for position, p in enumerate(problems):
      conn.execute(
          """
          INSERT INTO problem
            (id, title, difficulty, tags, sources, description, hint,
             primary_function, starter, solution, tests, position)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
          ON CONFLICT(id) DO UPDATE SET
            title=excluded.title, difficulty=excluded.difficulty,
            tags=excluded.tags, sources=excluded.sources,
            description=excluded.description, hint=excluded.hint,
            primary_function=excluded.primary_function,
            starter=excluded.starter, solution=excluded.solution,
            tests=excluded.tests, position=excluded.position
          """,
          (p["id"], p["title"], p["difficulty"], json.dumps(p["tags"]),
           json.dumps(p["sources"]), p["description"], p["hint"],
           p["primary_function"], p["starter"], p["solution"], p["tests"],
           position),
      )
    if ids:
      placeholders = ",".join("?" * len(ids))
      conn.execute(f"DELETE FROM problem WHERE id NOT IN ({placeholders})", ids)
    lessons, missing = import_lessons(conn, set(ids))

  print(f"Imported {len(problems)} problems into the problem table.")
  print(f"Imported {len(lessons)} lessons into the lesson table.")
  if skipped:
    print(f"Skipped {len(skipped)} folders missing solution.py/tests.py: {skipped}")
  if missing:
    print(f"WARNING: {len(missing)} lesson exercise ids not in catalog: {missing}")


if __name__ == "__main__":
  main()
