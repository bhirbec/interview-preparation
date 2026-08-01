class TrieNode(object):
  def __init__(self):
    self.children = {}
    self.is_word = False


def longest_word(words):
  root = TrieNode()
  for word in words:
    node = root
    for ch in word:
      if ch not in node.children:
        node.children[ch] = TrieNode()
      node = node.children[ch]
    node.is_word = True

  # Depth-first walk that may only step onto nodes ending a word, so every
  # prefix of the path is buildable. Visiting children in sorted order makes
  # the first deepest hit the lexicographically smallest one.
  best = ""
  stack = [(root, "")]
  while stack:
    node, prefix = stack.pop()
    if len(prefix) > len(best):
      best = prefix
    for ch in sorted(node.children, reverse=True):
      child = node.children[ch]
      if child.is_word:
        stack.append((child, prefix + ch))

  return best
