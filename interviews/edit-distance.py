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
    b = 'kitten'
    a = 'sitting'
    d = distance(list(a), list(b))
    print '=>', d

def distance(a, b):
    cache = {}

    def _distance(a, b, i, j, n, m):
        hit = cache.get((i, j))
        if hit is not None:
            return hit

        # characters are the same
        if i < n and j < m and a[i] == b[j]:
            cost = _distance(a, b, i+1, j+1, n, m)
            cache[(i, j)] = cost
            return cost

        if i < n and j < m:
            cost_replace = _distance(a, b, i+1, j+1, n, m)
            cost_insert = _distance(a, b, i, j+1, n, m)
            cost_delete = _distance(a, b, i+1, j, n, m)
            cache[(i, j)] = min(cost_replace, cost_insert, cost_delete) + 1
            return cache[(i, j)]

        # j has reached m and we can only perform deletions
        if i < n:
            cache[(i, j)] = n - i
            return cache[(i, j)]

        # i has reached n and we can only perform insertions
        if j < m:
            cache[(i, j)] = m - j
            return cache[(i, j)]

        return 0

    return _distance(a, b, 0, 0, len(a), len(b))

if __name__ == '__main__':
    main()
