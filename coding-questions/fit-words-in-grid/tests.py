import unittest


class TestCountWords(unittest.TestCase):
  def test_careercup_example(self):
    self.assertEqual(count_words(["Do", "Run"], 2, 9), 5)

  def test_single_char_word_per_row(self):
    self.assertEqual(count_words(["a"], 3, 1), 3)

  def test_only_first_word_fits(self):
    self.assertEqual(count_words(["ab", "cd"], 1, 2), 1)

  def test_word_never_fits(self):
    self.assertEqual(count_words(["hello"], 2, 3), 0)

  def test_single_row(self):
    self.assertEqual(count_words(["Do", "Run"], 1, 9), 3)

  def test_exact_fit_no_trailing_space(self):
    # "abc" fills a width-3 row exactly, one word per row.
    self.assertEqual(count_words(["abc"], 4, 3), 4)

  def test_empty_words(self):
    self.assertEqual(count_words([], 5, 10), 0)


if __name__ == '__main__':
  unittest.main()
