# Implement Trie (Prefix Tree)
#
# A trie (prefix tree) stores strings so that lookups by whole word or by
# prefix run in time proportional to the query length. Implement it:
#   - insert(word): add `word` to the trie.
#   - search(word): return True if `word` was inserted (exact match).
#   - starts_with(prefix): return True if any inserted word starts with
#     `prefix` (a word counts as a prefix of itself).
#
# Constraints:
#   - words and prefixes are non-empty strings of lowercase English letters
#   - insert may be called with the same word more than once
#
# Examples:
#   t = Trie()
#   t.insert("apple")
#   t.search("apple")       -> True
#   t.search("app")         -> False   (no such whole word)
#   t.starts_with("app")    -> True
#   t.insert("app")
#   t.search("app")         -> True


class Trie(object):
  def __init__(self):
    pass

  def insert(self, word):
    # TODO: implement
    raise NotImplementedError

  def search(self, word):
    # TODO: implement
    raise NotImplementedError

  def starts_with(self, prefix):
    # TODO: implement
    raise NotImplementedError
