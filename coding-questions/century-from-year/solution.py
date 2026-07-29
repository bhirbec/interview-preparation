def century_from_year(year):
  return (year + 99) // 100


def century_from_year_1(year):
  base = year // 100
  remain = year % 100

  if remain == 0:
    return base
  else:
    return base + 1
