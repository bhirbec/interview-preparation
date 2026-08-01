import unittest


class TestUnionFind(unittest.TestCase):
  def test_starts_as_singletons(self):
    uf = UnionFind(5)
    self.assertEqual(uf.count(), 5)
    for x in range(5):
      self.assertEqual(uf.find(x), x)
      self.assertEqual(uf.size(x), 1)
    self.assertFalse(uf.connected(0, 1))

  def test_union_merges(self):
    uf = UnionFind(5)
    self.assertTrue(uf.union(0, 1))
    self.assertTrue(uf.connected(0, 1))
    self.assertEqual(uf.count(), 4)
    self.assertEqual(uf.size(0), 2)
    self.assertEqual(uf.size(1), 2)

  def test_union_of_already_connected_is_a_noop(self):
    uf = UnionFind(3)
    self.assertTrue(uf.union(0, 1))
    self.assertFalse(uf.union(1, 0))
    self.assertFalse(uf.union(0, 0))
    self.assertEqual(uf.count(), 2)
    self.assertEqual(uf.size(0), 2)

  def test_transitive_connection(self):
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(2, 3)
    self.assertFalse(uf.connected(0, 3))
    uf.union(1, 2)
    self.assertTrue(uf.connected(0, 3))
    self.assertEqual(uf.count(), 2)
    self.assertEqual(uf.size(3), 4)
    self.assertEqual(uf.size(4), 1)

  def test_representative_is_shared(self):
    uf = UnionFind(4)
    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(0, 2)
    roots = {uf.find(x) for x in range(4)}
    self.assertEqual(len(roots), 1)

  def test_merging_everything(self):
    uf = UnionFind(10)
    for x in range(9):
      self.assertTrue(uf.union(x, x + 1))
    self.assertEqual(uf.count(), 1)
    self.assertEqual(uf.size(0), 10)
    for x in range(10):
      self.assertTrue(uf.connected(0, x))

  def test_long_chain_stays_answerable(self):
    # Unioning in order is the worst case for a naive implementation; with
    # union by rank plus path compression it stays flat.
    uf = UnionFind(20000)
    for x in range(19999):
      uf.union(x, x + 1)
    self.assertTrue(uf.connected(0, 19999))
    self.assertEqual(uf.size(12345), 20000)
    self.assertEqual(uf.count(), 1)

  def test_disjoint_groups(self):
    uf = UnionFind(6)
    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(4, 5)
    self.assertEqual(uf.count(), 3)
    self.assertFalse(uf.connected(1, 2))
    self.assertFalse(uf.connected(3, 4))
    self.assertTrue(uf.connected(4, 5))

  def test_out_of_range_element(self):
    uf = UnionFind(3)
    with self.assertRaises(IndexError):
      uf.find(3)
    with self.assertRaises(IndexError):
      uf.find(-1)
    with self.assertRaises(IndexError):
      uf.union(0, 7)

  def test_single_element(self):
    uf = UnionFind(1)
    self.assertEqual(uf.count(), 1)
    self.assertEqual(uf.find(0), 0)
    self.assertTrue(uf.connected(0, 0))

  def test_empty_universe(self):
    uf = UnionFind(0)
    self.assertEqual(uf.count(), 0)
    with self.assertRaises(IndexError):
      uf.find(0)

  def test_negative_size(self):
    with self.assertRaises(ValueError):
      UnionFind(-1)


if __name__ == '__main__':
  unittest.main()
