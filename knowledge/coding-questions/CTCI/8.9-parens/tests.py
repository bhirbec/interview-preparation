import unittest
from math import comb


def catalan(n):
  return comb(2 * n, n) // (n + 1)


def is_valid_parens(s):
  balance = 0
  for ch in s:
    balance += 1 if ch == '(' else -1
    if balance < 0:
      return False
  return balance == 0


class TestParens(unittest.TestCase):
  def test_zero_pairs(self):
    self.assertEqual(gen_parens(0), [''])

  def test_one_pair(self):
    self.assertEqual(gen_parens(1), ['()'])

  def test_two_pairs(self):
    self.assertEqual(sorted(gen_parens(2)), ['(())', '()()'])

  def test_three_pairs_full_enumeration(self):
    self.assertEqual(
      sorted(gen_parens(3)),
      ['((()))', '(()())', '(())()', '()(())', '()()()'],
    )

  def test_count_is_catalan(self):
    for n in range(0, 8):
      self.assertEqual(len(gen_parens(n)), catalan(n))

  def test_all_results_distinct_valid_and_correct_length(self):
    for n in range(0, 7):
      result = gen_parens(n)
      self.assertEqual(len(result), len(set(result)))
      for s in result:
        self.assertEqual(len(s), 2 * n)
        self.assertTrue(is_valid_parens(s))


if __name__ == '__main__':
  unittest.main()
