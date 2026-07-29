import unittest


class TestPerm(unittest.TestCase):

  def test_is_permutation_length(self):
    self.assertFalse(is_permutation('sew', 's'))

  def test_is_permutation_small(self):
    self.assertTrue(is_permutation('sew', 'wse'))

  def test_is_permutation_big(self):
    self.assertTrue(is_permutation('sewJdifjldifjdkwdkdsk', 'skeJdjwdkkdsilwjdiffd'))

  def test_is_permutation_notok(self):
    self.assertFalse(is_permutation('sew', 'wwse'))

  def test_is_permutation_empty(self):
    self.assertTrue(is_permutation('', ''))

  def test_is_permutation_case_sensitive(self):
    self.assertFalse(is_permutation('abc', 'abC'))

  def test_is_permutation_same_length_diff_chars(self):
    self.assertFalse(is_permutation('abc', 'abd'))

  def test_is_permutation_counts_differ(self):
    self.assertFalse(is_permutation('aab', 'abb'))


if __name__ == '__main__':
  unittest.main()
