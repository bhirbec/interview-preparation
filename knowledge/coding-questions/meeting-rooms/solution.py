def can_attend_meetings(intervals):
  ordered = sorted(intervals)
  for i in range(1, len(ordered)):
    if ordered[i][0] < ordered[i - 1][1]:
      return False
  return True
