# https://www.glassdoor.com/Interview/Given-a-set-of-Sentences-containing-lower-case-letters-only-remove-common-phrases-from-each-sentence-Here-a-phrase-is-def-QTN_171719.htm

# Given a set of Sentences containing lower case letters only, remove common phrases from each sentence.
# Here a phrase is defined by 3 or more consecutive words. E.g:

# S1 = "I my bye good";
# S2 = "my bye good boy";
# common phrase is: "my bye good"

# the two sentences become
# S1 = "I";
# s2 ="boy";


def main():
	sentences = [
		"hello my name is benoit",
		"hello my name is benoit",
	]

	chuncks = {}

	for sentence in sentences:
		for key in iter_words_window(sentence):
			chuncks[key] = True

	print chuncks

def iter_words_window(s):
	words = s.split(" ")
	n = len(words)
	for window in range(3, n+1):
		for i in range(n-window+1):
			key = ' '.join(words[i:i+window])
			yield key

main()
