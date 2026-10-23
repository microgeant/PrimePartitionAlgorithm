"""Full algorithm searched by "excess": a * b = prod(seeds) * k, for seed-smooth k <= K.

Every candidate pi_A +/- pi_B has every seed on exactly one side with exponent >= 1, so
pi_A * pi_B = prod(seeds) * k for some k built only from seed primes (k = 1 means every
exponent is 1). Witnesses found by the other searches cluster at small k: the extra
exponents sit on small primes (2, 3, 5) and only fine-tune an even split of the
seed product. So instead of capping exponents (E) or product size (X), this searches
k = 1, 2, 3, ... up to K.

For a fixed k, N = prod(seeds) * k has a fixed exponent f_p for each seed prime, and a
witness is a split of the prime powers p^f_p into two sides (a, b) with a * b = N. A
difference lands in the window only if a and b are within m^2 of each other, i.e. log a is
within a small tolerance of log(N) / 2. That is a subset-sum on the weights f_p * log p,
solved meet-in-the-middle (2^(n/2) per half); each hit is checked exactly with integers.
While seed sets are small (sums still possible), all 2^n splits are checked directly.

Usage: python3 prime_synthesis_excess.py [iterations] [log10_K]
"""
import math
import sys
import time
from bisect import bisect_left, bisect_right


def smooth_numbers(primes, limit):
    """All n <= limit built from `primes` (exponents >= 0), including 1."""
    out = [1]
    for p in primes:
        grown = []
        for n in out:
            v = n * p
            while v <= limit:
                grown.append(v)
                v *= p
        out += grown
    return out


def subset_products(powers):
    """(log, product) for every subset of `powers`."""
    out = [(0.0, 1)]
    for q in powers:
        lq = math.log(q)
        out += [(s + lq, v * q) for s, v in out]
    return out


def splits_near_half(powers, n_total, lo, hi):
    """Window values |a - b| (and a + b) over splits of `powers` into a * b = n_total."""
    found = set()
    if len(powers) <= 12:
        for _, a in subset_products(powers):
            b = n_total // a
            for v in (a + b, abs(a - b)):
                if lo < v <= hi:
                    found.add(v)
        return found

    # Differences only (sums can't reach the window this late). |a - b| <= hi with b = min(a, b)
    # needs b * (b + hi) >= n_total, and then |log a - log b| <= hi / b.
    b_min = max(1, math.isqrt(n_total + hi * hi // 4) - hi // 2 - 1)
    tol = hi / b_min * (1 + 1e-9) + 1e-12
    half = math.log(n_total) / 2
    k = len(powers) // 2
    left = subset_products(powers[:k])
    right = sorted(subset_products(powers[k:]))
    keys = [s for s, _ in right]
    for s, v in left:
        start = bisect_left(keys, half - tol / 2 - s)
        end = bisect_right(keys, half + tol / 2 - s, start)
        for _, w in right[start:end]:
            a = v * w
            d = abs(a - n_total // a)
            if lo < d <= hi:
                found.add(d)
    return found


def compute_primes(seeds, k_limit):
    """Window candidates over every seed-smooth excess k <= k_limit."""
    m = max(seeds)
    lo, hi = m, m * m
    primes = [p for p in seeds if p != 1]  # 1 only keeps both sides non-empty
    if not primes:
        return set()
    prod = math.prod(primes)
    found = set()
    for k in smooth_numbers(primes, k_limit):
        n_total = prod * k
        powers = []
        for p in primes:
            q = p
            while k % p == 0:
                k //= p
                q *= p
            powers.append(q)
        found |= splits_near_half(powers, n_total, lo, hi)
    return found


def main():
    iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    log10_k = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    k_limit = 10 ** log10_k
    current, pending = [1, 2], set()
    acc = set()
    t0 = time.perf_counter()
    for i in range(1, iterations + 1):
        t = time.perf_counter()
        found = sorted(compute_primes(current, k_limit))
        dt = time.perf_counter() - t
        print(f"iter {i}: seeds={current} K=1e{log10_k} time={dt:.3f}s found={len(found)}: {found}", flush=True)
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
