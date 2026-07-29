import unittest


class TestInsertBits(unittest.TestCase):
  def test_canonical_example(self):
    self.assertEqual(insert_bits(n=0b10000000000, m=0b10011, i=2, j=6), 0b10001001100)

  def test_second_example(self):
    self.assertEqual(insert_bits(n=161, m=5, i=2, j=4), 181)

  def test_insert_into_zero(self):
    self.assertEqual(insert_bits(n=0, m=0b111, i=0, j=2), 7)

  def test_clears_existing_bits(self):
    self.assertEqual(insert_bits(n=0b11111111, m=0, i=2, j=4), 0b11100011)

  def test_single_bit_window(self):
    self.assertEqual(insert_bits(n=0b0000, m=1, i=1, j=1), 0b0010)


if __name__ == '__main__':
  unittest.main()
