from collections import deque


def find_base(grid):
  if not grid or not grid[0]:
    return None

  rows, cols = len(grid), len(grid[0])
  sites = [
    (r, c)
    for r in range(rows)
    for c in range(cols)
    if grid[r][c] == '*'
  ]
  if not sites:
    return None

  total = [[0] * cols for _ in range(rows)]
  reach = [[0] * cols for _ in range(rows)]

  for sr, sc in sites:
    dist = [[-1] * cols for _ in range(rows)]
    dist[sr][sc] = 0
    queue = deque([(sr, sc)])
    while queue:
      r, c = queue.popleft()
      for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#' and dist[nr][nc] == -1:
          dist[nr][nc] = dist[r][c] + 1
          queue.append((nr, nc))

    for r in range(rows):
      for c in range(cols):
        if dist[r][c] != -1:
          reach[r][c] += 1
          total[r][c] += dist[r][c]

  best = None
  for r in range(rows):
    for c in range(cols):
      if grid[r][c] != '#' and reach[r][c] == len(sites):
        if best is None or total[r][c] < best[0]:
          best = (total[r][c], r, c)

  if best is None:
    return None
  return (best[1], best[2])
