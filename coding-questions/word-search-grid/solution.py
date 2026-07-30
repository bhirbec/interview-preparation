def word_search(grid, word):
  rows = len(grid)
  cols = len(grid[0])

  def dfs(r, c, i):
    if grid[r][c] != word[i]:
      return False
    if i == len(word) - 1:
      return True

    temp = grid[r][c]
    grid[r][c] = None  # mark visited
    found = False
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
      nr, nc = r + dr, c + dc
      if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] is not None:
        if dfs(nr, nc, i + 1):
          found = True
          break
    grid[r][c] = temp  # unmark on backtrack
    return found

  for r in range(rows):
    for c in range(cols):
      if dfs(r, c, 0):
        return True
  return False
