# Shell Tokenizer
#
# You are given a command string like the ones typed into a shell. Split it
# into tokens:
#   - tokens are separated by one or more spaces;
#   - a section wrapped in double quotes belongs to a single token, spaces
#     included, and the quotes themselves are dropped;
#   - a quoted section can sit right next to unquoted text, contributing to
#     the same token (ab"c d" is one token: 'abc d');
#   - a pair of quotes always contributes to a token, so "" produces an
#     empty token.
#
# Quotes are guaranteed to be balanced. Return the list of tokens.
#
# Constraints:
#   - 0 <= len(command) <= 10^4
#   - the only whitespace is the space character
#
# Examples:
#   tokenize('foo bar "foo_bar"')   == ['foo', 'bar', 'foo_bar']
#   tokenize('a "b c" d')           == ['a', 'b c', 'd']
#   tokenize('ab"c d"e')            == ['abc de']
#   tokenize('   ')                 == []


def tokenize(command):
  # TODO: implement
  raise NotImplementedError
