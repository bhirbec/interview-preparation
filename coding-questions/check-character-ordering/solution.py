def check_ordering(text, ordering):
  wanted = set(ordering)
  collapsed = []
  for c in text:
    if c in wanted and (not collapsed or collapsed[-1] != c):
      collapsed.append(c)
  return ''.join(collapsed) == ordering
