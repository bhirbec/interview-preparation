import unittest


class TestAllLongestStrings(unittest.TestCase):
  def test_example_one(self):
    self.assertEqual(
        all_longest_strings(["aba", "aa", "ad", "vcd", "aba"]),
        ["aba", "vcd", "aba"],
    )

  def test_example_two(self):
    self.assertEqual(
        all_longest_strings(["abc", "eeee", "abcd", "dcd"]),
        ["eeee", "abcd"],
    )

  def test_two_of_same_max(self):
    self.assertEqual(all_longest_strings(["a", "abc", "cba"]), ["abc", "cba"])

  def test_single_longest(self):
    self.assertEqual(all_longest_strings(["enn", "b"]), ["enn"])

  def test_single_element(self):
    self.assertEqual(all_longest_strings(["hello"]), ["hello"])

  def test_all_same_length(self):
    self.assertEqual(all_longest_strings(["ab", "cd", "ef"]), ["ab", "cd", "ef"])

  def test_order_preserved(self):
    self.assertEqual(
        all_longest_strings(["xx", "y", "zz", "w", "vv"]),
        ["xx", "zz", "vv"],
    )


if __name__ == '__main__':
  unittest.main()
