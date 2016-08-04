funcs = {
    '^': lambda a, b: int(a) ^ int(b),
    '|': lambda a, b: int(a) or int(b),
    '&': lambda a, b: int(a) and int(b),
}

def count_eval(expr, result):
    memo = {}

    def _count_eval(expr, result):
        if len(expr) == 1:
            return 1 if int(expr) == result else 0

        key = expr, result
        hit = memo.get(key)
        if hit is not None:
            return hit

        s = 0
        for left, op, right in split(expr):
            f = funcs[op]

            for r1, r2 in ((0, 0), (0, 1), (1, 0), (1, 1)):
                if f(r1, r2) == result:
                    s += count_eval(left, r1) * count_eval(right, r2)

        memo[key] = s
        return s

    return _count_eval(expr, result)

def split(expr):
    n = len(expr)
    for i in xrange(1, n, 2):
        yield expr[0:i], expr[i], expr[i+1:]

expr = '1^0|0|1'
print count_eval(expr, 0)

expr = '0&0&0&1^1|0'
print count_eval(expr, 1)
