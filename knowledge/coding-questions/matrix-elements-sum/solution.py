def matrix_elements_sum(matrix):
  total = 0
  nb_rows = len(matrix)
  nb_cols = len(matrix[0])
  for j in range(nb_cols):
    for i in range(nb_rows):
      cost = matrix[i][j]
      if cost == 0:
        break
      total += cost

  return total
