# https://www.careercup.com/question?id=5749533368647680
# Given the root of a binary tree containing integers, print the columns of the
# tree in order with the nodes in each column printed top-to-bottom. When two nodes
# share the same the position, they may be printed in either order.

# input
#        1
#      /   \
#     2     3
#    / \   / \
#   4   5 6   7

# output:
# 4, 2, 1, 5, 6, 3, 7
# or
# 4, 2, 1, 6, 6, 3, 7

# Here're the main ideas:
# - Store the columns in a hash table (col index -> columns)
# - Track min and max column indexes during tree traversal.
# - Explore the tree in layers with BFS and populate the hash table
# - Iter from min to max column index to print the columns in the right order

# Time: O(n)
# Space: O(n)

from Queue import Queue

tree = {
    'value': 1,
    'left': {
        'value': 2,
        'left': {
            'value': 4,
        },
        'right' : {
            'value': 5
        },
    },
    'right': {
        'value': 3,
        'left': {
            'value': 6,
        },
        'right' : {
            'value': 7
        },
    },
}

def print_tree_columns(n):
    columns = {}
    min_col = 0
    max_col = 0
    q = Queue()
    q.put((n, 0))

    while not q.empty():
        n, col = q.get()
        min_col = min(min_col, col)
        max_col = max(max_col, col)

        left_node = n.get('left')
        if left_node:
            q.put((left_node, col-1))

        right_node = n.get('right')
        if right_node:
            q.put((right_node, col+1))

        column = columns.setdefault(col, [])
        column.append(n['value'])

    for i in xrange(min_col, max_col+1):
        for v in columns[i]:
            print v

if __name__ == '__main__':
    print_tree_columns(tree)
