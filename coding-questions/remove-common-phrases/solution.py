def remove_common_phrases(sentences):
  tokenized = [s.split() for s in sentences]

  window_to_sentences = {}
  for idx, words in enumerate(tokenized):
    n = len(words)
    for size in range(3, n + 1):
      for i in range(n - size + 1):
        key = tuple(words[i:i + size])
        window_to_sentences.setdefault(key, set()).add(idx)

  common = {key for key, owners in window_to_sentences.items()
            if len(owners) >= 2}

  result = []
  for words in tokenized:
    n = len(words)
    remove = [False] * n
    for size in range(3, n + 1):
      for i in range(n - size + 1):
        if tuple(words[i:i + size]) in common:
          for j in range(i, i + size):
            remove[j] = True
    kept = [word for j, word in enumerate(words) if not remove[j]]
    result.append(' '.join(kept))
  return result
