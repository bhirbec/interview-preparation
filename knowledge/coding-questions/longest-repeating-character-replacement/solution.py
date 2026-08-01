def character_replacement(s, k):
  counts = {}
  best = 0
  # Highest letter count seen in any window so far. It is never decreased: a
  # window only ever matters when it beats the current best, and that requires
  # a strictly larger majority count.
  max_count = 0
  left = 0

  for right, ch in enumerate(s):
    counts[ch] = counts.get(ch, 0) + 1
    max_count = max(max_count, counts[ch])

    # Characters to rewrite = window length - the majority letter's count.
    if (right - left + 1) - max_count > k:
      counts[s[left]] -= 1
      left += 1

    best = max(best, right - left + 1)

  return best
