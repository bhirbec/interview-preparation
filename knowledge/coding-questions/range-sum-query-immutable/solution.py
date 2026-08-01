class NumArray(object):
  def __init__(self, nums):
    # prefix[i] holds the sum of the first i values, so prefix[0] == 0 and no
    # query needs a special case for left == 0.
    self.prefix = [0] * (len(nums) + 1)
    for i, n in enumerate(nums):
      self.prefix[i + 1] = self.prefix[i] + n

  def sum_range(self, left, right):
    return self.prefix[right + 1] - self.prefix[left]
