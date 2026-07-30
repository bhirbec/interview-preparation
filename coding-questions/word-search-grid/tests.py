import unittest


class TestWordSearch(unittest.TestCase):
  def setUp(self):
    self.grid = [['A', 'R', 'I', 'D', 'S'],
                 ['W', 'E', 'R', 'O', 'D'],
                 ['U', 'E', 'F', 'B', 'E'],
                 ['B', 'E', 'R', 'E', 'E']]

  def test_word_found(self):
    self.assertTrue(word_search(self.grid, 'UBER'))

  def test_word_not_found(self):
    self.assertFalse(word_search(self.grid, 'ZZZZ'))

  def test_l_shaped_path(self):
    self.assertTrue(word_search([['A', 'B'], ['C', 'D']], 'ABDC'))

  def test_non_adjacent_letters_fail(self):
    self.assertFalse(word_search([['A', 'B'], ['C', 'D']], 'ABCD'))

  def test_cannot_reuse_cell(self):
    self.assertFalse(word_search([['A', 'B'], ['C', 'D']], 'AA'))

  def test_single_cell_match(self):
    self.assertTrue(word_search([['X']], 'X'))

  def test_single_cell_no_match(self):
    self.assertFalse(word_search([['X']], 'Y'))

  def test_single_letter_word_anywhere(self):
    self.assertTrue(word_search([['A', 'B'], ['C', 'D']], 'D'))

  def test_snake_path_reusing_row(self):
    self.assertTrue(word_search([['A', 'B', 'C', 'E'],
                                 ['S', 'F', 'C', 'S'],
                                 ['A', 'D', 'E', 'E']], 'ABCCED'))

  def test_word_longer_than_grid_cells(self):
    self.assertFalse(word_search([['A', 'B'], ['C', 'D']], 'ABCDE'))

  def test_full_row(self):
    self.assertTrue(word_search([['A', 'B', 'C']], 'ABC'))

  def test_full_column(self):
    self.assertTrue(word_search([['A'], ['B'], ['C']], 'ABC'))


if __name__ == '__main__':
  unittest.main()
