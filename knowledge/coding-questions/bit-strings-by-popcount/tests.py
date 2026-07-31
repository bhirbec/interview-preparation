import unittest


class TestBitStringsByPopcount(unittest.TestCase):
  def test_k1(self):
    self.assertEqual(bit_strings_by_popcount(1), ['0', '1'])

  def test_k2(self):
    self.assertEqual(bit_strings_by_popcount(2), ['00', '01', '10', '11'])

  def test_k3(self):
    self.assertEqual(
      bit_strings_by_popcount(3),
      ['000', '001', '010', '100', '011', '101', '110', '111'],
    )

  def test_count_is_power_of_two(self):
    for k in range(1, 8):
      self.assertEqual(len(bit_strings_by_popcount(k)), 1 << k)

  def test_all_strings_have_length_k(self):
    for k in range(1, 8):
      self.assertTrue(all(len(s) == k for s in bit_strings_by_popcount(k)))

  def test_starts_all_zero_ends_all_one(self):
    result = bit_strings_by_popcount(5)
    self.assertEqual(result[0], '00000')
    self.assertEqual(result[-1], '11111')

  def test_non_decreasing_popcount(self):
    result = bit_strings_by_popcount(6)
    counts = [s.count('1') for s in result]
    self.assertEqual(counts, sorted(counts))

  def test_value_order_within_group(self):
    # Every string is a permutation-free set: no duplicates, and within a fixed
    # popcount the integer values strictly increase.
    result = bit_strings_by_popcount(4)
    self.assertEqual(len(set(result)), len(result))
    twos = [int(s, 2) for s in result if s.count('1') == 2]
    self.assertEqual(twos, sorted(twos))


if __name__ == '__main__':
  unittest.main()
