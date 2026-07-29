def gen_parens(n):
  depth = n * 2
  buff = [''] * depth
  result = []

  def f(pos=0, open=0, closed=0):
    if pos == depth:
      result.append(''.join(buff))
      return

    if open < n:
      buff[pos] = '('
      f(pos + 1, open + 1, closed)

    if closed < open:
      buff[pos] = ')'
      f(pos + 1, open, closed + 1)

  f()
  return result
