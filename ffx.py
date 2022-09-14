#!/usr/bin/env python3

import math
import typing

import cryptography.hazmat.primitives as crypto
import cryptography.hazmat.primitives.ciphers
import cryptography.hazmat.primitives.ciphers.algorithms
import cryptography.hazmat.primitives.ciphers.modes

AES_BLOCK_SIZE: typing.Final[int] = (int)(
    crypto.ciphers.algorithms.AES.block_size / 8)

class Context:
    def __init__(self,
                 key, twk,
                 maxtxtlen, mintwklen, maxtwklen,
                 radix):
        self.cipher = crypto.ciphers.Cipher(
            crypto.ciphers.algorithms.AES(key),
            crypto.ciphers.modes.CBC(bytes([0]*16)))

        # TODO: add check on radix

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

    def prf(self, buf):
        if len(buf) % AES_BLOCK_SIZE != 0:
            raise RuntimeError(
                'Plaintext length must be a multiple of ' +
                str(AES_BLOCK_SIZE))

        enc = self.cipher.encryptor()

        dst = bytes([0] * (AES_BLOCK_SIZE * 2 - 1))
        for i in range(int(len(buf) / AES_BLOCK_SIZE)):
            enc.update_into(
                buf[i * AES_BLOCK_SIZE:(i + 1) * AES_BLOCK_SIZE],
                dst)

        enc.finalize()

        return dst[0:AES_BLOCK_SIZE]

    def ciph(self, buf):
        return self.prf(buf[0:AES_BLOCK_SIZE])

def NumberToString(n, radix, l = 1):
    alpha = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8',
        '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
        'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
        'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    string = ''
    while n:
        string = alpha[int(n % radix)] + string
        n //= radix
    while len(string) < l:
        string = alpha[0] + string
    return string
