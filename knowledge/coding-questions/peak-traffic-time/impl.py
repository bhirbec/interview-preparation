# Peak Traffic Time
#
# A server log records one session per user visit as a pair (start, end): the
# session is active from time `start` (inclusive) up to `end` (exclusive).
#
# You are given a list of such sessions, in no particular order. Return the
# earliest time at which the number of simultaneously active sessions is at its
# maximum.
#
# Constraints:
#   - 1 <= len(sessions)
#   - 0 <= start < end for every session; times are integers
#
# Examples:
#   peak_traffic_time([(0, 10), (3, 15), (8, 29), (4, 14)]) == 8
#     # at t=8 all four sessions are active — the daily peak
#   peak_traffic_time([(0, 1), (2, 3)]) == 0
#     # concurrency never exceeds 1; the earliest such time is 0
#   peak_traffic_time([(0, 5), (5, 10)]) == 0
#     # [start, end) — a session ending at 5 does not overlap one starting at 5


def peak_traffic_time(sessions):
  # TODO: implement
  raise NotImplementedError
