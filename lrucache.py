class Node:
    def __init__(self, key, val):
        # This Creates a node storing key/value and prev/next pointers; TC: O(1), SC: O(1).
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        # This Initializes the hash map and dummy nodes ; TC: O(1), SC: O(1).
        self.capacity = capacity
        self.cache = {}

        self.head = Node(0, 0)
        self.tail = Node(0, 0)

        self.head.next = self.tail
        self.tail.prev = self.head

    def insert(self, node):
        # This function Inserts a node after head as MRU using pointer updates; TC: O(1), SC: O(1).
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def remove(self, node):
        # This function Removes a node by connecting its neighbors, enabling O(1) deletion; TC: O(1), SC: O(1).
        node.prev.next = node.next
        node.next.prev = node.prev

    def move_to_front(self, node):
        # Marks an accessed/updated node as MRU; TC: O(1), SC: O(1).
        self.remove(node)
        self.insert(node)

    def get(self, key: int) -> int:
        # This finds key in cache and updates its usage order; TC: O(1) average, SC: O(1).
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self.move_to_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        # Updates existing keys or deletes the LRU before inserting a new key; TC: O(1) average, SC: O(1) auxiliary.
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self.move_to_front(node)
            return

        if len(self.cache) >= self.capacity:
            lru = self.tail.prev
            self.remove(lru)
            del self.cache[lru.key]

        node = Node(key, value)
        self.cache[key] = node
        self.insert(node)

    ## this function is used to display the list
    def display(self):
        # Traverses and prints the cache from MRU to LRU for debugging; TC: O(n), SC: O(n).
        curr = self.head.next
        items = []

        while curr != self.tail:
            items.append(f"({curr.key}, {curr.val})")
            curr = curr.next

        print("MRU ->", " <-> ".join(items), "<- LRU")



lru = LRUCache(2)

lru.put(1, 10)
lru.put(2, 20)
lru.put(3, 30)
lru.display()
print(lru.get(1))
print(lru.get(2))
lru.display()

lru.put(4, 40)
lru.display()