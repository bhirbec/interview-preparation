from collections import deque


def find_ladder(begin, end, word_list):
  if begin == end:
    return [begin]

  words = set(word_list)
  if end not in words:
    return []

  queue = deque([[begin]])
  visited = {begin}

  while queue:
    path = queue.popleft()
    last = path[-1]
    if last == end:
      return path
    for i in range(len(last)):
      for code in range(ord('a'), ord('z') + 1):
        ch = chr(code)
        if ch == last[i]:
          continue
        nxt = last[:i] + ch + last[i + 1:]
        if nxt in words and nxt not in visited:
          visited.add(nxt)
          queue.append(path + [nxt])

  return []
