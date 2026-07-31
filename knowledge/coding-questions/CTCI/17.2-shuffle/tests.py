import unittest


class TestShuffle(unittest.TestCase):
  def test_empty(self):
    self.assertEqual(shuffle(0), [])

  def test_single(self):
    self.assertEqual(shuffle(1), [1])

  def test_is_permutation(self):
    for n in [2, 5, 10, 52]:
      for _ in range(50):
        result = shuffle(n)
        self.assertEqual(len(result), n)
        self.assertEqual(sorted(result), list(range(1, n + 1)))

  def test_no_duplicates(self):
    result = shuffle(52)
    self.assertEqual(len(set(result)), 52)

  def test_covers_multiple_orderings(self):
    # Over many runs the shuffle should not always yield the same ordering.
    seen = {tuple(shuffle(5)) for _ in range(200)}
    self.assertGreater(len(seen), 1)


if __name__ == '__main__':
  unittest.main()
