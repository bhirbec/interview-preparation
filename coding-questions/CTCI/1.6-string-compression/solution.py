def compress(s):
  if not s:
    return ''

  count = 1
  prev_char = s[0]
  buf = []

  for char in s[1:]:
    if char == prev_char:
      count += 1
    else:
      buf.append(prev_char)
      buf.append(str(count))
      count = 1
    prev_char = char

  buf.append(prev_char)
  buf.append(str(count))

  return ''.join(buf)
