"""
Project 5: Deque
CSE 331 FS23
Authored by Gabriel Sotelo
tests.py
"""
import string
import random
import unittest
from solution import CircularDeque, CDLL, CDLLCD
from xml.dom import minidom
from typing import TypeVar, List, Tuple

# for more information on typehinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type

random.seed(1342)

NAMES = ["Abhinay", "Lauren", "Nate", "Katelyn", "Ilyas", "Matt K.", "Misha", "Joel", "Hank",
         "Blake", "David", "Maria", "Gabriel", "Leo", "Aman", "Khushi", "Matt W.", "Jay", "Roshanak", "Sai"]


class CircularDequeTests(unittest.TestCase):
    def test_len(self):
        # Test 1 : length 0
        cd = CircularDeque()
        self.assertEqual(0, len(cd))

        # Test 2 : length 1
        cd = CircularDeque([1])
        self.assertEqual(1, len(cd))

        # Test 3 : length 2
        cd = CircularDeque([1, 2])
        self.assertEqual(2, len(cd))

        # Test 4 : length 50
        cd = CircularDeque(list(range(50)), capacity=50)
        self.assertEqual(50, len(cd))

    def test_is_empty(self):
        # Test 1 : Empty deque -> true
        cd = CircularDeque()
        self.assertTrue(cd.is_empty())

        # Test 2 : length 1 -> false
        cd = CircularDeque([1])
        self.assertFalse(cd.is_empty())

        # Test 3 : length 2 -> false
        cd = CircularDeque([1, 2])
        self.assertFalse(cd.is_empty())

        # Test 4 : length 50 -> false
        cd = CircularDeque(list(range(50)), capacity=50)
        self.assertFalse(cd.is_empty())

    def test_front_element(self):
        # Test 1: Empty deque -> None
        cd = CircularDeque()
        self.assertIsNone(cd.front_element())

        # Test 2: CD <1> -> 1
        cd = CircularDeque([1])
        self.assertEqual(1, cd.front_element())

        # Test 3: CD <2, 1> -> 2
        cd = CircularDeque([2, 1])
        self.assertEqual(2, cd.front_element())

        # Test 4: CD <50, 49, ..., 0> -> 50
        cd = CircularDeque(list(range(50, 0, -1)), capacity=50)
        self.assertEqual(50, cd.front_element())

    def test_back_element(self):
        # Test 1: Empty Deque -> None
        cd = CircularDeque()
        self.assertIsNone(cd.back_element())

        # Test 2: CD <1> -> 1
        cd = CircularDeque([1])
        self.assertEqual(1, cd.back_element())

        # Test 3: CD <1, 2> -> 2
        cd = CircularDeque([1, 2])
        self.assertEqual(2, cd.back_element())

        # Test 4: CD <50, 49, ..., 0> -> 0
        cd = CircularDeque(list(range(50, 0, -1)), capacity=50)
        self.assertEqual(1, cd.back_element())

    def test_grow(self):
        """
        Tests grow functionality without use of enqueue
        Note that we call the grow function directly
        thus if you have a capacity check in your grow function this will fail
        """
        # Test (1) Empty Dequeue
        cd = CircularDeque()
        cd.grow()
        self.assertEqual(0, cd.size)
        self.assertEqual(8, cd.capacity)
        self.assertEqual([None] * 8, cd.queue)

        # Test (2) Four element dequeue then grow
        cd = CircularDeque(NAMES[:4])
        cd.grow()
        self.assertEqual(4, cd.size)
        self.assertEqual(8, cd.capacity)
        self.assertEqual(0, cd.front)
        self.assertEqual(3, cd.back)
        self.assertEqual(NAMES[:4] + [None] * 4, cd.queue)

    def test_shrink(self):
        """
        Tests shrink without the use of dequeue
        NOTE: If you have a capacity/size check in your shrink this will fail since we call shrink directly
        """

        # Test 1, Capacity 8 -> 4
        cd = CircularDeque(NAMES[:4], capacity=8)
        cd.shrink()
        self.assertEqual(4, cd.capacity)
        self.assertEqual(4, cd.size)

        # Test 2, Capacity 16 -> 8
        cd = CircularDeque(NAMES[:8], capacity=16)
        cd.shrink()
        self.assertEqual(8, cd.capacity)
        self.assertEqual(8, cd.size)

    def test_front_enqueue_basic(self):
        """
        Tests front enqueue but does not test grow functionality
        """

        # Test 1: One element
        cd = CircularDeque()
        cd.enqueue('First')
        self.assertEqual(0, cd.front)
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(1, cd.size)
        self.assertEqual(['First', None, None, None], cd.queue)

        # Test 2: Wraparound two elements
        cd.enqueue('Second')
        self.assertEqual(3, cd.front)  # Test 2
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(2, cd.size)
        self.assertEqual(['First', None, None, 'Second'], cd.queue)

        # Set deque capacity to 100, use name list which has length 14 thus we'll
        # never grow with unique insertion because math

        # Test 2: Front enqueue no wrap-around
        cd = CircularDeque(front=50, capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name)
            self.assertEqual(name, cd.front_element())
            self.assertEqual(49 - i, cd.front)
            # back_element should never change
            self.assertEqual('Start', cd.back_element())
            self.assertEqual(50, cd.back)
            self.assertEqual(i + 2, len(cd))
            self.assertEqual(100, cd.capacity)

        # Test 3: Front enqueue wrap-around
        cd = CircularDeque(capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name)
            self.assertEqual(name, cd.front_element())
            self.assertEqual((100 - i) % 100, cd.front)
            # back_element should never change
            self.assertEqual('Abhinay', cd.back_element())
            self.assertEqual(0, cd.back)
            self.assertEqual(i + 1, len(cd))
            self.assertEqual(100, cd.capacity)

    def test_back_enqueue_basic(self):
        """
        Tests back enqueue but does not test grow functionality
        """

        # Test 1: One element
        cd = CircularDeque()
        cd.enqueue('First', front=False)
        self.assertEqual(0, cd.front)
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(1, cd.size)
        self.assertEqual(['First', None, None, None], cd.queue)

        # Test 2: Wraparound two elements
        cd = CircularDeque(data=['First'], front=3)
        cd.enqueue('Second', front=False)
        self.assertEqual(3, cd.front)
        self.assertEqual(0, cd.back)
        self.assertEqual(4, cd.capacity)
        self.assertEqual(2, cd.size)
        self.assertEqual(['Second', None, None, 'First'], cd.queue)

        # Test 3: Back enqueue normal (no wrap around) more elements
        cd = CircularDeque(capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name, front=False)
            self.assertEqual(name, cd.back_element())
            self.assertEqual(i, cd.back)
            # back_element should never change
            self.assertEqual('Abhinay', cd.front_element())
            self.assertEqual(0, cd.front)
            self.assertEqual(i + 1, len(cd))
            self.assertEqual(100, cd.capacity)

        # Test 4: Back enqueue wraparound (back < front) more elements
        cd = CircularDeque(front=99, capacity=100)
        for i, name in enumerate(NAMES):
            cd.enqueue(name, front=False)
            self.assertEqual(name, cd.back_element())
            self.assertEqual((100 + i) % 100, cd.back)
            # front_element should never change
            self.assertEqual('Start', cd.front_element())
            self.assertEqual(99, cd.front)
            self.assertEqual(i + 2, len(cd))
            self.assertEqual(100, cd.capacity)

    def test_front_enqueue(self):
        """
        Tests front_enqueue and grow functionality
        """
        # Test 1: Front_enqueue, multiple grows with 50 elements starting with default capacity
        cd = CircularDeque()
        for element in range(1, 51):
            cd.enqueue(element)
            # Test capacity of the dequeue while it grows
            # If this fails it means you dequeue is not properly growing
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            else:
                self.assertEqual(64, cd.capacity)
        # check the position of elements in the dequeue
        self.assertEqual(list(range(32, 0, -1)) +
                         [None] * 14 + list(range(50, 32, -1)), cd.queue)
        self.assertEqual(50, cd.size)

        # Test 2: Front_enqueue, multiple grows with 64 elements starting with default capacity
        cd = CircularDeque()
        for element in range(1, 65):
            cd.enqueue(element)
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            elif element < 64:
                self.assertEqual(64, cd.capacity)
        # check the position of elements in the cd
        self.assertEqual(list(range(64, 0, -1)) + [None] * 64, cd.queue)
        self.assertEqual(64, cd.size)
        self.assertEqual(128, cd.capacity)

    def test_back_enqueue(self):
        """
        Tests back_enqueue and grow functionality
        """
        # Test 1: 50 item, multiple grows
        cd = CircularDeque()
        for element in range(1, 51):
            cd.enqueue(element, front=False)
            # Test capacity of the cd while it grows
            # If this fails it means you dequeue is not properly growing
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            else:
                self.assertEqual(64, cd.capacity)
        self.assertEqual(list(range(1, 51)) + [None] * 14, cd.queue)
        self.assertEqual(64, cd.capacity)
        self.assertEqual(50, cd.size)

        # Test 2: 64 items, multiple grows
        cd = CircularDeque()
        for element in range(1, 65):
            cd.enqueue(element, front=False)
            # Test capacity of the cd while it grows
            # If this fails it means you dequeue is not properly growing
            if element < 4:
                self.assertEqual(4, cd.capacity)
            elif element < 8:
                self.assertEqual(8, cd.capacity)
            elif element < 16:
                self.assertEqual(16, cd.capacity)
            elif element < 32:
                self.assertEqual(32, cd.capacity)
            elif element < 64:
                self.assertEqual(64, cd.capacity)
        self.assertEqual(list(range(1, 65)) + [None] * 64, cd.queue)
        self.assertEqual(128, cd.capacity)
        self.assertEqual(64, cd.size)

    def test_front_dequeue_basic(self):
        """
        Testing front/back dequeue without shrinking
        Does not use either enqueue function
        """
        # Test 0: empty deque
        cd = CircularDeque()
        self.assertIsNone(cd.dequeue())

        # Test 1: 1 element front dequeue
        cd = CircularDeque([1])
        self.assertEqual(1, cd.dequeue())
        self.assertEqual(0, len(cd))

        # Test 2: Multiple element front dequeue
        cd = CircularDeque([0, 1, 2])
        for i in range(3):
            self.assertEqual(i, cd.front)
            self.assertEqual(i, cd.dequeue())
            self.assertEqual(2 - i, len(cd))

        # Test 3: front Dequeue wrap-around
        dequeue_result = [3, 0, 1, 2]
        cd = CircularDeque([0, 1, 2, 3])
        cd.front = 3
        cd.back = 2
        for i in range(4):
            self.assertEqual(dequeue_result[i], cd.front)
            self.assertEqual(dequeue_result[i], cd.dequeue())
            self.assertEqual(3 - i, len(cd))
        self.assertIsNone(cd.dequeue())

    def test_back_dequeue_basic(self):
        """
        Testing front/back dequeue without shrinking
        Does not use either enqueue function
        """
        # Test 0: empty deque
        cd = CircularDeque()
        self.assertIsNone(cd.dequeue(False))

        # Test 1: 1 element front dequeue
        cd = CircularDeque([1])
        self.assertEqual(1, cd.dequeue(False))
        self.assertEqual(0, len(cd))

        # Test 2: Multiple element front dequeue
        cd = CircularDeque([3, 2, 1, 0])
        for i in range(4):
            self.assertEqual(3 - i, cd.back)
            self.assertEqual(i, cd.dequeue(False))
            self.assertEqual(3 - i, len(cd))

        # Test 3: front Dequeue wrap-around
        dequeue_result = [0, 3, 2, 1]
        cd = CircularDeque([0, 1, 2, 3])
        cd.front = 1
        cd.back = 0
        for i in range(4):
            self.assertEqual(dequeue_result[i], cd.back)
            self.assertEqual(dequeue_result[i], cd.dequeue(False))
            self.assertEqual(3 - i, len(cd))
        self.assertIsNone(cd.dequeue(False))

    def test_back_dequeue(self):
        """
        Tests dequeue over shrinking conditions, does test size (length)
        Does not rely on enqueue functions
        """
        # Test 1: Begin with capacity 16, empty queue while checking all parameters
        cd = CircularDeque([i for i in range(15)], capacity=16)

        for item in range(15):
            self.assertEqual(14 - item, cd.dequeue(False))

            if item <= 9:  # shrunk 0 times
                self.assertEqual(list(range(15)) + [None], cd.queue)
                self.assertEqual(16, cd.capacity)
            elif item <= 11:  # shrunk 1 time
                self.assertEqual(list(range(4)) +
                                 [None, None, None, None], cd.queue)
                self.assertEqual(8, cd.capacity)
            else:  # shrunk twice
                self.assertEqual([0, 1, None, None], cd.queue)
                self.assertEqual(4, cd.capacity)

            # ensure back is set correctly - note: pointers for an empty queue are up to implementation
            if cd.size != 0:
                self.assertEqual(13 - item, cd.back)

    def test_front_dequeue(self):
        """
        Tests dequeue along with shrinking
        Does not rely on enqueue functions
        """
        # Test 1: identical to above but removing from front rather than back
        cd = CircularDeque([i for i in range(15)], capacity=16)

        fronts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 1, 0, 1]

        for item in range(15):
            self.assertEqual(item, cd.dequeue())

            if item <= 9:
                self.assertEqual(list(range(15)) + [None], cd.queue)
                self.assertEqual(16, cd.capacity)
            elif item <= 11:
                self.assertEqual(
                    [11, 12, 13, 14, None, None, None, None], cd.queue)
                self.assertEqual(8, cd.capacity)
            else:
                self.assertEqual([13, 14, None, None], cd.queue)

            if cd.size != 0:
                self.assertEqual(fronts[item], cd.front)

    def test_comprehensive(self):
        """
        A final (big) test for your dequeue
        This test is worth 0 points but is meant to help you debug your code
        """

        cd = CircularDeque()

        # (1) Grow a deque to a large size using enqueue
        for val in range(500):
            cd.enqueue(val, front=bool(val % 2))

        # (2) check that elements were successfully added
        for val in range(500):
            self.assertIn(val, cd.queue)

        # (2.5) intermediate size/cap check
        self.assertEqual(500, cd.size)
        self.assertEqual(512, cd.capacity)

        # (3) verify correct structure via dequing
        for val in range(499, -1, -1):
            self.assertEqual(cd.dequeue(bool(val % 2)), val)
            self.assertNotIn(val, cd.queue[cd.front:cd.back])

        # (3.5) closing size/cap check
        self.assertEqual(0, cd.size)
        self.assertEqual(4, cd.capacity)

        # (4) dequeue from empty queue to check for crashes
        for i in range(10):
            self.assertIsNone(cd.dequeue(bool(val % 2)))

        # (4.5) final size/capacity check
        self.assertEqual(0, cd.size)
        self.assertEqual(4, cd.capacity)


