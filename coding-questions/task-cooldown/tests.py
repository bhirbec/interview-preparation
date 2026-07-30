import unittest


class TestTaskCooldownTime(unittest.TestCase):
  def test_all_distinct(self):
    self.assertEqual(task_cooldown_time(['A', 'B', 'C', 'D'], 3), 4)

  def test_one_repeat(self):
    self.assertEqual(task_cooldown_time(['A', 'B', 'A', 'D'], 3), 6)

  def test_all_same(self):
    self.assertEqual(task_cooldown_time(['A', 'A', 'A', 'A'], 3), 13)

  def test_interleaved(self):
    tasks = ['A', 'B', 'C', 'A', 'C', 'B', 'D', 'A']
    self.assertEqual(task_cooldown_time(tasks, 4), 11)

  def test_empty(self):
    self.assertEqual(task_cooldown_time([], 3), 0)

  def test_single_task(self):
    self.assertEqual(task_cooldown_time(['A'], 5), 1)

  def test_zero_cooldown(self):
    # With k=0 a task may run on the very next unit, so no idling ever occurs.
    self.assertEqual(task_cooldown_time(['A', 'A', 'A'], 0), 3)

  def test_repeat_never_needs_idle(self):
    # The repeat is already far enough apart, so no idle units are inserted.
    self.assertEqual(task_cooldown_time(['A', 'B', 'C', 'D', 'A'], 3), 5)

  def test_large_cooldown(self):
    self.assertEqual(task_cooldown_time(['A', 'A'], 10), 12)


if __name__ == '__main__':
  unittest.main()
