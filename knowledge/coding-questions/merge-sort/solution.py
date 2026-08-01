def merge_sort(items):
  if len(items) <= 1:
    return list(items)
  middle = len(items) // 2
  return merge(merge_sort(items[:middle]), merge_sort(items[middle:]))


def merge(left, right):
  """Merge two already-sorted lists into one sorted list."""
  merged = []
  i = j = 0
  while i < len(left) and j < len(right):
    # `<=` rather than `<` keeps the sort stable: on a tie the left element,
    # which came first in the input, is emitted first.
    if right[j] < left[i]:
      merged.append(right[j])
      j += 1
    else:
      merged.append(left[i])
      i += 1
  merged.extend(left[i:])
  merged.extend(right[j:])
  return merged
