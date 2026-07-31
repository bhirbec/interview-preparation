import unittest


class TestCompress(unittest.TestCase):
  def test_go_source_example(self):
    self.assertEqual(compress('aaaannnnfffgggnngg'), 'a4n4f3g3n2g2')

  def test_ctci_example(self):
    self.assertEqual(compress('aabcccccaaa'), 'a2b1c5a3')

  def test_all_distinct_still_counted(self):
    self.assertEqual(compress('abc'), 'a1b1c1')

  def test_single_character(self):
    self.assertEqual(compress('a'), 'a1')

  def test_empty_string(self):
    self.assertEqual(compress(''), '')

  def test_single_long_run(self):
    self.assertEqual(compress('aaaa'), 'a4')

  def test_case_sensitive(self):
    self.assertEqual(compress('aAaA'), 'a1A1a1A1')

  def test_run_of_ten(self):
    self.assertEqual(compress('aaaaaaaaaa'), 'a10')


if __name__ == '__main__':
  unittest.main()
