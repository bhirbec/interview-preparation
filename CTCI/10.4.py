import unittest


class Listly(object):
  def __init__(self, arr):
    self.arr = arr

  def element_at(self, i):
    try:
      return self.arr[i]
    except IndexError:
      return -1

  def find(self, value):
    def _f(first, last):
      first_val = self.element_at(first)
      last_val = self.element_at(last)

      if first_val == value:
        return first
      elif last_val == value:
        return last
      elif first >= last:
        return None
      elif last_val == -1:
        # overshot, we divide the range by 2
        mid = int((last + first) / 2)
        return _f(first, mid)
      elif value > last_val:
        # value outside of the current range
        return _f(last+1, last*2)
      else:
        mid = int((last + first) / 2)
        return _f(first, mid)

    return _f(0, 2)


class TestListly(unittest.TestCase):
  def test_element_at(self):
    l = Listly([1, 4, 6, 17, 21, 34])
    self.assertTrue(l.element_at(0) == 1)
    self.assertTrue(l.element_at(3) == 17)
    self.assertTrue(l.element_at(5) == 34)
    self.assertTrue(l.element_at(6) == -1)
    self.assertTrue(l.element_at(11236) == -1)

  def test_find(self):
    l = Listly([1, 4, 6, 17, 21, 34])
    self.assertTrue(l.find(6) == 2)
    self.assertTrue(l.find(34) == 5)
    self.assertTrue(l.find(37) == None)

  def test_find_empty(self):
    l = Listly([])
    self.assertTrue(l.find(6) == None)

  def test_find_with_duplicate(self):
    l = Listly([1, 4, 6, 6, 6, 8, 9])
    self.assertTrue(l.find(6) in (2, 3, 4))


if __name__ == '__main__':
  unittest.main()

