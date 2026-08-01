import unittest


class TestEvalRpn(unittest.TestCase):
  def test_example_add_then_multiply(self):
    self.assertEqual(eval_rpn(["2", "1", "+", "3", "*"]), 9)

  def test_example_division_truncates(self):
    self.assertEqual(eval_rpn(["4", "13", "5", "/", "+"]), 6)

  def test_single_number(self):
    self.assertEqual(eval_rpn(["18"]), 18)

  def test_single_negative_number(self):
    self.assertEqual(eval_rpn(["-7"]), -7)

  def test_subtraction_operand_order(self):
    self.assertEqual(eval_rpn(["3", "10", "-"]), -7)

  def test_division_operand_order(self):
    self.assertEqual(eval_rpn(["12", "4", "/"]), 3)

  def test_negative_division_truncates_toward_zero(self):
    self.assertEqual(eval_rpn(["7", "-2", "/"]), -3)
    self.assertEqual(eval_rpn(["-7", "2", "/"]), -3)

  def test_long_mixed_expression(self):
    tokens = ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
    self.assertEqual(eval_rpn(tokens), 22)

  def test_result_can_be_zero(self):
    self.assertEqual(eval_rpn(["5", "5", "-"]), 0)


if __name__ == '__main__':
  unittest.main()
