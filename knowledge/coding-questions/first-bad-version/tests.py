import unittest


def make_is_bad(first_bad):
  calls = [0]

  def is_bad(version):
    calls[0] += 1
    return version >= first_bad
  return is_bad, calls


class TestFirstBadVersion(unittest.TestCase):
  def test_example(self):
    is_bad, _ = make_is_bad(4)
    self.assertEqual(first_bad_version(5, is_bad), 4)

  def test_single_version(self):
    is_bad, _ = make_is_bad(1)
    self.assertEqual(first_bad_version(1, is_bad), 1)

  def test_first_version_is_bad(self):
    is_bad, _ = make_is_bad(1)
    self.assertEqual(first_bad_version(10, is_bad), 1)

  def test_last_version_is_bad(self):
    is_bad, _ = make_is_bad(10)
    self.assertEqual(first_bad_version(10, is_bad), 10)

  def test_middle_version(self):
    is_bad, _ = make_is_bad(500)
    self.assertEqual(first_bad_version(1000, is_bad), 500)

  def test_every_answer_for_small_n(self):
    for first_bad in range(1, 9):
      is_bad, _ = make_is_bad(first_bad)
      self.assertEqual(first_bad_version(8, is_bad), first_bad)

  def test_large_n_uses_logarithmic_calls(self):
    n = 2**31 - 1
    is_bad, calls = make_is_bad(1702766719)
    self.assertEqual(first_bad_version(n, is_bad), 1702766719)
    # A linear scan would need ~1.7 billion calls; binary search needs ~31.
    self.assertLessEqual(calls[0], 40)


if __name__ == '__main__':
  unittest.main()
