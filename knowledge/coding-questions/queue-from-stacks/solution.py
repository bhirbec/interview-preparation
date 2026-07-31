class QueueFromStacks:
  def __init__(self):
    self.inbox = []
    self.outbox = []

  def enqueue(self, value):
    self.inbox.append(value)

  def dequeue(self):
    if not self.outbox:
      # Flip the inbox once its reversal is actually needed.
      while self.inbox:
        self.outbox.append(self.inbox.pop())
    if not self.outbox:
      raise IndexError("dequeue from empty queue")
    return self.outbox.pop()

  def size(self):
    return len(self.inbox) + len(self.outbox)
