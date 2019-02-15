# https://www.youtube.com/watch?v=2E7MmKv0Y24
import heapq


def shortest_path(V, E, src, dest):
  # Running time: O(n.log(n) + e)
  h = []
  heapq.heappush(h, (0, src))
  distances = {src: 0}

  while h:
    dist_u, u = heapq.heappop(h)
    if u == dest:
      path = reconstruct_path(src, dest, E, distances)
      return path, dist_u

    for v, w in E.get(u, {}).items():
      dist_v = dist_u + w
      if v not in distances:
        distances[v] = dist_v
        heapq.heappush(h, (dist_v, v))
      else:
        min_dist_v = distances[v] + w
        if dist_v < min_dist_v:
          distances[v] = dist_v

  return -1


def reconstruct_path(src, dest, E, distances):
  REV_E = {}
  for u, edges in E.items():
    for v, w in edges.items():
      REV_E.setdefault(v, {})[u] = w

  u = dest
  path = [u]

  while u != src:
    min_dist_v = None
    next_u = None

    for v, _ in REV_E.get(u, {}).items():
      dist_v = distances.get(v)
      if dist_v is None:
        continue
      elif min_dist_v is None:
        min_dist_v = dist_v
        next_u = v
      elif dist_v < min_dist_v:
        min_dist_v = dist_v
        next_u = v

    u = next_u
    path.append(u)

  return list(reversed(path))


def main():
  V = ["a", "b", "c", "d", "e", "f"]

  E = {
    "a": {"b": 7, "c": 9, "f": 14},
    "b": {"c": 10, "d": 15},
    "c": {"d": 11, "f": 2},
    "d": {"e": 6},
    "e": {"f": 9}
  }

  print(shortest_path(V, E, "a", "e"))


main()
