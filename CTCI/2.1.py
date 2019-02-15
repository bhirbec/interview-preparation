import unittest


class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None

    def append(self, value):
        n = self
        while n.next:
            n = n.next
        n.next = Node(value)

    def dedup(self):
        ht = {}
        n = self

        while n.next:
            if n.value in ht:
                previous = n
            else:
                previous = n
                ht[n.value] = True
                previous.next = n

            n = n.next