class CDLLTests(unittest.TestCase):
    def check_cdll(self, expected: List[T], cdll: CDLL):
        """
        Assert structure of cdll is proper and contains the values of result.
        Used as helper function throughout testcases. Not an actual testcase itself.
        Collapse/hide this by clicking the minus arrow on the left sidebar.

        :param expected: list of expected values in cdll
        :param cdll: CDLL to be validated
        :return: None
        """
        # Check size
        self.assertEqual(len(expected), cdll.size)

        # Short-circuit if empty list
        if len(expected) == 0:
            self.assertIsNone(cdll.head)
            return

        # Check head and tail are connected (circular property)
        self.assertIs(cdll.head.prev.next, cdll.head)
        self.assertIs(cdll.head.next.prev, cdll.head)

        # Check head value
        self.assertEqual(expected[0], cdll.head.val)

        # Check all intermediate connections and values
        left, right = cdll.head, cdll.head.next
        i = 0

        # Check values - we'll stop the loop when we circle back to the head.
        while right != cdll.head:
            self.assertIs(left.next, right)
            self.assertIs(left, right.prev)
            self.assertEqual(expected[i], left.val)
            self.assertEqual(expected[i + 1], right.val)
            left, right = left.next, right.next
            i += 1

        # Since i starts from 0 and right != cdll.head excludes last item
        self.assertEqual(len(expected) - 1, i)

    def test_insert(self):
        """
        Tests the insert function
        """
        # (1) push single node to the front of an empty list (default behavior)
        cdll = CDLL()
        cdll.insert(0)
        self.check_cdll([0], cdll)

        # (2) push single node to the back of an empty list
        cdll = CDLL()
        cdll.insert(0, front=False)
        self.check_cdll([0], cdll)

        # (3) insert multiple nodes to the front
        cdll = CDLL()
        cdll.insert(2)
        cdll.insert(1)
        self.check_cdll([1, 2], cdll)

        # (4) insert multiple nodes to the back
        cdll = CDLL()
        cdll.insert(1)
        cdll.insert(2, front=False)
        self.check_cdll([1, 2], cdll)

        # (5) mix of insertions (front and back)
        cdll = CDLL()
        # to back of empty list (should be same as to front of empty list)
        cdll.insert(3, front=False)
        cdll.insert(2)  # to front
        cdll.insert(4, front=False)  # to back
        cdll.insert(1)  # to front
        self.check_cdll([1, 2, 3, 4], cdll)

        # (6) large mix of insertions with random strings
        cdll = CDLL()
        expected_list = []

        for _ in range(100):
            # Generate a random string of length 5
            rand_string = ''.join(random.choices(string.ascii_lowercase, k=5))

            # Randomly decide whether to insert to the front or back
            if random.choice([True, False]):
                cdll.insert(rand_string)
                # prepend to the expected list
                expected_list.insert(0, rand_string)
            else:
                cdll.insert(rand_string, front=False)
                # append to the expected list
                expected_list.append(rand_string)

        self.check_cdll(expected_list, cdll)

    def test_remove(self):
        """
        Tests the remove function
        """
        # (1) remove from an empty list
        cdll = CDLL()
        cdll.remove()
        self.check_cdll([], cdll)

        # (2) remove a single node from a list until it's empty
        cdll = CDLL()
        cdll.insert(1)
        cdll.remove()
        self.check_cdll([], cdll)
        cdll.remove()  # should be a no-op
        self.check_cdll([], cdll)

        # (3) insert then remove multiple nodes from the front
        cdll = CDLL()
        cdll.insert(1)
        cdll.insert(2)
        cdll.insert(3)
        cdll.remove()
        self.check_cdll([2, 1], cdll)
        cdll.remove()
        self.check_cdll([1], cdll)

        # (4) insert then remove multiple nodes from the back
        cdll = CDLL()
        cdll.insert(1, front=False)
        cdll.insert(2, front=False)
        cdll.insert(3, front=False)
        cdll.remove(front=False)
        self.check_cdll([1, 2], cdll)
        cdll.remove(front=False)
        self.check_cdll([1], cdll)

        # (5) large mix of insertions followed by a mix of removals
        cdll = CDLL()
        expected_list = []
        for _ in range(100):
            rand_string = ''.join(random.choices(string.ascii_lowercase, k=5))
            if random.choice([True, False]):
                cdll.insert(rand_string)
                expected_list.insert(0, rand_string)
            else:
                cdll.insert(rand_string, front=False)
                expected_list.append(rand_string)

        # Randomly removing some nodes (let's say 50 for this example)
        for _ in range(50):
            if random.choice([True, False]):
                cdll.remove()
                del expected_list[0]
            else:
                cdll.remove(front=False)
                del expected_list[-1]

        self.check_cdll(expected_list, cdll)


