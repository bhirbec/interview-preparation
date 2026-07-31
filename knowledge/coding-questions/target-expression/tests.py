import unittest


class TestFindExpression(unittest.TestCase):
  def _assert_valid(self, digits, target):
    expr = find_expression(digits, target)
    self.assertIsNotNone(expr)
    # The stripped digits must match the original sequence, in order.
    stripped = expr.replace('+', '').replace('-', '')
    self.assertEqual(stripped, ''.join(str(d) for d in digits))
    self.assertEqual(eval(expr), target)

  def test_concatenate_pair(self):
    self._assert_valid([1, 2, 3, 4], 46)

  def test_concatenate_everything(self):
    self.assertEqual(find_expression([1, 2, 3, 4], 1234), "1234")

  def test_single_digit_reachable(self):
    self.assertEqual(find_expression([5], 5), "5")

  def test_single_digit_unreachable(self):
    self.assertIsNone(find_expression([5], 3))

  def test_impossible_target(self):
    self.assertIsNone(find_expression([1, 2], 100))

  def test_empty_input(self):
    self.assertIsNone(find_expression([], 0))

  def test_subtraction_needed(self):
    self._assert_valid([1, 2], -1)

  def test_sum_of_singles(self):
    self._assert_valid([1, 2, 3, 4], 10)

  def test_negative_target(self):
    self._assert_valid([5, 9], -4)

  def test_no_leading_zero_multi_digit(self):
    # "0" then "5": 0+5 or 0-5 possible, but "05" (=5) is forbidden.
    self._assert_valid([0, 5], 5)
    self.assertIsNone(find_expression([0, 5], 50))

  def test_zero_target_with_cancellation(self):
    self._assert_valid([1, 1], 0)


if __name__ == '__main__':
  unittest.main()
