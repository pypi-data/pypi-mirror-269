# 초기값이 None인 item, prev, next을 가진 Node클래스
class Node:
    def __init__(self, item = None, prev = None, next = None):
        self.item = item
        self.prev = prev
        self.next = next


# 더미헤드를 가진 양방향 원형 연결 리스트
class DoublyCircularLinkedList:
    def __init__(self):
        self.head = Node("dummy")
        self.head.prev = self.head
        self.head.next = self.head

        self.tail = Node(None, self.head, self.head)

        self.numItems = 0

    # i번째 인덱스의 노드를 반환
    def getNode(self, i: int):
        # 리스트가 빈 리스트인 경우 경고문 출력 및 None 반환
        if self.numItems == 0:
            print("there is no Item in List")
            return None
        
        else:
            curr = self.head
            for index in range(i+1):
                curr = curr.next
            
            return curr
    
    # 리스트를 출력하는 함수
    def printList(self):
        # 리스트가 빈 리스트인 경우 경고문 출력 및 None 반환
        if self.numItems == 0:
            print("there is no Item in List")
            return None
        
        curr = self.head

        for i in range(self.numItems):
            curr = curr.next

            if i == self.numItems - 1:
                print(curr.item)
            
            else:
                print(curr.item, " -> ", end='')

    # 리스트 끝에 x값을 가진 노드를 추가
    def append(self, x):
        # 리스트의 끝 노드를 = prev로
        prev = self.head.prev
        newNode = Node(x, prev, self.head)
        prev.next = newNode
        self.head.prev = newNode
        self.tail = newNode
        self.numItems += 1
    

    # 매개변수를 인덱스로 하여 그 위치에 노드를 삭제 및 반환, 매개변수를 안 줄 경우 제일 끝 노드를 삭제 및 반환
    def pop(self, *args):
        # 리스트가 빈 리스트인 경우 경고문 출력 및 None 반환
        if self.numItems == 0:
            print("there is no Item in List")
            return None

        if len(args) != 0:
            i = args[0]
            # 매개변수가 범위를 넘어간경우
            if self.numItems - 1 < i:
                print("failed pop(), Out of Bounds")
                return None
            
        # pop()을 하거나 pop(-1)을 하면 제일 뒤에 노드를 삭제
        if len(args) == 0 or i == -1:
            curr = self.head.prev
            prev = curr.prev
            prev.next = curr.next
            self.head.prev = prev
            self.tail = prev
            self.numItems -= 1

            return curr.item
        
        else:
            curr = self.getNode(i)
            prev = curr.prev
            next = curr.next

            prev.next = next
            next.prev = prev

            if i == self.numItems - 1:
                self.tail = prev
            
            self.numItems -= 1
            return curr.item

    # 매개변수 i를 인덱스로 하여, 그 위치에 x를 가진 노드를 삽입
    def insert(self, i: int, x):
        if i > self.numItems:
            print("failed insert(), Out of Bounds")
            return None
        
        if self.numItems == 0:
            self.append(x)
        
        else:
            curr = self.getNode(i)
            prev = curr.prev
            
            newNode = Node(x, prev, curr)
            prev.next = newNode
            curr.prev = newNode

            if i == self.numItems:
                self.tail = newNode

            self.numItems += 1