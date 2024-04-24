class Heap:
    """ 
    A heap implementation in Python

    Args:
        maxheap: return a max-heap if True  (default), otherwise return a min-heap
    """
    def __init__(self, maxheap=True):
        self._array = []

        # comparator determines the order of the insertion by flipping its sign if min-heap 
        if maxheap:
            self.comparator = lambda x: x
        else:
            self.comparator = lambda x: -x
    
    def root(self):
        """
        Get the root value.

        Returns:
        The root node's value. None if count is 0.
        """
        if self.count() == 0:
            return None

        return self._array[0]
    
    def peek(self):
        """
        Get the max value if max-heap and min value if min-heap.

        Returns:
        Get the max value if max-heap and min value if min-heap.
        """
        return self.root()

    def last(self):
        """
        Get the last node of the heap.

        Returns:
        The last node's value. None if count is 0.
        """
        if self.count() == 0:
            return None

        return self._array[-1] 
    
    def left_index(self, index) -> int:
        """
        Get the value of the left child.

        Args:
            index: current index  

        Returns:
        the index of the left child
        """
        return (index * 2) + 1

    def right_index(self, index) -> int:
        """
        Get the value of the right child.

        Args:
            index: current node index  

        Returns:
        the index of the right child
        """
        return (index * 2) + 2

    def parent_index(self, index) -> int:
        """
        Get the value of the parent child.

        Args:
            index: current node index  

        Returns:
        the index of the parent child
        """
        return (index - 1) // 2
    
    def has_left(self, index) -> bool:
        """
        Check if current node has an left child.

        Args:
            index: current node index  

        Returns:
        the index of the left child
        """
        return self.left_index(index) < self.count()
    
    def has_right(self, index) -> bool:
        """
        Check if current node has an right child.

        Args:
            index: current node index  

        Returns:
        the index of the left child
        """
        return self.right_index(index) < self.count()

    def has_parent(self, index) -> bool:
        """
        Check if current node has a parent node.

        Args:
            index: current index  

        Returns:
        the index of the left child
        """
        return self.parent_index(index) >= 0
    
    def insert(self, value):
        """
        Insert a value into the heap.

        Args:
            value: value to insert  
        """
        self._array.append(value)
        
        start_index = self.count() - 1
        self.heapify_up(start_index)
    
    def heapify_up(self, index):
        """
        Perform heapify up starting at a given index.

        Args:
            index: starting index  
        """
        parent_index = self.parent_index(index)
        while self.has_parent(index) and self.comparator(self._array[index]) > self.comparator(self._array[parent_index]):
            self._array[index], self._array[parent_index] = self._array[parent_index], self._array[index]
            index = parent_index
            parent_index = self.parent_index(index)

    def pop(self):
        """
        Get the value of the root node and remove it from the heap.

        Returns:
        value of the root node
        """
        root_value = self.root()
        
        # start at root node
        start_index = 0
        if self.count() == 1:
            self._array.pop()
        else:
            self._array[start_index] = self._array.pop()
        
        self.heapify_down(start_index)
        return root_value
        
    def heapify_down(self, index):
        """
        Perform heapify down starting at a given index.

        Args:
            index: starting index  
        """
        while self.has_left(index):
            higher_index = self.left_index(index)
            right_index = self.right_index(index)
            if self.has_right(index) and self.comparator(self._array[right_index]) > self.comparator(self._array[higher_index]):
                higher_index = right_index
            
            if self.comparator(self._array[index]) > self.comparator(self._array[higher_index]):
                break
            else:
                self._array[index], self._array[higher_index] = self._array[higher_index], self._array[index]
                
            index = higher_index
    
    def enumerate(self):
        """
        Return the enumeration of a heap.

        Returns:
        enumeration of a heap
        """
        return enumerate(self._array)

    def count(self) -> int:
        """
        Return the number of items in the heap.

        Returns:
        the number of items in the heap
        """
        return len(self._array)
    
    def is_empty(self) -> bool:
        """
        Check if a heap has any items.

        Returns:
        True if heap has no items.
        False if heap has more than 0 items.
        """
        return self.count() == 0

    def print(self):
        """
        Print the contents of a heap.
        """
        node_count = 1
        for i in range(self.count()):
            if i + 1 >= node_count:
                print()
                node_count *= 2
            print(self._array[i], end=" ")
