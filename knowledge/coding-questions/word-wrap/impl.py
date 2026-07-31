# Word Wrap
#
# Source: https://www.glassdoor.com/Interview/Given-a-message-one-two-three-four-five-six-seven-eight-nine-chop-it-in-chunks-no-exceed-the-give-buffer-size-and-print-QTN_1438219.htm
#
# You are given a message `text` made of words separated by single spaces, and a
# positive integer `width`. Break the message into lines using greedy word wrap:
# read the words left to right and pack as many whole words as possible onto the
# current line, where words on a line are joined by single spaces, without any
# line's length exceeding `width`. A word is never split across lines.
#
# Return the list of lines, in order. You may assume every individual word fits
# within `width` (i.e. len(word) <= width for every word).
#
# Constraints:
#   - width >= 1
#   - text has no leading/trailing spaces and single spaces between words
#   - every word length <= width
#
# Examples:
#   text = "a b c", width = 5   -> ["a b c"]
#   text = "a b c", width = 3   -> ["a b", "c"]
#   text = "aaa bbb ccc", width = 3 -> ["aaa", "bbb", "ccc"]
#   text = "the quick brown fox", width = 9 -> ["the quick", "brown fox"]
#   text = "hello", width = 10   -> ["hello"]


def word_wrap(text, width):
  # TODO: implement
  raise NotImplementedError
