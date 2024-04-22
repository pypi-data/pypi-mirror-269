
class ListNode:
    def __init__(self, newitem, nextNode: 'ListNode'):
        self.item = newitem
        self.next = nextNode

class LinkedListBasic:
    def __init__(self):
        self.__head = ListNode('dummy', None)
        self.__numItems = 0

    def insert(self, i ,newItem):
        if i >= 0 and i <= self.__numItems:
            prev = self.getNode(i-1)
            newNode = ListNode(newItem, prev.next)
            prev.next = newNode
            self.__numItems += 1
        else:
            print("에러")
    
    def getNode(self, i:int) -> ListNode:
        curr = self.__head
        for index in range(i+1):
            curr = curr.next
        return curr
    
    def append(self, newItem):
        prev = self.__getNode(self.__numItems - 1)
        newNode = ListNode(newItem, prev.next)
        prev.next = newNode
        self.__numItems += 1

    def pop(self, i:int):
        if(i >= 0 and i <= self.__numItems - 1):
            prev = self.getNode(i-1)
            curr = prev.next
            prev.next = curr.next
            retItem = curr.item
            self.__numItems -= 1
            return retItem
        else:
            return None
        
    def remove(self, x):
        (prev, curr) = self.__findNode(x)
        if curr != None:
            prev.next = curr.next
            self.__numItems -= 1
            return x
        else:
            return None

    def __findNode(self, i:int)->{ListNode, ListNode}:
        prev = self.__head
        curr = prev.next
        while curr != None:
            if curr.item == i:
                return (prev, curr)
            else:
                prev = curr
                curr = prev.next.next
        return (None, None)
    
    def get(self, i:int):
        if self.isEmpty():
            return None
        if (i >= 0 and i <= self.__numItems - 1):
            return self.getNode(i).item
        else:
            return None

    def isEmpty(self) -> bool:
        return self.__numItems == 0
        
    def index(self, x) -> int:
        curr = self.__head.next
        for index in range(self.__numItems):
            if curr.item == x:
                return index
            else:
                curr = curr.next
        return -12345
    
    def count(self, x) -> int:
        cnt = 0
        curr = self.__head.next
        while curr != None:
            if curr.item == x:
                cnt += 1
            curr = curr.next
        return cnt
    
    def clear(self):
        self.__head = ListNode('dummy', None)
        self.__numItems = 0
    
    def size(self) -> int:
        return self.__numItems
