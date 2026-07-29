def find(arr, value):
  if not arr:
    return None

  r = find_rotation_point(arr)

  # arr[0 .. r-1] is the higher, left run; arr[r .. end] is the lower, right run.
  if r > 0 and arr[0] <= value <= arr[r - 1]:
    idx = binary_search(arr, value, 0, r - 1)
    if idx is not None:
      return idx

  return binary_search(arr, value, r, len(arr) - 1)


def find_rotation_point(arr):
  # A non-rotated array's minimum is at index 0.
  if arr[0] <= arr[-1]:
    return 0

  def _f(arr, start, end):
    if end - start <= 1:
      return end

    mid = (end + start) // 2

    if arr[mid] > arr[end]:
      # rotation point is in the right half
      return _f(arr, mid, end)
    else:
      # rotation point is in the left half
      return _f(arr, start, mid)

  return _f(arr, 0, len(arr) - 1)


def binary_search(arr, value, start, end):
  if end < start:
    return None

  mid = (end + start) // 2
  if arr[mid] == value:
    return mid
  elif arr[mid] > value:
    return binary_search(arr, value, start, mid - 1)
  else:
    return binary_search(arr, value, mid + 1, end)
