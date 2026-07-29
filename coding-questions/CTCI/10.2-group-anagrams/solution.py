def group_anagrams(arr):
  buckets = {}
  for w in arr:
    key = ''.join(sorted(w))
    buckets.setdefault(key, []).append(w)

  output = []
  for words in buckets.values():
    output.extend(words)

  return output
