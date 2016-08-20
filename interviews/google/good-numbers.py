# https://www.careercup.com/question?id=5751843230580736

# Let "t" be a good number if "t" can be written as sum of 2 cubes in at least 2 distinct ways.
# Given n, write a method which prints all good numbers up to and including n.

# Time: O(n^2) Space: O(n)
def good_numbers(n):
    counts = [0 for _ in xrange(n+1)]
    n_sqrt = int(n**0.5)

    for x in xrange(n_sqrt+1):
        x_squared = x**2
        for y in xrange(x, n_sqrt+1):
            s = x_squared + y**2
            # TODO: can we remove this if statement?
            if s > n:
                break
            counts[s] += 1

    for i, c in enumerate(counts):
        if c > 1:
            print i

good_numbers(2900)
