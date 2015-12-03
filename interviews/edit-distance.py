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
    d = distance('kitten', 'sitting')
    print d

def distance(a, b):
    cache = {}

    def _distance(a, b, i, j, n, m):
        if i == n and j == m:
            return 0

        # i has reached n and the cost can only be m - j insertions
        if i == n:
            return m - j

        # j has reached m and the cost can only be n - i deletions
        if j == m:
            return n - i

        hit = cache.get((i, j))
        if hit is not None:
            return hit

        if a[i] == b[j]:
            cost = _distance(a, b, i+1, j+1, n, m)
        else:
            cost_replace = _distance(a, b, i+1, j+1, n, m)
            cost_insert = _distance(a, b, i, j+1, n, m)
            cost_delete = _distance(a, b, i+1, j, n, m)
            cost = min(cost_replace, cost_insert, cost_delete) + 1

        cache[(i, j)] = cost
        return cache[(i, j)]

    return _distance(a, b, 0, 0, len(a), len(b))

if __name__ == '__main__':
    main()
