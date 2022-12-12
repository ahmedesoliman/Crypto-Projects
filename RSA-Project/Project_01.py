import random, itertools, math


# Generate random prime number with n bits.
def MRT(bits, isPrime):

  get_random_t = lambda: random.getrandbits(bits) | 1 << bits | 1

  p = get_random_t()

  for i in itertools.count(1):
    if isPrime(p):
      print("In loop", p)
      return p
    else:
      if i % (bits * 2) == 0:
        p = get_random_t()
      else:
        p += 2  # Add 2 since we are only interested in odd numbers


def isPrime(n):
  k = 40
  # Corner cases
  if (n <= 1 or n == 4):
    return False

  if (n <= 3):
    return True

  # Find r such that n = 2^d * r + 1 for some r >= 1
  d = n - 1
  while (d % 2 == 0):
    d //= 2

  # Iterate given nber of 'k' times
  for i in range(k):
    if (miillerTest(d, n) == False):
      return False

  return True

# Returns True if n is a prime. False otherwise.
# def simple_is_prime(n):

#   if n % 2 == 0:
#     return n == 2
#   if n % 3 == 0:
#     return n == 3
#   k = 6
#   while (k - 1)**2 <= n:
#     if n % (k - 1) == 0 or n % (k + 1) == 0:
#       return False
#     k += 6
#   return True


# def rabin_miller_is_prime(n, k=20):
#     """
#     Test n for primality using Rabin-Miller algorithm, with k
#     random witness attempts. False return means n is certainly a composite.
#     True return value indicates n is *probably* a prime. False positive
#     probability is reduced exponentially the larger k gets.
#     """
#     b = basic_is_prime(n, K=100)
#     if b is not None:
#         return b

#     m = n - 1
#     s = 0
#     while m % 2 == 0:
#         s += 1
#         m //= 2
#     liars = set()
#     get_new_x = lambda: random.randint(2, n - 1)
#     while len(liars) < k:
#         x = get_new_x()
#         while x in liars:
#             x = get_new_x()
#         xi = pow(x, m, n)
#         witness = True
#         if xi == 1 or xi == n - 1:
#             witness = False
#         else:
#             for __ in xrange(s - 1):
#                 xi = (xi ** 2) % n
#                 if xi == 1:
#                     return False
#                 elif xi == n - 1:
#                     witness = False
#                     break
#             xi = (xi ** 2) % n
#             if xi != 1:
#                 return False
#         if witness:
#             return False
#         else:
#             liars.add(x)
#     return True

# def basic_is_prime(n, K=-1):
#   """Returns True if n is a prime, and False it is a composite
#     by trying to divide it by two and first K odd primes. Returns
#     None if test is inconclusive."""
#   if n % 2 == 0:
#     return n == 2
#   for p in primes_list.less_than_hundred_thousand[:K]:
#     if n % p == 0:
#       return n == p
#   return None


def miillerTest(d, n):
  # Pick a random number in [2..n-2]
  # Corner cases make sure that n > 4
  a = 2 + random.randint(1, n - 4)

  # Compute a^d % n
  x = power(a, d, n)

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
def power(x, m, n):
  a = 1
  while m > 0:
    if m % 2 == 1:
      a = (a * x) % n
  x = (x * x) % n
  m //= 2
  return a

def powmod_sm(base, exp, n):
  exp_b = bin(exp)
  value = base
  
  for i in range(3, len(exp_b)):
    value = (value ** 2) % n
    if(exp_b[i:i+1]== '1'):
      value = (value * base) % n
  
  return value

def rsa_generate_key(bits):
  p = MRT(bits, isPrime)
  q = MRT(bits, isPrime)

  # Ensure q != p, though for large values of bits this is
  # statistically very unlikely
  while q == p:
    q = MRT(bits, isPrime)
  n = p * q
  phi = (p - 1) * (q - 1)

    # Here we pick a random e, but a fixed value for e can also be used.
  while True:
    e = random.randint(3, phi - 1)
    if math.gcd(e, phi) == 1:
      break
  d = multiplicative_inverse(e, phi)
  return (n, e, d)


def rsa_encrypt(message, n, e):
  return powmod_sm(message, e, n)


def rsa_decrypt(cipher, n, d):
  return powmod_sm(cipher, d, n)


#Driver code
print("Inside encryptiona & decryption program using RSA")
n, e, d = rsa_generate_key(512)

message = 121345465

encrypted_message = rsa_encrypt(message, n, e)

print(encrypted_message)

print(rsa_decrypt(encrypted_message, n, d))  #121345465
