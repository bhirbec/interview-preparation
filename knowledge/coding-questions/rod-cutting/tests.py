import unittest

CLRS_PRICES = [0, 1, 5, 8, 9, 10, 17, 17, 20]


class TestRodCutting(unittest.TestCase):
  def test_clrs_length_4(self):
    self.assertEqual(rod_cutting(CLRS_PRICES, 4), 10)

  def test_clrs_length_8(self):
    self.assertEqual(rod_cutting(CLRS_PRICES, 8), 22)

  def test_lecture_example(self):
    prices = [0, 2, 7, 10, 12, 13, 16, 17, 18, 23]
    self.assertEqual(rod_cutting(prices, 9), 31)

  def test_zero_length(self):
    self.assertEqual(rod_cutting(CLRS_PRICES, 0), 0)

  def test_length_one_cannot_cut(self):
    self.assertEqual(rod_cutting(CLRS_PRICES, 1), 1)

  def test_no_cut_is_best(self):
    # Whole rod is worth more than any combination of pieces.
    self.assertEqual(rod_cutting([0, 1, 10], 2), 10)

  def test_cutting_beats_whole(self):
    # Two unit pieces beat the intact rod.
    self.assertEqual(rod_cutting([0, 5, 1], 2), 10)

  def test_all_unit_cuts(self):
    self.assertEqual(rod_cutting([0, 3, 3, 3], 3), 9)


if __name__ == '__main__':
  unittest.main()
