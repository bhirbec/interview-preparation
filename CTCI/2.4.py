
class Node():
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node

def main():
    n = Node(70, Node(134, Node(3, Node(1, Node(10, Node(9))))))

    n = partition(n, 10)
    while n:
        print n.value
        n = n.next_node

def partition(n, k):
    left, right = None, None
    while n:
        next_node = n.next_node

        if n.value >= k:
            n.next_node = right
            right = n
        else:
            n.next_node = left
            left = n

        n = next_node

    if right is None:
        return left
    elif left is None:
        return right

    n = left
    while n.next_node:
        n = n.next_node

    n.next_node = right
    return left

main()
