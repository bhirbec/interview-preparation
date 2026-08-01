class HashTable:
  # Sentinel for a slot whose key was removed. Probing walks past it, but add()
  # may reuse it.
  _DELETED = object()

  def __init__(self, m=16):
    if not isinstance(m, int) or isinstance(m, bool) or m <= 0:
      raise ValueError('table size must be a positive integer')
    self._m = m
    self._slots = [None] * m
    self._count = 0

  def hash(self, key, m):
    # A plain polynomial rolling hash over the key's text, so the layout is
    # reproducible across processes (unlike the built-in salted hash()).
    h = 0
    for character in str(key):
      h = (h * 31 + ord(character)) % m
    return h

  def add(self, key, value):
    first_free = None
    for index in self._probe(key):
      slot = self._slots[index]
      if slot is None:
        target = index if first_free is None else first_free
        self._slots[target] = (key, value)
        self._count += 1
        return
      if slot is self._DELETED:
        if first_free is None:
          first_free = index
        continue
      if slot[0] == key:
        self._slots[index] = (key, value)
        return
    if first_free is not None:
      self._slots[first_free] = (key, value)
      self._count += 1
      return
    raise RuntimeError('hash table is full')

  def exists(self, key):
    return self._find(key) is not None

  def get(self, key):
    index = self._find(key)
    if index is None:
      raise KeyError(key)
    return self._slots[index][1]

  def remove(self, key):
    index = self._find(key)
    if index is None:
      raise KeyError(key)
    self._slots[index] = self._DELETED
    self._count -= 1

  def size(self):
    return self._count

  def _probe(self, key):
    start = self.hash(key, self._m)
    for step in range(self._m):
      yield (start + step) % self._m

  def _find(self, key):
    for index in self._probe(key):
      slot = self._slots[index]
      if slot is None:
        return None
      if slot is not self._DELETED and slot[0] == key:
        return index
    return None
