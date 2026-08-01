def insertion_sort(items):
  for i in range(1, len(items)):
    current = items[i]
    j = i - 1
    # Shift every element greater than `current` one slot to the right. The
    # comparison is strict, so equal elements are never swapped past each
    # other and the sort stays stable.
    while j >= 0 and current < items[j]:
      items[j + 1] = items[j]
      j -= 1
    items[j + 1] = current
  return items
