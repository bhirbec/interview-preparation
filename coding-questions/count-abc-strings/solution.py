from functools import lru_cache


def count_abc_strings(n):
  @lru_cache(None)
  def count_from(pos, used_b, run_c):
    if pos == n:
      return 1

    total = count_from(pos + 1, used_b, 0)          # place 'a'
    if used_b == 0:
      total += count_from(pos + 1, 1, 0)            # place 'b'
    if run_c < 2:
      total += count_from(pos + 1, used_b, run_c + 1)  # place 'c'
    return total

  return count_from(0, 0, 0)
