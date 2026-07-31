import unittest


class TestValidBraces(unittest.TestCase):
  def test_long_balanced(self):
    self.assertTrue(valid_braces("{[]{}[{{{}}}]{{}}}"))

  def test_simple_pair(self):
    self.assertTrue(valid_braces("()"))

  def test_empty_string(self):
    self.assertTrue(valid_braces(""))

  def test_all_three_types_nested(self):
    self.assertTrue(valid_braces("{[()]}"))

  def test_mismatched_types(self):
    self.assertFalse(valid_braces("(]"))

  def test_wrong_nesting_order(self):
    self.assertFalse(valid_braces("([)]"))

  def test_unclosed_openers(self):
    self.assertFalse(valid_braces("((("))

  def test_closer_before_opener(self):
    self.assertFalse(valid_braces(")("))

  def test_single_closer(self):
    self.assertFalse(valid_braces("]"))

  def test_single_opener(self):
    self.assertFalse(valid_braces("{"))

  def test_extra_closer_after_balanced(self):
    self.assertFalse(valid_braces("()]"))


if __name__ == '__main__':
  unittest.main()
