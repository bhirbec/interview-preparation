import unittest


class TestBinaryWildcardCombinations(unittest.TestCase):
  def test_trailing_wildcard(self):
    self.assertEqual(binary_wildcard_combinations('1?'), ['10', '11'])

  def test_wildcard_between_fixed(self):
    self.assertEqual(
        binary_wildcard_combinations('?0?'),
        ['000', '001', '100', '101'],
    )

  def test_no_wildcard_returns_itself(self):
    self.assertEqual(binary_wildcard_combinations('101'), ['101'])

  def test_single_wildcard(self):
    self.assertEqual(binary_wildcard_combinations('?'), ['0', '1'])

  def test_empty_string(self):
    self.assertEqual(binary_wildcard_combinations(''), [''])

  def test_two_wildcards_ascending_order(self):
    self.assertEqual(
        binary_wildcard_combinations('??'),
        ['00', '01', '10', '11'],
    )

  def test_three_wildcards_full_binary_count(self):
    self.assertEqual(
        binary_wildcard_combinations('???'),
        ['000', '001', '010', '011', '100', '101', '110', '111'],
    )

  def test_all_fixed_no_expansion(self):
    self.assertEqual(binary_wildcard_combinations('0010'), ['0010'])

  def test_count_is_two_to_the_k(self):
    s = '10??1??01???'
    out = binary_wildcard_combinations(s)
    self.assertEqual(len(out), 2 ** s.count('?'))
    self.assertEqual(len(set(out)), len(out))  # all distinct

  def test_fixed_positions_are_preserved(self):
    out = binary_wildcard_combinations('1?0?')
    for combo in out:
      self.assertEqual(combo[0], '1')
      self.assertEqual(combo[2], '0')


if __name__ == '__main__':
  unittest.main()
