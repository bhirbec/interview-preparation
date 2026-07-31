import unittest


class TestPermOfPalindrome(unittest.TestCase):
  def test_ok(self):
    self.assertTrue(check_perm_of_palindrome('Tact Coa'))

  def test_empty_string(self):
    self.assertTrue(check_perm_of_palindrome(''))

  def test_single_char(self):
    self.assertTrue(check_perm_of_palindrome('a'))

  def test_even_counts(self):
    self.assertTrue(check_perm_of_palindrome('aabb'))

  def test_one_odd_count(self):
    self.assertTrue(check_perm_of_palindrome('aab'))

  def test_multiple_odd_counts(self):
    self.assertFalse(check_perm_of_palindrome('abc'))

  def test_case_insensitive(self):
    self.assertTrue(check_perm_of_palindrome('AaBb'))

  def test_spaces_ignored(self):
    self.assertTrue(check_perm_of_palindrome('a a'))


if __name__ == '__main__':
  unittest.main()
