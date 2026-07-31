import unittest


class TestSearch(unittest.TestCase):
  def setUp(self):
    self.arr = ['at', '', '', '', 'ball', '', '', 'car', '', '', 'dad', '', '']

  def test_search_middle(self):
    self.assertEqual(binary_search(self.arr, 'ball'), 4)

  def test_search_start(self):
    self.assertEqual(binary_search(self.arr, 'at'), 0)

  def test_search_end(self):
    self.assertEqual(binary_search(self.arr, 'dad'), 10)

  def test_not_found(self):
    self.assertIsNone(binary_search(self.arr, 'xxx'))

  def test_empty_array(self):
    self.assertIsNone(binary_search([], 'xxx'))

  def test_all_empty_strings(self):
    self.assertIsNone(binary_search(['', '', '', '', '', '', ''], 'xxx'))

  def test_single_target_among_empties(self):
    self.assertEqual(binary_search(['', '', '', 'a', '', '', ''], 'a'), 3)

  def test_correctness_over_many_runs(self):
    # The probe is random, so exercise it repeatedly: present values must be
    # located, absent values must return None, every time.
    present = {'at', 'ball', 'car', 'dad'}
    for _ in range(500):
      for v in ['at', 'ball', 'car', 'dad', 'xxx', 'aaa', 'zzz']:
        r = binary_search(self.arr, v)
        if v in present:
          assert r is not None
          self.assertEqual(self.arr[r], v)
        else:
          self.assertIsNone(r)


if __name__ == '__main__':
  unittest.main()
