# Format Preserving Encryption in Python

An implementation of the NIST-approved FF1 algorithm in Python.

This implementation conforms (as best as possible) to
[Draft SP 800-38G Rev. 1][800-38g1]. The implementation passes all tests
specified by NIST in their Cryptographic Standards and Guidelines
[examples for FF1][ff1-examples]


## Documentation

See the [Python API docs](https://dev.ubiqsecurity.com/docs/api).

## Installation

#### Using the package manager:
You may want to make sure you are running the latest version of pip3 by
first executing
```sh
$ pip3 install --upgrade pip
```

You don't need this source code unless you want to modify the package. If you just want to use the package, install from PyPi using pip3, a package manager for Python3.

```sh
$ pip3 install --upgrade ubiq_security_fpe
```


#### Installing from source:
From within the cloned git repository directory, Install from source with:


```
$ cd ubiq-fpe-python
$ pip3 install -r requirements.txt
$ python3 setup.py install
```
You may need to run the python3 commands above using sudo.

# Testing

To run the tests:

```sh
$ python3 -m unittest  ubiq_security_fpe/*test.py -v
```


### Requirements

-   Python 3.5+


### About alphabets and the radix parameter

The interfaces operate on strings, and the radix parameter determines which
characters are valid within those strings, i.e. the alphabet. For example, if
your radix is 10, then the alphabet for your plain text consists of the
characters in the string "0123456789". If your radix is 16, then the
alphabet is the characters in the string "0123456789abcdef".

More concretely, if you want to encrypt, say, a 16 digit number grouped into
4 groups of 4 using a `-` as a delimiter as in `0123-4567-8901-2345`, then you
would need a radix of at least 11, and you would need to translate the `-`
character to an `a` (as that is the value that follows `9`) prior to the
encryption. Conversely, you would need to translate an `a` to a `-` after
decryption.

This mapping of user inputs to alphabets defined by the radix is not performed
by the library and must be done prior to calling the encrypt and after calling
the decrypt functions.

A radix of up to 36 is supported, and the alphabet for a radix of 36 is
"0123456789abcdefghijklmnopqrstuvwxyz".

### Tweaks

Tweaks are very much like Initialization Vectors (IVs) in "traditional"
encryption algorithms. For FF1, the minimun and maximum allowed lengths of
the tweak may be specified by the user, and any tweak length between those
values may be used.

### Plain/ciphertext input lengths

For FF1, the minimum length is determined by the inequality:
- radix<sup>minlen</sup> >= 1000000

or:
- minlen >= 6 / log<sub>10</sub> radix

Thus, the minimum length is determined by the radix and is automatically
calculated from it.

For FF1, the maximum input length is
- 2<sup>32</sup>

## Examples

The [unit test code](ff1_test.py) provides the best
and simplest example of how to use the interfaces.

### FF1
```python
    /*
     * @key is a byte array whose length must be 16, 24, or 32
     * @twk is an optional byte array that can be used for the FF1 context
     * @twk_min_len is a constraint that can be applied for the tweak during
     *      the encrypt or decrypt calls
     * @twk_max_len is a constraint that can be applied for the tweak during
     *      the encrypt or decrypt calls
     * @radix is the radix for the text string
     * @alpha is the character set to use when perfoming the FPE encryption
     */

    ctx = ff1.Context(bytes(key), bytes(twk), twk_min_len, twk_max_len, radix, alpha)

    /*
     * @pt is the plain text string where the characters correspond to the 
     *     alpha character set and the radix value
     * @tweak is an optional byte array that will override the twk value
     *     supplied in the Context function.  If supplied it must be constrained to
     *     the twk_min_len and twk_max_len values
     */


    ct = ctx.Encrypt(pt, tweak)
    out = ctx.Decrypt(ct, tweak)
```



[dashboard]:https://dashboard.ubiqsecurity.com/
[credentials]:https://dev.ubiqsecurity.com/docs/how-to-create-api-keys
[800-38g1]:https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-38Gr1-draft.pdf
[ff1-examples]:https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Standards-and-Guidelines/documents/examples/FF1samples.pdf

