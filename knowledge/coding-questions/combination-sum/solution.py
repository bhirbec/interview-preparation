def combination_sum(candidates, target):
  results = []
  current = []

  def backtrack(start, remaining):
    if remaining == 0:
      results.append(current[:])
      return
    for i in range(start, len(candidates)):
      value = candidates[i]
      if value <= remaining:
        current.append(value)
        backtrack(i, remaining - value)
        current.pop()

  backtrack(0, target)
  return results
