def find_subarray_with_sum(arr, target):
  start = 0
  running = 0
  for end in range(len(arr)):
    running += arr[end]
    while running > target and start < end:
      running -= arr[start]
      start += 1
    if running == target:
      return (start, end)
  return None
