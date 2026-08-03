#!/usr/bin/env python3
"""Build the static knowledge content served by the React app.

Reads knowledge/ (coding questions + lessons) and writes plain JSON files the
browser fetches directly — the content is immutable between builds, so it needs
no database. Only user state (submission/run/attempt) lives in SQLite; this
module never imports db.

Each coding-question folder (under knowledge/coding-questions/) has four files:

    impl.py      # description comment + input classes + the STUBBED primary
    meta.json    # { difficulty, tags, sources, hint }
    solution.py  # input classes + the full solution
    tests.py     # import unittest + test helpers + the unittest.TestCase

The problem id is the folder path relative to the coding-questions dir (e.g.
"maximum-subarray" or "CTCI/1.1-is-unique"). The emitted `starter` is impl.py
with its leading description comment stripped (shown in its own panel); `tests`
is tests.py with its `if __name__ == '__main__'` guard stripped.

Output (under CONTENT_OUT, default app/public/data):

    catalog.json          { generatedAt, count, problems: [...] } in position order
    problems/<id>.json    one file per problem, mirroring the id path
    lessons.json          { generatedAt, lessons: [...] } with bodies inlined

Run it inside the api container (which has the read-only content mounts and a
writable mount of app/public):

    docker compose exec api python build_content.py

or on the host (stdlib only, no dependencies):

    CONTENT_OUT=app/public/data python3 backend/build_content.py
"""

import json
import os
import re
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
QUESTIONS_DIR = os.environ.get(
    "QUESTIONS_DIR", os.path.join(ROOT, "knowledge", "coding-questions")
)
LESSONS_DIR = os.environ.get(
    "LESSONS_DIR", os.path.join(ROOT, "knowledge", "lessons")
)
CONTENT_OUT = os.environ.get(
    "CONTENT_OUT", os.path.join(ROOT, "app", "public", "data")
)

# Ids become URL path segments and file paths, so keep them boring.
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")


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
  meta = parse_metadata(comment)  # title, description (from impl.py)

  # difficulty / tags / sources / hint live in meta.json (fall back to impl.py
  # if absent).
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
      "sources": mj.get("sources", meta["sources"]),
      "description": meta["description"],
      "hint": mj.get("hint", ""),
      "primary_function": primary,
      "starter": _strip(code),
      "solution": _strip(solution),
      "tests": _strip(tests),
  }


def natural_key(pid):
  return re.sub(r"\d+", lambda m: m.group().zfill(6), pid)


def load_lessons(valid_ids):
  """Read lessons/<nn>-<slug>/ (meta.json + lesson.md) into (lessons, missing).

  Lesson id = folder slug without the numeric prefix; position = prefix. Reports
  (but keeps) exercise ids not in the catalog."""
  if not os.path.isdir(LESSONS_DIR):
    return [], []
  lessons = []
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
    lessons.append({
        "id": lid,
        "title": meta["title"],
        "topic": meta.get("topic", ""),
        "position": position,
        "body": body,
        "exercises": exercises,
    })
  lessons.sort(key=lambda l: (l["position"], l["id"]))
  return lessons, missing


def check_ids(ids):
  """Fail the build on ids that can't be safely turned into output paths."""
  errors = []
  for pid in ids:
    if not ID_RE.match(pid):
      errors.append(f"illegal problem id: {pid!r}")
    elif any(seg in (".", "..") for seg in pid.split("/")):
      errors.append(f"problem id has a '.' or '..' segment: {pid!r}")
  # macOS is case-insensitive, so two ids differing only in case would clobber
  # each other's JSON file on a developer machine but not in CI.
  folded = {}
  for pid in ids:
    folded.setdefault(pid.casefold(), []).append(pid)
  for _key, group in sorted(folded.items()):
    if len(group) > 1:
      errors.append(f"problem ids collide case-insensitively: {sorted(group)}")
  return errors


def _dump(path, obj):
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, "w") as f:
    json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
  return path


def _prune(out_dir, keep):
  """Delete everything under out_dir that this build didn't just write."""
  for dirpath, dirnames, filenames in os.walk(out_dir, topdown=False):
    for name in filenames:
      path = os.path.join(dirpath, name)
      if path not in keep:
        os.remove(path)
    for name in dirnames:
      path = os.path.join(dirpath, name)
      if not os.listdir(path):
        os.rmdir(path)


def write_content(out_dir, problems, lessons, generated_at):
  """Write the JSON tree, then delete whatever this build didn't write.

  Plain writes never reconcile deletions (the old ETL did that with a
  DELETE ... WHERE id NOT IN), so a renamed problem would otherwise leave a
  stale JSON forever. Reconcile rather than swapping a temp dir into place:
  replacing the directory changes its inode, and the frontend container's view
  of the bind mount then goes stale for part of the tree until it restarts.
  """
  written = set()
  os.makedirs(out_dir, exist_ok=True)

  written.add(_dump(os.path.join(out_dir, "catalog.json"), {
      "generatedAt": generated_at,
      "count": len(problems),
      "problems": [
          {
              "id": p["id"],
              "title": p["title"],
              "difficulty": p["difficulty"],
              "tags": p["tags"],
              "position": position,
          }
          for position, p in enumerate(problems)
      ],
  }))

  for p in problems:
    written.add(_dump(os.path.join(out_dir, "problems", *p["id"].split("/")) + ".json", {
        "id": p["id"],
        "title": p["title"],
        "difficulty": p["difficulty"],
        "tags": p["tags"],
        "sources": p["sources"],
        "description": p["description"],
        "hint": p["hint"],
        "primaryFunction": p["primary_function"],
        "starter": p["starter"],
        "solution": p["solution"],
        "tests": p["tests"],
    }))

  written.add(_dump(os.path.join(out_dir, "lessons.json"), {
      "generatedAt": generated_at,
      "lessons": lessons,
  }))

  _prune(out_dir, written)


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

  ids = [p["id"] for p in problems]
  errors = check_ids(ids)
  if errors:
    for e in errors:
      print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)

  lessons, missing = load_lessons(set(ids))
  generated_at = datetime.now(timezone.utc).isoformat()
  write_content(CONTENT_OUT, problems, lessons, generated_at)

  print(f"Wrote {len(problems)} problems and {len(lessons)} lessons to {CONTENT_OUT}.")
  if skipped:
    print(f"Skipped {len(skipped)} folders missing solution.py/tests.py: {skipped}")
  if missing:
    print(f"WARNING: {len(missing)} lesson exercise ids not in catalog: {missing}")


if __name__ == "__main__":
  main()
