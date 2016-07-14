

def recursive_fib(n):
    memo = {}

    def _fib(n):
        if n <= 2:
            return 1
        elif n in memo:
            f = memo[n]
        else:
            f = _fib(n-2) + _fib(n-1)
            memo[n] = f
        return f

    return _fib(n)

def bottom_up_fib(n):
    memo = {}
    for k in range(1, n+1):
        if k <= 2:
            memo[k] = 1
        else:
            memo[k] = memo[k-2] + memo[k-1]
    return memo[n]

print recursive_fib(10)
print bottom_up_fib(10)
