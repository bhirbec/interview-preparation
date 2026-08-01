# Text Justification
#
# You are given a list of words and a page width. Split the words, keeping
# their order, into consecutive lines. A line holds words joined by single
# spaces and its total length must not exceed the width. The "badness" of a
# line is (width - line_length) ** 3, penalizing ragged lines; the cost of a
# layout is the sum of the badness of ALL its lines (including the last).
#
# Return the lines (list of strings) of a layout with minimum total cost. If
# several layouts tie, any optimal one is accepted.
#
# Greedily packing each line as full as possible is NOT always optimal — a
# slightly emptier line now can avoid a terribly empty line later.
#
# Constraints:
#   - 1 <= len(words) <= 200
#   - every word fits alone on a line: len(word) <= width
#
# Examples:
#   justify(["ab", "cd"], 5)  == ["ab cd"]          # cost (5-5)^3 = 0
#   justify(["hello"], 10)    == ["hello"]          # cost (10-5)^3 = 125
#   justify(["aaa", "bb", "cc", "ddddd"], 6)
#     -> [["aaa bb"], ["cc"], ["ddddd"]] flavour: total cost 29


def justify(words, width):
  # TODO: implement
  raise NotImplementedError
