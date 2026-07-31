def merge(arr1, arr2):
  # i indexes the last real (non-buffer) element of arr1. The buffer occupies
  # the final len(arr2) slots, so the real elements end at this index. The
  # original hardcoded i = 3, which only worked for the demo input.
  i = len(arr1) - len(arr2) - 1
  j = len(arr2) - 1
  k = len(arr1) - 1

  while i > -1 and j > -1:
    if arr1[i] >= arr2[j]:
      arr1[k] = arr1[i]
      i -= 1
    else:
      arr1[k] = arr2[j]
      j -= 1
    k -= 1

  # Any remaining arr2 elements are smaller than every placed value; copy them.
  while j > -1:
    arr1[k] = arr2[j]
    j -= 1
    k -= 1

  return arr1
