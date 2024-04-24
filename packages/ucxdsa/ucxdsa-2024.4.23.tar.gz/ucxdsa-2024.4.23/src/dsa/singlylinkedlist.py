class Node:
    """ 
    A singly linked list node implementation in Python
    """
    def __init__(self, value):
        """ 
        Args:
            value: the value of the node
        """
        #: value of the node
        self.value = value
        #: reference to the next node
        self.next = None

class LinkedList:
    """ 
    A singly linked list implementation in Python
    """
    def __init__(self, head: Node=None, tail: Node=None, count: int=0):
        """ 
        Initialize a singly linked list.
        
        if only the head node is specified, tail is set to the head node and count is automatically set to 0
        if both head and tail nodes are specified, count should be specified as well
        
        Args:
            head: reference to the head node
            tail: reference to the tail node
            count: the number of nodes in the linked list

        """        
        self.head = head
        if head is not None and tail is None:
            self.tail = head
            self.count = 1
        else:
            self.tail = tail
            self.count = count

    @classmethod
    def from_array(cls, mylist=None):
        """
        Create a linked list from an array.

        Args:
            mylist: an array or container to conver from
        
        Returns:
            Linked List
        """
        '''  '''
        ll = cls()
        for value in mylist:
            ll.append(value)

        return ll
    
    def print(self):
        """
        Print the contents of the linked list.
        """
        current = self.head
        while current is not None:
            print(current.value, end=" ")
            current = current.next
        print()

            
    def __repr__(self):
        s = ""
        current = self.head
        while current is not None:
            s += str(current.value) + " "
            current = current.next

        return f"[{s}] Count: {self.count}"
    
    def search(self, value) -> int:
        """
        Search for a value in the linked list.

        Args:
            value: value to search for

        Returns:
            return index of found value
        """
        i = 0
        current = self.head
        while current is not None:
            if current.value == value:
                return i
            i += 1
            current = current.next
        raise Exception("Value not found")
    
    def insert(self, index: int, value):
        """
        Insert a value at a specified index.

        Args:
            index: the index to insert a value
            value: a value to append
        """
        i = 0
        
        # insert front
        if index == 0:
            new_node = Node(value)
            new_node.next = self.head
            self.head = new_node
            self.count += 1
            return
            
        current = self.head
        while index < i or current is not None:
            i += 1
            if i == index:
                break
            current = current.next
        
        if index > i:
            raise Exception("Index Out of Bounds")
        new_node = Node(value)
        tmp = current.next
        current.next = new_node
        new_node.next = tmp
        self.count += 1

        
    def append(self, value):
        """
        Place a value at the end of the linked list.

        Args:
            value: a value to append
        """
        if self.head is None:
            self.head = Node(value)
            if self.count == 0:
                self.tail = self.head
            self.count += 1
            return

        # go to the end of the list
        new_node = Node(value)
        self.tail.next = new_node
        self.tail = new_node
        
        self.count += 1

    def delete(self, index: int):
        """
        Delete a node at a specified index. Raise Exception if linked list is empty or if index is not found.

        Args:
            index: index of element to be deleted
        """
        if index == 0:
            if self.head is None:
                raise Exception("LinkedList is Empty")
            self.head = self.head.next
            self.count -= 1
            return
        
        i = 0
        current = self.head
        prev = current
        while current is not None:
            if index == i:
                prev.next = current.next
                self.count -= 1
                return
            i += 1
            prev = current
            current = current.next
        raise Exception("Index not found")
        
    
