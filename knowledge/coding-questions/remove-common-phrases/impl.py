# Remove Common Phrases
#
# You are given a list of sentences; each sentence is a string of lower-case
# words separated by single spaces. A "phrase" is any run of 3 or more
# consecutive words within a sentence. A phrase is "common" if the exact same run
# of words appears in at least two different sentences.
#
# Remove common phrases from every sentence: a word is deleted from a sentence if
# it is covered by an occurrence of any common phrase in that sentence. Return the
# list of sentences after removal, each rebuilt from its surviving words joined by
# single spaces (a sentence with every word removed becomes an empty string).
#
# Constraints:
#   - words contain lower-case letters only
#   - a phrase must be at least 3 words long to be considered
#
# Examples:
#   ["i my bye good", "my bye good boy"]
#     "my bye good" appears in both -> ["i", "boy"]
#   ["hello my name is benoit", "hello my name is benoit"]
#     every 3+ word run is shared -> ["", ""]
#   ["one two three", "four five six"]
#     no run is shared             -> ["one two three", "four five six"]
#   ["a b"]  (fewer than 3 words, single sentence) -> ["a b"]


def remove_common_phrases(sentences):
  # TODO: implement
  raise NotImplementedError
