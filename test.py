import unittest

import ff1
import ffx

class TestFFX(unittest.TestCase):
    def test_context(self):
        self.assertIsNotNone(
            ffx.Context(bytes([0]*32), bytes([0]*7), 2**32, 0, 7, 10))

class TestFF1(unittest.TestCase):
    def test_context(self):
        self.assertIsNotNone(
            ff1.Context(bytes([0]*16), bytes([0]*7), 0, 7, 10))

if __name__ == '__main__':
    unittest.main()
