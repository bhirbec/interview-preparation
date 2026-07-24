


def countPalindromes(s):
    return sum(1 for substr in iter_substr(s) if is_palindrom(substr))

def iter_substr(s):
    n = len(s)
    for i in range(0, n):
        for j in range(i+1, n+1):
            yield s[i:j]

def is_palindrom(s):
    n = len(s)
    for i in range(int(n / 2)):
        if s[i] != s[n- i - 1]:
            return False
    return True

# print is_palindrom('a')
# print countPalindromes('abccba')


def countPalindromes(s):
    # WIP
    n = len(s)
    mid = int(n / 2)
    counter = 0

    for i in range(n):
        for diff in range(mid+1):
            before = i - diff
            after = i + diff
            if before < 0 or after > n - 1:
                break
            print(s[before:after+1])
            if s[before] == s[after]:
                counter += 1
            else:
                break

    return counter


# print is_palindrom('a')
print(countPalindromes('abccba'))
