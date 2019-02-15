import unittest


def find(arr, value):
    r = find_rotation_point(arr)
    if arr[0] <= value <= arr[r]:
        return binary_search(arr, value, 0, r)
    else:
        return binary_search(arr, value, r, len(arr) - 1)


def find_rotation_point(arr):
    def _f(arr, start, end):
        if end - start <= 1:
            return end

        mid = int((end + start) / 2)

        if arr[mid] > arr[end]:
            # right side contains rotation point.
            return _f(arr, mid, end)
        else:
            # left side contains rotation point
            return _f(arr, start, mid)

    return _f(arr, 0, len(arr) - 1)


def binary_search(arr, value, start, end):
    if end < start:
        return None

    mid = int((end + start) / 2)
    if arr[mid] == value:
        return mid
    elif arr[mid] > value:
        return binary_search(arr, value, start, mid-1)
    else:
        return binary_search(arr, value, mid+1, end)


class TestSearch(unittest.TestCase):
    def test_find_rotation_point(self):
        arr = [15, 16, 19, 20, 25, 1, 3, 4, 5, 7, 10, 14]
        idx = find_rotation_point(arr)
        self.assertTrue(idx == 5)

    def test_find(self):
        arr = [15, 16, 19, 20, 25, 1, 3, 4, 5, 7, 10, 14]
        idx = find(arr, 5)
        self.assertTrue(idx == 8)


if __name__ == '__main__':
    unittest.main()

