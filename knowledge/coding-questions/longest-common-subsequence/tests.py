import unittest


def is_subsequence(sub, s):
  it = iter(s)
  return all(ch in it for ch in sub)


class TestLongestCommonSubsequence(unittest.TestCase):
  def check(self, s1, s2, expected_len):
    result = longest_common_subsequence(s1, s2)
    self.assertEqual(len(result), expected_len,
                     msg='%r has wrong length for %r/%r' % (result, s1, s2))
    self.assertTrue(is_subsequence(result, s1),
                    msg='%r is not a subsequence of %r' % (result, s1))
    self.assertTrue(is_subsequence(result, s2),
                    msg='%r is not a subsequence of %r' % (result, s2))

  def test_canonical_example(self):
    self.check('HELLO', 'MELODY', 3)

  def test_classic_clrs_pair(self):
    self.check('ABCBDAB', 'BDCABA', 4)

  def test_dna_strings(self):
    self.check('ATGCACTGAACCTGCACGT', 'ACTGCGCAAACGCGTTGTACGGGG', 14)

  def test_identical_strings(self):
    self.assertEqual(longest_common_subsequence('ABC', 'ABC'), 'ABC')

  def test_no_common_characters(self):
    self.assertEqual(longest_common_subsequence('ABC', 'XYZ'), '')

  def test_empty_first(self):
    self.assertEqual(longest_common_subsequence('', 'ABC'), '')

  def test_empty_second(self):
    self.assertEqual(longest_common_subsequence('ABC', ''), '')

  def test_single_common_character(self):
    self.check('A', 'BAC', 1)

  def test_subsequence_not_substring(self):
    # The common subsequence is non-contiguous in both strings.
    self.check('AXBXC', 'AYBYC', 3)


if __name__ == '__main__':
  unittest.main()