class CDLLCDTests(unittest.TestCase):
    def setUp(self):
        self.cdllcd = CDLLCD()

    """
    The following test cases are very simple, but they are meant to serve as a sanity check for you.
    """

    def test_len(self):
        """
        Tests the len function
        """
        self.assertEqual(0, len(self.cdllcd))
        self.cdllcd.enqueue(1)
        self.assertEqual(1, len(self.cdllcd))
        self.cdllcd.enqueue(2, front=False)
        self.assertEqual(2, len(self.cdllcd))

    def test_is_empty(self):
        """
        Tests the is_empty function
        """
        self.assertTrue(self.cdllcd.is_empty())
        self.cdllcd.enqueue(1)
        self.assertFalse(self.cdllcd.is_empty())

    def test_front_element(self):
        """
        Tests the front_element function
        """
        self.assertIsNone(self.cdllcd.front_element())
        self.cdllcd.enqueue(1)
        self.assertEqual(1, self.cdllcd.front_element())
        self.cdllcd.enqueue(2)
        self.assertEqual(2, self.cdllcd.front_element())

    def test_back_element(self):
        """
        Tests the back_element function
        """
        self.assertIsNone(self.cdllcd.back_element())
        self.cdllcd.enqueue(1, front=False)
        self.assertEqual(1, self.cdllcd.back_element())
        self.cdllcd.enqueue(2, front=False)
        self.assertEqual(2, self.cdllcd.back_element())

    def test_enqueue(self):
        """
        Tests the enqueue function
        """
        self.cdllcd.enqueue(1)
        self.assertEqual(1, self.cdllcd.front_element())
        self.cdllcd.enqueue(2, front=False)
        self.assertEqual(2, self.cdllcd.back_element())
        self.cdllcd.enqueue(3)
        self.assertEqual(3, self.cdllcd.front_element())

    def test_dequeue(self):
        """
        Tests the dequeue function
        """
        self.assertIsNone(self.cdllcd.dequeue())
        self.cdllcd.enqueue(1)
        self.cdllcd.enqueue(2)
        self.assertEqual(2, self.cdllcd.dequeue())
        self.assertEqual(1, self.cdllcd.dequeue(front=False))
        self.assertIsNone(self.cdllcd.dequeue())

    def test_application_comprehensive(self):
        """
        Tests the application: note that this test doesn't verify underlying structure, only behavior.
        Failure to implement the CDLLCD without a CDLL will void all points (testcase + manual) related to the application problem
        """

        cd = CDLLCD()

        def searcher(q, val) -> bool:
            cur = q.head
            while cur:
                if cur.val == val:
                    return True
                if cur.next is q.head:
                    break
                cur = cur.next
            return False

        # (1) Grow to a large size with enqueue
        for val in range(500):
            cd.enqueue(val, bool(val % 2))

        for val in range(500):
            self.assertTrue(searcher(cd.CDLL, val))

        # (1.1) Check if size is accurate after enqueuing
        self.assertEqual(500, len(cd))

        # (1.2) Check if front_element and back_element report correctly
        self.assertEqual(499, cd.front_element())
        self.assertEqual(498, cd.back_element())

        # (2) Dequeue and check for correct values
        for val in range(499, -1, -1):
            self.assertEqual(val, cd.dequeue(bool(val % 2)))
            self.assertFalse(searcher(cd.CDLL, val))

        # (2.1) Check if size is accurate after dequeuing
        self.assertEqual(0, len(cd))

        # (2.2) Check if front_element and back_element are None after dequeuing all
        self.assertIsNone(cd.front_element())
        self.assertIsNone(cd.back_element())

        # (3) Make sure it doesn't break dequeing when empty
        for i in range(2):
            self.assertIsNone(cd.dequeue(bool(i % 2)))

        # (4) Check is_empty function after all operations
        self.assertTrue(cd.is_empty())

        # (5) Enqueue after clearing everything and verify
        cd.enqueue(10)
        self.assertFalse(cd.is_empty())
        self.assertEqual(10, cd.front_element())
        self.assertEqual(10, cd.back_element())


if __name__ == '__main__':
    unittest.main()
