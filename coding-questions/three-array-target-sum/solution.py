def target_sum(a, b, c, target):
  pair_sums = {}
  for x in a:
    for y in b:
      pair_sums.setdefault(x + y, []).append((x, y))

  triples = []
  for z in c:
    for x, y in pair_sums.get(target - z, []):
      triples.append([x, y, z])
  return triples
