def find(root, path):
  fragments = path.split('.')
  n = len(fragments)
  output = []

  def _walk(node, i):
    fragment = fragments[i]

    if fragment == '*':
      if isinstance(node, list):
        next_fragments = list(range(len(node)))
      else:
        next_fragments = list(node.keys())
    elif isinstance(node, list):
      next_fragments = [int(fragment)]
    else:
      next_fragments = [fragment]

    for frag in next_fragments:
      try:
        next_node = node[frag]
      except (IndexError, KeyError, TypeError):
        continue

      if i == n - 1:
        output.append(next_node)
      else:
        _walk(next_node, i + 1)

  _walk(root, 0)
  return output
