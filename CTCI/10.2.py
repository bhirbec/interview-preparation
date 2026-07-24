import unittest


def sort_anagram(arr):
    radix_table = {}
    for w in arr:
        key = ''.join(sorted(w))
        radix_table.setdefault(key, [])
        radix_table[key].append(w)

    output = []
    for words in radix_table.values():
        for w in words:
            output.append(w)

    return output


class TestSort(unittest.TestCase):
    def test_sort_anagram(self):
        arr = ['add', 'kii', 'dad', 'iki']
        sorted_arr = sort_anagram(arr)
        self.assertTrue(sorted_arr == ['add', 'dad', 'kii', 'iki'])


if __name__ == '__main__':
    unittest.main()
