def count_words(words, num_rows, num_cols):
  n = len(words)
  if n == 0 or num_rows <= 0:
    return 0

  count = 0
  k = 0  # index into the cyclic stream of words

  for _ in range(num_rows):
    line_len = 0
    while True:
      word = words[k % n]
      needed = len(word) if line_len == 0 else len(word) + 1
      if line_len + needed <= num_cols:
        line_len += needed
        k += 1
        count += 1
      else:
        break

  return count
