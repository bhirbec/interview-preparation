# https://careercup.com/question?id=5659201272545280

# Given an input string and ordering string, need to return true if the ordering string
# is present in Input string.

# input = "hello world!"
# ordering = "hlo!"
# result = FALSE (all Ls are not before all Os)

# input = "hello world!"
# ordering = "!od"
# result = FALSE (the input has '!' coming after 'o' and after 'd', but the pattern needs it to come before 'o' and 'd')

# input = "hello world!"
# ordering = "he!"
# result = TRUE

# input = "aaaabbbcccc"
# ordering = "ac"
# result = TRUE


def main():
	string = "hello world!"
	ordering = "hlo!"
	print check_ordering(string, ordering) # False (all Ls are not before all Os)

	string = "hello world!"
	ordering = "!od"
	print check_ordering(string, ordering) # False (the string has '!' coming after 'o' and after 'd', but the pattern needs it to come before 'o' and 'd')

	string = "hello world!"
	ordering = "he!"
	print check_ordering(string, ordering) # True

	string = "aaaabbbcccc"
	ordering = "ac"
	print check_ordering(string, ordering) # True


def check_ordering(string, ordering):
	ordered_chars = dict((c, 1) for c in ordering)
	output = []

	for c in string:
		if c in ordered_chars:
			if len(output) == 0:
				output.append(c)
			else:
				last = output[-1]
				if last != c:
					output.append(c)

	return ''.join(output) == ordering

if __name__ == '__main__':
	main()
