from heapq import heappush, heappop


def first_day_reachable(grid):
  n = len(grid)
  if n == 0:
    return -1
  m = len(grid[0])

  visited = [[False] * m for _ in range(n)]
  heap = [(grid[0][0], 0, 0)]  # (max elevation on path so far, i, j)

  while heap:
    day, i, j = heappop(heap)
    if visited[i][j]:
      continue
    visited[i][j] = True

    if i == n - 1 and j == m - 1:
      return day

    for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
      ni, nj = i + di, j + dj
      if 0 <= ni < n and 0 <= nj < m and not visited[ni][nj]:
        heappush(heap, (max(day, grid[ni][nj]), ni, nj))

  return -1
