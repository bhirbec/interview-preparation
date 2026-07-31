import unittest


class TestBuildOrder(unittest.TestCase):
  def _assert_valid_order(self, projects, dependencies, order):
    # every project appears exactly once
    self.assertEqual(sorted(order), sorted(projects))
    # every dependency (a, b) has a before b
    position = {p: i for i, p in enumerate(order)}
    for a, b in dependencies:
      self.assertLess(
          position[a], position[b],
          msg='%r should come before %r in %r' % (a, b, order))

  def test_canonical_example(self):
    projects = ['a', 'b', 'c', 'd', 'e', 'f']
    dependencies = [('a', 'd'), ('f', 'b'), ('b', 'd'), ('f', 'a'), ('d', 'c')]
    order = build_order(projects, dependencies)
    self._assert_valid_order(projects, dependencies, order)

  def test_single_project_no_dependencies(self):
    self.assertEqual(build_order(['a'], []), ['a'])

  def test_no_dependencies(self):
    projects = ['a', 'b', 'c']
    order = build_order(projects, [])
    self.assertEqual(sorted(order), ['a', 'b', 'c'])

  def test_linear_chain(self):
    projects = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('b', 'c'), ('c', 'd')]
    order = build_order(projects, dependencies)
    self.assertEqual(order, ['a', 'b', 'c', 'd'])

  def test_direct_cycle(self):
    self.assertEqual(build_order(['a', 'b'], [('a', 'b'), ('b', 'a')]), 'ERROR')

  def test_indirect_cycle(self):
    projects = ['a', 'b', 'c']
    dependencies = [('a', 'b'), ('b', 'c'), ('c', 'a')]
    self.assertEqual(build_order(projects, dependencies), 'ERROR')

  def test_self_cycle(self):
    self.assertEqual(build_order(['a'], [('a', 'a')]), 'ERROR')

  def test_disconnected_components(self):
    projects = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('c', 'd')]
    order = build_order(projects, dependencies)
    self._assert_valid_order(projects, dependencies, order)


if __name__ == '__main__':
  unittest.main()
