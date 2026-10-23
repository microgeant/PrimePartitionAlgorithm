"""Meet-in-the-middle sweep for the left-only variant (prime_synthesis_left_exp.py).

Produces exactly the same candidate set per iteration as prime_synthesis_left_exp.py's
compute_primes, without enumerating every exponent vector.

Why it works:
- Left subset A gets exponents 1..E; the right subset B is a plain product (exponent 1).
  So pi_A * pi_B >= prod(seeds), and once 2*sqrt(prod(seeds)) > m^2 no SUM can land in
  the window (AM-GM). Only differences remain.
- With L = log(prod(seeds)): log(pi_A) - log(pi_B) = sum_{i in A} (e_i + 1) * log(p_i) - L.
  A difference lands in the window only when that is ~0, i.e. the weighted sum
  S = sum_{i in A} (e_i + 1) * log(p_i) is within a tolerance of L.
- Every weight is positive, so any partial assignment with S > L + tol is pruned while
  enumerating. This bounds the useful exponents on its own, so even an uncapped
  (adaptive) schedule stays small.
- Split the seeds into two halves, enumerate each half's pruned (S, state) pairs, sort
  one, and match pairs whose sums land within tol of L. Each match is checked exactly
  with integers; floating point only narrows the search.
- Tolerance: if m < |a - b| <= m^2 with b = min(a, b), then |log(a/b)| <= m^2 / b, and
  b*(b + m^2) >= a*b >= prod(seeds) gives a lower bound on b.

Usage: python3 prime_synthesis_left_exp_mitm.py [iterations] [max_exp_cap]
"""
import math
import sys
import time
from bisect import bisect_left, bisect_right
from itertools import product as itertools_product


def brute_force(primes, max_exp, lo, hi):
    """Plain enumeration (each prime: right, or left with exponent 1..E); used only while sums are possible."""
    found = set()
    for exps in itertools_product(range(max_exp + 1), repeat=len(primes)):  # 0 = right side
        if not any(exps):
            continue  # left subset must be non-empty
        a = b = 1
        for p, e in zip(primes, exps):
            if e:
                a *= p ** e
            else:
                b *= p
        for v in (a + b, abs(a - b)):
            if lo < v <= hi:
                found.add(v)
    return found


def half_states(primes, max_exp, limit):
    """All (S, exps) for `primes` with S = sum over left primes of (e + 1) * log(p) <= limit."""
    states = [(0.0, ())]
    for p in primes:
        lp = math.log(p)
        weights = [(0.0, 0)] + [((e + 1) * lp, e) for e in range(1, max_exp + 1)]
        states = [(s + w, exps + (e,)) for s, exps in states for w, e in weights if s + w <= limit]
    return states


def products(primes, exps):
    a = b = 1
    for p, e in zip(primes, exps):
        if e:
            a *= p ** e
        else:
            b *= p
    return a, b


def compute_primes(seeds, max_exp):
    """Same window and candidate set as prime_synthesis_left_exp.py's compute_primes (as a set)."""
    m = max(seeds)
    lo, hi = m, m * m
    primes = [p for p in seeds if p != 1]  # 1 always sits on the right; 1^e = 1
    if not primes:
        return set()
    prod = math.prod(primes)
    if 4 * prod <= hi * hi:  # 2*sqrt(prod) <= m^2: sums may still land in the window
        return brute_force(primes, max_exp, lo, hi)

    b_min = math.isqrt(prod + hi * hi // 4) - hi // 2 - 1
    tol = hi / max(b_min, 1) * (1 + 1e-9) + 1e-12
    L = math.log(prod)

    k = len(primes) // 2
    h1, h2 = primes[:k], primes[k:]
    s1 = half_states(h1, max_exp, L + tol)
    s2 = sorted(half_states(h2, max_exp, L + tol))
    keys = [s for s, _ in s2]

    found = set()
    for x, e1 in s1:
        start = bisect_left(keys, L - tol - x)
        end = bisect_right(keys, L + tol - x, start)
        if start == end:
            continue
        a1, b1 = products(h1, e1)
        for _, e2 in s2[start:end]:
            a2, b2 = products(h2, e2)
            a, b = a1 * a2, b1 * b2
            if a == 1:
                continue  # left subset empty
            d = abs(a - b)
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
