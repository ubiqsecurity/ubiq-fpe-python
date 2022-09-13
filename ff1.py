#!/usr/bin/env python3

import ffx

def ff1_Context(key, twk, mintwklen, maxtwklen, radix):
    return ffx.Context(key, twk, 2**32, mintwklen, maxtwklen, radix)

def ff1_cipher(ctx, pt, twk, enc):
    return ''

if __name__ == "__main__":
    ctx = ff1_Context(bytes([0]*16), bytes([0]*7), 0, 7, 10)
