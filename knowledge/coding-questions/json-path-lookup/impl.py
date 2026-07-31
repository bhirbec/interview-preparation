# JSON Path Lookup
#
# You are given a nested JSON-like structure `root` (composed of dicts and lists)
# and a dot-separated `path` string. Return a list of every value reached by
# following the path from the root. A path segment names a dict key, or — when the
# current node is a list — a numeric list index.
#
# The wildcard segment "*" matches EVERY child of the current node: all values of
# a dict, or all elements of a list. A path may contain several wildcards, in
# which case results are collected in traversal order. Segments that do not
# resolve (missing key, out-of-range index) contribute nothing; if nothing
# resolves, return an empty list.
#
# Constraints:
#   - dict keys are strings; list indices in the path are decimal integers
#   - the path is non-empty
#
# Examples (data = {"books": {"novels": [{"title": "LOTR", "author": "Tolkien"},
#                                         {"title": "Hobbit", "author": "Tolkien"}]}}):
#   "books.novels.0.author"  -> ["Tolkien"]
#   "books.novels"           -> [ the whole novels list ]
#   "books.novels.*.author"  -> ["Tolkien", "Tolkien"]
#   "books.novels.2.author"  -> []           (index out of range)


def find(root, path):
  # TODO: implement
  raise NotImplementedError
