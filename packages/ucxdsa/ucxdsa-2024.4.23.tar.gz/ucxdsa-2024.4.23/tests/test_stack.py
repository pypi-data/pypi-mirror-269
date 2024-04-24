import unittest
from dsa.stack import Stack, DynamicStack

class TestStack(unittest.TestCase):
    def test_create(self):
        st = Stack()
        self.assertTrue(st.is_empty())
        self.assertEqual(st.capacity(), 10)
        self.assertEqual(st.top(), -1)

        dst = DynamicStack()
        self.assertTrue(dst.is_empty())
        self.assertEqual(dst.capacity(), 10)
        self.assertEqual(dst.top(), -1)

    def test_insert(self):
        st = Stack()

        for _ in range(10):
            st.push(_ * 2)
            self.assertEqual(st.peek(), _ * 2)
        self.assertEqual(st.top(), 9)
        self.assertEqual(st.count, 10)
        self.assertEqual(st.capacity(), 10)
        self.assertRaises(Exception, st.push, 10)
        print(st)

        dst = DynamicStack()
        for _ in range(20):
            dst.push(_ * 2)
            self.assertEqual(dst.peek(), _ * 2)
        self.assertEqual(dst.top(), 19)
        self.assertEqual(dst.count, 20)
        self.assertGreater(dst.capacity(), 10)
        try:
            dst.push(20)
        except Exception:
            self.fail("push raised Exception unexpectedly")
        print(dst)

    def test_delete(self):
        st = Stack()
        self.assertRaises(Exception, st.pop)

        for _ in range(10):
            st.push(_ * 2)

        for _ in range(10):
            v = st.pop()
            self.assertEqual(18 - _ * 2, v)
        self.assertTrue(st.is_empty())
        self.assertRaises(Exception, st.pop)

        dst = DynamicStack()
        self.assertRaises(Exception, dst.pop)
        for _ in range(20):
            dst.push(_ * 2)

        for _ in range(20):
            v = dst.pop()
            self.assertEqual(38 - _ * 2, v)
        self.assertTrue(dst.is_empty())
        self.assertRaises(Exception, dst.pop)

if __name__ == '__main__':
    unittest.main()
