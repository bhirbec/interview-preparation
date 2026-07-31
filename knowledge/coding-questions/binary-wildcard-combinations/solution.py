def binary_wildcard_combinations(s):
  results = []
  chars = list(s)
  n = len(chars)

  def backtrack(pos):
    if pos == n:
      results.append(''.join(chars))
      return

    if chars[pos] == '?':
      for bit in ('0', '1'):
        chars[pos] = bit
        backtrack(pos + 1)
      chars[pos] = '?'
    else:
      backtrack(pos + 1)

  backtrack(0)
  return results


def binary_wildcard_combinations_1(s):
  n = len(s)
  output = [''] * n
  outputs = []

  def traverse(pos):
    if pos == n:
      outputs.append(''.join(output))
      return

    if s[pos] == '?':
      output[pos] = '0'
      traverse(pos + 1)

      output[pos] = '1'
      traverse(pos + 1)
    else:
      output[pos] = s[pos]
      traverse(pos + 1)

  traverse(0)
  return outputs
