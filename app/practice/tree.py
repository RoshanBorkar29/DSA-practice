from collections import deque


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def preorder(root):
    if root is None:
        return

    print(root.data, end=" ")
    preorder(root.left)
    preorder(root.right)


def level_order(root):
    if root is None:
        return

    queue = deque([root])

    while queue:
        node = queue.popleft()

        print(node.data, end=" ")

        if node.left:
            queue.append(node.left)

        if node.right:
            queue.append(node.right)


# BST insertion
def insert(root, value):
    if root is None:
        return TreeNode(value)

    if root.data > value:
        root.left = insert(root.left, value)

    elif root.data < value:
        root.right = insert(root.right, value)

    return root


# BST search
def search(root, value):
    if root is None:
        return False

    if root.data == value:
        return True

    if root.data > value:
        return search(root.left, value)

    return search(root.right, value)


# Find a node in a GENERAL binary tree
def find_node(root, value):

    if root is None:
        return None

    queue = deque([root])

    while queue:

        node = queue.popleft()

        if node.data == value:
            return node

        if node.left:
            queue.append(node.left)

        if node.right:
            queue.append(node.right)

    return None


# Find deepest node + its parent
def deepest_node(root):

    queue = deque([(root, None)])

    deepest = None
    parent = None

    while queue:

        node, node_parent = queue.popleft()

        deepest = node
        parent = node_parent

        if node.left:
            queue.append((node.left, node))

        if node.right:
            queue.append((node.right, node))

    return parent, deepest


# General Binary Tree deletion
def delete(root, value):

    if root is None:
        return None

    target = find_node(root, value)

    if target is None:
        print("Value not present, can't be deleted!")
        return root

    parent, deepest = deepest_node(root)

    # Only one node
    if parent is None:
        return None

    # Replace target with deepest node
    target.data = deepest.data

    # Remove deepest node
    if parent.left == deepest:
        parent.left = None
    else:
        parent.right = None

    return root


# Build BST
root = None

values = [10, 5, 20, 3, 7, 15, 25]

for val in values:
    root = insert(root, val)


print("Before deletion:")
print("Preorder:")
preorder(root)

print("\nLevel order:")
level_order(root)

print("\n\nDeleting 5...")
root = delete(root, 5)

print("\nAfter deletion:")
print("Preorder:")
preorder(root)

print("\nLevel order:")
level_order(root)