import unittest


class TestHighlightSymbols(unittest.TestCase):
  def test_given_example(self):
    names = ['Amazon', 'Microsoft', 'Google']
    symbols = ['i', 'Am', 'cro', 'Na', 'le', 'abc']
    self.assertEqual(
      highlight_symbols(names, symbols),
      ['[Am]azon', 'Mi[cro]soft', 'Goog[le]'])

  def test_longest_symbol_wins(self):
    self.assertEqual(highlight_symbols(['aaa'], ['a', 'aa']), ['[aa]a'])

  def test_tie_length_earliest_index_wins(self):
    self.assertEqual(highlight_symbols(['abab'], ['ab', 'ba']), ['[ab]ab'])

  def test_no_symbol_matches_leaves_name_unchanged(self):
    self.assertEqual(highlight_symbols(['Boron'], ['xy', 'qz']), ['Boron'])

  def test_case_sensitive_matching(self):
    self.assertEqual(highlight_symbols(['Amazon'], ['am']), ['Amazon'])

  def test_symbol_at_start(self):
    self.assertEqual(highlight_symbols(['Sodium'], ['So']), ['[So]dium'])

  def test_symbol_at_end(self):
    self.assertEqual(highlight_symbols(['Google'], ['le']), ['Goog[le]'])

  def test_symbol_equals_whole_name(self):
    self.assertEqual(highlight_symbols(['Fe'], ['Fe']), ['[Fe]'])

  def test_empty_names(self):
    self.assertEqual(highlight_symbols([], ['a']), [])

  def test_empty_symbols(self):
    self.assertEqual(highlight_symbols(['Amazon'], []), ['Amazon'])

  def test_first_occurrence_is_wrapped(self):
    self.assertEqual(highlight_symbols(['banana'], ['an']), ['b[an]ana'])


if __name__ == '__main__':
  unittest.main()
