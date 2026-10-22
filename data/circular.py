class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class CircularLinkedList:
    def __init__(self):
        self.head = None

    def display(self):
        if self.head is None:
            print("Empty")
            return

        current = self.head

        while True:
            print(current.data, end=" → ")

            current = current.next

            if current == self.head:
                break

        print("(back to head)")

    def insert_beginning(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            new_node.next = self.head
            return

        current = self.head

        while current.next != self.head:
            current = current.next

        new_node.next = self.head
        current.next = new_node
        self.head = new_node

    def insert_end(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            new_node.next = self.head
            return

        current = self.head

        while current.next != self.head:
            current = current.next

        current.next = new_node
        new_node.next = self.head

    def insert_at(self, data, position):
        if position == 0:
            self.insert_beginning(data)
            return

        if self.head is None:
            return

        new_node = Node(data)
        current = self.head

        for _ in range(position - 1):
            current = current.next

            if current == self.head:
                return

        new_node.next = current.next
        current.next = new_node

    def delete_beginning(self):
        if self.head is None:
            return

        if self.head.next == self.head:
            self.head = None
            return

        current = self.head

        while current.next != self.head:
            current = current.next

        self.head = self.head.next
        current.next = self.head

    def delete_end(self):
        if self.head is None:
            return

        if self.head.next == self.head:
            self.head = None
            return

        current = self.head

        while current.next.next != self.head:
            current = current.next

        current.next = self.head

    def delete_value(self, value):
        if self.head is None:
            return

        if self.head.data == value:
            self.delete_beginning()
            return

        current = self.head

        while current.next != self.head:
            if current.next.data == value:
                current.next = current.next.next
                return

            current = current.next

    def search(self, value):
        if self.head is None:
            return False

        current = self.head

        while True:
            if current.data == value:
                return True

            current = current.next

            if current == self.head:
                break

        return False


cll = CircularLinkedList()

cll.insert_end(10)
cll.insert_end(20)
cll.insert_end(30)

cll.display()