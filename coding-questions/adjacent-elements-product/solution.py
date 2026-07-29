def adjacent_elements_product(arr):
  max_product = None
  for i in range(1, len((arr))):
    product = arr[i-1] * arr[i]
    if max_product is None or product > max_product:
      max_product = product

  return max_product
