import random, math, itertools

def MRT(bits):
    """Generate random prime number with n bits."""
    get_random_t = lambda: random.getrandbits(bits) | 1 << bits | 1
    p = get_random_t()
    for i in itertools.count(1):
        if isPrime(p):
            return p
        else:
            if i % (bits * 2) == 0:
             p = get_random_t()
            else:
                p += 2 # Add 2 since we are only interested in odd numbers

def miillerTest(d, n):
    # Pick a random number in [2..n-2]
    # Corner cases make sure that n > 4
    a = 2 + random.randint(1, n - 4);

    # Compute a^d % n
    x = power(a, d, n);

    if (x == 1 or x == n - 1):
        return True;

    # Keep squaring x while one
    # of the following doesn't
    # happen
    # (i) d does not reach n-1
    # (ii) (x^2) % n is not 1
    # (iii) (x^2) % n is not n-1
    while (d != n - 1):
        x = (x * x) % n;
        d *= 2;

        if (x == 1):
            return False;
        if (x == n - 1):
            return True;

        # Return composite
        return False;

def isPrime( n, k=100):
    # Corner cases
    if (n <= 1 or n == 4):
        return False;
    if (n <= 3):
        return True;

    # Find r such that n = 2^d * r + 1 for some r >= 1
    d = n - 1;
    while (d % 2 == 0):
        d //= 2;

    # Iterate given nber of 'k' times
    for i in range(k):
        if (miillerTest(d, n) == False):
            return False;

    return True;

def EEA(a, b):
    """Returns pair (x, y) such that xa + yb = gcd(a, b)"""
    x, lastx, y, lasty = 0, 1, 1, 0
    while b != 0:
        q, r = divmod(a, b)
        a, b = b, r
        x, lastx = lastx - q * x, x
        y, lasty = lasty - q * y, y
        
    return lastx, lasty

def multiplicative_inverse(e, n):
    """Find the multiplicative inverse of e mod n."""
    x, y = EEA(e, n)
    if x < 0:
        return n + x

    return x

def power(x, m, n):
    """Calculate x^m modulo n using O(log(m)) operations."""
    a = 1
    while m > 0:
        if m % 2 == 1:
            a = (a * x) % n
        x = (x * x) % n
        m //= 2

    return a

def rsa_generate_key(bits):
    p = MRT(bits // 2)
    q = MRT(bits // 2)
    # Ensure q != p, though for large values of bits this is
    # statistically very unlikely
    while q == p:
        q = MRT(bits // 2)
    
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
    return power(message, e, n)

def rsa_decrypt(cipher, n, d):
    return power(cipher, d, n)

n , e , d = rsa_generate_key(1024)

message = 121345465

print(message)

encrypted_message = rsa_encrypt(message,n,e)

print(encrypted_message)

print(rsa_decrypt(encrypted_message , n ,d)) #121345465