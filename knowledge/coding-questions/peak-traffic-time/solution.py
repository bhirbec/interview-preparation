def peak_traffic_time(sessions):
  events = []
  for start, end in sessions:
    events.append((start, 1))
    events.append((end, -1))
  # Ends sort before starts at the same time: [start, end) intervals that only
  # touch do not overlap.
  events.sort(key=lambda e: (e[0], e[1]))

  current = best = 0
  best_time = None
  for time, delta in events:
    current += delta
    if current > best:
      best = current
      best_time = time
  return best_time
