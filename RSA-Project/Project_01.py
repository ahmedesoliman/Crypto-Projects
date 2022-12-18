# @file: Project_Final.py
# RSA Project
# @author: ahmedesoliman
# @breif: This is a python program that implements RSA algorithm to encrypt and decrypt messages using public and private keys
# and also it implements the miller rabin primality test to generate prime numbers of a given bit length
#  and also it implements the extended euclidean algorithm to calculate the multiplicative inverse of a number mod n
#  and also it implements the powmod_sm function to calculate (base^expo) mod n
#
# @version: 0.1
# @date: 12-3-2022
# @copyright: copyright (c) 2022
import random
import math
import itertools

# Generate random prime number with n bits.


def MRT(bits):  # bits is the number of bits in the prime number
    # get a random number with bits length and make sure it is odd and greater than 2
    def get_random_t(): return random.getrandbits(
        bits) | 1 << bits | 1  # this is like 2^(bits-1)+2^(bits)+1
    # p is a random number with bits length and make sure it is odd and greater than 2
    p = get_random_t()
    for i in itertools.count(1):  # for i in count 1 to infinity
        if isPrime(p):  # if p is prime then
            return p  # return p
        else:
            if i % (bits * 2) == 0:  # if i is divisible by bits*2 then
                # p is a random number with bits length and make sure it is odd and greater than 2
                p = get_random_t()
            else:
                p += 2  # Add 2 since we are only interested in odd numbers

# imolement millerTest function to test if a number is prime or not


def miillerTest(d, n):
    # Pick a random number in [2..n-2]
    # Corner cases make sure that n > 4
    a = 2 + random.randint(1, n - 4)

    # Compute a^d % n
    x = powmod_sm(a, d, n)

    if (x == 1 or x == n - 1):
        return True

    # Keep squaring x while one
    # of the following doesn't
    # happen
    # (i) d does not reach n-1
    # (ii) (x^2) % n is not 1
    # (iii) (x^2) % n is not n-1
    while (d != n - 1):
        x = (x * x) % n
        d *= 2

        if (x == 1):
            return False
        if (x == n - 1):
            return True

        # Return composite
        return False

# This function is called for all k trials. It returns false if n is composite and returns false if n is probably prime. d is an odd number such that d*2<sup>r</sup> = n-1 for some r >= 1


def isPrime(n, k=100):
    # Corner cases
    if (n <= 1 or n == 4):  # 1 is not prime and 4 is not prime
        return False
    if (n <= 3):  # 2 and 3 are prime
        return True

    # Find r such that n = 2^d * r + 1 for some r >= 1
    d = n - 1
    while (d % 2 == 0):  # while d is even
        d //= 2

    # Iterate given nber of 'k' times
    for i in range(k):
        if (miillerTest(d, n) == False):  # if n is composite
            return False

    return True

# Returns pair (x, y) such that xa + yb = gcd(a, b)


def EEA(a, b):

    x, lastx, y, lasty = 0, 1, 1, 0
    while b != 0:
        q, r = divmod(a, b)
        a, b = b, r
        x, lastx = lastx - q * x, x
        y, lasty = lasty - q * y, y

    return lastx, lasty

# Find the multiplicative inverse of e mod n.


def multiplicative_inverse(e, n):
    x, y = EEA(e, n)
    if x < 0:
        return n + x

    return x

# Calculate x^m modulo n using O(log(m)) operations.


def powmod_sm(x, m, n):  # x is the base , m is the exponent and n is the modulus
    a = 1  # a is the result
    while m > 0:  # while m is greater than 0
        if m % 2 == 1:  # if m is odd
            a = (a * x) % n  # a = a*x mod n
        x = (x * x) % n  # x = x^2 mod n
        m //= 2  # m = m/2

    return a

# Generate a public/private key pair. The public key is (n, e) and the private key is (n, d).


def rsa_generate_key(bits):  # bits is the number of bits in the prime number
    p = MRT(bits // 2)  # p is a random prime number with bits/2 length
    q = MRT(bits // 2)  # q is a random prime number with bits/2 length
    # Ensure q != p, though for large values of bits this is
    # statistically very unlikely
    while q == p:  # while q is equal to p
        q = MRT(bits // 2)  # q is a random prime number with bits/2 length

    n = p * q  # n = p*q
    phi = (p - 1) * (q - 1)  # phi = (p-1)*(q-1)
    # Here we pick a random e, but a fixed value for e can also be used.
    while True:
        # e is a random number between 3 and phi-1
        e = random.randint(3, phi - 1)
        if math.gcd(e, phi) == 1:  # if e and phi are coprime
            break
    # d is the multiplicative inverse of e mod phi
    d = multiplicative_inverse(e, phi)

    return (n, e, d)


# message is the message to be encrypted , n is the modulus and e is the public key
def rsa_encrypt(message, n, e):
    return powmod_sm(message, e, n)  # return the encrypted message

# cipher is the encrypted message , n is the modulus and d is the private key


def rsa_decrypt(cipher, n, d):
    return powmod_sm(cipher, d, n)  # return the decrypted message


# Driver Code
# n is the modulus , e is the public key and d is the private key
n, e, d = rsa_generate_key(1024)

msg = 19191919

eMsg = rsa_encrypt(msg, n, e)

print("Plain text: ", msg)
print("Cipher Text: ", eMsg)

dMsg = rsa_decrypt(eMsg, n, d)
print("Decrypted message: ", dMsg)  # 19191919
