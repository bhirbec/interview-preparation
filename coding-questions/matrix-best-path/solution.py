def find_best_path(matrix):
  rows = len(matrix)
  cols = len(matrix[0])

  location = [None] * (rows * cols + 1)
  for i in range(rows):
    for j in range(cols):
      location[matrix[i][j]] = (i, j)

  removed = [[False] * cols for _ in range(rows)]

  def mark_top_right(i, j):
    for row in range(i - 1, -1, -1):
      for col in range(j + 1, cols):
        if removed[row][col]:
          return
        removed[row][col] = True

  def mark_bottom_left(i, j):
    for row in range(i + 1, rows):
      for col in range(j - 1, -1, -1):
        if removed[row][col]:
          return
        removed[row][col] = True

  positions = []
  for number in range(1, rows * cols + 1):
    i, j = location[number]
    if removed[i][j]:
      continue
    positions.append((i, j))
    mark_top_right(i, j)
    mark_bottom_left(i, j)

  positions.sort()
  return [matrix[i][j] for i, j in positions]
