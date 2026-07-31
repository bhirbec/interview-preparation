import unittest


class TestTokenize(unittest.TestCase):
  def test_interview_example(self):
    self.assertEqual(tokenize('foo bar "foo_bar"'), ['foo', 'bar', 'foo_bar'])

  def test_quoted_section_keeps_spaces(self):
    self.assertEqual(tokenize('a "b c" d'), ['a', 'b c', 'd'])

  def test_quotes_glued_to_text(self):
    self.assertEqual(tokenize('ab"c d"e'), ['abc de'])

  def test_multiple_spaces_collapse(self):
    self.assertEqual(tokenize('a   b'), ['a', 'b'])

  def test_leading_and_trailing_spaces(self):
    self.assertEqual(tokenize('  hello world  '), ['hello', 'world'])

  def test_empty_string(self):
    self.assertEqual(tokenize(''), [])

  def test_only_spaces(self):
    self.assertEqual(tokenize('   '), [])

  def test_empty_quotes_make_empty_token(self):
    self.assertEqual(tokenize('a "" b'), ['a', '', 'b'])

  def test_whole_string_quoted(self):
    self.assertEqual(tokenize('"one two three"'), ['one two three'])


if __name__ == '__main__':
  unittest.main()
