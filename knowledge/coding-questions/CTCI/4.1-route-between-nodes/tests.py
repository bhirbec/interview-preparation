import unittest


class TestExistsPath(unittest.TestCase):
  def setUp(self):
    self.graph = {
        1: [2, 3],
        2: [4, 3],
        3: [],
        4: [1, 5],
        5: [2],
        6: [5],
    }

  def test_path_exists_multi_hop(self):
    self.assertTrue(exists_path(self.graph, 1, 5))

  def test_direct_edge(self):
    self.assertTrue(exists_path(self.graph, 1, 2))

  def test_no_path(self):
    self.assertFalse(exists_path(self.graph, 5, 6))

  def test_node_reaches_itself(self):
    self.assertTrue(exists_path(self.graph, 3, 3))

  def test_cycle_terminates(self):
    # 1 -> 2 -> 3 -> 1 forms a cycle; searching within it must terminate.
    cyclic = {1: [2], 2: [3], 3: [1]}
    self.assertTrue(exists_path(cyclic, 1, 3))
    self.assertTrue(exists_path(cyclic, 3, 2))

  def test_single_node_graph(self):
    self.assertTrue(exists_path({1: []}, 1, 1))
    self.assertFalse(exists_path({1: [], 2: []}, 1, 2))


if __name__ == '__main__':
  unittest.main()
