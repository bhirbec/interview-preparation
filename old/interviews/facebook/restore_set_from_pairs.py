# https://www.careercup.com/question?id=5751343965798400

# Let be X and S a tow sets of numbers such that
# X = {x1, x2, x3, x4, ..., xN} with N >= 3
# S = {x1+x2, x1+x3, x1+x4, x2+x3, x2+x4, x3+x4,...} with s_k = x_i + x_j where i != j

# Given S you have to restore X. You don't know given some k, to which i and j it
# refers, (i.e. input is given in undefined order)

# Solution

# Starting from X it's easy to find S
# X = {1, 2, 3}
# S = {3, 4, 5}

# Here's the matrix with the computation:
#   1 2 3
# 1   3 4
# 2     5
# 3

# In this matrix each number maintain invariants:
# 1. all the right numbers >=
# 2. all the bottom numbers are >=
# 3. all the numbers in the diagonal are >=

# If you can build that matrix then the problem can be reduce to a linear equation problem.
# However given a set S how many matrix can you build?

# With S = {3, 4, 5, 18, 19, 20} you can build at least two matrices.

# X = {1, 2, 3, 17}
# X = {-5.5, 8.5, 9.5, 10.5}

#   1 2 3 17
# 1   3 4 18
# 2     5 19
# 3       20
# 17

#      -5.5 8.5 9.5 10.5
# -5.5        3   4    5
# 8.5            18   19
# 9.5                 20
# 10.5

# To solve this problem we need to find a strategy to build a valid matrix.
