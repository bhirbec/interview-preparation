import unittest


class TestBooleanEvaluation(unittest.TestCase):
  def test_ctci_examples(self):
    self.assertEqual(count_eval('1^0|0|1', 0), 2)
    self.assertEqual(count_eval('0&0&0&1^1|0', 1), 10)

  def test_single_operand(self):
    self.assertEqual(count_eval('1', 1), 1)
    self.assertEqual(count_eval('1', 0), 0)
    self.assertEqual(count_eval('0', 0), 1)
    self.assertEqual(count_eval('0', 1), 0)

  def test_single_operator(self):
    # '1^0' evaluates to 1 in the only possible parenthesization.
    self.assertEqual(count_eval('1^0', 1), 1)
    self.assertEqual(count_eval('1^0', 0), 0)
    self.assertEqual(count_eval('1&1', 1), 1)
    self.assertEqual(count_eval('1|0', 1), 1)

  def test_counts_are_complementary(self):
    # Total parenthesizations = ways-to-1 + ways-to-0 for any expression.
    expr = '1^0|0|1'
    ways_true = count_eval(expr, 1)
    ways_false = count_eval(expr, 0)
    # Catalan(3) = 5 parenthesizations for 4 operands.
    self.assertEqual(ways_true + ways_false, 5)


if __name__ == '__main__':
  unittest.main()
