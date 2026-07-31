# Fit Words In Grid
#
# Difficulty: medium
# Source: https://www.careercup.com/question?id=5701279419465728
# Tags: #string #google
#
# You are given a list of `words`, a number of rows `num_rows`, and a number of
# columns `num_cols`. The words are written out in order, cycling back to the
# first word after the last, and packed greedily into rows: within a row, words
# are separated by a single space and a word is placed only if it fits in the
# remaining columns; otherwise the row ends and the word starts the next row.
# Fill exactly `num_rows` rows. Return the total number of words written.
#
# Constraints:
#   - 1 <= num_rows
#   - each word's length is at most num_cols (so it can fit on a line)
#   - words is non-empty
#
# Examples:
#   words = ["Do", "Run"], num_rows = 2, num_cols = 9 -> 5
#     Row 1: "Do Run Do"  (2+1+3+1+2 = 9)
#     Row 2: "Run Do"     ("Run" would overflow -> 10)
#   words = ["a"], num_rows = 3, num_cols = 1          -> 3   (one "a" per row)
#   words = ["ab", "cd"], num_rows = 1, num_cols = 2   -> 1   (only "ab" fits)
#   words = ["hello"], num_rows = 2, num_cols = 3      -> 0   (never fits)
#
# Approach: simulate row by row, keeping a cyclic index into words and the current
# line length; a word of length L needs L (or L+1 with a leading space) columns.


def count_words(words, num_rows, num_cols):
  # TODO: implement
  raise NotImplementedError
