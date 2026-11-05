"""The paper's algorithm over the Gaussian integers Z[i] ("rotations" by units and by Gaussian primes).

Same recipe as ../prime_synthesis.py, with Z[i] in place of Z:
- Seeds start at {1, 1+i} (1+i is the Gaussian prime over 2). Every seed sits on exactly one side
  of a binary partition with an exponent 1..E (E = iteration index); candidates are
  pi_A + u * pi_B for the four units u in {1, i, -1, -i} (over Z only u = +-1 exist: sum and
  difference). Values are kept up to associates (canonical form: re > 0, im >= 0).
- The smallest pending value (by norm, then re, im) joins the seeds each iteration.

No primality test. Euclid still applies, since Z[i] has unique factorization: every seed divides
exactly one side, so no seed divides a candidate. Window: M < N(z) < N(g)^2, with M the largest
seed norm and g the smallest-norm non-unit that is not a seed and is coprime to every seed (one
Gaussian gcd per tried value; no candidate is ever divided). A composite coprime to the seeds has
a prime factor q outside them, so its norm is at least N(q)^2 >= N(g)^2. (The paper's (m, m^2]
would not be safe here: conjugates such as 2+i and 2-i become seeds one at a time.)

Search: |pi_A + u pi_B| < sqrt(W) needs | |pi_A| - |pi_B| | < sqrt(W), so the halves of the seeds
are matched meet-in-the-middle on log|pi_A| - log|pi_B| = sum of +-e * log|rho| (as over Z), and
each match is checked exactly for all four units. The angle condition is what over Z does not
exist: a match also needs arg(pi_A) ~ arg(-u pi_B).

Gaussian primality is used only in the report, to verify results.

Usage: python3 gaussian_prime_synthesis.py [iterations] > report.md
"""
import math
import sys
import time
from bisect import bisect_left, bisect_right

UNITS = ((1, 0), (0, 1), (-1, 0), (0, -1))


