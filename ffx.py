#!/usr/bin/env python3

import math
import typing

import cryptography.hazmat.primitives as crypto
import cryptography.hazmat.primitives.ciphers
import cryptography.hazmat.primitives.ciphers.algorithms
import cryptography.hazmat.primitives.ciphers.modes

DEFAULT_ALPHABET: typing.Final[str] = '0123456789abcdefghijklmnopqrstuvwxyz'

class Context:
    def __init__(self,
                 key, twk,
                 maxtxtlen, mintwklen, maxtwklen,
                 radix, alpha):
        self.BLKSZ = (int)(crypto.ciphers.algorithms.AES.block_size / 8)

        self.cipher = crypto.ciphers.Cipher(
            crypto.ciphers.algorithms.AES(key),
            crypto.ciphers.modes.CBC(bytes([0]*16)))

        if radix < 2 or radix > len(alpha):
            raise RuntimeError('Unsupported radix or incompatible alphabet')

        self.alpha = alpha

        #
        # for both ff1 and ff3-1: radix**minlen >= 1000000
        #
        # therefore:
        #   minlen = ceil(log_radix(1000000))
        #          = ceil(log_10(1000000) / log_10(radix))
        #          = ceil(6 / log_10(radix))
        #
        mintxtlen = math.ceil(6 / math.log10(radix));
        if mintxtlen < 2 or mintxtlen > maxtxtlen:
            raise RuntimeError('Invalid text length bounds')

        if (mintwklen > maxtwklen or
            len(twk) < mintwklen or
            (maxtwklen > 0 and len(twk) > maxtwklen)):
            raise RuntimeError('Invalid tweak length or bounds')

        self.radix = radix

        self.mintxtlen = mintxtlen
        self.maxtxtlen = maxtxtlen
        self.mintwklen = mintwklen
        self.maxtwklen = maxtwklen

        self.twk = twk

    def PRF(self, buf):
        BLKSZ = self.BLKSZ

        if len(buf) % BLKSZ != 0:
            raise RuntimeError(
                'Plaintext length must be a multiple of ' +
                str(BLKSZ))

        enc = self.cipher.encryptor()

        dst = bytes([0] * (BLKSZ * 2 - 1))
        for i in range(int(len(buf) / BLKSZ)):
            enc.update_into(
                buf[i * BLKSZ:(i + 1) * BLKSZ],
                dst)

        enc.finalize()

        return dst[0:BLKSZ]

    def Ciph(self, buf):
        return self.PRF(buf[0:self.BLKSZ])

def StringToNumber(radix, alpha, s):
    p = 1
    n = 0
    for i in range(len(s)):
        x = alpha.index(s[len(s) - i - 1])
        n += x * p
        p *= radix
    return n

def NumberToString(radix, alpha, n, l = 1):
    s = ''
    while n:
        s = alpha[int(n % radix)] + s
        n //= radix
    while len(s) < l:
        s = alpha[0] + s
    return s
