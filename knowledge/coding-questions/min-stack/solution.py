class MinStack(object):
  def __init__(self):
    # Each entry is (value, min of the stack up to and including this entry).
    self.stack = []

  def push(self, value):
    current_min = value if not self.stack else min(value, self.stack[-1][1])
    self.stack.append((value, current_min))

  def pop(self):
    self.stack.pop()

  def top(self):
    return self.stack[-1][0]

  def get_min(self):
    return self.stack[-1][1]
