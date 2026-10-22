class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def display(self):
        current = self.head

        while current:
            print(current.data, end=" → ")
            current = current.next

        print("None")

    def insert_beginning(self, data):
        new_node = Node(data)

        new_node.next = self.head
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

    def delete_beginning(self):
        if self.head is None:
            return

        self.head = self.head.next

    def delete_end(self):
        if self.head is None:
            return

        if self.head.next is None:
            self.head = None
            return

        current = self.head

        while current.next.next:
            current = current.next

        current.next = None

    def delete_value(self, value):
        if self.head is None:
            return

        if self.head.data == value:
            self.head = self.head.next
            return

        current = self.head

        while current.next and current.next.data != value:
            current = current.next

        if current.next:
            current.next = current.next.next

    def search(self, value):
        current = self.head

        while current:
            if current.data == value:
                return True

            current = current.next

        return False

    def reverse(self):
        previous = None
        current = self.head

        while current:
            next_node = current.next
            current.next = previous

            previous = current
            current = next_node

        self.head = previous

ll = LinkedList()

ll.insert_end(10)
ll.insert_end(20)
ll.insert_end(30)

ll.display()

ll.insert_beginning(5)
ll.display()

ll.delete_beginning()
ll.display()

ll.delete_value(20)
ll.display()

ll.reverse()
ll.display()