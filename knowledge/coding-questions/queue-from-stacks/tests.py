import unittest


class TestQueueFromStacks(unittest.TestCase):
  def test_fifo_order(self):
    q = QueueFromStacks()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    self.assertEqual([q.dequeue(), q.dequeue(), q.dequeue()], [1, 2, 3])

  def test_interleaved_operations(self):
    q = QueueFromStacks()
    q.enqueue(1)
    q.enqueue(2)
    self.assertEqual(q.dequeue(), 1)
    q.enqueue(3)
    self.assertEqual(q.dequeue(), 2)
    self.assertEqual(q.dequeue(), 3)

  def test_dequeue_empty_raises(self):
    q = QueueFromStacks()
    with self.assertRaises(IndexError):
      q.dequeue()

  def test_dequeue_after_draining_raises(self):
    q = QueueFromStacks()
    q.enqueue(1)
    q.dequeue()
    with self.assertRaises(IndexError):
      q.dequeue()

  def test_size_tracks_both_stacks(self):
    q = QueueFromStacks()
    self.assertEqual(q.size(), 0)
    q.enqueue(1)
    q.enqueue(2)
    self.assertEqual(q.size(), 2)
    q.dequeue()             # forces the flip; one element remains
    self.assertEqual(q.size(), 1)
    q.enqueue(3)
    self.assertEqual(q.size(), 2)

  def test_large_sequence_stays_fifo(self):
    q = QueueFromStacks()
    out = []
    for i in range(100):
      q.enqueue(i)
      if i % 3 == 2:
        out.append(q.dequeue())
    while q.size():
      out.append(q.dequeue())
    self.assertEqual(out, list(range(100)))


if __name__ == '__main__':
  unittest.main()
