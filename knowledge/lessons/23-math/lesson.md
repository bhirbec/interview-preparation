# Math & Numbers

Number problems reward **exact integer thinking**: integer division and modulo
for digits and grouping, divisors and primes for structure, and counting
arguments that replace brute force with a formula.

## Integer division & digits

- Group k-sized buckets with ceiling division: `(n + k - 1) // k` — no floats.
- Peel digits with `n % 10` / `n //= 10`; or process the number one **digit
  position** at a time (count patterns per position instead of per number —
  that's how you count digit occurrences up to n in O(log n)).

```python
# nth digit-position analysis: how many '2's does position p contribute?
# split n into higher | current | lower parts around position p
higher, cur, lower = n // (p * 10), (n // p) % 10, n % p
```

## Divisors & primes

Enumerate divisors in O(√n): every divisor `d ≤ √n` pairs with `n // d`. Sieve
of Eratosthenes for primes up to n in O(n log log n). gcd via `math.gcd`;
`lcm(a, b) = a * b // gcd(a, b)`.

## Counting over simulating

Before simulating, ask if a closed form exists — sums of ranges, symmetry
("each pair counted twice"), or complementary counting (total minus the ones
that violate). Interviewers love an O(1)/O(log n) answer to an "obviously
O(n)" problem.

## The essentials

Python ints never overflow, but say where 32/64-bit code would. Beware floats:
`(a + b) / 2` and `10 ** 0.5` introduce error — stay in integers (`//`,
`math.isqrt`). Check n = 0, negatives, and exact boundaries (a year divisible
by 100 is the *last* of its century, not the first of the next).
