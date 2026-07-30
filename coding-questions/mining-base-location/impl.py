# Mining Base Location
#
# Difficulty: medium
# Tags: #bfs #matrix #graph #google
#
# You are given a rectangular map given as a list of equal-length strings, where
# each cell is one of:
#   '#' - a mountain (impassable)
#   '*' - a mining site
#   ' ' - open space
# A rover moves one step up, down, left or right at a time and may never enter a
# mountain cell. Choose a cell (any non-mountain cell) to place a base so that the
# sum of shortest-path distances from the base to every mining site is minimized.
# Return the base cell as a (row, col) tuple.
#
# The base must be able to reach every mining site. If no non-mountain cell can
# reach all mining sites, or there are no mining sites, return None. When several
# cells tie for the minimum total distance, return the one that comes first in
# row-major order.
#
# Constraints:
#   - All rows have the same length.
#   - Distances are counted in 4-directional steps between adjacent cells.
#   - A base placed on a mining site has distance 0 to that site.
#
# Examples:
#   ["*", " "]                 -> (0, 0)   # single site
#   ["   ", "   "]             -> None     # no mining sites
#   ["*#", "#*"]               -> None     # sites are mutually unreachable
#   ["*   ", "    ", "*  *"]   -> (2, 0)   # geometric median of the three sites
#
# Approach: BFS from each mining site to accumulate, per cell, the total distance
# and how many sites reached it; the answer is the reachable-by-all cell with the
# smallest total (first in row-major order on ties).


def find_base(grid):
  # TODO: implement
  raise NotImplementedError
