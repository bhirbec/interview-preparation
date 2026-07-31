import unittest


class TestLRUCache(unittest.TestCase):
  def test_get_missing_returns_minus_one(self):
    c = LRUCache(2)
    self.assertEqual(c.get(1), -1)

  def test_put_then_get(self):
    c = LRUCache(2)
    c.put(1, 10)
    self.assertEqual(c.get(1), 10)

  def test_update_existing_key(self):
    c = LRUCache(2)
    c.put(1, 1)
    c.put(1, 100)
    self.assertEqual(c.get(1), 100)

  def test_eviction_of_least_recently_used(self):
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    self.assertEqual(c.get(1), 1)   # 1 becomes most recent
    c.put(3, 3)                     # evicts key 2
    self.assertEqual(c.get(2), -1)
    c.put(4, 4)                     # evicts key 1
    self.assertEqual(c.get(1), -1)
    self.assertEqual(c.get(3), 3)
    self.assertEqual(c.get(4), 4)

  def test_get_counts_as_use(self):
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.get(1)          # touch 1 so 2 is now least recently used
    c.put(3, 3)       # evicts 2
    self.assertEqual(c.get(2), -1)
    self.assertEqual(c.get(1), 1)

  def test_update_counts_as_use(self):
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 11)      # updating 1 also refreshes recency
    c.put(3, 3)       # evicts 2, not 1
    self.assertEqual(c.get(2), -1)
    self.assertEqual(c.get(1), 11)

  def test_capacity_one(self):
    c = LRUCache(1)
    c.put(1, 1)
    self.assertEqual(c.get(1), 1)
    c.put(2, 2)       # evicts 1
    self.assertEqual(c.get(1), -1)
    self.assertEqual(c.get(2), 2)

  def test_repeated_access_pattern(self):
    c = LRUCache(3)
    c.put(1, 1)
    c.put(2, 2)
    c.put(3, 3)
    self.assertEqual(c.get(1), 1)
    self.assertEqual(c.get(2), 2)
    self.assertEqual(c.get(3), 3)
    c.put(4, 4)       # evicts 1 (least recently used)
    self.assertEqual(c.get(1), -1)
    self.assertEqual(c.get(4), 4)


if __name__ == '__main__':
  unittest.main()
