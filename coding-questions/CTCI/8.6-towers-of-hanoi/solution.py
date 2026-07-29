def solve_hanoi(n):
  towers = {
    'A': list(range(n, 0, -1)),
    'B': [],
    'C': [],
  }
  moves = []

  def move_top(origin, dest):
    disk = towers[origin].pop()
    # A disk may never sit on a smaller one.
    assert not towers[dest] or towers[dest][-1] > disk
    towers[dest].append(disk)
    moves.append((origin, dest))

  def move_disks(k, origin, buff, dest):
    if k == 1:
      move_top(origin, dest)
      return

    move_disks(k - 1, origin, dest, buff)
    move_top(origin, dest)
    move_disks(k - 1, buff, origin, dest)

  if n > 0:
    move_disks(n, 'A', 'B', 'C')

  return moves
