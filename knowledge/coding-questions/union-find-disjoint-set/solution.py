class UnionFind:
  def __init__(self, n):
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
      raise ValueError('n must be a non-negative integer')
    self._parent = list(range(n))
    self._rank = [0] * n
    self._set_size = [1] * n
    self._count = n

  def find(self, x):
    if not isinstance(x, int) or isinstance(x, bool) or x < 0 or x >= len(self._parent):
      raise IndexError('element out of range: %r' % (x,))
    # Walk to the root, then re-point everything on the path straight at it.
    root = x
    while self._parent[root] != root:
      root = self._parent[root]
    while self._parent[x] != root:
      self._parent[x], x = root, self._parent[x]
    return root

  def union(self, x, y):
    root_x = self.find(x)
    root_y = self.find(y)
    if root_x == root_y:
      return False
    # Union by rank: the shallower tree hangs under the deeper one, so the
    # combined depth only grows when the two are equally deep.
    if self._rank[root_x] < self._rank[root_y]:
      root_x, root_y = root_y, root_x
    self._parent[root_y] = root_x
    self._set_size[root_x] += self._set_size[root_y]
    if self._rank[root_x] == self._rank[root_y]:
      self._rank[root_x] += 1
    self._count -= 1
    return True

  def connected(self, x, y):
    return self.find(x) == self.find(y)

  def count(self):
    return self._count

  def size(self, x):
    return self._set_size[self.find(x)]
