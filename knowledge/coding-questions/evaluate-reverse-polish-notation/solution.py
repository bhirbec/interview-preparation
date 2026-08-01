def eval_rpn(tokens):
  stack = []
  for token in tokens:
    if token == '+':
      b, a = stack.pop(), stack.pop()
      stack.append(a + b)
    elif token == '-':
      b, a = stack.pop(), stack.pop()
      stack.append(a - b)
    elif token == '*':
      b, a = stack.pop(), stack.pop()
      stack.append(a * b)
    elif token == '/':
      b, a = stack.pop(), stack.pop()
      # int() truncates toward zero; // would floor toward -infinity.
      stack.append(int(a / b))
    else:
      stack.append(int(token))
  return stack[0]
