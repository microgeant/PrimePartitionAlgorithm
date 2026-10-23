"""Full algorithm with the exponent cap replaced by a size bound X on the products.

A candidate is pi_A +/- pi_B where every seed sits on exactly one side with exponent >= 1
(as in ../prime_synthesis.py), but instead of capping each exponent at E, both products
are only required to be <= X. Exponents are otherwise unbounded.

How it works:
- pi_A and pi_B are seed-smooth numbers with complementary supports: every seed prime
  divides exactly one of them. So enumerate every seed-smooth number n <= X together with
  its support (bitmask of the seed primes dividing it), and sort them.
- A difference lands in the window only if pi_A and pi_B are within m^2 of each other, so
  a two-pointer sweep over the sorted list visits only pairs that close together, and
  keeps those whose supports are complementary.
- pi_A * pi_B >= prod(seeds) and |pi_A - pi_B| <= m^2 give a lower bound b_min on the
  smaller product, so numbers below it are skipped.
- Sums can land in the window only while 2*sqrt(prod(seeds)) <= m^2 (AM-GM); those
  iterations are small and checked directly.

Usage: python3 prime_synthesis_size_bound.py [iterations] [log10_X]
"""
import math
import sys
import time


def smooth_numbers(primes, limit):
    """All (n, mask) with n <= limit built from `primes` (exponents >= 0); mask = primes used."""
    out = [(1, 0)]
    for i, p in enumerate(primes):
        bit = 1 << i
        grown = []
        for n, mask in out:
            v = n * p
            while v <= limit:
                grown.append((v, mask | bit))
                v *= p
        out += grown
    return out


def compute_primes(seeds, limit):
    """Window candidates pi_A +/- pi_B with complementary supports and both products <= limit."""
    m = max(seeds)
    lo, hi = m, m * m
    primes = [p for p in seeds if p != 1]  # 1^e = 1; it only keeps both sides non-empty
    if not primes:
        return set()
    full = (1 << len(primes)) - 1
    prod = math.prod(primes)
    found = set()

    if 4 * prod <= hi * hi:  # sums still possible: both sides <= m^2
        small = smooth_numbers(primes, min(limit, hi))
        for a, ma in small:
            for b, mb in small:
                if ma & mb == 0 and ma | mb == full and lo < a + b <= hi:
                    found.add(a + b)

    # Pack each (n, mask) into one int, n << k | mask: sorts by n and costs far less memory than tuples.
    b_min = max(1, math.isqrt(prod + hi * hi // 4) - hi // 2 - 1)
    k = len(primes)
    nums = sorted(packed_smooth_numbers(primes, limit, b_min))
    low_bits = (1 << k) - 1
    count = len(nums)
    for i, x in enumerate(nums):
        a, need = x >> k, full ^ (x & low_bits)
        j = i + 1
        while j < count:
            y = nums[j]
            b = y >> k
            if b - a > hi:
                break
            if b - a > lo and y & low_bits == need:
                found.add(b - a)
            j += 1
    return found


def packed_smooth_numbers(primes, limit, floor):
    """Yield n << len(primes) | mask for every primes-smooth n with floor <= n <= limit (iterative DFS)."""
    k = len(primes)
    stack = [(1, 0, 0)]  # (n, mask, index of the next prime allowed); primes taken in order, so no duplicates
    while stack:
        n, mask, start = stack.pop()
        if n >= floor:
            yield n << k | mask
        for i in range(start, k):
            v = n * primes[i]
            if v > limit:
                break  # primes are ascending, so larger primes overshoot too
            stack.append((v, mask | 1 << i, i))


def main():
    iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    log10_x = int(sys.argv[2]) if len(sys.argv) > 2 else 18
    limit = 10 ** log10_x
    current, pending = [1, 2], set()
    acc = set()
    t0 = time.perf_counter()
    for i in range(1, iterations + 1):
        t = time.perf_counter()
        found = sorted(compute_primes(current, limit))
        dt = time.perf_counter() - t
        print(f"iter {i}: seeds={current} X=1e{log10_x} time={dt:.3f}s found={len(found)}: {found}", flush=True)
        current_set = set(current)
        pending.update(x for x in found if x not in current_set)
        if pending:
            nxt = min(pending)
            pending.discard(nxt)
            current = current + [nxt]
        acc.update(found)
    print(f"Total time: {time.perf_counter() - t0:.2f}s")
    print(f"Discovered primes: {sorted({2} | acc)}")


if __name__ == "__main__":
    main()
