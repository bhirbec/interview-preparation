def longest_unique_substring_length(s):
  last_index = {}
  best = 0
  left = 0
  for right, ch in enumerate(s):
    if ch in last_index and last_index[ch] >= left:
      left = last_index[ch] + 1
    last_index[ch] = right
    best = max(best, right - left + 1)
  return best
