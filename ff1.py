#!/usr/bin/env python3

import math

import ffx

class Context:
    def __init__(self, key, twk, mintwklen, maxtwklen, radix):
        self.ffx = ffx.Context(key, twk, 2**32, mintwklen, maxtwklen, radix)

    def cipher(self, X, T, enc):
        n = len(X)
        u = int(n / 2)
        v = n - u

        b = int((math.ceil(math.log2(self.ffx.radix) * v) + 7) / 8)
        d = 4 * int((b + 3) / 4) + 4

        p = 16
        r = int((d + 16) / 16) * 16

        if T == None:
            T = self.ffx.twk
        if T == None:
            T = bytes([])

        if (n < self.ffx.mintxtlen or
            n > self.ffx.maxtxtlen or
            len(T) < self.ffx.mintwklen or
            (self.ffx.maxtwklen > 0 and
             len(T) > self.ffx.maxtwklen)):
            raise RuntimeError('Input or tweak length error')

        q = int((len(T) + b + 1 + 15) / 16) * 16

        if enc:
            A = X[:u]
            B = X[u:]
        else:
            B = X[:u]
            A = X[u:]

        P = [1, 2, 1,
             self.ffx.radix >> 16 & 0xff,
             self.ffx.radix >> 8 & 0xff,
             self.ffx.radix & 0xff,
             10, u & 0xff,
             0, 0, 0, 0,
             0, 0, 0, 0]
        P[8:12] = n.to_bytes(4, byteorder='big')
        P[12:16] = len(T).to_bytes(4, byteorder='big')

        Q = [0] * q
        Q[:len(T)] = T

        R = [0] * r

        nA = int(A, self.ffx.radix)
        nB = int(B, self.ffx.radix)

        mU = self.ffx.radix ** u
        mV = mU
        if u != v:
            mV *= self.ffx.radix

        for i in range(10):
            if int(enc) == i % 2:
                mX = mV
            else:
                mX = mU

            if enc:
                Q[-b - 1] = i
            else:
                Q[-b - 1] = 9 - i

            Q[-b:] = nB.to_bytes(b, byteorder='big')

            R[:ffx.AES_BLOCK_SIZE] = list(self.ffx.prf(bytes(P + Q)))

            for j in range(int(len(R) / 16) - 1):
                w = int.from_bytes(R[12:16], byteorder='big')
                w ^= j + 1
                R[12:16] = w.to_bytes(4, byteorder='big')
                R[16 * (j + 1):16 * (j + 2)] = list(
                    self.ffx.ciph(bytes(R[:16])))
                w ^= j + 1
                R[12:16] = w.to_bytes(4, byteorder='big')

            y = int.from_bytes(R[:d], byteorder='big')
            if enc:
                y = nA + y
            else:
                y = nA - y

            nA, nB = nB, nA
            nB = y % mX

        if enc:
            Y = (ffx.NumberToString(nA, self.ffx.radix, u) +
                 ffx.NumberToString(nB, self.ffx.radix, v))
        else:
            Y = (ffx.NumberToString(nB, self.ffx.radix, u) +
                 ffx.NumberToString(nA, self.ffx.radix, v))

        return Y

    def Encrypt(self, pt, twk):
        return self.cipher(pt, twk, True)

    def Decrypt(self, ct, twk):
        return self.cipher(ct, twk, False)
