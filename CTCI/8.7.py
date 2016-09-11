
def perms(chars):
    n = len(chars)
    buff = [''] * n

    def _f(i):
        if i == n:
            yield ''.join(buff)
            return

        for j in xrange(n):
            if buff[j] == '':
                buff[j] = chars[i]
                for p in _f(i+1):
                    yield p
                buff[j] = ''

    return _f(0)

def main():
    for p in perms('abcde'):
        print p

main()
