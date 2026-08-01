class Trie(object):
  _END = '#'

  def __init__(self):
    self.root = {}

  def insert(self, word):
    node = self.root
    for ch in word:
      node = node.setdefault(ch, {})
    node[self._END] = True

  def search(self, word):
    node = self._walk(word)
    return node is not None and self._END in node

  def starts_with(self, prefix):
    return self._walk(prefix) is not None

  def _walk(self, s):
    node = self.root
    for ch in s:
      if ch not in node:
        return None
      node = node[ch]
    return node
