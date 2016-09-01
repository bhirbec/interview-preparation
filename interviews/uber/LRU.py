
class LRU(object):

    def __init__(self, load, size):
        self._load = load
        self._size = size
        self._h = {}
        self._list = LinkedList()

    def get(self, key):
        node = self._h.get(key)
        if node is not None:
            self._list.move_front(node)
            return node.value

        if self._list.get_size() == self._size:
            self._list.delete_tail()

        node = Node(self._load(key))
        self._list.insert(node)
        self._h[key] = node
        return node.value

class LinkedList(object):
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def get_size(self):
        return self._size

    def move_front(self, node):
        if node is self._head:
            return

        prev_node = node.prev
        next_node = node.next

        node.prev = None
        node.next = self._head
        self._head.prev = node
        self._head = node

        if next_node is None:
            prev_node.next = next_node
            self._tail = prev_node
        else:
            prev_node.next = next_node
            next_node.prev = prev_node

    def insert(self, node):
        if self._head is None:
            self._head = node
            self._tail = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node
        self._size += 1

    def delete_tail(self):
        if self._tail is not None:
            prev_node = self._tail.prev
            prev_node.next = None
            self._tail = prev_node
            self._size -= 1

    def __str__(self):
        output = []
        n = self._head
        while n:
            output.append(n)
            n = n.next
        return '<=>'.join(str(n.value) for n in output)

class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


def main():
    lru = LRU(load=lambda x: x**1, size=5)
    print lru.get(1)
    print lru.get(2)
    print lru.get(3)
    print '*', lru._list

    print lru.get(1)
    print '*', lru._list

    print lru.get(4)
    print lru.get(5)
    print '*', lru._list

    print lru.get(1)
    print lru.get(6)
    print '*', lru._list

main()
