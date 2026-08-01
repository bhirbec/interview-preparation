def quicksort(items):
  _quicksort_range(items, 0, len(items) - 1)
  return items


def _quicksort_range(items, low, high):
  # Recurse into the smaller side and loop on the larger one, so the stack
  # stays O(log n) even when the partitions come out lopsided.
  while low < high:
    pivot_index = partition(items, low, high)
    if pivot_index - low < high - pivot_index:
      _quicksort_range(items, low, pivot_index - 1)
      low = pivot_index + 1
    else:
      _quicksort_range(items, pivot_index + 1, high)
      high = pivot_index - 1


def partition(items, low, high):
  """Partition items[low..high] around a pivot and return the pivot's index."""
  # Take the middle element as the pivot and park it at the end, so a sorted or
  # reverse-sorted input still splits down the middle.
  middle = (low + high) // 2
  items[middle], items[high] = items[high], items[middle]
  pivot = items[high]

  boundary = low
  for i in range(low, high):
    if items[i] < pivot:
      items[boundary], items[i] = items[i], items[boundary]
      boundary += 1
  items[boundary], items[high] = items[high], items[boundary]
  return boundary
