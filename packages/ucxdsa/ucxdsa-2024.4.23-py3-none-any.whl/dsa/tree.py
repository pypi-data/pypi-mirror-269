class Node:
    """ 
    A binary tree node implementation in Python
    """
    def __init__(self, value, left=None, right=None):
        """ 
        Args:
            value: value of the node
            left: left node
            right: right node
        """
        self.value = value
        self.left = left
        self.right = right

    def print(self, level=0):
        """ 
        Print the contents of a node.

        Args:
            level: starting level of node
        """
        if self.right:
            self.right.print(level + 1)
        print("   " * level + str(self.value))
        if self.left:
            self.left.print(level + 1)

class Tree:
    """ 
    A binary search tree implementation in Python
    """
    def __init__(self, root=None):
        """ 
        Args:
            root: root node of the BST
        """
        self.root = root
        
    def search(self, value):
        """ 
        Search for a value in the binary search tree.

        Args:
            value: value to search for
        
        Returns:
        node with matching value
        None if not found
        """
        current = self.root
        
        while current is not None:
            if value == current.value:
                return current
            elif value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return None
        
        return None
    
    def insert(self, value):
        """ 
        Insert a value in the binary search tree.

        Args:
            value: value to insert
        
        Returns:
        None
        """
        current = self.root
        if self.root is None:
            self.root = Node(value)
            return
        
        while current is not None:
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    return
                else:
                    current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = Node(value)
                    return
                else:
                    current = current.right
            else:
                return 
   
    def delete(self, value):
        """ 
        Delete a value from the binary search tree.

        Args:
            value: value to delete
        
        Returns:
        None
        """
        return self.delete_node(value, self.root)
        
    def delete_node(self, value, node):
        """ 
        Helper function to delete a value from the binary search tree. (Use delete() instead)

        Args:
            value: value to delete
            node: current node
        """
        if node is None:
            return None
        
        if value < node.value:
            node.left = self.delete_node(value, node.left)
        elif value > node.value:
            node.right = self.delete_node(value, node.right)
        else:
            if node.left is None:
                branch = node.right
                node = None
                return branch
            elif node.right is None:
                branch = node.left
                node = None
                return branch
            
            branch = self.min_node(node.right)
            node.value = branch.value
            node.right = self.delete_node(branch.value, node.right)
            
        return node
    
    def min_node(self, node=None):
        """ 
        Return the node with the minimum value in a binary search tree.

        Args:
            node: starting node
        
        Returns:
        node with the lowest value in the BST
        None if not found
        """
        if node is None:
            node = self.root
        
        if node.left is None:
            return node
        else:
            return self.min_node(node.left)
    
    def print(self):
        """ 
        Print the values in the BST.

        """
        self.root.print()
        
        
