# https://www.careercup.com/question?id=14947965

# Given one start word and a target word, and a dictionary of words. you have to find the path from start
# to target word by changing one letter at a time, and the new word should be in the dictionary. given word
# cat, target word- dog Dictionary: cat, dog, dat, dot, dit, dag. find the path cat->dat -> dot -> dog

from heapq import heappush, heappop

alphabet = 'abcedfghijklmnopqrstuvwxyx'

def main():
    d = distance('cat', 'dog')
    print d

def distance(a, b):
    n, m = len(a), len(b)
    table = distance_table(a, b)
    print_mat(table)
    return table[n][m]

def distance_table(a, b):
    a, b = [''] + list(a), [''] + list(b)
    n, m = len(a), len(b)
    table = [[0 for j in range(m)] for i in range(n)]

    for i in range(n):
        table[i][0] = i

    for j in range(m):
        table[0][j] = j

    for i in range(1, n):
        for j in range(1, m):
            if a[i] == b[j]:
                cost = table[i-1][j-1]
            else:
                cost_replace = table[i-1][j-1] + 2
                # cost_insert = table[i-1][j] + 1
                # cost_delete = table[i][j-1] + 1
                cost = min(cost_replace, cost_insert, cost_delete)
            table[i][j] = cost
    return table

dictionary = 'cat', 'dog', 'dat', 'dot', 'dit', 'dag'

def _compute_replace_cost(a, b, i, j, max_cost):
    tmp = a[i]
    a[i] = b[j]
    word = ''.join(a)
    if word in dictionary:
        print word
    a[i] = tmp
    return 2 if word in dictionary else None

def _compute_insertion_cost(a, b, i, j, max_cost):
    a.insert(i, b[j])
    word = ''.join(a)
    if word in dictionary:
        print word
    a.pop(i)
    return 1 if word in dictionary else None

def _compute_deletion_cost(a, b, i, j, max_cost):
    tmp = a.pop(i)
    word = ''.join(a)
    if word in dictionary:
        print word

    a.insert(i, tmp)
    return 1 if word in dictionary else None

def print_mat(mat):
    for r in mat:
        print ' '.join('%2s' % (v or 0) for v in r)

main()
