"""Run prime_synthesis_left_exp.py for N iterations and print a Markdown report.

Usage: python3 prime_synthesis_left_exp_report.py [iterations] [max_exp_cap] > results.md
Per-iteration progress goes to stderr.
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prime_synthesis_left_exp import compute_primes

def is_prime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True

ITER = int(sys.argv[1]) if len(sys.argv) > 1 else 7
CAP = int(sys.argv[2]) if len(sys.argv) > 2 else None
max_exp, current, pending = 1, [1, 2], set()
first_found = {2: "seed (initial)"}
seeds_used = {2}
rows, per_iter = [], []
t0 = time.perf_counter()
for i in range(1, ITER + 1):
    seeds_before = list(current)
    t = time.perf_counter()
    exp = max_exp if CAP is None else min(max_exp, CAP)
    found = compute_primes(current, exp)
    dt = time.perf_counter() - t
    distinct = sorted(set(found))
    for x in distinct: first_found.setdefault(x, i)
    cs = set(current)
    pending.update(x for x in distinct if x not in cs)
    added = ""
    if pending:
        nxt = min(pending); pending.discard(nxt); current = current + [nxt]
        seeds_used.add(nxt); added = str(nxt)
    rows.append((i, seeds_before, exp, dt, len(distinct), added))
    per_iter.append((i, seeds_before, exp, dt, distinct))
    max_exp += 1
    print(f"iter {i}: {dt:.2f}s, {len(distinct)} found", file=sys.stderr, flush=True)
total = time.perf_counter() - t0
allv = sorted(first_found)
bad = [x for x in allv if not is_prime(x)]
missing = [p for p in range(2, max(allv) + 1) if is_prime(p) and p not in first_found]

o = []
o.append(f"# prime_synthesis_left_exp.py — {ITER}-Iteration Run" + (f" (max_exp capped at {CAP})" if CAP else "") + " Results\n")
o.append("Variant: exponents applied to the **left subset only**; the right subset is a plain product (all exponents = 1).\n")
o.append(f"Total wall-clock time: **{total:.2f}s**\n")
o.append(f"Final accumulated prime set size: **{len(allv)}**\n\n")
o.append("**✅ Primality check PASSED — all discovered numbers verified prime.**\n" if not bad else f"**❌ Primality check FAILED — composites found: {', '.join(map(str, bad))}**\n")
o.append(f"**{'✅ Completeness check PASSED — no primes missing' if not missing else '❌ Completeness check FAILED — missing primes: ' + ', '.join(map(str, missing))} up to {max(allv)}.**\n\n")
o.append("## Per-Iteration Summary\n")
o.append(f"| Iteration | Seeds before | max_exp{' (capped)' if CAP else ''} | Time (s) | # Distinct Found | Added to Seeds |\n|---|---|---|---|---|---|")
for i, s, e, dt, n, a in rows:
    o.append(f"| {i} | {', '.join(map(str, s))} | {e} | {dt:.4f} | {n} | {a} |")
o.append("\n## All Numbers Discovered (sorted)\n")
o.append("| # | Value | First Found In Iteration | Used as Seed? |\n|---|---|---|---|")
for k, v in enumerate(allv, 1):
    o.append(f"| {k} | {v} | {first_found[v]} | {'yes' if v in seeds_used else ''} |")
o.append("\n## Per-Iteration Discovered Values\n")
for i, s, e, dt, d in per_iter:
    o.append(f"\n### Iteration {i} (seeds: {s}, max_exp={e}, time={dt:.4f}s)\n")
    o.append(", ".join(map(str, d)))
print("\n".join(o), flush=True)
