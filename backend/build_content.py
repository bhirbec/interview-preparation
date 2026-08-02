#!/usr/bin/env python3
"""Build the static content artifacts from knowledge/.

Same extract/transform as etl.py, but instead of loading into SQLite it writes
plain JSON files the React app can serve statically:

    <CONTENT_OUT>/catalog.json          # id/title/difficulty/tags/position, in
                                        # position order (no sorting downstream)
    <CONTENT_OUT>/problems/<id>.json    # the full problem, one file per id
    <CONTENT_OUT>/lessons.json          # every lesson, sorted by (position, id)

The problem id is the folder path relative to the coding-questions dir (e.g.
"maximum-subarray" or "CTCI/1.1-is-unique") and it maps straight onto the file
path, so nested ids produce nested directories.

Only the stdlib is used, so it runs on the host as well as in the container:

    docker compose exec api python build_content.py
    CONTENT_OUT=app/public/data python3 backend/build_content.py
"""

import datetime
import json
import os
import re
import shutil
import sys

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
  """Read lessons/<nn>-<slug>/ (meta.json + lesson.md) into a list of dicts.
  Lesson id = folder slug without the numeric prefix; position = prefix. Warns
  about (but keeps) exercise ids not in the catalog."""
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
  """Return the list of reasons the ids are unsafe as relative file paths."""
  errors = []
  seen = {}
  for pid in ids:
    if not ID_RE.match(pid):
      errors.append(f"id {pid!r} does not match {ID_RE.pattern}")
    if pid.endswith("/"):
      errors.append(f"id {pid!r} ends with a slash")
    if any(seg in (".", "..") for seg in pid.split("/")):
      errors.append(f"id {pid!r} has a '.' or '..' path segment")
    other = seen.setdefault(pid.casefold(), pid)
    if other != pid:
      errors.append(f"id {pid!r} collides with {other!r} on a case-insensitive "
                    "filesystem")
  return errors


def problem_json(p):
  """The problem detail payload — identical to server._problem_dict()."""
  return {
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
  }


def write_json(path, obj):
  """Write obj as compact UTF-8 JSON, creating parent dirs. Returns its size."""
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, "w", encoding="utf-8") as f:
    json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
  return os.path.getsize(path)


def human_size(n):
  if n < 1024:
    return f"{n} B"
  if n < 1024 * 1024:
    return f"{n / 1024:.0f} KB"
  return f"{n / (1024 * 1024):.1f} MB"


def now_iso():
  return (datetime.datetime.now(datetime.timezone.utc)
          .isoformat(timespec="seconds").replace("+00:00", "Z"))


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
    return 1

  lessons, missing = load_lessons(set(ids))
  generated_at = now_iso()

  # Build into a sibling temp dir and swap it in, so a renamed or deleted
  # problem can't leave a stale JSON file behind (plain writes never reconcile
  # deletions the way the ETL's `DELETE ... WHERE id NOT IN (...)` did).
  out = os.path.abspath(CONTENT_OUT)
  tmp = out + f".tmp-{os.getpid()}"
  os.makedirs(os.path.dirname(out), exist_ok=True)
  shutil.rmtree(tmp, ignore_errors=True)
  try:
    problems_bytes = 0
    for p in problems:
      problems_bytes += write_json(
          os.path.join(tmp, "problems", *p["id"].split("/")) + ".json",
          problem_json(p))

    catalog_bytes = write_json(os.path.join(tmp, "catalog.json"), {
        "generatedAt": generated_at,
        "count": len(problems),
        "problems": [{
            "id": p["id"],
            "title": p["title"],
            "difficulty": p["difficulty"],
            "tags": p["tags"],
            "position": position,
        } for position, p in enumerate(problems)],
    })

    lessons_bytes = write_json(os.path.join(tmp, "lessons.json"), {
        "generatedAt": generated_at,
        "lessons": lessons,
    })

    shutil.rmtree(out, ignore_errors=True)
    os.replace(tmp, out)
  finally:
    shutil.rmtree(tmp, ignore_errors=True)

  print(f"Wrote {out}: {len(problems)} problems ({human_size(problems_bytes)}), "
        f"{len(lessons)} lessons ({human_size(lessons_bytes)}), "
        f"catalog {human_size(catalog_bytes)}")
  if skipped:
    print(f"Skipped {len(skipped)} folders missing solution.py/tests.py: {skipped}")
  if missing:
    print(f"WARNING: {len(missing)} lesson exercise ids not in catalog: {missing}")
  return 0


if __name__ == "__main__":
  sys.exit(main())
