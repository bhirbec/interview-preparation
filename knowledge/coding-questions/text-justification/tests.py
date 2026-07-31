import unittest


def total_badness(lines, width):
  return sum((width - len(line)) ** 3 for line in lines)


class TestJustify(unittest.TestCase):
  def check(self, words, width, optimal_cost):
    lines = justify(words, width)
    # The layout must be the words, in order, joined by single spaces.
    self.assertEqual(" ".join(lines).split(" "), words)
    for line in lines:
      self.assertLessEqual(len(line), width, msg='line too long: %r' % line)
    self.assertEqual(total_badness(lines, width), optimal_cost)

  def test_two_words_fit_exactly(self):
    self.assertEqual(justify(["ab", "cd"], 5), ["ab cd"])

  def test_single_word(self):
    self.assertEqual(justify(["hello"], 10), ["hello"])
    self.check(["hello"], 10, 125)

  def test_small_split(self):
    self.check(["aaa", "bb", "cc", "ddddd"], 6, 29)

  def test_greedy_is_suboptimal(self):
    # Greedy packs "The quick brown" style lines and pays for it later; the
    # optimal layout spreads the slack. Cost checked against a reference DP.
    words = ["The", "quick", "brown", "fox", "jumps", "over", "the",
             "lazy", "dog"]
    self.check(words, 13, 156)

  def test_each_word_alone_when_width_is_tight(self):
    self.check(["aa", "bb", "cc"], 2, 0)

  def test_word_exactly_width(self):
    self.check(["abcdef"], 6, 0)


if __name__ == '__main__':
  unittest.main()
