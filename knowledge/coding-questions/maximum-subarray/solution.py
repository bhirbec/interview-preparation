def max_subarray(array):
  current_sum = 0
  max_sum = 0
  start, end = 0, 0

  for k, value in enumerate(array):
    current_sum += value
    if current_sum < 0:
      current_sum = 0
      start = k + 1
    elif current_sum > max_sum:
      max_sum = current_sum
      end = k

  return max_sum, start, end
