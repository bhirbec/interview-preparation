# Group Anagrams
# Difficulty: medium
# Tags: #hashtable #string #sorting
#
# You are given an array of strings. Sort (group) the array so that all anagrams
# are adjacent to one another. Any ordering that keeps anagrams together is a
# valid answer.
#
# Input:
#   arr -- a list of strings.
# Output:
#   A list of the same strings reordered so that every set of mutual anagrams is
#   contiguous. The relative order of groups, and of words within a group, is
#   unspecified.
#
# Examples:
#   group_anagrams(['add', 'kii', 'dad', 'iki'])
#     -> ['add', 'dad', 'kii', 'iki']   (or any grouping-preserving permutation)
#   group_anagrams([]) -> []
#   group_anagrams(['abc']) -> ['abc']
#
# Approach: map each word to a canonical key (its letters sorted). Words sharing
# a key are anagrams, so bucket them in a hash table, then concatenate the
# buckets. Building the canonical key costs O(w log w) per word of length w.


def group_anagrams(arr):
  # TODO: implement
  raise NotImplementedError
