#!/usr/bin/env python3

import ffx

def Context(key, twk, mintwklen, maxtwklen, radix):
    return ffx.Context(key, twk, 2**32, mintwklen, maxtwklen, radix)

def cipher(ctx, pt, twk, enc):
    return ''
