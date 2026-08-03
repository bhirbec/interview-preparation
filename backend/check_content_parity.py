#!/usr/bin/env python3
"""One-off proof that build_content.py's JSON matches the ETL-loaded rows.

Run inside the api container, after `python etl.py` and `python build_content.py`:

    docker compose exec api python check_content_parity.py

Compares, field by field, the generated catalog/problem/lesson JSON against what
server._problem_dict() and the lesson endpoints would have returned from the
`problem` / `lesson` tables. Exits non-zero on any difference.
"""

import json
import os
import sys

import db
import server
from build_content import CONTENT_OUT


def _read_json(path):
  with open(path) as f:
    return json.load(f)


def main():
  problems_dir = os.path.join(CONTENT_OUT, "problems")
  catalog = _read_json(os.path.join(CONTENT_OUT, "catalog.json"))
  lessons_json = _read_json(os.path.join(CONTENT_OUT, "lessons.json"))

  with db.connect() as conn:
    rows = conn.execute("SELECT * FROM problem ORDER BY position").fetchall()
    lesson_rows = conn.execute("SELECT * FROM lesson ORDER BY position").fetchall()

  errors = []

  db_ids = [r["id"] for r in rows]
  json_ids = [p["id"] for p in catalog["problems"]]
  same_order = db_ids == json_ids
  print(f"problems: db={len(db_ids)} json={len(json_ids)} "
        f"same-ids-in-order={same_order}")
  if not same_order:
    errors.append("catalog id order differs from the problem table")
  if catalog["count"] != len(json_ids):
    errors.append("catalog count field disagrees with its own problems array")
  for position, p in enumerate(catalog["problems"]):
    if p["position"] != position:
      errors.append(f"{p['id']}: catalog position {p['position']} != {position}")

  # Every problem file, field by field, against server._problem_dict().
  compared = 0
  for r in rows:
    want = server._problem_dict(r)
    path = os.path.join(problems_dir, *r["id"].split("/")) + ".json"
    if not os.path.exists(path):
      errors.append(f"{r['id']}: no JSON file at {path}")
      continue
    got = _read_json(path)
    for key in sorted(set(want) | set(got)):
      if want.get(key) != got.get(key):
        errors.append(f"{r['id']}: field {key!r} differs")
    # The catalog row must agree with the detail file.
    cat = next((c for c in catalog["problems"] if c["id"] == r["id"]), None)
    if cat is None:
      errors.append(f"{r['id']}: missing from catalog.json")
    else:
      for key in ("title", "difficulty", "tags"):
        if cat[key] != want[key]:
          errors.append(f"{r['id']}: catalog {key!r} differs from the detail file")
    compared += 1
  print(f"problem detail docs compared field-by-field: {compared}")

  on_disk = []
  for dirpath, _dirnames, filenames in os.walk(problems_dir):
    for name in filenames:
      if name.endswith(".json"):
        rel = os.path.relpath(os.path.join(dirpath, name), problems_dir)
        on_disk.append(rel[: -len(".json")].replace(os.sep, "/"))
  strays = sorted(set(on_disk) - set(db_ids))
  print(f"problem files on disk: {len(on_disk)} (no strays: {not strays})")
  if strays:
    errors.append(f"stale problem files: {strays}")

  # Lessons: the generated entries against the lesson table.
  db_lessons = [r["id"] for r in lesson_rows]
  json_lessons = [l["id"] for l in lessons_json["lessons"]]
  same_lessons = db_lessons == json_lessons
  print(f"lessons: db={len(db_lessons)} json={len(json_lessons)} "
        f"same-ids-in-order={same_lessons}")
  if not same_lessons:
    errors.append("lesson id order differs from the lesson table")
  by_id = {l["id"]: l for l in lessons_json["lessons"]}
  for r in lesson_rows:
    got = by_id.get(r["id"])
    if got is None:
      errors.append(f"lesson {r['id']}: missing from lessons.json")
      continue
    want = {
        "id": r["id"],
        "title": r["title"],
        "topic": r["topic"],
        "position": r["position"],
        "body": r["body"],
        "exercises": json.loads(r["exercises"] or "[]"),
    }
    for key in sorted(want):
      if want[key] != got.get(key):
        errors.append(f"lesson {r['id']}: field {key!r} differs")

  if errors:
    print()
    for e in errors:
      print(f"ERROR: {e}")
    print(f"\nFAIL - {len(errors)} differences.")
    sys.exit(1)
  print("\nPASS - generated JSON is field-for-field identical to the ETL-loaded rows.")


if __name__ == "__main__":
  main()
