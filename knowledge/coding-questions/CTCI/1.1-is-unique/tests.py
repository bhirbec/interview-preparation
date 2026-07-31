import unittest


class TestUniqueChar(unittest.TestCase):
  def test_all_unique(self):
    self.assertTrue(unique_char('abcde'))

  def test_repeated_char(self):
    self.assertFalse(unique_char('hello'))

  def test_empty_string(self):
    self.assertTrue(unique_char(''))

  def test_single_char(self):
    self.assertTrue(unique_char('a'))

  def test_case_sensitive(self):
    self.assertTrue(unique_char('aA'))

  def test_immediate_duplicate(self):
    self.assertFalse(unique_char('aa'))

  def test_too_long_to_be_unique(self):
    self.assertFalse(unique_char('a' * 129))


if __name__ == '__main__':
  unittest.main()
