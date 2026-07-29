import unittest


class TestGetLayers(unittest.TestCase):
  def _values(self, tree):
    return [list(layer) for layer in get_layers(tree)]

  def test_empty_tree(self):
    self.assertEqual(get_layers(None), [])

  def test_single_node(self):
    self.assertEqual(self._values({'value': 1}), [[1]])

  def test_full_tree_left_to_right_order(self):
    tree = {
        'value': 1,
        'left': {
            'value': 2,
            'left': {'value': 4},
            'right': {'value': 5},
        },
        'right': {
            'value': 3,
            'left': {'value': 6},
            'right': {'value': 7},
        },
    }
    self.assertEqual(self._values(tree), [[1], [2, 3], [4, 5, 6, 7]])

  def test_skewed_left_tree(self):
    tree = {
        'value': 1,
        'left': {'value': 2, 'left': {'value': 3}},
    }
    self.assertEqual(self._values(tree), [[1], [2], [3]])

  def test_number_of_layers_equals_depth(self):
    tree = {
        'value': 1,
        'left': {'value': 2},
        'right': {'value': 3, 'right': {'value': 4}},
    }
    self.assertEqual(len(get_layers(tree)), 3)

  def test_linked_list_str(self):
    layers = get_layers({'value': 1,
                         'left': {'value': 2},
                         'right': {'value': 3}})
    self.assertEqual(str(layers[1]), '2, 3')


if __name__ == '__main__':
  unittest.main()
