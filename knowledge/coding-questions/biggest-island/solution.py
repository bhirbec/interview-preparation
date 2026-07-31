def biggest_island(grid):
  if not grid:
    return 0

  n = len(grid)
  m = len(grid[0])

  visited = {}
  max_size = 0

  for i in range(n):
    for j in range(m):
      value = grid[i][j]
      if value != 'L' or (i, j) in visited:
        continue

      size = 0
      stack = []
      stack.append((i, j))

      while len(stack) > 0:
        i, j = stack.pop()
        if (i, j) in visited:
          continue

        visited[(i, j)] = True
        size += 1

        top = (i + 1, j)
        right = (i, j + 1)
        bottom = (i - 1, j)
        left = (i, j - 1)

        for next_i, next_j in [top, right, bottom, left]:
          if 0 <= next_i < n and 0 <= next_j < m:
            adjacent_value = grid[next_i][next_j]

            if adjacent_value == 'L' and (next_i, next_j) not in visited:
              stack.append((next_i, next_j))

      if size > max_size:
        max_size = size

  return max_size
