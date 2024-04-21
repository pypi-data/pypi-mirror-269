from stackNqueue.DoublyCircularLinkedList import * 

class Stack(DoublyCircularLinkedList):
    def __init__(self):
        super().__init__()
        self.__top = self.head

    def push(self, x):
        super().append(x)
        self.__top = self.head.prev

    def pop(self):
        rtn = super().pop()
        self.__top = self.head.prev
        return rtn
    
    def top(self):
        return self.__top.item