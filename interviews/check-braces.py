def valid_braces(s):
	braces = {
		']': '[',
		')': '(',
		'}': '{',
	}

	open_braces = list(braces.values())
	closing_braces = list(braces.keys())

	stack = []
	for ch in s:
		if ch in open_braces:
			stack.append(ch)
		elif ch in closing_braces:
			if len(stack) == 0:
				return False
			last = stack.pop()
			expected = braces[ch]
			if last != expected:
				return False

	return len(stack) == 0

print(valid_braces("{[]{}[{{{}}}]{{}}}"))
