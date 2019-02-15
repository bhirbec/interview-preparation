import unittest


def is_permutation_naive(s1, s2):
    '''
    Return True if s1 is a permutation of s2. Otherwise return False.
    Running Time O(nlogn)
    Space O(n)
    '''
    if len(s1) != len(s2):
        return False

    return sorted(s1) == sorted(s2)


def is_permutation(s1, s2):
    '''
    Return True if s1 is a permutation of s2. Otherwise return False.
    Running Time O(n)
    Space O(n)
    '''
    if len(s1) != len(s2):
        return False

    chars = {}
    for c in s1:
        chars[c] = chars.setdefault(c, 0) + 1

    for c in s2:
        if c not in chars:
            return False
        chars[c] -= 1

    return all(v == 0 for v in chars.values())


class TestPerm(unittest.TestCase):

    def test_is_permutation_length(self):
        self.assertFalse(is_permutation('sew', 's'))

    def test_is_permutation_small(self):
        self.assertTrue(is_permutation('sew', 'wse'))

    def test_is_permutation_big(self):
        self.assertTrue(is_permutation('sewJdifjldifjdkwdkdsk', 'skeJdjwdkkdsilwjdiffd'))

    def test_is_permutation_notok(self):
        self.assertFalse(is_permutation('sew', 'wwse'))

if __name__ == '__main__':
    unittest.main()
