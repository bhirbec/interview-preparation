from queue import Queue


def exists_path(graph, origin, dest):
  q = Queue()
  q.put(origin)
  visited = {}

  while not q.empty():
    n = q.get()
    if n in visited:
      continue

    if n == dest:
      return True

    for ni in graph[n]:
      q.put(ni)

    visited[n] = True

  return False
