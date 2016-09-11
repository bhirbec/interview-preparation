
"""
Return True if the given string has all unique characters, otherwise return False.
Running time complexity is O(n), space complexity is O(1).
"""
def unique_char(s):
	if len(s) > 128:
		return False

	char_set = [False]*256

	for ch in s:
		i = ord(ch)
		if char_set[i]:
			return False
		char_set[i] = True

	return True

def unique_char_bitvector(s):
	bits = 0

	for ch in s:
		i = ord(ch)
		new_bit = 1 << i

		# two identical bits set to true and'd together will return true or '1'
		if (bits & new_bit) > 0:
			return False

		bits |= new_bit

	return True

print unique_char("coucou")
print unique_char_bitvector("qwertyuio")

