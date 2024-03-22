# Elliptic Curve Cryptography

The [**Elliptic Curve Cryptography (ECC)**](https://en.wikipedia.org/wiki/Elliptic-curve\_cryptography) is modern **family of public-key cryptosystems**, which is based on the algebraic structures of the **elliptic curves over finite fields** and on the difficulty of the [**Elliptic Curve Discrete Logarithm Problem (ECDLP)**](https://en.wikipedia.org/wiki/Elliptic-curve\_cryptography#Rationale).

**ECC** implements all major capabilities of the asymmetric cryptosystems: **encryption**, **signatures** and **key exchange**.

The **ECC cryptography** is considered a natural modern **successor of the RSA** cryptosystem, because ECC uses **smaller keys** and signatures than RSA for the same level of security and provides very **fast key generation**, **fast key agreement** and **fast signatures**.


## ECC Keys

The **private keys** in the ECC are integers (in the range of the curve's field size, typically **256-bit** integers). Example of 256-bit ECC private key (hex encoded, 32 bytes, 64 hex digits) is: `0x51897b64e85c3f714bba707e867914295a1377a7463a9dae8ea6a8b914246319`.

The **key generation** in the ECC cryptography is as simple as securely generating a **random integer** in certain range, so it is extremely fast. Any number within the range is valid ECC private key.

## Elliptic Curves

In mathematics [**elliptic curves**](http://mathworld.wolfram.com/EllipticCurve.html) are plane algebraic curves, consisting of all points {_**x**_, _**y**_}, described by the equation:

Cryptography uses **elliptic curves** in a simplified form (Weierstras form), which is defined as:

* y2 = x3 + \_**a**\_x + _**b**_

This is a visualization of the above elliptic curve:

