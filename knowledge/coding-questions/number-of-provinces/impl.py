# Number of Provinces
#
# You are given the adjacency matrix of an undirected graph on `n` nodes,
# encoded as a list of `n` strings each of length `n`. `matrix[i][j] == '1'`
# means there is a direct edge between node i and node j, and '0' means there
# is not. The matrix is symmetric and `matrix[i][i] == '1'`.
#
# Two nodes belong to the same group if they are connected directly or
# indirectly (through a chain of edges). Return the number of connected
# components (groups).
#
# Constraints:
#   - 0 <= n, and every string has length n
#   - each character is '0' or '1'
#   - matrix[i][j] == matrix[j][i] (symmetric)
#
# Examples:
#   ["1100",                    -> 2   nodes {0,1,2} form one group (0-1, 1-2),
#    "1110",                          node 3 is alone
#    "0110",
#    "0001"]
#
#   ["10000",                   -> 5   identity matrix: every node is isolated
#    "01000",
#    "00100",
#    "00010",
#    "00001"]
#
#   ["110", "111", "011"]       -> 1   0-1 and 1-2 connect all three transitively
#   ["1"]                       -> 1
#   []                          -> 0


def number_of_provinces(matrix):
  # TODO: implement
  raise NotImplementedError
