# Queue From Stacks
#
# Implement a FIFO queue using only two stacks. The only operations you may
# perform on the internal stacks are push (list.append), pop (list.pop) on the
# last element, and emptiness/length checks — no indexing into the middle, no
# insert(0, ...).
#
# Implement the class below:
#   - enqueue(value): add value to the back of the queue.
#   - dequeue(): remove and return the value at the front of the queue;
#     raise IndexError if the queue is empty.
#   - size(): number of elements currently in the queue.
#
# Each element should be moved between the stacks at most once, making both
# operations amortized O(1).
#
# Examples:
#   q = QueueFromStacks()
#   q.enqueue(1); q.enqueue(2); q.enqueue(3)
#   q.dequeue() == 1
#   q.enqueue(4)
#   q.dequeue() == 2 ; q.dequeue() == 3 ; q.dequeue() == 4


class QueueFromStacks:
  def __init__(self):
    self.inbox = []
    self.outbox = []

  def enqueue(self, value):
    # TODO: implement
    raise NotImplementedError

  def dequeue(self):
    # TODO: implement
    raise NotImplementedError

  def size(self):
    # TODO: implement
    raise NotImplementedError
