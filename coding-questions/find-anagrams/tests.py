import unittest


class TestFindAnagrams(unittest.TestCase):
  def test_example(self):
    words = ["tea", "ate", "eat", "apple", "java", "vaja", "cut", "utc"]
    self.assertEqual(
        find_anagrams(words),
        ["tea", "ate", "eat", "java", "vaja", "cut", "utc"])

  def test_empty(self):
    self.assertEqual(find_anagrams([]), [])

  def test_single_word(self):
    self.assertEqual(find_anagrams(["hello"]), [])

  def test_no_anagrams(self):
    self.assertEqual(find_anagrams(["abc", "def", "ghi"]), [])

  def test_all_anagrams(self):
    self.assertEqual(find_anagrams(["abc", "bca", "cab"]),
                     ["abc", "bca", "cab"])

  def test_duplicates_kept(self):
    self.assertEqual(find_anagrams(["ab", "ba", "ab"]), ["ab", "ba", "ab"])

  def test_identical_word_is_anagram_of_itself(self):
    # Two copies of the same word are anagrams and both qualify.
    self.assertEqual(find_anagrams(["xy", "xy"]), ["xy", "xy"])

  def test_order_preserved_with_lone_word_dropped(self):
    self.assertEqual(find_anagrams(["cat", "dog", "act"]), ["cat", "act"])


if __name__ == '__main__':
  unittest.main()
