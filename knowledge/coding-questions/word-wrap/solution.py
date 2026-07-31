def word_wrap(text, width):
  if not text:
    return []

  lines = []
  line = []
  line_size = 0

  for word in text.split(' '):
    new_size = line_size + len(word)
    if line_size > 0:
      new_size += 1  # the space before this word

    if new_size <= width:
      line.append(word)
      line_size = new_size
    else:
      lines.append(' '.join(line))
      line = [word]
      line_size = len(word)

  if line:
    lines.append(' '.join(line))

  return lines
