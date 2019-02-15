
# unival tree
#    1
# 1  1  1

# not a unival
#    1
# 1     1
#          2

#3 unival subtrees
#    1
# 1     1

# 2 unival subtrees
#     1(2, 0)
# 1(1, 1)    1(1, 0)
#              2(1 , 1)


class Node(object):
    def __init__(self, value):
        self.value = value
        self.children = []
        self.is_unival_tree = False
        self.nb_unival_tree = 0

    def add_child(self, value):
        ...


def is_unival_tree(root):
    ref_value = root.value

    def _dfs(n):
        if n.value != ref_value:
            return False

        for child in n.children:
            if not _dfs(child)
                return False

        return True

    return _dfs(root)

# 1 (2, 0)
# 2 (2, 1)
# 2 (1, 1)

def nb_unival_tree(root):
    def _dfs(n):
        if not n.children:
            return 1, 1

        node_unival_tree = 0
        node_is_unival = True

        for child in n.children:
            is_unival, nb_unival = dfs(child)
            node_unival_tree += nb_unival
            node_is_unival = node_is_unival and is_unival and n.value == child.value

        if node_is_unival:
            node_unival_tree += 1

        return node_unival_tree, node_is_unival

    return _dfs(root)


