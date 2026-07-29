import unittest


class TestCenturyFromYear(unittest.TestCase):
  def test_examples(self):
    self.assertEqual(century_from_year(1905), 20)
    self.assertEqual(century_from_year(1700), 17)

  def test_century_boundaries(self):
    # A year that is a multiple of 100 is the LAST year of its century.
    self.assertEqual(century_from_year(100), 1)
    self.assertEqual(century_from_year(200), 2)
    self.assertEqual(century_from_year(2000), 20)
    # The next year starts a new century.
    self.assertEqual(century_from_year(101), 2)
    self.assertEqual(century_from_year(201), 3)
    self.assertEqual(century_from_year(2001), 21)

  def test_smallest_years(self):
    self.assertEqual(century_from_year(1), 1)
    self.assertEqual(century_from_year(99), 1)


if __name__ == '__main__':
  unittest.main()
