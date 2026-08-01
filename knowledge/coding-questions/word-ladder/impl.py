# Word Ladder
#
# Given a start word, a target word, and a dictionary of words (all of the same
# length), find a shortest transformation sequence from start to target such that
# each step changes exactly one letter and every intermediate word AND the target
# word appears in the dictionary. Return the sequence as a list of words
# (including both start and target). If no such sequence exists, return [].
#
# The start word does not need to be in the dictionary. If there are several
# shortest sequences, any one of them is acceptable.
#
# Constraints:
#   - All words (start, target, dictionary entries) have the same length.
#   - Letters are lowercase 'a'-'z'.
#
# Examples:
#   begin="cat", end="dog",
#   words=["cat","cot","dog","dat","dot","dit","dag"]
#     -> ["cat","dat","dot","dog"]   (one shortest ladder of length 4)
#   begin="hit", end="hot", words=["hot"]     -> ["hit","hot"]
#   begin="cat", end="dog", words=["cat","dog"] -> []   (no single-letter bridge)
#   begin="cat", end="dog", words=["cat","dat","dit"] -> []  (target not present)


def find_ladder(begin, end, word_list):
  # TODO: implement
  raise NotImplementedError
