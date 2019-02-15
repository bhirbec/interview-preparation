# https://www.careercup.com/question?id=14947965

# Given one start word and a target word, and a dictionary of words. you have to find the path from start
# to target word by changing one letter at a time, and the new word should be in the dictionary. given word
# cat, target word- dog Dictionary: cat, dog, dat, dot, dit, dag. find the path cat->dat -> dot -> dog

letters = 'abcedfghijklmnopqrstuvwxyx'

D = {
  'cat': 1,
  'cot': 1,
  'dog': 1,
  'dat': 1,
  'dot': 1,
  'dit': 1,
  'dag': 1,
}

def find_path(w1, w2):
  n, m = len(w1), len(w2)
  w = list(w1)

  def _dfs(i):
    if i > 2:
      return

    # s = ''.join(w)
    # if s not in D:
    #   return

    print(w)

    # if s == w2:
    #   print(w)
    #   return

    for j, c in enumerate(w2):
      if c != w[i]:
        w[j] = c
        _dfs(i+1)

  _dfs(0)


def find_path1(w1, w2):
  costs = {}
  n, m = len(w1), len(w2)
  w = list(w1)

  for i, c1 in enumerate(w1):
    for j, c2 in enumerate(w2):
      w[i], w[j] = c1

      if c1 == c2:
        cost = costs.get((i-1, j-1), 0)
      else:
        cost = min(
          costs.get((i-1, j-1), 0) + 2,
          costs.get((i-1, j), 0) + 1,
          costs.get((i, j-1), 0) + 1,
        )

      costs[(i, j)] = cost

  return costs[(n-1, m-1)]


def find_path2(w1, w2):
  path = [None] * 3

  w1, w2 = list(w1), list(w2)
  def _edit(i):
    if i > 2:
      return

    w = ''.join(w1)
    path[i] = w

    if w1 == w2:
      print('*', path, '*')
      print(w1, w2)
      return

    if w1[i] != w2[i]:
      w1[i] = w2[i]
    # else:
    #   _edit(i + 1)
    #   return

    if w not in D:
      return

    path.append(w1)

    for char in w2:
      w1[i] = char
      _edit(i + 1)

  return _edit(0)



print(find_path('cat', 'dog'))
# input: cat -> dog
# output: cat->dat -> dot -> dog
