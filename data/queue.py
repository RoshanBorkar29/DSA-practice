class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, data):
        self.queue.append(data)

    def dequeue(self):
        if not self.queue:
            return None

        return self.queue.pop(0)

    def peek(self):
        if not self.queue:
            return None

        return self.queue[0]

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

    def display(self):
        print(self.queue)

q = Queue()

q.enqueue(10)
q.enqueue(20)
q.enqueue(30)
q.enqueue(40)

q.display()

print("Front:", q.peek())

print("Removed:", q.dequeue())
print("Removed:", q.dequeue())

q.display()

print("Front:", q.peek())
print("Size:", q.size())