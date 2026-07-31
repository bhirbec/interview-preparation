def task_cooldown_time(tasks, k):
  last_run = {}
  i = 0
  t = 0
  n = len(tasks)
  while i < n:
    task = tasks[i]
    if task not in last_run or t - last_run[task] > k:
      last_run[task] = t
      i += 1
    t += 1
  return t
