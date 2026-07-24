import unittest


def check_perm_of_palindrome(s):
    s = s.lower().replace(' ', '')

    chars = {}
    for c in s:
        chars[c] = chars.setdefault(c, 0) + 1

    print(chars)
    found_odd = False
    for counter in chars.values():
        if is_even(counter):
            continue

        if not found_odd:
            found_odd = True
        else:
            return False

    return True


def is_even(i):
    return (i & 1) == 0


class TestEven(unittest.TestCase):
    def test_is_even(self):
        self.assertTrue(is_even(-22))
        self.assertTrue(is_even(0))
        self.assertTrue(is_even(4))

    def test_is_odd(self):
        self.assertFalse(is_even(3))
        self.assertFalse(is_even(-19))


class TestPermOfPalindrome(unittest.TestCase):
    def test_ok(self):
        self.assertTrue(check_perm_of_palindrome('Tact Coa'))


if __name__ == '__main__':
    unittest.main()
