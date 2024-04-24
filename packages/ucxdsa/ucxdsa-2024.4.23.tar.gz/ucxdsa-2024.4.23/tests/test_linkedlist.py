import unittest
from dsa.singlylinkedlist import LinkedList, Node

class TestLinkedList(unittest.TestCase):
    def test_create(self):
        ll = LinkedList()
        self.assertEqual(ll.count, 0)

        n1 = Node(10)
        ll = LinkedList(n1)
        self.assertEqual(ll.count, 1)
        self.assertEqual(ll.head.value, 10)
        self.assertEqual(ll.tail.value, 10)

        n2 = Node(20)
        n1.next = n2
        ll = LinkedList(n1, n2, 2)
        self.assertEqual(ll.count, 2)
        self.assertEqual(ll.head.value, 10)
        self.assertEqual(ll.tail.value, 20)

        n3 = Node(30)
        n2.next = n3
        ll = LinkedList(n1, n3, 3)
        self.assertEqual(ll.count, 3)
        self.assertEqual(ll.head.value, 10)
        self.assertEqual(ll.tail.value, 30)

    def test_from_array(self):
        ll = LinkedList.from_array([])
        self.assertEqual(ll.count, 0)
        self.assertEqual(ll.head, None)
        self.assertEqual(ll.tail, None)
        print(ll)

        ll = LinkedList.from_array([1])
        self.assertEqual(ll.count, 1)
        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.tail.value, 1)
        print(ll)

        ll = LinkedList.from_array([1, 2])
        self.assertEqual(ll.count, 2)
        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.tail.value, 2)
        print(ll)

        ll = LinkedList.from_array([1, 2, 3])
        self.assertEqual(ll.count, 3)
        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.tail.value, 3)
        print(ll)
        
    def test_search(self):
        ll = LinkedList.from_array(range(20))
        self.assertRaises(Exception, ll.search, -1)
        self.assertEqual(ll.search(1), 1)
        self.assertEqual(ll.search(10), 10)
        self.assertRaises(Exception, ll.search, 20)


    def test_insert(self):
        ll = LinkedList()

        for _ in range(15):
            ll.append(_)
        self.assertEqual(ll.count, 15)

    def test_delete(self):
        ll = LinkedList()

        for _ in range(15):
            ll.append(_)
        self.assertEqual(ll.head.value, 0)
        self.assertEqual(ll.tail.value, 14)
        self.assertEqual(ll.count, 15)
        
        for _ in range(15):
            ll.delete(0)
            self.assertEqual(ll.count, 14 - _)
        self.assertRaises(Exception, ll.delete, 0)


    def test_traverse(self):
        ll = LinkedList()

        for _ in range(15):
            ll.append(_)

        node = ll.head
        for _ in range(15):
            self.assertEqual(node.value, _)
            node = node.next

        ll.print()


if __name__ == '__main__':
    unittest.main()
