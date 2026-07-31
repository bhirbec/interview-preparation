from random import randint


def binary_search(arr, value):
  def _f(arr, start, end):
    if end < start:
      return None

    p = randint(start, end)
    if value == arr[p] and arr[p] != '':
      return p

    if arr[start] == '':
      start += 1
    if arr[end] == '':
      end -= 1

    if arr[p] == '':
      return _f(arr, start, end)
    elif value < arr[p]:
      return _f(arr, start, p - 1)
    else:
      return _f(arr, p + 1, end)

  return _f(arr, 0, len(arr) - 1)
