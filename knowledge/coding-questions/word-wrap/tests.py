import unittest


class TestWordWrap(unittest.TestCase):
  def test_all_words_fit_on_one_line(self):
    self.assertEqual(word_wrap('a b c', 5), ['a b c'])

  def test_exact_fit_wraps_after_full_line(self):
    self.assertEqual(word_wrap('a b c', 3), ['a b', 'c'])

  def test_each_word_on_its_own_line(self):
    self.assertEqual(word_wrap('aaa bbb ccc', 3), ['aaa', 'bbb', 'ccc'])

  def test_greedy_packing(self):
    self.assertEqual(word_wrap('the quick brown fox', 9),
                     ['the quick', 'brown fox'])

  def test_single_word(self):
    self.assertEqual(word_wrap('hello', 10), ['hello'])

  def test_single_word_exact_width(self):
    self.assertEqual(word_wrap('hello', 5), ['hello'])

  def test_empty_text(self):
    self.assertEqual(word_wrap('', 5), [])

  def test_word_plus_space_exceeds_width(self):
    # "ab" fits (2), adding " cd" would be 5 > 4, so "cd" starts a new line.
    self.assertEqual(word_wrap('ab cd', 4), ['ab', 'cd'])

  def test_width_one_forces_single_char_words(self):
    self.assertEqual(word_wrap('a b c', 1), ['a', 'b', 'c'])

  def test_mixed_lengths(self):
    self.assertEqual(word_wrap('I am a very tired coder', 6),
                     ['I am a', 'very', 'tired', 'coder'])


if __name__ == '__main__':
  unittest.main()
