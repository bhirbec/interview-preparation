# Century From Year
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


def century_from_year(year):
  # TODO: implement
  raise NotImplementedError
