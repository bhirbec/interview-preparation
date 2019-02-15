# https://www.facebook.com/careers/life/sample_interview_questions
import unittest


def spiral(size):
  directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

  output = [[None for _ in range(size)] for _ in range(size)]
  i = 0
  n = int(size / 2)

  for layer in range(n):
    pos = layer, layer
    for x_dir, y_dir in directions:
      for _ in range(size - (layer * 2) - 1):
        i += 1
        x, y = pos
        output[x][y] = i
        x += x_dir * 1
        y += y_dir * 1
        pos = x, y

  if size & 1:
    output[n][n] = i + 1

  return output


class TestSpiral(unittest.TestCase):
  def test_spiral(self):
    s = spiral(size=2)
    result = [
      [1, 2],
      [4, 3],
    ]
    self.assertTrue(s == result)

    s = spiral(size=3)
    result = [
      [1, 2, 3],
      [8, 9, 4],
      [7, 6, 5],
    ]
    self.assertTrue(s == result)



if __name__ == '__main__':
  unittest.main()
