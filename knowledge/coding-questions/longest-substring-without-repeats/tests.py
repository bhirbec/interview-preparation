import unittest


class TestLongestUniqueSubstringLength(unittest.TestCase):
  def test_example(self):
    self.assertEqual(longest_unique_substring_length("abcabcbb"), 3)

  def test_all_same_character(self):
    self.assertEqual(longest_unique_substring_length("bbbbb"), 1)

  def test_substring_not_subsequence(self):
    self.assertEqual(longest_unique_substring_length("pwwkew"), 3)

  def test_empty(self):
    self.assertEqual(longest_unique_substring_length(""), 0)

  def test_single_character(self):
    self.assertEqual(longest_unique_substring_length("z"), 1)

  def test_all_distinct(self):
    self.assertEqual(longest_unique_substring_length("abcdef"), 6)

  def test_best_window_at_the_end(self):
    self.assertEqual(longest_unique_substring_length("aabcd"), 4)

  def test_repeat_before_window_does_not_shrink(self):
    # After "ab" repeats, window restarts; the earlier 'a' must not clamp it.
    self.assertEqual(longest_unique_substring_length("abba"), 2)
    self.assertEqual(longest_unique_substring_length("tmmzuxt"), 5)

  def test_spaces_and_symbols_count_as_characters(self):
    self.assertEqual(longest_unique_substring_length("a b!c"), 5)
    self.assertEqual(longest_unique_substring_length("ab ab"), 3)

  def test_digits_and_letters(self):
    self.assertEqual(longest_unique_substring_length("a1b2a1"), 4)


if __name__ == '__main__':
  unittest.main()
