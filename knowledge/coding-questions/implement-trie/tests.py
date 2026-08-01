import unittest


class TestTrie(unittest.TestCase):
  def test_example(self):
    t = Trie()
    t.insert("apple")
    self.assertTrue(t.search("apple"))
    self.assertFalse(t.search("app"))
    self.assertTrue(t.starts_with("app"))
    t.insert("app")
    self.assertTrue(t.search("app"))

  def test_empty_trie(self):
    t = Trie()
    self.assertFalse(t.search("a"))
    self.assertFalse(t.starts_with("a"))

  def test_word_is_prefix_of_itself(self):
    t = Trie()
    t.insert("car")
    self.assertTrue(t.starts_with("car"))

  def test_longer_query_than_inserted_word(self):
    t = Trie()
    t.insert("car")
    self.assertFalse(t.search("cars"))
    self.assertFalse(t.starts_with("cars"))

  def test_single_character_word(self):
    t = Trie()
    t.insert("a")
    self.assertTrue(t.search("a"))
    self.assertTrue(t.starts_with("a"))

  def test_shared_prefixes_stay_distinct(self):
    t = Trie()
    t.insert("cat")
    t.insert("cab")
    self.assertTrue(t.search("cat"))
    self.assertTrue(t.search("cab"))
    self.assertFalse(t.search("ca"))
    self.assertTrue(t.starts_with("ca"))

  def test_duplicate_insert_is_harmless(self):
    t = Trie()
    t.insert("dog")
    t.insert("dog")
    self.assertTrue(t.search("dog"))

  def test_no_false_positive_on_sibling_branch(self):
    t = Trie()
    t.insert("bat")
    self.assertFalse(t.search("bar"))
    self.assertFalse(t.starts_with("bo"))


if __name__ == '__main__':
  unittest.main()
