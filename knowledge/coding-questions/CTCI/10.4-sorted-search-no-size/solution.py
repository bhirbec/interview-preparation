class Listy(object):
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
        # overshot the end, so shrink the range by half
        mid = int((last + first) / 2)
        return _f(first, mid)
      elif value > last_val:
        # target is beyond the current range, so double the window
        return _f(last + 1, last * 2)
      else:
        mid = int((last + first) / 2)
        return _f(first, mid)

    return _f(0, 2)
