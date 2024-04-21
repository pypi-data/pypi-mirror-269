from stackNqueue.DoublyCircularLinkedList import *

class Queue(DoublyCircularLinkedList):
    def __init__(self):
        super().__init__()
        self.__front = self.head
        self.__rear = self.tail

    def enqueue(self, x):
        super().insert(0, x)
        self.__front = self.head.next
        self.__rear = self.head.prev
    
    def dequeue(self):
        rtn = super().pop()
        self.__front = self.head.next
        self.__rear = self.head.prev

    def rear(self):
        return self.__rear.item
