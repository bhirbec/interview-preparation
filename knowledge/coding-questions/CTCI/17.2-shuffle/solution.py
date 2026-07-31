import random


def shuffle(n):
  if n == 0:
    return []

  # shuffle 1..n-1
  result = shuffle(n - 1)
  # pick a position between 0 and n-1
  i = int(random.uniform(0, n))
  # append the nth number
  result.append(n)
  # swap the nth element into position i
  result[i], result[n - 1] = result[n - 1], result[i]
  return result
