import unittest


class TestDivisorFreeTeamSize(unittest.TestCase):
  def test_single_player(self):
    self.assertEqual(divisor_free_team_size(1), 2)

  def test_two_players(self):
    self.assertEqual(divisor_free_team_size(2), 2)

  def test_three_players(self):
    self.assertEqual(divisor_free_team_size(3), 3)

  def test_four_players(self):
    self.assertEqual(divisor_free_team_size(4), 3)

  def test_ten_players(self):
    self.assertEqual(divisor_free_team_size(10), 6)

  def test_odd_n(self):
    # {5,6,7,8,9} is the largest clean team, size 5.
    self.assertEqual(divisor_free_team_size(9), 6)

  def test_large_n(self):
    self.assertEqual(divisor_free_team_size(1000000), 500001)

  def test_matches_brute_force(self):
    # Cross-check the formula against an exhaustive antichain search.
    def brute(n):
      best = 0
      players = list(range(1, n + 1))
      for mask in range(1, 1 << n):
        team = [players[i] for i in range(n) if mask & (1 << i)]
        if all(b % a != 0 for i, a in enumerate(team)
               for b in team[i + 1:]):
          best = max(best, len(team))
      return best + 1

    for n in range(1, 11):
      self.assertEqual(divisor_free_team_size(n), brute(n))


if __name__ == '__main__':
  unittest.main()
