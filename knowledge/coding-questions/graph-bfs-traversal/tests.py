import unittest


DIAMOND = {'a': ['b', 'c'], 'b': ['d'], 'c': ['d'], 'd': [], 'e': ['a']}


class TestBfsOrder(unittest.TestCase):
  def test_example(self):
    self.assertEqual(bfs_order(DIAMOND, 'a'), ['a', 'b', 'c', 'd'])

  def test_single_node(self):
    self.assertEqual(bfs_order({'a': []}, 'a'), ['a'])

  def test_isolated_start(self):
    self.assertEqual(bfs_order(DIAMOND, 'd'), ['d'])

  def test_unreachable_nodes_are_omitted(self):
    self.assertNotIn('e', bfs_order(DIAMOND, 'a'))

  def test_visits_level_by_level(self):
    graph = {
      1: [2, 3],
      2: [4],
      3: [5],
      4: [6],
      5: [6],
      6: [],
    }
    self.assertEqual(bfs_order(graph, 1), [1, 2, 3, 4, 5, 6])

  def test_neighbour_order_within_a_level_is_preserved(self):
    graph = {'a': ['c', 'b'], 'b': [], 'c': []}
    self.assertEqual(bfs_order(graph, 'a'), ['a', 'c', 'b'])

  def test_cycle_terminates(self):
    self.assertEqual(bfs_order({1: [2], 2: [3], 3: [1]}, 1), [1, 2, 3])

  def test_self_loop(self):
    self.assertEqual(bfs_order({'a': ['a', 'b'], 'b': []}, 'a'), ['a', 'b'])

  def test_node_reachable_twice_appears_once(self):
    graph = {'a': ['b', 'c'], 'b': ['c'], 'c': []}
    self.assertEqual(bfs_order(graph, 'a'), ['a', 'b', 'c'])

  def test_neighbour_missing_as_a_key(self):
    self.assertEqual(bfs_order({'a': ['b']}, 'a'), ['a', 'b'])

  def test_unknown_start_raises(self):
    with self.assertRaises(KeyError):
      bfs_order(DIAMOND, 'z')

  def test_undirected_graph(self):
    graph = {
      'a': ['b', 'c'],
      'b': ['a', 'd'],
      'c': ['a'],
      'd': ['b'],
    }
    self.assertEqual(bfs_order(graph, 'a'), ['a', 'b', 'c', 'd'])
    self.assertEqual(bfs_order(graph, 'd'), ['d', 'b', 'a', 'c'])


class TestBfsDistances(unittest.TestCase):
  def test_example(self):
    self.assertEqual(bfs_distances(DIAMOND, 'a'),
                     {'a': 0, 'b': 1, 'c': 1, 'd': 2})

  def test_start_is_zero(self):
    self.assertEqual(bfs_distances({'a': []}, 'a'), {'a': 0})

  def test_shortest_of_two_paths_wins(self):
    # 'a' -> 'd' directly is 1 hop; via 'b' -> 'c' it would be 3.
    graph = {'a': ['b', 'd'], 'b': ['c'], 'c': ['d'], 'd': []}
    self.assertEqual(bfs_distances(graph, 'a'),
                     {'a': 0, 'b': 1, 'd': 1, 'c': 2})

  def test_chain(self):
    graph = {1: [2], 2: [3], 3: [4], 4: []}
    self.assertEqual(bfs_distances(graph, 1), {1: 0, 2: 1, 3: 2, 4: 3})

  def test_unreachable_nodes_are_omitted(self):
    graph = {'a': ['b'], 'b': [], 'far': []}
    self.assertEqual(bfs_distances(graph, 'a'), {'a': 0, 'b': 1})

  def test_cycle_terminates(self):
    self.assertEqual(bfs_distances({1: [2], 2: [3], 3: [1]}, 1),
                     {1: 0, 2: 1, 3: 2})

  def test_unknown_start_raises(self):
    with self.assertRaises(KeyError):
      bfs_distances(DIAMOND, 'z')


if __name__ == '__main__':
  unittest.main()
