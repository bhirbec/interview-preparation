def find_expression(digits, target):
  n = len(digits)
  if n == 0:
    return None
  s = ''.join(str(d) for d in digits)

  def backtrack(pos, current, expr):
    if pos == n:
      return expr if current == target else None
    for end in range(pos + 1, n + 1):
      token = s[pos:end]
      if len(token) > 1 and token[0] == '0':
        break
      num = int(token)
      if pos == 0:
        found = backtrack(end, num, token)
        if found is not None:
          return found
      else:
        found = backtrack(end, current + num, expr + '+' + token)
        if found is not None:
          return found
        found = backtrack(end, current - num, expr + '-' + token)
        if found is not None:
          return found
    return None

  return backtrack(0, 0, '')
