#!/usr/bin/env python3

import unittest

import ff1

class TestFF1(unittest.TestCase):
    def test_context(self):
        self.assertIsNotNone(
            ff1.Context(bytes([0]*16), bytes([0]*7), 0, 7, 10))

    def cipherTest(self, key, twk, pt, ct, radix):
        ctx = ff1.Context(bytes(key), bytes(twk), 0, len(twk), radix)
        self.assertIsNotNone(ctx)
        res = ctx.Encrypt(pt, None)
        self.assertEqual(res, ct)
        res = ctx.Decrypt(ct, None)
        self.assertEqual(res, pt)

    def test_nist1(self):
        self.cipherTest(
            [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
             0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c],
            [],
            '0123456789', '2433477484', 10)

    def test_nist2(self):
        self.cipherTest(
            [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
             0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c],
            [0x39, 0x38, 0x37, 0x36, 0x35, 0x34, 0x33, 0x32, 0x31, 0x30],
            '0123456789', '6124200773', 10)

    def test_nist3(self):
        self.cipherTest(
            [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
             0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c],
            [0x37, 0x37, 0x37, 0x37, 0x70, 0x71, 0x72, 0x73, 0x37, 0x37, 0x37],
            '0123456789abcdefghi', 'a9tv40mll9kdu509eum', 36)

    def test_nist3_prime(self):
        self.cipherTest(
            [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6,
             0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c],
            [0x37, 0x37, 0x37, 0x37, 0x70, 0x71, 0x72, 0x73, 0x37, 0x37, 0x37],
            '0123456789abcdefghijklmnopqrstuvwxyz012345',
            'l4zpm8zauhw2zkke9o0i7oi17iojfqog7dmjze3her',
            36)
