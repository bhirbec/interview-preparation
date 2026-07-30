import unittest


class TestRemoveCommonPhrases(unittest.TestCase):
  def test_basic_shared_phrase(self):
    self.assertEqual(
      remove_common_phrases(["i my bye good", "my bye good boy"]),
      ["i", "boy"])

  def test_identical_sentences(self):
    self.assertEqual(
      remove_common_phrases(
        ["hello my name is benoit", "hello my name is benoit"]),
      ["", ""])

  def test_no_common_phrase(self):
    self.assertEqual(
      remove_common_phrases(["one two three", "four five six"]),
      ["one two three", "four five six"])

  def test_short_sentence_never_forms_phrase(self):
    self.assertEqual(remove_common_phrases(["a b", "a b"]), ["a b", "a b"])

  def test_shared_run_must_be_three_words(self):
    # "my bye" is shared but only 2 words long, so nothing is removed.
    self.assertEqual(
      remove_common_phrases(["i my bye", "my bye boy"]),
      ["i my bye", "my bye boy"])

  def test_single_sentence(self):
    # A phrase needs two sentences to be common; one sentence removes nothing.
    self.assertEqual(
      remove_common_phrases(["a b c d e"]), ["a b c d e"])

  def test_empty_input(self):
    self.assertEqual(remove_common_phrases([]), [])

  def test_phrase_in_the_middle(self):
    self.assertEqual(
      remove_common_phrases(["x red green blue y", "red green blue z"]),
      ["x y", "z"])

  def test_three_sentences_pairwise_share(self):
    # "a b c" shared by first two; "d e f" shared by last two.
    self.assertEqual(
      remove_common_phrases(["a b c", "a b c d e f", "d e f"]),
      ["", "", ""])


if __name__ == '__main__':
  unittest.main()
