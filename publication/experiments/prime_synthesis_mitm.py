"""Meet-in-the-middle difference sweep for the full algorithm (exponents on BOTH subsets).

Produces exactly the same candidate set as ../prime_synthesis.py's compute_primes,
without enumerating all (2E)^n configurations.

Why it works:
- Every seed must sit on one side with exponent >= 1, so pi_A * pi_B >= prod(seeds).
  By AM-GM, pi_A + pi_B >= 2*sqrt(prod(seeds)), so once that exceeds m^2 no SUM can
  land in the window. Only differences remain, and a difference lands in the window
  only when pi_A and pi_B are nearly equal.
- log(pi_A) - log(pi_B) = sum over seeds of (+/-) e_i * log(p_i), which splits over
  the SEEDS (not the partition sides). Enumerate each half of the seeds separately
  ((2E)^(n/2) states each), sort one half by log-ratio, and match states from the
  other half whose log-ratios nearly cancel. Each match is then checked exactly with
  integers, so floating point only ever narrows the search, never decides it.
- Tolerance: if m < |a - b| <= m^2 with b = min(a, b), then
  |log(a/b)| <= m^2 / b, and b*(b + m^2) >= a*b >= prod(seeds) gives a lower bound
  on b. So |r| <= m^2 / b_min is a necessary condition.

Usage: python3 prime_synthesis_mitm.py [iterations] [max_exp_cap]
"""
import math
import sys
import time
from bisect import bisect_left, bisect_right
from itertools import product as itertools_product


def brute_force(primes, max_exp, lo, hi):
    """Plain enumeration over (side, exponent) per prime; used only while sums are still possible."""
    found = set()
    states = [(s, e) for s in (1, -1) for e in range(1, max_exp + 1)]
    for combo in itertools_product(states, repeat=len(primes)):
        a = b = 1
        for p, (s, e) in zip(primes, combo):
            if s == 1:
                a *= p ** e
            else:
                b *= p ** e
        for v in (a + b, abs(a - b)):
            if lo < v <= hi:
                found.add(v)
    return found


def half_states(primes, max_exp, fix_first_side):
    """Log-ratios for every (side, exponent) assignment of `primes`, as a flat list.

    Flat index decodes in mixed radix: the last prime varies fastest.
    """
    r = [0.0]
    for i, p in enumerate(primes):
        lp = math.log(p)
        sides = (1,) if (fix_first_side and i == 0) else (1, -1)
        choices = [s * e * lp for s in sides for e in range(1, max_exp + 1)]
        r = [x + c for x in r for c in choices]
    return r


def decode(idx, primes, max_exp, fix_first_side):
    """Turn a flat state index back into exact integer products (a, b)."""
    radices = [max_exp if (fix_first_side and i == 0) else 2 * max_exp for i in range(len(primes))]
    digits = []
    for rad in reversed(radices):
        digits.append(idx % rad)
        idx //= rad
    digits.reverse()
    a = b = 1
    for p, d in zip(primes, digits):
        side, e = (1, d + 1) if d < max_exp else (-1, d - max_exp + 1)
        if side == 1:
            a *= p ** e
        else:
            b *= p ** e
    return a, b


def compute_primes(seeds, max_exp):
    """Same window and candidate set as ../prime_synthesis.py's compute_primes (as a set)."""
    m = max(seeds)
    lo, hi = m, m * m
    primes = [p for p in seeds if p != 1]  # 1^e = 1 on either side; it only keeps both sides non-empty
    if not primes:
        return set()
    prod = math.prod(primes)
    if 4 * prod <= hi * hi:  # 2*sqrt(prod) <= m^2: sums may still land in the window
        return brute_force(primes, max_exp, lo, hi)

    b_min = math.isqrt(prod + hi * hi // 4) - hi // 2 - 1
    tol = hi / max(b_min, 1) * (1 + 1e-9) + 1e-12

    # h2 (the smaller half) is materialized and sorted; h1 is streamed, never stored.
    k = len(primes) - len(primes) // 2
    h1, h2 = primes[:k], primes[k:]
    r2 = half_states(h2, max_exp, fix_first_side=False)
    order = sorted(range(len(r2)), key=r2.__getitem__)
    r2s = [r2[j] for j in order]
    del r2

    # Stream h1's states as (prefix x suffix) so its flat index i = ia * len(rb) + ib
    # still decodes in the same mixed radix (last prime fastest).
    j1 = len(h1) // 2 or 1
    ra = half_states(h1[:j1], max_exp, fix_first_side=True)  # global side swap gives the same |a - b|
    rb = half_states(h1[j1:], max_exp, fix_first_side=False)
    nb = len(rb)

    found = set()
    for ia, xa in enumerate(ra):
        for ib, xb in enumerate(rb):
            x = xa + xb
            start = bisect_left(r2s, -x - tol)
            end = bisect_right(r2s, -x + tol, start)
            if start == end:
                continue
            a1, b1 = decode(ia * nb + ib, h1, max_exp, True)
            for j in order[start:end]:
                a2, b2 = decode(j, h2, max_exp, False)
                d = abs(a1 * a2 - b1 * b2)
                if lo < d <= hi:
                    found.add(d)
    return found


def main():
    iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    cap = int(sys.argv[2]) if len(sys.argv) > 2 else None
    max_exp, current, pending = 1, [1, 2], set()
    acc = set()
    t0 = time.perf_counter()
    for i in range(1, iterations + 1):
        exp = max_exp if cap is None else min(max_exp, cap)
        t = time.perf_counter()
        found = sorted(compute_primes(current, exp))
        dt = time.perf_counter() - t
        print(f"iter {i}: seeds={current} max_exp={exp} time={dt:.3f}s found={len(found)}: {found}", flush=True)
        current_set = set(current)
        pending.update(x for x in found if x not in current_set)
        if pending:
            nxt = min(pending)
            pending.discard(nxt)
            current = current + [nxt]
        acc.update(found)
        max_exp += 1
    print(f"Total time: {time.perf_counter() - t0:.2f}s")
    print(f"Discovered primes: {sorted({2} | acc)}")


if __name__ == "__main__":
    main()
