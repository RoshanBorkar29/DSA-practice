class Node:
    def __init__(self,data):
        self.data=data
        self.next=None


class Stack:
    def __init__(self):
        self.top=None
    def push(self,data):
        new_node=Node(data)
        new_node.next=self.top
        self.top=new_node
    def pop(self):
        if self.top is None:
            return None
        data=self.top.data
        self.top=self.top.next
        return data

    def peek(self):
        if  self.top is None:
            return None

        return self.top.data

    def is_empty(self):
        return self.top is None

   
    def display(self):
       curr=self.top
       while curr is not None:
           print(curr.data,end=" ->")
           curr=curr.next

       print("None")


s = Stack()

s.push(10)
s.push(20)
s.push(30)

s.display()
print(s.peek())
print(s.pop())
print(s.pop())
