# First Bad Version
#
# A product has versions numbered 1 to n. At some version the build went bad,
# and every version after a bad one is also bad (so the versions look like
# good, good, ..., good, bad, bad, ..., bad). You are given `n` and a function
# `is_bad(version) -> bool`. It is guaranteed at least one version is bad.
#
# Return the number of the first bad version. Calls to `is_bad` are expensive:
# use O(log n) calls, not a linear scan.
#
# Constraints:
#   - 1 <= n <= 2^31 - 1
#   - is_bad is monotone: if is_bad(v) then is_bad(w) for every w > v
#
# Examples:
#   n = 5, versions 1-3 good, 4-5 bad  -> 4
#   n = 1, version 1 bad               -> 1


def first_bad_version(n, is_bad):
  # TODO: implement
  raise NotImplementedError
