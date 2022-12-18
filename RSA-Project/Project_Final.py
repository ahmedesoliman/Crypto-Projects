import random
import math

num = random.SystemRandom()  # used to generate random numbers

# Generate a random prime number of a given bit length.
def gen_prime(bits):  # bits is the number of bits in the prime number
    while True:
        # Guarantees that a is odd.
        # this is used to generate random nun of buts length 1<<bits-1 is 2^(bits-1) and 1<<bits is 2^bits
        a = (num.randrange(1 << bits - 1, 1 << bits) << 1) + 1
        if miller_rabin(a):  # if a is prime then return a
            return a

# implement miller rabin test for primality test  # https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
def MRT(n, a):  # n is the number to be tested and a is the random number
    exp = n - 1  # exp is n-1
    while not exp & 1:  # while exp is even
        exp >>= 1  # bit shift right by 1 this is same as exp = exp/2

    if pow(a, exp, n) == 1:  # used pow() function to calculate a^exp mod n beacuse it is faster than generic method
        return True  # if a^exp mod n is equal to 1 then return true

    while exp < n - 1:  # while exp is less than n-1
        # used pow() function to calculate a^exp mod n beacuse it is faster than generic method
        if pow(a, exp, n) == n - 1:
            return True  # if a^exp mod n is equal to n-1 then return true

        exp <<= 1  # bit shift left by 1 this is same as exp = exp*2

    return False  # if a^exp mod n is not equal to 1 or n-1 then return false

# k is the number of times we want to run the test. The higher the value of k, the more accurate the result will be. # https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
# n is the number to be tested and k is the number of times we want to run the test
def miller_rabin(n, k=500):
    for i in range(k):  # for i in range k
        a = num.randrange(2, n - 1)  # a is a random number between 2 and n-1
        if not MRT(n, a):  # if MRT(n, a) is false then return false
            return False

    return True

# define gcd function to calculate gcd of two numbers using euclidean algorithm
def gcd(a, b):  # a is first number and b is second number
    while b != 0:  # while b is not equal to 0
        a, b = b, a % b  # a is b and b is a%b
    return a  # return a

# Returns pair (x, y) such that xa + yb = gcd(a, b) # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
def EEA(a, b):  # a is public key and b is modulus

    x, lastx, y, lasty = 0, 1, 1, 0

    while b != 0:  # while b is not equal to 0
        q, r = divmod(a, b)  # q is quotient and r is remainder
        a, b = b, r  # a is b and b is r
        x, lastx = lastx - q * x, x  # x is lastx - q*x and lastx is x
        y, lasty = lasty - q * y, y  # y is lasty - q*y and lasty is y

    return lastx, lasty  # return lastx and lasty

# Find the multiplicative inverse of e mod n. # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
def multiplicative_inverse(e, n):  # e is public key and n is modulus
    x, y = EEA(e, n)  # x is multiplicative inverse of e mod n
    if x < 0:  # if x is negative then add n to it
        return n + x
    return x

# implement powmod_sm function to calculate (base^expo) mod n
def powmod_sm(base, expo, n):  # base is the base, expo is the exponent and n is the modulus
    expoBits = bin(expo)  # convert expo to binary
    value = base  # value is base

    for i in range(3, len(expoBits)):  # for i in range 3 to length of expoBits
        value = (value**2) % n  # value is value^2 mod n
        if (expoBits[i:i + 1] == '1'):  # if expoBits[i:i+1] is 1 then
            value = (value * base) % n  # value is value*base mod n

    return value

# Generate a public/private key pair. The public key is (n, e) and the private key is (n, d).
def rsa_generate_key(bits):  # bits is the number of bits in the prime number
    p = gen_prime(bits//2)  # generate a prime number of bits length
    q = gen_prime(bits//2)  # generate a prime number of bits length

    # Ensure q != p, though for large values of bits this is
    # statistically very unlikely
    while q == p:  # while q is equal to p
        q = gen_prime(bits)  # generate a prime number of bits length
    n = p * q  # n is p*q
    phi = (p - 1) * (q - 1)  # phi is (p-1)*(q-1)

    # Here we pick a random e, but a fixed value for e can also be used.
    while True:
        # e is a random number between 3 and phi-1
        e = random.randint(3, phi - 1)
        if math.gcd(e, phi) == 1:  # if gcd(e, phi) is 1 then
            break
    # d * e = 1 mod phi
    # computer d using extended euclidean algorithm
    d = multiplicative_inverse(e, phi)
    return (n, e, d)

# message is the message to be encrypted, n is modulus and e is public key
def rsa_encrypt(message, n, e):
    return powmod_sm(message, e, n)  # return (message^e) mod n

def rsa_decrypt(cipher, n, d):  # cipher is the cipher text, n is modulus and d is private key
    return powmod_sm(cipher, d, n)  # return (cipher^d) mod n


# Driver code
print("RSA Encryptiona & Decryption program")
n, e, d = rsa_generate_key(1024)

msg = 19191919

eMsg = rsa_encrypt(msg, n, e)

print("Plain text: ", msg)
print("Cipher Text: ", eMsg)

dMsg = rsa_decrypt(eMsg, n, d)
print("Decrypted message: ", dMsg)  # 19191919
