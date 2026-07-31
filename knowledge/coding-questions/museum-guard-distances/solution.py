from collections import deque


def museum_distances(matrix):
  n = len(matrix)
  result = [list(row) for row in matrix]

  q = deque()
  seen = set()
  for i in range(n):
    for j in range(len(matrix[i])):
      if matrix[i][j] == 'G':
        q.append((i, j, 0))
        seen.add((i, j))

  moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
           (0, 1), (1, -1), (1, 0), (1, 1)]

  while q:
    i, j, dist = q.popleft()
    if matrix[i][j] == 'O':
      result[i][j] = dist
    for di, dj in moves:
      ni, nj = i + di, j + dj
      if 0 <= ni < n and 0 <= nj < len(matrix[ni]):
        if (ni, nj) not in seen and matrix[ni][nj] != 'W':
          seen.add((ni, nj))
          q.append((ni, nj, dist + 1))

  return result
