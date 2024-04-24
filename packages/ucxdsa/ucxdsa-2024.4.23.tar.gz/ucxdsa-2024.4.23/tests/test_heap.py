import unittest

from dsa.heap import Heap

class TestHeap(unittest.TestCase):
    def test_create(self):
        mxh = Heap()
        mnh = Heap(maxheap=False)
        self.assertEqual(mxh.count(), 0)
        self.assertEqual(mnh.count(), 0)
    
    def test_add(self):
        mxh = Heap()
        mnh = Heap(maxheap=False)

        for _ in range(20):
            mxh.insert(_)
            mnh.insert(_)

        self.assertEqual(mxh.count(), 20)
        self.assertEqual(mxh.peek(), 19)
        self.assertEqual(mnh.count(), 20)
        self.assertEqual(mnh.peek(), 0)

    def test_delete(self):
        mxh = Heap()
        mnh = Heap(maxheap=False)

        for _ in range(20):
            mxh.insert(_)
            mnh.insert(_)

        i = 19
        while not mxh.is_empty():
            v = mxh.pop()
            self.assertEqual(v, i)
            i = i - 1
        self.assertTrue(mxh.is_empty())

        i = 0
        while not mnh.is_empty():
            v = mnh.pop()
            self.assertEqual(v, i)
            i += 1
        self.assertTrue(mnh.is_empty())
