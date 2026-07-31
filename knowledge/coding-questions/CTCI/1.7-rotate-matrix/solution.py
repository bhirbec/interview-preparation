def rotate(mat):
  n = len(mat)

  for layer in range(n // 2):
    last = n - 1 - layer
    for i in range(n - 1 - 2 * layer):
      top = mat[layer][last - i]
      # right -> top
      mat[layer][last - i] = mat[last - i][last]
      # bottom -> right
      mat[last - i][last] = mat[last][layer + i]
      # left -> bottom
      mat[last][layer + i] = mat[layer + i][layer]
      # top -> left
      mat[layer + i][layer] = top

  return mat
