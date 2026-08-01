from collections import deque


def bfs_order(graph, start):
  if start not in graph:
    raise KeyError(start)

  order = []
  seen = {start}
  queue = deque([start])
  while queue:
    node = queue.popleft()
    order.append(node)
    for neighbour in graph.get(node, ()):
      # Mark on enqueue, not on dequeue: a node reachable from two nodes on the
      # same level would otherwise be queued twice.
      if neighbour not in seen:
        seen.add(neighbour)
        queue.append(neighbour)
  return order


def bfs_distances(graph, start):
  if start not in graph:
    raise KeyError(start)

  distances = {start: 0}
  queue = deque([start])
  while queue:
    node = queue.popleft()
    for neighbour in graph.get(node, ()):
      if neighbour not in distances:
        distances[neighbour] = distances[node] + 1
        queue.append(neighbour)
  return distances
