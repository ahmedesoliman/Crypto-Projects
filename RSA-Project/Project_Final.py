import random, math

num = random.SystemRandom()  # A single dice.

# implement miller rabin test for primality test  # https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test

def MRT(n, a): 
  exp = n - 1
  while not exp & 1:
    exp >>= 1 # bit shift right by 1 

  if pow(a, exp, n) == 1: # used pow() function to calculate a^exp mod n beacuse it is faster than normal method
    return True

  while exp < n - 1:
    if pow(a, exp, n) == n - 1:
      return True

    exp <<= 1

  return False

# k is the number of times we want to run the test. The higher the value of k, the more accurate the result will be. # https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
def miller_rabin(n, k=100):  
  for i in range(k):
    a = num.randrange(2, n - 1)
    if not MRT(n, a):
      return False

  return True

# Generate a random prime number of a given bit length.
def gen_prime(bits): # bits is the number of bits in the prime number
  while True:
    # Guarantees that a is odd.
    a = (num.randrange(1 << bits - 1, 1 << bits) << 1) + 1 # 1<<bits-1 is 2^(bits-1) and 1<<bits is 2^bits
    if miller_rabin(a): # if a is prime then return a
      return a


# Returns pair (x, y) such that xa + yb = gcd(a, b) # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
def EEA(a, b):

  x, lastx, y, lasty = 0, 1, 1, 0

  while b != 0:
    q, r = divmod(a, b)
    a, b = b, r
    x, lastx = lastx - q * x, x
    y, lasty = lasty - q * y, y

  return lastx, lasty


# Find the multiplicative inverse of e mod n. # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
def multiplicative_inverse(e, n):
  x, y = EEA(e, n)
  if x < 0:
    return n + x
  return x

# Generate a public/private key pair.
def rsa_generate_key(bits):
  p = gen_prime(bits)
  q = gen_prime(bits)

  # Ensure q != p, though for large values of bits this is
  # statistically very unlikely
  while q == p:
    q = gen_prime(bits)
  n = p * q
  phi = (p - 1) * (q - 1)

    # Here we pick a random e, but a fixed value for e can also be used.
  while True:
    e = random.randint(3, phi - 1)
    if math.gcd(e, phi) == 1:
      break
  # d * e = 1 mod phi 
  d = multiplicative_inverse(e, phi) # computer d using extended euclidean algorithm 
  return (n, e, d)


def powmod_sm(base, expo, n):
  expoBits = bin(expo)
  value = base

  for i in range(3, len(expoBits)):
    value = (value**2) % n
    if (expoBits[i:i + 1] == '1'):
      value = (value * base) % n

  return value


def rsa_encrypt(message, n, e):
  return powmod_sm(message, e, n)


def rsa_decrypt(cipher, n, d):
  return powmod_sm(cipher, d, n)


#Driver code
print("RSA Encryptiona & Decryption program")
n, e, d = rsa_generate_key(512)

msg = 121345465

eMsg = rsa_encrypt(msg, n, e)

print("Plain text: ", msg)
print("Cipher Text: ", eMsg)

dMsg = rsa_decrypt(eMsg, n, d)
print("Decrypted message: ", dMsg)



