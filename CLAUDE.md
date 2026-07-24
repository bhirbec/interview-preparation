# Repository conventions

## Code style

- **Python indentation: 2 spaces.** Use 2-space indentation for all Python code
  (no tabs, no 4-space). This is the going-forward convention; older files in the
  repo predate it and may still use tabs or 4 spaces — match 2 spaces for new and
  edited code.

- **snake_case identifiers.** Name functions, parameters, and variables in
  `snake_case`, even when the source problem (e.g. CodeSignal) uses camelCase.
  Rename `inputString` to `input_string`, `arr` stays fine, etc. Class names
  still use `CapWords` per PEP 8.
