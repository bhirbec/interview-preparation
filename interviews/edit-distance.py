# From Wikipedia (https://en.wikipedia.org/wiki/Edit_distance)
# ============================================================
# In computer science, edit distance is a way of quantifying how dissimilar two strings (e.g., words) are
# to one another by counting the minimum number of operations required to transform one string into the other.
# Edit distances find applications in natural language processing, where automatic spelling correction can
# determine candidate corrections for a misspelled word by selecting words from a dictionary that have a low
# distance to the word in question. In bioinformatics, it can be used to quantify the similarity of macromolecules
# such as DNA, which can be viewed as strings of the letters A, C, G and T.

# From MIT OpenCourseWare (https://youtu.be/ocZMDMZwhCY?t=1441)
# =============================================================
# Given two strings A and B, what's the cheapest possible sequence of character edits to turn A into B?
# Character edits are as follow:
# - insert
# - delete
# - replace

# Recurrence:
# DP(i, j) = min(
#     (cost of inserting Bj) + DP(i, j+1),
#     (cost of deleting Ai) + DP(i+1, j),
#     (cost of replacing Ai -> Bj) + DP(i+1, j+1)
# )

# Base case:
# DP(0,0) = 0

# Time complexity = Theta(|A|.|B|)
# - number of subproblems = Theta(|A|.|B|)
# - time / subproblem = O(1)

def main():
    print distance('intention', 'execution')
    print distance_bottom_up('intention', 'execution')

def distance(a, b):
    n, m = len(a), len(b)
    cache = [[None for i in range(m)] for j in range(n)]

    def _distance(i, j):
        if i < 0 and j < 0:
            return 0

        # i has reached n and we need to insert j+1 chars to produce Bj
        if i < 0:
            return j+1

        # j has reached m and we need to delete i+1 chars to produce Ai
        if j < 0:
            return i+1

        cost = cache[i][j]
        if cost is not None:
            return cost

        if a[i] == b[j]:
            cost = _distance(i-1, j-1)
        else:
            cost_replace = _distance(i-1, j-1) + 2
            cost_insert = _distance(i, j-1) + 1
            cost_delete = _distance(i-1, j) + 1
            cost = min(cost_replace, cost_insert, cost_delete)

        cache[i][j] = cost
        return cost

    return _distance(n-1, m-1)

def distance_bottom_up(a, b):
    a, b = [''] + list(a), [''] + list(b)
    n, m = len(a), len(b)
    cache = [[0 for j in range(m)] for i in range(n)]

    for i in range(n):
        cache[i][0] = i

    for j in range(m):
        cache[0][j] = j

    for i in range(1, n):
        for j in range(1, m):
            if a[i] == b[j]:
                cost = cache[i-1][j-1]
            else:
                cost_replace = cache[i-1][j-1] + 2
                cost_insert = cache[i-1][j] + 1
                cost_delete = cache[i][j-1] + 1
                cost = min(cost_delete, cost_insert, cost_delete)
            cache[i][j] = cost

    return cache[n-1][m-1]

if __name__ == '__main__':
    main()
