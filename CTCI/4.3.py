from Queue import Queue


def main():
    tree = {
        'value': 1,
        'left': {
            'value': 2,
            'left': {
                'value': 4
            },
            'right': {
                'value': 5
            }
        },
        'right': {
            'value': 3,
            'left': {
                'value': 6
            },
            'right': {
                'value': 7
            }
        }
    }

    for layer in get_layers(tree):
        print layer


class LinkedList():

    class _Node():
        def __init__(self, value, next_node=None):
            self.value = value
            self.next_node = next_node

    def __init__(self, value):
        n = self._Node(value)
        self._head = n
        self._tail = n

    def append(self, value):
        n = self._Node(value)
        self._tail.next_node = n
        self._tail = n

    def insert(self, value):
        n = self._Node(value, self._head)
        self._head = n

    def __str__(self):
        return ', '.join(str(v) for v in self)

    def __iter__(self):
        n = self._head
        while n is not None:
            yield n.value
            n = n.next_node


def get_layers(n):
    q = Queue()
    q.put((n, 0))
    layers = []

    while not q.empty():
        n, d = q.get()

        if len(layers) == d:
            layers.append(LinkedList(n['value']))
        else:
            l = layers[d]
            l.insert(n['value'])

        if 'left' in n:
            q.put((n['left'], d+1))

        if 'right' in n:
            q.put((n['right'], d+1))

    return layers


if __name__ == '__main__':
    main()
