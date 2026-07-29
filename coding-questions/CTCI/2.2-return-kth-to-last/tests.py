import unittest


def build_list(values):
  head = None
  for v in reversed(values):
    head = Node(v, head)
  return head


class TestReturnKthToLast(unittest.TestCase):
  def setUp(self):
    self.head = build_list([12, 10, 3, 1, 156, 43])

  def test_runner_second_to_last(self):
    self.assertEqual(find_kth_from_tail_runner(self.head, 2), 156)

  def test_runner_last(self):
    self.assertEqual(find_kth_from_tail_runner(self.head, 1), 43)

  def test_runner_first(self):
    self.assertEqual(find_kth_from_tail_runner(self.head, 6), 12)

  def test_runner_out_of_range(self):
    self.assertIsNone(find_kth_from_tail_runner(build_list([1, 2, 3]), 4))

  def test_runner_empty_list(self):
    self.assertIsNone(find_kth_from_tail_runner(None, 2))

  def test_runner_single_node(self):
    self.assertEqual(find_kth_from_tail_runner(build_list([9]), 1), 9)


if __name__ == '__main__':
  unittest.main()
