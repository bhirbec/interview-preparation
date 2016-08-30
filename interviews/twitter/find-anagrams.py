# https://careercup.com/question?id=5687065971785728

# Find the anagrams from a list of strings
# Input : {"tea", "ate", "eat", "apple", "java", "vaja", "cut", "utc"}
# Output : {"tea", "ate", "eat","java", "vaja", "cut", "utc"}</p>

def main():
	words = ["tea", "ate", "eat", "apple", "java", "vaja", "cut", "utc"]
	print find_anagrams(words)

def find_anagrams(words):
	counters = {}
	for w in words:
		key = ''.join(sorted(w))
		count = counters.setdefault(key, 0)
		counters[key] += 1

	anagrams = []
	for w in words:
		key = ''.join(sorted(w))
		if counters[key] > 1:
			anagrams.append(w)

	return anagrams

main()
