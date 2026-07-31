import unittest


class TestFibonacci(unittest.TestCase):
  def test_first_term(self):
    self.assertEqual(fibonacci(1), 1)

  def test_second_term(self):
    self.assertEqual(fibonacci(2), 1)

  def test_first_composed_term(self):
    self.assertEqual(fibonacci(3), 2)

  def test_tenth_term(self):
    self.assertEqual(fibonacci(10), 55)

  def test_medium_term(self):
    self.assertEqual(fibonacci(50), 12586269025)

  def test_large_term_requires_linear_time(self):
    # Exponential recursion would never finish this one.
    self.assertEqual(
        fibonacci(200),
        280571172992510140037611932413038677189525)

  def test_recurrence_holds(self):
    self.assertEqual(fibonacci(30), fibonacci(29) + fibonacci(28))


if __name__ == '__main__':
  unittest.main()
