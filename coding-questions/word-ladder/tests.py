import unittest


def _is_valid_ladder(path, begin, end, word_list):
  if not path:
    return False
  if path[0] != begin or path[-1] != end:
    return False
  words = set(word_list)
  for i in range(1, len(path)):
    a, b = path[i - 1], path[i]
    if len(a) != len(b):
      return False
    if sum(1 for x, y in zip(a, b) if x != y) != 1:
      return False
    if path[i] not in words:
      return False
  return True


class TestFindLadder(unittest.TestCase):
  DICT = ["cat", "cot", "dog", "dat", "dot", "dit", "dag"]

  def test_classic_example(self):
    path = find_ladder("cat", "dog", self.DICT)
    self.assertTrue(_is_valid_ladder(path, "cat", "dog", self.DICT))
    self.assertEqual(len(path), 4)  # cat -> _ -> _ -> dog is shortest

  def test_direct_neighbour(self):
    self.assertEqual(find_ladder("hit", "hot", ["hot"]), ["hit", "hot"])

  def test_begin_equals_end(self):
    self.assertEqual(find_ladder("dog", "dog", ["dog"]), ["dog"])

  def test_no_bridge(self):
    self.assertEqual(find_ladder("cat", "dog", ["cat", "dog"]), [])

  def test_target_not_in_dictionary(self):
    self.assertEqual(find_ladder("cat", "dog", ["cat", "dat", "dit"]), [])

  def test_single_char_words(self):
    self.assertEqual(find_ladder("a", "c", ["a", "b", "c"]), ["a", "c"])

  def test_empty_dictionary(self):
    self.assertEqual(find_ladder("cat", "dog", []), [])

  def test_returns_shortest(self):
    # Long detour plus a short hop both exist; BFS must pick the short one.
    words = ["az", "bz", "cz", "ab"]
    path = find_ladder("aa", "ab", words)
    self.assertEqual(path, ["aa", "ab"])


if __name__ == '__main__':
  unittest.main()
