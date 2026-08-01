def daily_temperatures(temperatures):
  answer = [0] * len(temperatures)
  # Indices of days still waiting for a warmer day; temperatures at these
  # indices are non-increasing from bottom to top.
  stack = []
  for i, temp in enumerate(temperatures):
    while stack and temperatures[stack[-1]] < temp:
      j = stack.pop()
      answer[j] = i - j
    stack.append(i)
  return answer
