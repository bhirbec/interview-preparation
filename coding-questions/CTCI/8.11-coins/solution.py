COINS = (25, 10, 5, 1)


def count_repr(n):
  cache = {}

  def f(amount, index):
    if amount == 0:
      return 1
    if index == len(COINS):
      return 0

    key = (amount, index)
    hit = cache.get(key)
    if hit is not None:
      return hit

    coin = COINS[index]
    ways = 0
    qty = 0
    while coin * qty <= amount:
      ways += f(amount - coin * qty, index + 1)
      qty += 1

    cache[key] = ways
    return ways

  return f(n, 0)
