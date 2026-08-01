# Implement a Hash Table with Linear Probing
#
# Build an open-addressing hash table over a fixed-size array of `m` slots.
# Collisions are resolved by linear probing: if the slot a key hashes to is
# taken by a different key, walk forward one slot at a time (wrapping around at
# the end) until a usable slot turns up.
#
# Do not use a Python dict or set anywhere in your storage -- the point of the
# exercise is the probing.
#
# Required API:
#   HashTable(m)      - allocate a table of m slots; ValueError if m <= 0
#   hash(key, m)      - map a key to a slot index in [0, m); must be
#                       deterministic across runs, so do NOT use the built-in
#                       hash() (it is salted per process for strings)
#   add(key, value)   - insert, or overwrite the value if the key is present;
#                       RuntimeError when the table is full and the key is new
#   exists(key)       - True when the key is in the table
#   get(key)          - the value stored for key; KeyError if absent
#   remove(key)       - delete the key; KeyError if absent
#   size()            - number of keys currently stored
#
# The subtle part is remove(): a probe sequence stops at the first never-used
# slot, so blanking a slot in the middle of a chain would hide every key after
# it. Mark removed slots with a tombstone that probing walks past and that a
# later add() is free to reuse.
#
# Examples:
#   t = HashTable(8)
#   t.add('a', 1); t.add('b', 2)
#   t.get('a'), t.exists('b'), t.size()  -> 1, True, 2
#   t.add('a', 99); t.get('a')           -> 99   (update, not a second entry)
#   t.size()                             -> 2
#   t.exists('zz')                       -> False
#   t.remove('a'); t.exists('a')         -> False
#   t.get('a')                           -> raises KeyError


class HashTable:
  def __init__(self, m=16):
    # TODO: implement
    raise NotImplementedError

  def hash(self, key, m):
    # TODO: implement
    raise NotImplementedError

  def add(self, key, value):
    # TODO: implement
    raise NotImplementedError

  def exists(self, key):
    # TODO: implement
    raise NotImplementedError

  def get(self, key):
    # TODO: implement
    raise NotImplementedError

  def remove(self, key):
    # TODO: implement
    raise NotImplementedError

  def size(self):
    # TODO: implement
    raise NotImplementedError
