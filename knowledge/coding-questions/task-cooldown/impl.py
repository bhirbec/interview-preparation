# Task Cooldown Time
#
# You are given a list of tasks `tasks` that must be executed in the given order,
# and a cooldown `k`. Each time unit the CPU either runs the next pending task or
# stays idle. The same task cannot run twice within `k` time units of its previous
# run: after a task runs at time t, it may run again only at time t + k + 1 or
# later. When the next task is still cooling down, the CPU idles for that unit.
#
# Return the total number of time units needed to finish every task in order.
#
# Constraints:
#   - 0 <= len(tasks) <= 10^4
#   - 0 <= k <= 10^4
#   - tasks may be any hashable labels
#
# Examples:
#   tasks=[A, B, C, D],             k=3 -> 4    (A B C D)
#   tasks=[A, B, A, D],             k=3 -> 6    (A B . . A D)
#   tasks=[A, A, A, A],             k=3 -> 13   (A . . . A . . . A . . . A)
#   tasks=[A, B, C, A, C, B, D, A], k=4 -> 11   (A B C . . A . C B D A)


def task_cooldown_time(tasks, k):
  # TODO: implement
  raise NotImplementedError
