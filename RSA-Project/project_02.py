import random


def MRT(p):
  if p == 2 or p == 3:
    return True
  if p <= 1 or p % 2 == 0:
    return False

  p1 = p - 1
  t = 15
  u = 0
  r = p1

  while r % 2 == 0:
    u = u + 1
    r = r / 2
    for i in range(1, t):
      a = random.randint(2, p - 2)
      z = powMod_sm(a, int(r), p)
      if z != 1 and z != p1:
        j = 1

        while j < u and z != p1:
          z = powMod_sm(z, 2, p)
          if z == 1:
            return False
          j += 1

        if z != p1:
          return False

    return True


def gen_prime(len):
  n = random.getrandbits(len)
  n |= (1 << len - 1) | 1
  while not MRT(n):
    n = random.getrandbits(len)
    n |= (1 << len - 1) | 1
  return n


def computeGCD(x, y):
  while y:
    x, y = y, x % y

  return x


def extendedGCD(a, b):
  if a == 0:
    return b, 0, 1
  gcd, x1, y1 = extendedGCD(b % a, a)
  x = y1 - (b // a) * x1
  y = x1
  return gcd, x, y


def mod_Inv(b, n):
  gcd, _, t = extendedGCD(n, b)
  if gcd == 1:
    i = t % n
  elif gcd != 1:
    print("No inverse found")
  return i


def powMod_sm(base, exp, n):
  exp_b = bin(exp)
  value = base
  for i in range(3, len(exp_b)):
    value = (value**2) % n
    if exp_b[i:i + 1] == '1':
      value = (value * base) % n
  return value


def rsa_keyGen(p, q):
  n = p * q
  phi_n = (p - 1) * (q - 1)
  for i in range(2, 124):
    if computeGCD(i, phi_n) == 1:
      e = i
      break
    d = mod_Inv(e, phi_n)
    return n, e, d



#driver code block
p = gen_prime(512)
q = gen_prime(512)

# while p != q:
#   q = gen_prime(512)

print("First prime #", p)
print("Second prime #", q)

n, e, d, = rsa_keyGen(p, q)

print("public key (e, n) =", e, n)
print("private key (d, n) =", d, n)

m = 540
print("message = ", m)

y = int(powMod_sm(m, e, n))
print("encrypted = ", y)

x = int(powMod_sm(y, int(d), n))
print("decrypted = ", x)
