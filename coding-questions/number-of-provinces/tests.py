import unittest


class TestNumberOfProvinces(unittest.TestCase):
  def test_source_example(self):
    self.assertEqual(number_of_provinces(['1100', '1110', '0110', '0001']), 2)

  def test_identity_all_isolated(self):
    matrix = ['10000', '01000', '00100', '00010', '00001']
    self.assertEqual(number_of_provinces(matrix), 5)

  def test_transitive_chain_is_one_group(self):
    self.assertEqual(number_of_provinces(['110', '111', '011']), 1)

  def test_single_node(self):
    self.assertEqual(number_of_provinces(['1']), 1)

  def test_empty(self):
    self.assertEqual(number_of_provinces([]), 0)

  def test_fully_connected(self):
    self.assertEqual(number_of_provinces(['111', '111', '111']), 1)

  def test_two_separate_pairs(self):
    matrix = ['1100', '1100', '0011', '0011']
    self.assertEqual(number_of_provinces(matrix), 2)

  def test_two_isolated_nodes(self):
    self.assertEqual(number_of_provinces(['10', '01']), 2)

  def test_two_connected_nodes(self):
    self.assertEqual(number_of_provinces(['11', '11']), 1)

  def test_last_node_bridges_two_halves(self):
    # 0-1 linked, 2-3 linked, and 4 links to both 1 and 2 -> all one group
    matrix = [
        '11001',
        '11001',
        '00111',
        '00111',
        '11111',
    ]
    self.assertEqual(number_of_provinces(matrix), 1)

  def test_component_discovered_from_later_index(self):
    # node 0 isolated; nodes 1,2,3 form a component reached only from index 1
    matrix = ['1000', '0110', '0111', '0011']
    self.assertEqual(number_of_provinces(matrix), 2)


if __name__ == '__main__':
  unittest.main()
