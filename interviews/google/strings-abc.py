# https://www.careercup.com/question?id=5717453712654336

# Given a length n, return the number of strings of length n that can be made up of the letters
# 'a', 'b', and 'c', where there can only be a maximum of 1 'b's and can only have up to two consecutive 'c's

# Example:
# find_strings(3) returns 19 since the possible combinations are:
# aaa,aab,aac,aba,abc,aca,acb,baa,bac,bca,caa,cab,cac,cba,cbc,acc,bcc,cca,ccb

# Invalid combinations are:
# abb,bab,bba,bbb,bbc,bcb,cbb,ccc


def find_strings(n):
    buf = [''] * n
    chars = 'a', 'b', 'c'

    def _f(p, count_b, consecutive_c):
        if count_b > 1 or consecutive_c > 2:
            return

        if p == n:
            print ''.join(buf)
            return

        buf[p] = 'a'
        _f(p+1, count_b, 0)

        buf[p] = 'b'
        _f(p+1, count_b+1, 0)

        buf[p] = 'c'
        _f(p+1, count_b, consecutive_c+1)

    _f(0, 0, 0)

find_strings(3)
