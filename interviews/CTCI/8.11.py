COINS = 1, 5, 10, 25

def count_repr(n):
    cache = {}

    def f(n):
        hit = cache.get(n)
        if hit is not None:
            return hit

        s = 0
        for c in COINS:
            if n >= c:
                s += f(n - c) + 1

        cache[n] = s
        return s

    return f(n)

print count_repr(100)
