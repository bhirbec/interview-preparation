def number_of_provinces(matrix):
  n = len(matrix)
  visited = [False] * n
  groups = 0

  for start in range(n):
    if visited[start]:
      continue
    groups += 1
    stack = [start]
    visited[start] = True
    while stack:
      node = stack.pop()
      row = matrix[node]
      for nxt in range(n):
        if row[nxt] == '1' and not visited[nxt]:
          visited[nxt] = True
          stack.append(nxt)
  return groups
