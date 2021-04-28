import random
from collections import namedtuple


def get_primes(start, stop):
    if start >= stop:
        return []

    primes = [2]

    for n in range(3, stop + 1, 2):
        for p in primes:
            if n % p == 0:
                break
        else:
            primes.append(n)

    while primes and primes[0] < start:
        del primes[0]

    return primes


def are_relatively_prime(a, b):
    for n in range(2, min(a, b) + 1):
        if a % n == b % n == 0:
            return False
    return True


def make_key_pair(length):
    """Create a public-private key pair.

    The key pair is generated from two random prime numbers. The argument
    ``length`` specifies the bit length of the number ``n`` shared between
    the two keys: the higher, the better.
    """
    if length < 4:
        raise ValueError('cannot generate a key of length less '
                         'than 4 (got {!r})'.format(length))

    # First step: find a number ``n`` which is the product of two prime
    # numbers (``p`` and ``q``). ``n`` must have the number of bits specified
    # by ``length``, therefore it must be in ``range(n_min, n_max + 1)``.
    n_min = 1 << (length - 1)
    n_max = (1 << length) - 1

    # The key is stronger if ``p`` and ``q`` have similar bit length. We
    # choose two prime numbers in ``range(start, stop)`` so that the
    # difference of bit lengths is at most 2.
    start = 1 << (length // 2 - 1)
    stop = 1 << (length // 2 + 1)
    primes = get_primes(start, stop)

    # Now that we have a list of prime number candidates, randomly select
    # two so that their product is in ``range(n_min, n_max + 1)``.
    while primes:
        p = random.choice(primes)
        primes.remove(p)
        q_candidates = [q for q in primes
                        if n_min <= p * q <= n_max]
        if q_candidates:
            q = random.choice(q_candidates)
            break
    else:
        raise AssertionError("cannot find 'p' and 'q' for a key of "
                             "length={!r}".format(length))

    # Second step: choose a number ``e`` lower than ``(p - 1) * (q - 1)``
    # which shares no factors with ``(p - 1) * (q - 1)``.
    stop = (p - 1) * (q - 1)
    for e in range(3, stop, 2):
        if are_relatively_prime(e, stop):
            break
    else:
        raise AssertionError("cannot find 'e' with p={!r} "
                             "and q={!r}".format(p, q))

    # Third step: find ``d`` such that ``(d * e - 1)`` is divisible by
    # ``(p - 1) * (q - 1)``.
    for d in range(3, stop, 2):
        if d * e % stop == 1:
            break
    else:
        raise AssertionError("cannot find 'd' with p={!r}, q={!r} "
                             "and e={!r}".format(p, q, e))
    return PublicKey(p * q, e), PrivateKey(p * q, d)


class PublicKey(namedtuple('PublicKey', 'n e')):
    __slots__ = ()

    def encrypt(self, x):
        return pow(x, self.e, self.n)


class PrivateKey(namedtuple('PrivateKey', 'n d')):
    __slots__ = ()

    def decrypt(self, x):
        return pow(x, self.d, self.n)


if __name__ == '__main__':
    public_key, private_key = make_key_pair(12)
    print(public_key)
    print(private_key)

    encrypted_message = public_key.encrypt(123)
    print(encrypted_message)
    decrypted_message = private_key.decrypt(encrypted_message)
    print(decrypted_message)
