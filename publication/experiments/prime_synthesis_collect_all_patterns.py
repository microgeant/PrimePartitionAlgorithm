"""Window-less variant with the paper's adaptive exponents, analysed for exponent patterns.

Same partitions and exponents as ../prime_synthesis.py (iteration k: every seed takes an
exponent 1..k, on both sides), but no range check: every sum and difference is collected,
and the smallest new value becomes the next seed.

For every exponent vector it records whether pi_A + pi_B and |pi_A - pi_B| are prime, then
compares each group of vectors against the number of primes its sizes alone would predict:
a value N coprime to every seed is prime with probability about prod(p / (p - 1)) / ln N over
the seed primes p (and certainly prime below g^2, g the smallest prime missing from the seeds).
A ratio far from 1 means the exponents matter beyond size.

Primality (Miller-Rabin, first 20 prime bases) is used only for this analysis.

Usage: python3 prime_synthesis_collect_all_patterns.py [iterations] > report.md
"""
import math
import sys
import time
from collections import defaultdict
from functools import reduce
from itertools import product as itertools_product

BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71)


def is_prime(n):
    if n < 2:
        return False
    for p in BASES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in BASES:
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


class Stats:
    def __init__(self):
        self.n = 0
        self.primes = 0
        self.expected = 0.0

    def add(self, prime, expected):
        self.n += 1
        self.primes += prime
        self.expected += expected

    def row(self, label):
        ratio = self.primes / self.expected if self.expected else float("nan")
        return f"| {label} | {self.n} | {self.primes} | {100 * self.primes / self.n:.1f}% | {self.expected:.0f} | **{ratio:.2f}** |"


def main():
    iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    current, pending = [1, 2], set()
    groups = defaultdict(lambda: defaultdict(Stats))  # table -> key -> Stats
    per_iter = []
    t0 = time.perf_counter()

    for it in range(1, iterations + 1):
        max_exp = it
        primes = [p for p in current if p != 1]
        boost = math.prod(p / (p - 1) for p in primes)
        g = 2
        while g in current or math.gcd(g, math.prod(primes)) != 1:
            g += 1
        safe = g * g  # below this, a value coprime to the seeds is certainly prime
        found = set()
        n_vec = n_prime = 0
        t = time.perf_counter()
        # Each prime: side (+1 = A, -1 = B) and exponent. Fix the first prime on side A:
        # swapping the sides gives the same sum and |difference|.
        choices = [[(1, e) for e in range(1, max_exp + 1)]] + \
                  [[(s, e) for s in (1, -1) for e in range(1, max_exp + 1)] for _ in primes[1:]]
        for vec in itertools_product(*choices):
            a = b = 1
            for p, (s, e) in zip(primes, vec):
                if s > 0:
                    a *= p ** e
                else:
                    b *= p ** e
            exps = [e for _, e in vec]
            gcd_e = reduce(math.gcd, exps)
            n_big = sum(1 for e in exps if e > 1)
            e2 = vec[0][1]
            same_side_2 = "2 alone" if all(s < 0 for s, _ in vec[1:]) else "2 with others"
            for op, v in (("sum", a + b), ("diff", abs(a - b))):
                if v < 2:
                    continue
                found.add(v)
                prime = is_prime(v)
                expected = 1.0 if v < safe else min(1.0, boost / math.log(v))
                n_vec += 1
                n_prime += prime
                groups["gcd"][(op, gcd_e)].add(prime, expected)
                groups["parity"][(op, "all even" if gcd_e % 2 == 0 else "some odd")].add(prime, expected)
                groups["nbig"][(op, n_big)].add(prime, expected)
                groups["e2"][(op, e2)].add(prime, expected)
                groups["side2"][(op, same_side_2)].add(prime, expected)
                groups["all"][op].add(prime, expected)
        dt = time.perf_counter() - t
        current_set = set(current)
        pending.update(x for x in found if x not in current_set)
        added = min(pending) if pending else None
        if added is not None:
            pending.discard(added)
        per_iter.append((it, list(current), max_exp, n_vec, n_prime, len(found), added, is_prime(added) if added else None, dt))
        print(f"iter {it}: seeds={current} E={max_exp} values={n_vec} primes={n_prime} time={dt:.1f}s", file=sys.stderr, flush=True)
        if added is not None:
            current = current + [added]

    total = time.perf_counter() - t0
    o = [f"# prime_synthesis_collect_all_patterns.py — {iterations}-Iteration Run Results\n",
         "Window-less, with the paper's adaptive exponents (iteration k: exponents 1..k on every seed, "
         "both sides). Every sum and difference is collected; the smallest new value becomes the next seed. "
         "Counts are per exponent vector (one sum and one difference each), not per distinct value.\n",
         "**Ratio** = primes observed / primes expected from size alone "
         "(prod p/(p-1) / ln N for values coprime to the seeds; 1 below g²). "
         "1.00 means the exponents add nothing beyond size; 0 means never prime.\n",
         f"Total wall-clock time: **{total:.1f}s**\n",
         "## Per-Iteration Summary\n",
         "| Iteration | Seeds | E | Values (vectors × 2) | Prime | Distinct values | Next seed | Next seed prime? | Time (s) |",
         "|---|---|---|---|---|---|---|---|---|"]
    for it, seeds, e, nv, npr, nd, added, ap, dt in per_iter:
        o.append(f"| {it} | {', '.join(map(str, seeds))} | {e} | {nv} | {npr} ({100 * npr / nv:.1f}%) | {nd} | {added} | {'yes' if ap else 'NO'} | {dt:.1f} |")

    def table(name, title, keyfmt):
        o.append(f"\n## {title}\n")
        o.append("| Group | Values | Prime | Prime rate | Expected from size | Ratio |\n|---|---|---|---|---|---|")
        for key in sorted(groups[name], key=lambda k: (str(k[0]), k[1]) if isinstance(k, tuple) else (k,)):
            o.append(groups[name][key].row(keyfmt(key)))

    table("all", "All values", lambda k: k)
    table("gcd", "By gcd of all exponents", lambda k: f"{k[0]}, gcd = {k[1]}")
    table("parity", "All exponents even vs. not", lambda k: f"{k[0]}, {k[1]}")
    table("nbig", "By number of exponents above 1", lambda k: f"{k[0]}, {k[1]} above 1")
    table("e2", "By the exponent on 2", lambda k: f"{k[0]}, 2^{k[1]}")
    table("side2", "2 alone on its side vs. with other seeds", lambda k: f"{k[0]}, {k[1]}")
    print("\n".join(o))


if __name__ == "__main__":
    main()