def mul(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def norm(x):
    return x[0] * x[0] + x[1] * x[1]


def canonical(x):
    """The associate with re > 0 and im >= 0."""
    for u in UNITS:
        a, b = mul(x, u)
        if a > 0 and b >= 0:
            return (a, b)
    return x  # zero


def gauss_gcd(x, y):
    while y != (0, 0):
        n = norm(y)
        p = mul(x, (y[0], -y[1]))  # x / y = p / n
        q = ((2 * p[0] + n) // (2 * n), (2 * p[1] + n) // (2 * n))  # round to nearest
        qy = mul(q, y)
        x, y = y, (x[0] - qy[0], x[1] - qy[1])
    return x


def show(z):
    a, b = z
    return str(a) if b == 0 else f"{a}{'+' if b > 0 else '-'}{abs(b) if abs(b) != 1 else ''}i"


def window_top(seeds):
    """N(g)^2 - 1, g as in the module docstring (searched in order of norm)."""
    prod = (1, 0)
    for s in seeds:
        prod = mul(prod, s)
    seed_set = set(seeds)
    n = 2
    while True:
        r = math.isqrt(n)
        for a in range(1, r + 1):
            b2 = n - a * a
            b = math.isqrt(b2)
            if b * b == b2 and (a, b) not in seed_set and norm(gauss_gcd(prod, (a, b))) == 1:
                return n * n - 1
        n += 1


class Half:
    """(side, exponent) assignments of some seed primes; digit d < E: side A with e = d + 1."""

    def __init__(self, primes, max_exp, fix_first):
        self.primes, self.E, self.fix_first = primes, max_exp, fix_first
        self.logs = [0.5 * math.log(norm(p)) for p in primes]
        self.pows = [[(1, 0)] + [None] * max_exp for _ in primes]
        for i, p in enumerate(primes):
            for e in range(1, max_exp + 1):
                self.pows[i][e] = mul(self.pows[i][e - 1], p)

    def radix(self, i):
        return self.E if self.fix_first and i == 0 else 2 * self.E

    def keys(self):
        r = [0.0]
        for i, lp in enumerate(self.logs):
            ch = [(d + 1) * lp if d < self.E else -(d - self.E + 1) * lp for d in range(self.radix(i))]
            r = [x + c for x in r for c in ch]
        return r

    def decode(self, idx):
        a = b = (1, 0)
        for i in reversed(range(len(self.primes))):
            idx, d = divmod(idx, self.radix(i))
            if d < self.E:
                a = mul(a, self.pows[i][d + 1])
            else:
                b = mul(b, self.pows[i][d - self.E + 1])
        return a, b


def compute(seeds, max_exp):
    """Canonical candidates z = pi_A + u pi_B with M < N(z) <= window_top(seeds); also the hit count."""
    lo = max(norm(s) for s in seeds)
    hi = window_top(seeds)
    primes = [s for s in seeds if s != (1, 0)]
    q = math.prod(norm(p) for p in primes)
    root_w = math.sqrt(hi + 1)
    b_min = max((-root_w + math.sqrt(hi + 1 + 4 * math.sqrt(q))) / 2, 1e-300)
    tol = root_w / b_min * (1 + 1e-9) + 1e-12  # | log|a| - log|b| | bound for a hit

    k = (len(primes) + 1) // 2
    h1 = Half(primes[:k], max_exp, fix_first=True)  # swapping sides gives an associate
    h2 = Half(primes[k:], max_exp, fix_first=False)
    k2 = h2.keys()
    order = sorted(range(len(k2)), key=k2.__getitem__)
    k2s = [k2[j] for j in order]
    found, hits = set(), 0
    for i, x in enumerate(h1.keys()):
        s = bisect_left(k2s, -x - tol)
        e = bisect_right(k2s, -x + tol, s)
        if s == e:
            continue
        a1, b1 = h1.decode(i)
        for j in range(s, e):
            a2, b2 = h2.decode(order[j])
            a, b = mul(a1, a2), mul(b1, b2)
            for u in UNITS:
                ub = mul(u, b)
                z = (a[0] + ub[0], a[1] + ub[1])
                if lo < norm(z) <= hi:
                    hits += 1
                    found.add(canonical(z))
    return found, lo, hi, hits


def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def rational_prime(z):
    """The rational prime under Gaussian prime z, or None if z is not a Gaussian prime (report only)."""
    a, b = z
    if a == 0 or b == 0:
        q = abs(a or b)
        return q if is_prime(q) and q % 4 == 3 else None
    return norm(z) if is_prime(norm(z)) else None


def main():
    iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    current, pending, acc = [(1, 0), (1, 1)], set(), {(1, 1)}
    rows = []
    t0 = time.perf_counter()
    for it in range(1, iterations + 1):
        t = time.perf_counter()
        found, lo, hi, hits = compute(current, it)
        dt = time.perf_counter() - t
        new = found - acc
        acc |= found
        pending |= {z for z in found if z not in current}
        nxt = min(pending, key=lambda z: (norm(z), z)) if pending else None
        if nxt is not None:
            pending.discard(nxt)
        rows.append((it, list(current), lo, hi, hits, len(found), len(new), nxt, dt))
        print(f"iter {it}: seeds={[show(s) for s in current]} window=({lo}, {hi}] hits={hits} "
              f"found={len(found)} new={len(new)} time={dt:.2f}s", file=sys.stderr, flush=True)
        if nxt is not None:
            current = current + [nxt]
    total = time.perf_counter() - t0

    bad = sorted((z for z in acc if rational_prime(z) is None), key=lambda z: (norm(z), z))
    rat = sorted({rational_prime(z) for z in acc} - {None})
    gap = 2
    while gap in rat:
        gap += 1
        while not is_prime(gap):
            gap += 1
    split = sorted(p for p in rat if p % 4 == 1)
    split_both = [p for p in split if sum(1 for z in acc if norm(z) == p) == 2]

    o = [f"# gaussian_prime_synthesis.py — {iterations}-Iteration Run Results\n",
         "The paper's algorithm over Z[i]: seeds start at {1, 1+i}; candidates pi_A + u*pi_B for the four "
         "units u; window M < N(z) < N(g)^2 (see the script's docstring). Values are up to associates.\n",
         f"Total wall-clock time: **{total:.2f}s**\n",
         f"Gaussian primes found: **{len(acc)}** (including the seed 1+i); "
         + ("**all verified Gaussian primes**" if not bad else f"**NOT prime: {', '.join(map(show, bad))}**") + "\n",
         f"Rational primes recovered (2, norms p ≡ 1 mod 4, inert q ≡ 3 mod 4): **{len(rat)}**, "
         f"largest {max(rat)}, gap-free up to **{max(p for p in rat if p < gap)}** (first missing: {gap})\n",
         f"Split primes p ≡ 1 mod 4 with both conjugates found: {len(split_both)} of {len(split)}\n",
         "\n## Per-Iteration Summary\n",
         "| Iteration | Seeds before | E | Norm window | Window hits | Distinct found | New | Added to seeds | Time (s) |",
         "|---|---|---|---|---|---|---|---|---|"]
    for it, seeds, lo, hi, hits, nf, nn, nxt, dt in rows:
        o.append(f"| {it} | {', '.join(map(show, seeds))} | {it} | ({lo}, {hi}] | {hits} | {nf} | {nn} | "
                 f"{show(nxt) if nxt else '—'} | {dt:.2f} |")
    o.append("\n## Rational Primes Recovered\n")
    o.append(", ".join(map(str, rat)))
    o.append("\n## Gaussian Primes Found (by norm)\n")
    o.append(", ".join(f"{show(z)} ({norm(z)})" for z in sorted(acc, key=lambda z: (norm(z), z))))
    print("\n".join(o))


if __name__ == "__main__":
    main()
