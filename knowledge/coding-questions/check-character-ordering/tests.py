import unittest


class TestCheckOrdering(unittest.TestCase):
  def test_interleaved_is_false(self):
    self.assertFalse(check_ordering('hello world!', 'hlo!'))

  def test_wrong_relative_order_is_false(self):
    self.assertFalse(check_ordering('hello world!', '!od'))

  def test_correct_prefix_order_is_true(self):
    self.assertTrue(check_ordering('hello world!', 'he!'))

  def test_grouped_blocks_are_true(self):
    self.assertTrue(check_ordering('aaaabbbcccc', 'ac'))

  def test_single_char_ordering_present(self):
    self.assertTrue(check_ordering('abc', 'b'))

  def test_single_char_ordering_absent(self):
    self.assertFalse(check_ordering('abc', 'z'))

  def test_empty_ordering_matches_when_no_wanted_chars(self):
    self.assertTrue(check_ordering('abc', ''))

  def test_all_identical_characters(self):
    self.assertTrue(check_ordering('aaaa', 'a'))

  def test_reversed_order_is_false(self):
    self.assertFalse(check_ordering('abc', 'cb'))

  def test_full_ordering_over_whole_string(self):
    self.assertTrue(check_ordering('abbccc', 'abc'))

  def test_extra_occurrence_breaks_order(self):
    self.assertFalse(check_ordering('abca', 'abc'))


if __name__ == '__main__':
  unittest.main()
