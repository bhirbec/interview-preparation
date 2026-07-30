def valid_braces(s):
  match = {')': '(', ']': '[', '}': '{'}
  stack = []
  for ch in s:
    if ch in '([{':
      stack.append(ch)
    elif ch in match:
      if not stack or stack.pop() != match[ch]:
        return False
  return not stack
