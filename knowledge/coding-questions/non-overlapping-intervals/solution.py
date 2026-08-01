def erase_overlap_intervals(intervals):
  if not intervals:
    return 0

  # Classic activity selection: taking the interval that ends earliest is
  # always at least as good as any alternative, so scan in end order and drop
  # anything that starts before the last kept interval finished.
  ordered = sorted(intervals, key=lambda pair: pair[1])

  removed = 0
  current_end = ordered[0][1]
  for start, end in ordered[1:]:
    if start < current_end:
      removed += 1
    else:
      current_end = end

  return removed
