# Google interview onsite 02/11/2019

# Given a JSON data structure return the data for a given path (see
# unittest for example) - Follow up: what if the path contains '*' that
# matches any segment.

import unittest


def find(root, path):
  def _f(node, i):
    next_framents = []
    fragment = fragments[i]

    if fragment == '*':
      if isinstance(node, list):
        next_framents = list(range(len(node)))
      else:
        next_framents = node.keys()
    elif isinstance(node, list):
      next_framents = [int(fragment)]
    else:
      next_framents = [fragment]

    for fragment in next_framents:
      try:
        next_node = node[fragment]
      except (IndexError, KeyError):
        continue

      if i == n-1:
        output.append(next_node)
      else:
        _f(next_node, i+1)

  output = []
  fragments = path.split('.')
  n = len(fragments)
  _f(root, 0)
  return output


class TestFind(unittest.TestCase):
  DATA = {
    "books": {
      "novels": [{
          "title": "The Lord of the Rings",
          "author": "Tolkien",
        }, {
          "title": "The Hobbit",
          "author": "Tolkien",
        }
      ],
      "fictions": [{
          "title": "Dune",
          "author": "Frank Herbert"
        }, {
          "title": "The Martian Chronicles",
          "author": "Ray Bradbury",
        }
      ]
    }
  }

  def test_find_leaf(self):
    res = find(self.DATA, 'books.novels.0.author')
    self.assertTrue(res[0] == "Tolkien")

  def test_find_subtree(self):
    res = find(self.DATA, 'books.novels')
    self.assertTrue(res[0] == self.DATA['books']['novels'])

  def test_find_wildcard(self):
    res = find(self.DATA, 'books.novels.*.author')
    self.assertTrue(res == ["Tolkien", "Tolkien"])

    res = find(self.DATA, 'books.novels.0.*')
    self.assertTrue(res == ["The Lord of the Rings", "Tolkien"])

    # For this case the interviewer asked to put the result in list of list
    # like such (but I was out of time):
    # [
    #   ["The Lord of the Rings", "Dune"],
    #   ["Tolkien", , "Frank Herbert"],
    # ]
    res = find(self.DATA, 'books.*.0.*')
    self.assertTrue(res == ["The Lord of the Rings", "Tolkien", "Dune", "Frank Herbert"])

  def test_not_found(self):
    res = find(self.DATA, 'books.novels.2.author')
    self.assertTrue(res == [])

    res = find(self.DATA, 'books.science-fiction')
    self.assertTrue(res == [])


if __name__ == '__main__':
  unittest.main()
