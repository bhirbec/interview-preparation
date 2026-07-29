import unittest


class TestPowerSet(unittest.TestCase):
  def test_empty_string(self):
    self.assertEqual(subsets(''), [''])

  def test_single_element(self):
    self.assertEqual(sorted(subsets('a')), ['', 'a'])

  def test_two_elements(self):
    self.assertEqual(sorted(subsets('ab')), sorted(['', 'a', 'ab', 'b']))

  def test_three_elements(self):
    expected = ['', 'a', 'ab', 'abc', 'ac', 'b', 'bc', 'c']
    self.assertEqual(sorted(subsets('abc')), sorted(expected))

  def test_count_is_power_of_two(self):
    for s in ['', 'a', 'ab', 'abcd', 'abcde']:
      self.assertEqual(len(subsets(s)), 2 ** len(s))

  def test_all_subsets_unique(self):
    result = subsets('abcd')
    self.assertEqual(len(result), len(set(result)))

  def test_empty_subset_included(self):
    self.assertIn('', subsets('xyz'))

  def test_full_set_included(self):
    self.assertIn('abc', subsets('abc'))


if __name__ == '__main__':
  unittest.main()
