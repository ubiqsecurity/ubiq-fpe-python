#!/usr/bin/env python3

import unittest

import ffx

class TestFFX(unittest.TestCase):
    def test_context(self):
        self.assertIsNotNone(
            ffx.Context(bytes([0]*32), bytes([0]*7), 2**32, 0, 7, 10))