class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def display_forward(self):
        current = self.head

        while current:
            print(current.data, end=" ⇄ ")
            current = current.next

        print("None")

    def display_backward(self):
        if self.head is None:
            return

        current = self.head

        while current.next:
            current = current.next

        while current:
            print(current.data, end=" ⇄ ")
            current = current.prev

        print("None")

    def insert_beginning(self, data):
        new_node = Node(data)

        new_node.next = self.head

        if self.head:
            self.head.prev = new_node

        self.head = new_node

    def insert_end(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next:
            current = current.next

        current.next = new_node
        new_node.prev = current

    def insert_at(self, data, position):
        if position == 0:
            self.insert_beginning(data)
            return

        new_node = Node(data)
        current = self.head

        for _ in range(position - 1):
            if current is None:
                return

            current = current.next

        if current is None:
            return

        new_node.next = current.next
        new_node.prev = current

        if current.next:
            current.next.prev = new_node

        current.next = new_node

    def delete_beginning(self):
        if self.head is None:
            return

        self.head = self.head.next

        if self.head:
            self.head.prev = None

    def delete_end(self):
        if self.head is None:
            return

        if self.head.next is None:
            self.head = None
            return

        current = self.head

        while current.next:
            current = current.next

        current.prev.next = None

    def delete_value(self, value):
        if self.head is None:
            return

        current = self.head

        while current and current.data != value:
            current = current.next

        if current is None:
            return

        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next

        if current.next:
            current.next.prev = current.prev

    def search(self, value):
        current = self.head

        while current:
            if current.data == value:
                return True

            current = current.next

        return False

    def reverse(self):
        current = self.head

        while current:
            current.prev, current.next = current.next, current.prev

            if current.prev is None:
                self.head = current

            current = current.prev


dll = DoublyLinkedList()

dll.insert_end(10)
dll.insert_end(20)
dll.insert_end(30)

dll.display_forward()