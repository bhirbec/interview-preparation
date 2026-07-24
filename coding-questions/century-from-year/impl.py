# Century From Year
#
# Difficulty: easy
# Tags: #math #implementation
#
# Given a year, return the century it is in. The first century spans from the
# year 1 up to and including the year 100, the second - from the year 101 up to
# and including the year 200, etc.
#
# Example:
#   century_from_year(1905) == 20   # years 1901..2000 are the 20th century
#   century_from_year(1700) == 17   # 1700 is the last year of the 17th century
#   century_from_year(100)  == 1    # year 100 still belongs to the 1st century
#   century_from_year(101)  == 2    # year 101 starts the 2nd century
#
# Idea: century = ceil(year / 100). Since a year that is an exact multiple of
# 100 belongs to the century it ends (not the next one), we can compute this
# with integer arithmetic as (year + 99) // 100, which avoids floating point.
import unittest


def century_from_year(year):
  return (year + 99) // 100


def century_from_year_1(year):
  base = year // 100
  remain = year % 100

  if remain == 0:
    return base
  else:
    return base + 1


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
