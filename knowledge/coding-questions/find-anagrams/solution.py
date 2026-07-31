def find_anagrams(words):
  counts = {}
  for w in words:
    key = ''.join(sorted(w))
    counts[key] = counts.get(key, 0) + 1

  result = []
  for w in words:
    key = ''.join(sorted(w))
    if counts[key] > 1:
      result.append(w)
  return result
