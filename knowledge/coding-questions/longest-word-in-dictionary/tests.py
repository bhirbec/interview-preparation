import unittest


class TestLongestWord(unittest.TestCase):
  def test_single_chain(self):
    self.assertEqual(longest_word(["w", "wo", "wor", "worl", "world"]),
                     "world")

  def test_tie_breaks_lexicographically(self):
    words = ["a", "banana", "app", "appl", "ap", "apply", "apple"]
    self.assertEqual(longest_word(words), "apple")

  def test_no_buildable_word(self):
    self.assertEqual(longest_word(["abc", "bc"]), "")

  def test_one_character_word_always_qualifies(self):
    # "c" has no proper prefix to look up, so it beats the unbuildable "abc".
    self.assertEqual(longest_word(["abc", "bc", "c"]), "c")

  def test_empty_input(self):
    self.assertEqual(longest_word([]), "")

  def test_single_letters_only(self):
    self.assertEqual(longest_word(["b", "a", "c"]), "a")

  def test_longest_chain_is_not_the_longest_word(self):
    # "zebra" is longer but unbuildable; "ab" builds from "a".
    self.assertEqual(longest_word(["a", "ab", "zebra"]), "ab")

  def test_duplicates_are_harmless(self):
    self.assertEqual(longest_word(["a", "a", "ab", "ab"]), "ab")

  def test_two_independent_chains(self):
    words = ["m", "mo", "moo", "t", "to", "top", "tops"]
    self.assertEqual(longest_word(words), "tops")

  def test_broken_chain_falls_back_to_shorter_prefix(self):
    # "abcd" is missing "abc", so the best buildable word is "ab".
    self.assertEqual(longest_word(["a", "ab", "abcd"]), "ab")


if __name__ == '__main__':
  unittest.main()
