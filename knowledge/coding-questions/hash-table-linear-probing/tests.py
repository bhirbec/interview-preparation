import unittest


class TestHashTable(unittest.TestCase):
  def test_starts_empty(self):
    t = HashTable(8)
    self.assertEqual(t.size(), 0)
    self.assertFalse(t.exists('anything'))

  def test_add_and_get(self):
    t = HashTable(8)
    t.add('a', 1)
    t.add('b', 2)
    self.assertEqual(t.get('a'), 1)
    self.assertEqual(t.get('b'), 2)
    self.assertEqual(t.size(), 2)

  def test_add_existing_key_updates_in_place(self):
    t = HashTable(8)
    t.add('a', 1)
    t.add('a', 99)
    self.assertEqual(t.get('a'), 99)
    self.assertEqual(t.size(), 1)

  def test_get_missing_key_raises(self):
    t = HashTable(8)
    with self.assertRaises(KeyError):
      t.get('nope')

  def test_remove(self):
    t = HashTable(8)
    t.add('a', 1)
    t.remove('a')
    self.assertFalse(t.exists('a'))
    self.assertEqual(t.size(), 0)
    with self.assertRaises(KeyError):
      t.get('a')

  def test_remove_missing_key_raises(self):
    t = HashTable(8)
    with self.assertRaises(KeyError):
      t.remove('nope')

  def test_hash_is_in_range_and_deterministic(self):
    t = HashTable(8)
    for key in ['a', 'zebra', '', 42, 'a longer key with spaces']:
      index = t.hash(key, 8)
      self.assertIsInstance(index, int)
      self.assertGreaterEqual(index, 0)
      self.assertLess(index, 8)
      self.assertEqual(index, t.hash(key, 8))

  def test_colliding_keys_both_survive(self):
    t = HashTable(4)
    # 'a' and 'e' land on the same slot in a table of 4 under any reasonable
    # character-sum hash; whatever the hash, both keys must remain reachable.
    t.add('a', 1)
    t.add('e', 2)
    t.add('i', 3)
    self.assertEqual(t.get('a'), 1)
    self.assertEqual(t.get('e'), 2)
    self.assertEqual(t.get('i'), 3)
    self.assertEqual(t.size(), 3)

  def test_removal_does_not_hide_later_keys_in_a_chain(self):
    t = HashTable(4)
    t.add('a', 1)
    t.add('e', 2)
    t.add('i', 3)
    t.remove('e')
    self.assertFalse(t.exists('e'))
    self.assertEqual(t.get('a'), 1)
    self.assertEqual(t.get('i'), 3)

  def test_tombstone_is_reusable(self):
    t = HashTable(4)
    for key in ['a', 'b', 'c', 'd']:
      t.add(key, key.upper())
    t.remove('b')
    t.add('z', 'Z')
    self.assertEqual(t.size(), 4)
    self.assertEqual(t.get('z'), 'Z')
    self.assertEqual(t.get('a'), 'A')
    self.assertEqual(t.get('c'), 'C')
    self.assertEqual(t.get('d'), 'D')

  def test_full_table_rejects_a_new_key(self):
    t = HashTable(2)
    t.add('a', 1)
    t.add('b', 2)
    with self.assertRaises(RuntimeError):
      t.add('c', 3)
    # An update of an existing key still works on a full table.
    t.add('a', 11)
    self.assertEqual(t.get('a'), 11)

  def test_many_keys(self):
    t = HashTable(64)
    for i in range(50):
      t.add('key-%d' % i, i * i)
    self.assertEqual(t.size(), 50)
    for i in range(50):
      self.assertEqual(t.get('key-%d' % i), i * i)
    for i in range(0, 50, 2):
      t.remove('key-%d' % i)
    self.assertEqual(t.size(), 25)
    for i in range(50):
      self.assertEqual(t.exists('key-%d' % i), i % 2 == 1)

  def test_non_string_keys(self):
    t = HashTable(8)
    t.add(1, 'one')
    t.add(2, 'two')
    self.assertEqual(t.get(1), 'one')
    self.assertEqual(t.get(2), 'two')

  def test_invalid_table_size(self):
    with self.assertRaises(ValueError):
      HashTable(0)
    with self.assertRaises(ValueError):
      HashTable(-4)


if __name__ == '__main__':
  unittest.main()
