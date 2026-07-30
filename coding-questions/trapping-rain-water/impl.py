# Trapping Rain Water
#
# Difficulty: hard
# Tags: #array #two-pointers #twitter
#
# You are given a list of non-negative integers `heights` where each value is the
# height of a bar of unit width, laid out side by side. After it rains, water is
# trapped between the bars.
#
# Return the total amount of water that can be held.
#
# Constraints:
#   - 0 <= len(heights) <= 2 * 10^4
#   - 0 <= heights[i] <= 10^5
#
# Examples:
#   [0,1,0,2,1,0,1,3,2,1,2,1] -> 6
#   [4,2,0,3,2,5]             -> 9
#   [3,3,3]                   -> 0    (flat, nothing trapped)
#   [5,4,3,2,1]               -> 0    (monotonic, no basin)
#
# Approach: walk inward from both ends; the shorter side bounds the water there,
# so advance whichever side is lower, banking (running max - height) as you go.


def trap_water(heights):
  # TODO: implement
  raise NotImplementedError
