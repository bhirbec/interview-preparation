import unittest


class TestCircularQueue(unittest.TestCase):
  def test_starts_empty(self):
    q = CircularQueue(3)
    self.assertTrue(q.empty())
    self.assertFalse(q.full())
    self.assertEqual(q.size(), 0)
    self.assertEqual(q.capacity(), 3)

  def test_fifo_order(self):
    q = CircularQueue(3)
    q.enqueue('a')
    q.enqueue('b')
    q.enqueue('c')
    self.assertTrue(q.full())
    self.assertEqual(q.dequeue(), 'a')
    self.assertEqual(q.dequeue(), 'b')
    self.assertEqual(q.dequeue(), 'c')
    self.assertTrue(q.empty())

  def test_peek_does_not_remove(self):
    q = CircularQueue(2)
    q.enqueue(1)
    q.enqueue(2)
    self.assertEqual(q.peek(), 1)
    self.assertEqual(q.peek(), 1)
    self.assertEqual(q.size(), 2)

  def test_wraps_around_the_buffer(self):
    q = CircularQueue(3)
    q.enqueue('a')
    q.enqueue('b')
    q.enqueue('c')
    self.assertEqual(q.dequeue(), 'a')
    q.enqueue('d')
    self.assertTrue(q.full())
    self.assertEqual(q.dequeue(), 'b')
    self.assertEqual(q.dequeue(), 'c')
    self.assertEqual(q.dequeue(), 'd')
    self.assertTrue(q.empty())

  def test_many_wraps(self):
    q = CircularQueue(4)
    q.enqueue(0)
    q.enqueue(1)
    for value in range(2, 30):
      self.assertEqual(q.dequeue(), value - 2)
      q.enqueue(value)
    self.assertEqual(q.size(), 2)
    self.assertEqual(q.dequeue(), 28)
    self.assertEqual(q.dequeue(), 29)

  def test_enqueue_when_full_raises(self):
    q = CircularQueue(1)
    q.enqueue('only')
    with self.assertRaises(OverflowError):
      q.enqueue('too many')
    self.assertEqual(q.dequeue(), 'only')

  def test_dequeue_and_peek_when_empty_raise(self):
    q = CircularQueue(2)
    with self.assertRaises(IndexError):
      q.dequeue()
    with self.assertRaises(IndexError):
      q.peek()

  def test_reusable_after_draining(self):
    q = CircularQueue(2)
    q.enqueue(1)
    q.dequeue()
    self.assertTrue(q.empty())
    q.enqueue(2)
    q.enqueue(3)
    self.assertEqual(q.dequeue(), 2)
    self.assertEqual(q.dequeue(), 3)

  def test_capacity_of_one(self):
    q = CircularQueue(1)
    for value in range(5):
      q.enqueue(value)
      self.assertTrue(q.full())
      self.assertEqual(q.dequeue(), value)
      self.assertTrue(q.empty())

  def test_none_is_a_storable_value(self):
    q = CircularQueue(2)
    q.enqueue(None)
    self.assertEqual(q.size(), 1)
    self.assertFalse(q.empty())
    self.assertIsNone(q.dequeue())

  def test_invalid_capacity(self):
    with self.assertRaises(ValueError):
      CircularQueue(0)
    with self.assertRaises(ValueError):
      CircularQueue(-1)


if __name__ == '__main__':
  unittest.main()
