import unittest


class TestFind(unittest.TestCase):
  DATA = {
    "books": {
      "novels": [
        {"title": "The Lord of the Rings", "author": "Tolkien"},
        {"title": "The Hobbit", "author": "Tolkien"},
      ],
      "fictions": [
        {"title": "Dune", "author": "Frank Herbert"},
        {"title": "The Martian Chronicles", "author": "Ray Bradbury"},
      ],
    }
  }

  def test_find_leaf(self):
    self.assertEqual(find(self.DATA, 'books.novels.0.author'), ["Tolkien"])

  def test_find_subtree(self):
    self.assertEqual(find(self.DATA, 'books.novels'),
                     [self.DATA['books']['novels']])

  def test_wildcard_over_list(self):
    self.assertEqual(find(self.DATA, 'books.novels.*.author'),
                     ["Tolkien", "Tolkien"])

  def test_wildcard_over_dict(self):
    self.assertEqual(find(self.DATA, 'books.novels.0.*'),
                     ["The Lord of the Rings", "Tolkien"])

  def test_multiple_wildcards(self):
    self.assertEqual(find(self.DATA, 'books.*.0.*'),
                     ["The Lord of the Rings", "Tolkien",
                      "Dune", "Frank Herbert"])

  def test_index_out_of_range(self):
    self.assertEqual(find(self.DATA, 'books.novels.2.author'), [])

  def test_missing_key(self):
    self.assertEqual(find(self.DATA, 'books.science-fiction'), [])

  def test_single_segment_root_dict(self):
    self.assertEqual(find({"a": 1, "b": 2}, 'a'), [1])


if __name__ == '__main__':
  unittest.main()
