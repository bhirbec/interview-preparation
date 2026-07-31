def bit_strings_by_popcount(k):
  numbers = sorted(range(1 << k), key=lambda x: (bin(x).count('1'), x))
  return [format(x, '0{}b'.format(k)) for x in numbers]
