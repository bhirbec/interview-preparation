def build_order(projects, dependencies):
  adjacency_list = _build_adjacency_list(projects, dependencies)
  projects = list(projects)
  n = len(projects)
  order: list = [None] * n
  visited = {}
  visiting = {}
  index = n - 1

  def _dfs(p):
    nonlocal index
    if p in visiting:
      # we're currently visiting this node which means that we're in a cycle
      return False

    if p in visited:
      return True

    visiting[p] = True
    for p1 in adjacency_list[p]:
      if not _dfs(p1):
        return False

    visited[p] = visiting.pop(p)
    order[index] = p
    index -= 1
    return True

  for p in projects:
    if p not in visited:
      if not _dfs(p):
        return 'ERROR'

  return order


def _build_adjacency_list(projects, dependencies):
  adjacency_list = dict((p, []) for p in projects)
  for dep, p in dependencies:
    adjacency_list[dep].append(p)
  return adjacency_list
