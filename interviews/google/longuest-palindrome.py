# https://www.careercup.com/question?id=5631060781039616

# Given a string return the longest palindrome that can be constructed by removing or shuffling characters.

# Example:
# 'aha'  -> 'aha'
# 'ttaatta' -> ' ttaaatt'
# 'abc' -> 'a' or 'b' or 'c'
# 'gggaaa' -> 'gaaag' or 'aggga'

# Note if there are multiple correct answers you only need to return 1 palindrome.

def main(s):
    '''
    Time complexity: O(n)
    Space complexity: O(n)

    - set S = a map that will stores number of occurences per char
    - for each c in s:
        - S[c] += 1
        - if S[c] == 2 then we can keep the char
    - the map can only have 0 or 1. We keep the first char with 1 occurence.
    '''
    chars = []
    char_counts = {}

    for c in s:
        if c not in char_counts:
            char_counts[c] = 0
        char_counts[c] += 1

        if char_counts[c] == 2:
            chars.append(c)
            char_counts[c] = 0

    middle = ''
    for c, count in char_counts.iteritems():
        if count > 0:
            middle = c
            break

    return ''.join(chars) + middle + '' .join(reversed(chars))

print main(s="baazzxkkkuiuoioiikaab")
