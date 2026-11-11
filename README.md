# Prime Partition Algorithm

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Preprint](https://img.shields.io/badge/preprint-Zenodo-blue)](https://zenodo.org/records/20727496)
[![Languages](https://img.shields.io/badge/implementations-9-brightgreen)](#implementations)

**Grow prime numbers instead of sieving for them.**

Every prime generator you've used works by elimination: list a range of integers, cross out the composites, keep what's left. The Prime Partition Algorithm flips that around. Starting from the seed set `{1, 2}`, it *constructs* new primes algebraically — partitioning the set, exponentiating and multiplying within each half, then combining the results — and lets the set of known primes grow itself, iteration by iteration.

No sieve. No primality test. Just a seed set, a few algebraic operations, and [one observation from Euclid](#why-no-primality-test).

![Demo](publication/demo/demo.gif)

## Overview

A rough version of this technique was originally published [here](https://github.com/EtherBit/A-Most-Curious-Algorithm) and [here](https://github.com/EtherBit/On-Immeasurable-Magnitudes). A formal preprint, *"A Useless Recipe for Primes,"* is available on [Zenodo](https://zenodo.org/records/20727496) and in this repo under [`publication/`](publication).

## The Algorithm in a Nutshell

Starting with a seed set (e.g., `{1, 2}`):

1. **Partition** the set into two groups (all possible ways)
2. **Exponentiate** elements (raise to powers 1–E; the paper grows E by 1 each iteration, the demos fix it at 2)
3. **Multiply** within each group to get two products
4. **Combine** via sum and absolute difference
5. **Keep** candidates in the range `(max, max²]`
6. **Grow** the seed set with newly discovered primes
7. **Repeat** for multiple iterations

Each iteration reaches further into the number line — new primes sprouting from the arithmetic of the ones before them.

![Recipe](publication/demo/recipe.gif)

### Why No Primality Test?

Step 5 only checks the range. It never tests a candidate for primality, and it doesn't need to. This is the same idea as Euclid's proof that there are infinitely many primes. Every prime in the seed set divides exactly one of the two products, so it can't divide their sum or their difference. That means every candidate has no prime factor ≤ `max`. A composite number below `max²` must have a prime factor ≤ `max`, so as long as the seed set contains every prime up to `max`, every candidate inside `(max, max²]` is prime. (If a prime were ever skipped, say 311, a composite like 311·313 could slip into a later window.)

### The Arithmetic Fulcrum

Step 4 of the algorithm (in the paper) has a nice geometric reading, which I call an *arithmetic fulcrum*. Each partition produces two products: the larger one is a fulcrum on the number line, and the smaller one is its reach. The sum and difference land the same distance away on each side of it. For example, with the seed set `{1, 2, 3, 5, 7}`, the partition `({1, 2, 5}, {3, 7})` gives products 10 and 21. That puts a fulcrum at 21 with a reach of ±10, which balances two primes at once: **11** and **31**.

Several fulcrums work together to fill the quadratic window `(7, 49]`, and some primes get found more than once (over-determined). Here, 37 comes from both the fulcrum at 30 (reach ±7) and the fulcrum at 42 (reach ±5).

![Fulcrums](publication/demo/fulcrums.gif)

For a longer view, [this Manim animation](publication/demo/NumberLineMagnification.mp4) follows the fulcrums across the first 5 iterations as the window keeps growing:

![Fulcrums On The Number Line](publication/demo/NumberLineMagnification_Fulcrums.gif)

## Quick Start

No dependencies required — grab the Python version and run it:

```bash
git clone https://github.com/microgeant/PrimePartitionAlgorithm.git
cd PrimePartitionAlgorithm/python
python3 prime_partition.py
```

```
=== PYTHON VERSION ===
Hello primes: [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, ...]
Total discovered: 64
Found composites: []
```

## Implementations

The same algorithm, faithfully reimplemented across nine languages — pick the one you're comfortable reading, or compare a few to see how the idea translates across paradigms.

| Language | Source | Notes |
|----------|--------|-------|
| [Python](python) | [`prime_partition.py`](python/prime_partition.py) | Reference implementation, easiest to read |
| [Rust](rust) | [`prime_partition.rs`](rust/prime_partition.rs) | |
| [C](c) | [`prime_partition.c`](c/prime_partition.c) | Includes a `Makefile` |
| [Kotlin](kotlin) | [`PrimePartition.kt`](kotlin/PrimePartition.kt) | |
| [Haskell](haskell) | [`PrimePartition.hs`](haskell/PrimePartition.hs) | |
| [Julia](julia) | [`prime_partition.jl`](julia/prime_partition.jl) | |
| [Scheme](scheme) | [`prime-partition.scm`](scheme/prime-partition.scm) | |
| [Zig](zig) | [`prime_partition.zig`](zig/prime_partition.zig) | Includes a `build.zig` |
| [Jai](jai) | [`prime_partition.jai`](jai/prime_partition.jai) | |

Each directory has its own `README.md` with prerequisites and exact run instructions.

## Repository Layout

```
PrimePartitionAlgorithm/
├── python/, rust/, c/, kotlin/, haskell/, julia/, scheme/, zig/, jai/
│   └── implementation + language-specific README
├── publication/
│   ├── A Useless Recipe for Primes.pdf   # the preprint
│   ├── demo/                             # gifs + Manim animations (.mp4)
│   ├── experiments/                      # faster searches (Python, Kotlin) + run reports
│   ├── prime_synthesis.py
│   ├── PrimeSynthesis.kt
│   └── prime_synthesis_results*.md       # run reports (adaptive + capped schedules)
└── LICENSE
```

## Performance & Limitations

![Complexity](publication/demo/complexity.gif)

This is a constructive curiosity, not a practical prime generator. Each iteration partitions a seed set of size `n`, raises elements to exponents up to `E`, and filters every combination by range — roughly `2(2E)^n` candidates per step, giving a cumulative cost of `O(N · (2E)^N)` over `N` iterations. Every newly discovered prime makes the next one exponentially more expensive to find (the paper's "Price of Magic").

In practice, [`publication/prime_synthesis.py`](publication/prime_synthesis.py) (the full algorithm from the paper's Listing 1: exponents on both subsets, with an uncapped adaptive exponent schedule) takes **~21 minutes** across 7 iterations to synthesize every prime up to **199** (it reaches as high as 283, but misses 211 and 223) — over 20 of those minutes in the last iteration alone. A Sieve of Eratosthenes finds the same primes in well under a millisecond. Full numbers in [`publication/prime_synthesis_results.md`](publication/prime_synthesis_results.md).

| | Prime Partition Algorithm | Sieve of Eratosthenes |
|---|---|---|
| Complexity | `O(N · (2E)^N)` — exponential | `O(n log log n)` — near-linear |
| Every prime up to 199 | ~21 minutes (0.15 s with [meet in the middle](#experiments)) | microseconds |
| Good for | studying the structure of primes (e.g., how primes are born from their predecessors) | generating primes efficiently |

The sieve wins on every practical axis — see *"The Combinatorial Explosion: An Exponential Barrier"* in [the preprint](publication/A%20Useless%20Recipe%20for%20Primes.pdf).

**A sharper limitation:** the per-language demos hard-code `max_exponent = 2` for speed and readability, but completeness depends on that bound, and whether any bound guarantees it is an open question (the paper's Exponent Conjecture). Capped too low, later iterations silently find *zero* primes instead of erroring: a 13-iteration run capped at `max_exp=2` finds 0 new primes at iteration 12 ([`prime_synthesis_results_capped2_13iter.md`](publication/prime_synthesis_results_capped2_13iter.md)). The adaptive schedule avoids this stall, though it isn't gap-free either.

## Experiments

[`publication/experiments/`](publication/experiments) holds faster searches over the same kind of candidates, each with its run reports. Every candidate still passes only the range check, so none of them needs a primality test.

| Code | What it searches | 15 iterations | Primes found | Gap-free up to |
|---|---|---|---|---|
| [`FulcrumTargetingMitm.kt`](publication/experiments/FulcrumTargetingMitm.kt) | The full algorithm, exact (exponents capped at 5) | 34 s | 115 | 283 |
| [`prime_synthesis_mitm.py`](publication/experiments/prime_synthesis_mitm.py) | Same, in Python | ~8 min | 115 | 283 |
| [`prime_synthesis_left_exp_mitm.py`](publication/experiments/prime_synthesis_left_exp_mitm.py) | Exponents on one subset only (adaptive) | 0.7 s | 77 | 181 |
| [`prime_synthesis_size_bound.py`](publication/experiments/prime_synthesis_size_bound.py) | Both products ≤ X = 10¹², exponents otherwise free | 19 s | 123 | 307 |
| [`prime_synthesis_excess.py`](publication/experiments/prime_synthesis_excess.py) | π_A·π_B = (product of seeds)·k, smooth k ≤ 10⁴, window `g²` | 3.5 s | 135 | 389 |
| [`LeafRunsSynthesis.kt`](publication/experiments/LeafRunsSynthesis.kt) | The full algorithm (exponents capped at 5), plus one search on seeds + {v} for each found prime v not yet a seed | 31 min | 216 | 953 |
| [`LeafRunsSynthesis.kt`](publication/experiments/LeafRunsSynthesis.kt) (depth 2) | Same, plus seeds + {v, w} for every pair of such primes at iteration 12 (12 iterations) | 2.2 h | 219 | **1367** (the whole window) |

- **Meet in the middle:** from `max = 13` on, the sum π_A + π_B always overshoots the window, so only differences of nearly equal products land. Each seed adds `±e·log p` to `log π_A − log π_B`, so the seeds split into two halves that are enumerated separately and matched on their log-ratios, then confirmed exactly with integers. This reproduces the full algorithm iteration for iteration (checked against every report): 7 iterations take 0.15 s instead of ~21 minutes.
- **One subset only:** applying the exponents to one subset of each partition (as in early rough versions, [`prime_synthesis_left_exp.py`](publication/experiments/prime_synthesis_left_exp.py)) is far cheaper but misses more primes: 7 iterations are gap-free only up to 167, vs. 199 for the full algorithm.
- **Patterns:** the exponents that produce primes sit on the smallest seeds (2, 3, 5), and the extra factor `k` is small and smooth. The excess search exploits this.
- **A wall at 311, then at 541:** with the paper's window `(max, max²]` every method above except the leaf searches stops at gap-free 307. The excess search with the wider `g²` window (below) gets past it: runs of days (K up to 10¹¹, 25 iterations) reach 160 primes, gap-free up to 523, largest 2521, with no composites, and then nothing new after iteration 15 at any K. The expected hits per iteration fall below 1 around iterations 15–17, so the searches dry up rather than fill the gaps. The one-subset variant likewise finds nothing after iteration 13 through iteration 26.
- **Exponent patterns outside the window** ([`prime_synthesis_collect_all_patterns.py`](publication/experiments/prime_synthesis_collect_all_patterns.py), 105 million values): only the gcd `d` of all exponents matters, through the algebraic factorizations. `xᵈ − yᵈ` is divisible by `x − y`, so differences with `d > 1` are essentially never prime; `xᵈ + yᵈ` is divisible by `x + y` when `d` has an odd factor; sums with `d = 2` or `4` behave normally. Every other grouping (exponent on 2, how many exponents exceed 1, which side 2 is on) is prime as often as size and coprimality to the seeds predict (ratio 0.94–1.00).
- **Prime-only exponents:** restricting exponents to the primes already among the seeds never finds 7 without exponent 1; with exponent 1 and the window, 7 iterations still miss 173, whose only witnesses in that iteration need exponents 4 or 6.
- **Gaussian integers** ([`gaussian_prime_synthesis.py`](publication/experiments/gaussian_prime_synthesis.py)): the same recipe over Z[i], with seeds starting at {1, 1+i}, candidates `π_A + u·π_B` for the four units `u`, and a norm window `N(g)²`. Euclid's argument carries over (Z[i] has unique factorization). 9 iterations find 138 Gaussian primes, all verified, complete by norm up to 293; their norms give rational primes up to 829, 541 included. Primes `q ≡ 3 (mod 4)` stay prime in Z[i] with norm `q²`, so they wait for the window to pass `q²` (31 is the first missing). Landing needs both size and angle to match; heuristically the extra Gaussian primes and units offset that, so it should stall like the integer version (iteration 9 found only 8 new primes, against 70 in iteration 8).
- **Leaf searches** ([`LeafRunsSynthesis.kt`](publication/experiments/LeafRunsSynthesis.kt), after the leaf runs in [`prime_number_algorithm_2.kt`](https://github.com/EtherBit/On-Immeasurable-Magnitudes/blob/master/prime_number_algorithm_2.kt)): each iteration also repeats the search with one extra seed `v`, once for every prime found but not yet a seed, in the same window `(max, max²]`. `v` sits on one side like any seed, so Euclid's argument still holds and no composite appears. With exponents capped at 5, 16 iterations (87 minutes) find 219 primes, gap-free up to 953, against 115 and 283 for the plain search; 124 come only from leaf searches, among them 541 = 2·5³·13·17²·23·149 − 3·7·11⁴·19²·29 (iteration 10, `v` = 149). Where the plain search finds nothing (iterations 14–16), the leaves still add 8, 7 and 3 new primes, but their extra hits fall (30, 11, 4) while each iteration costs 2.5–6× more, so they delay the stall rather than remove it. Using only the previous iteration's new primes as leaves (as the original does) stalls at iteration 14 with the plain search: that iteration finds nothing new, so the next has no leaves.
- **Leaf pairs fill the window:** combining leaves instead of adding iterations works much better. At iteration 12 (seeds up to 37, window `(37, 1369]`), searching seeds + {v, w} for every pair of the 148 pending primes (11,026 searches of 15 primes, 2.2 hours) finds every prime in the window: 12 iterations end gap-free up to 1367 with nothing missing below it, where 16 iterations of single leaves stop at 953 with 174 primes missing. 55 primes come only from pairs, among them 967 = 2³·3·7·11³·19·29·31·79 − 5⁴·13·17²·23·37·151 (leaves 79 and 151), the prime that blocked the single-leaf run for five iterations. Extra seeds add freedom without raising the window, while each iteration makes both products larger and a landing rarer, so depth is the cheaper direction ([report](publication/experiments/leaf_runs_synthesis_results_capped5_pending_depth2_12iter.md)).

## Open Questions

- **The Exponent Conjecture:** does some exponent bound guarantee that every prime is eventually found?
- **The wall at 541:** can a missing prime such as 541 be built at all as π_A − π_B from the seeds below it, and with what exponents? This is an S-unit equation (`x − y = q` with `x`, `y` built from a fixed set of primes), for which LLL-based methods (de Weger) bound the exponents of every solution. With one extra prime it can: the leaf searches build 541 from the seeds up to 29 and 149, with exponents at most 5; with two, every prime up to 1367 is built from the seeds up to 37. Whether a fixed number of extra primes always suffices is the open form of the question.
- **Wider safe windows:** coprimality alone guarantees primality up to `g²`, where `g` is the smallest prime missing from the seeds, which goes beyond `max²` (used by `prime_synthesis_excess.py`; `g` is found with one gcd per tried value, so still no primality test). A quadratic-residue condition (every prime factor `r` of `π_A − π_B` has `π_A·π_B` as a square mod `r`) may push it further, still without a primality test.

## Citing

If you use this work, please cite the Zenodo preprint (https://zenodo.org/records/20727496):

```bibtex
@misc{kongawi2026useless,
  author    = {Kongawi, Bruno Ziki},
  title     = {A Useless Recipe for Primes: A Partition-Based Algorithm for Prime Synthesis},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20727496},
  url       = {https://zenodo.org/records/20727496}
}
```

## License

[MIT](LICENSE)
