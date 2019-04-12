class Queue:
    def __init__(self):
        self.data = []

    def is_empty(self):
        return self.data == []

    def enqueue(self, value):
        self.data.insert(0, value)

    def dequeue(self):
        return self.data.pop()