# Fibonacci Numbers

Sources:
- [YouTube - MIT OpenCourseWare](https://youtu.be/OQ5jsbhAv_M?t=306)

Number of rabbits you have on day N if they reproduce.

```
F1 = F2 = 1
Fn = Fn-1 + Fn-2
```

## Naive Recursive Algorithm

```
Fib(n):
	if n <= 2
		f = 1
	else
		f = Fib(n-1) + Fib(n-2)
	return f
```

```
T(n) = T(n-1) + T(n-2) + O(1)
T(n) >= 2 * T(n-2)
      = Theta(2^(n/2))
```

Exponential Time :/

## Memoized Algorithm

```
memo = {}

Fib(n):
	if <= 2:
		f = 1
	elif n in memo:
		f = memo[n]
	else:
		f = Fib(n-2) + Fib(n-1)
		memo[n] = f
	return f
```

By drawing the recursion tree we can see how we cut some work:
- Fib(k) only recurses the first time it's called for any k
- memoized calls cost O(1)
- number of memoized calls is n
- non-recursive calls cost O(1)
- total cost O(n)

Generalization:
- memoization + reuse + guess
- Running time = # of subproblem + time per subproblems (don't count memoized recursive calls)

## Bottom-up Algo

```
Fib(n):
	fib = {}
	if k in range(1, n+1):
		if n <= 2:
			return 1
		else:
			fib[k] = fib[k-1] + fib[k-2]
	return fib[n]
```

Generalization of bottom-up:
- exact same computation than the recursive
- topological sort of subproblem dependency DAG (directed acyclic graph)
- save space (for Fibonacci we only need to remember the last 2 values)

DAG:
```
  /----------------\
Fn-3 --> Fn-2 --> Fn-1 --> Fn
			\-------------/
```
