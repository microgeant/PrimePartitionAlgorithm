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
2. **Exponentiate** elements (raise to powers 1–E; the paper grows E by 1 each iteration up to 5, the demos fix it at 2)
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

This is a constructive curiosity, not a practical prime generator. Each iteration partitions a seed set of size `n`, raises elements to exponents up to `E`, and filters every combination by range — roughly `(2E)^n` candidates per step (counted with repetitions), giving a cumulative cost of `O(N · (2E)^N)` over `N` iterations. Every prime added to the seed set multiplies the cost of finding the next one by roughly `2E` (the paper's "Price of Magic").

In practice, [`publication/prime_synthesis.py`](publication/prime_synthesis.py) (the full algorithm from the paper's Listing 1: exponents on both subsets, with an uncapped adaptive exponent schedule) takes **~21 minutes** across 7 iterations to synthesize every prime up to **199** (it reaches as high as 283, but misses 211 and 223) — over 20 of those minutes in the last iteration alone. A Sieve of Eratosthenes finds the same primes in well under a millisecond. Full numbers in [`publication/prime_synthesis_results.md`](publication/prime_synthesis_results.md).

| | Prime Partition Algorithm | Sieve of Eratosthenes |
|---|---|---|
| Complexity | `O(N · (2E)^N)` — exponential | `O(n log log n)` — near-linear |
| Every prime up to 199 | ~21 minutes (0.15 s with [meet in the middle](#experiments)) | microseconds |
| Good for | studying the structure of primes (e.g., how primes are born from their predecessors) | generating primes efficiently |

The sieve wins on every practical axis — see *"The Combinatorial Explosion: An Exponential Barrier"* in [the preprint](publication/A%20Useless%20Recipe%20for%20Primes.pdf).

**A sharper limitation:** the per-language demos hard-code `max_exponent = 2` for speed and readability, but completeness depends on that bound, and whether any bound guarantees it is an open question (the paper's Exponent Question). Capped too low, later iterations silently find *zero* primes instead of erroring: a 13-iteration run capped at `max_exp=2` finds 0 new primes at iteration 12 ([`prime_synthesis_results_capped2_13iter.md`](publication/prime_synthesis_results_capped2_13iter.md)). The adaptive schedule avoids this stall, though it isn't gap-free either.

## Experiments

[`publication/experiments/`](publication/experiments) holds faster searches over the same kind of candidates, each with its run reports. Every candidate still passes only the range check, so none of them needs a primality test.

| Code | What it searches | 15 iterations | Primes found | Gap-free up to |
|---|---|---|---|---|
| [`FulcrumTargetingMitm.kt`](publication/experiments/FulcrumTargetingMitm.kt) | Full algorithm, exponents ≤ 5 | 34 s | 115 | 283 |
| [`prime_synthesis_mitm.py`](publication/experiments/prime_synthesis_mitm.py) | Same, in Python | ~8 min | 115 | 283 |
| [`prime_synthesis_left_exp_mitm.py`](publication/experiments/prime_synthesis_left_exp_mitm.py) | Exponents on one subset only | 0.7 s | 77 | 181 |
| [`prime_synthesis_size_bound.py`](publication/experiments/prime_synthesis_size_bound.py) | Both products ≤ 10¹², exponents free | 19 s | 123 | 307 |
| [`prime_synthesis_excess.py`](publication/experiments/prime_synthesis_excess.py) | π_A·π_B = (product of seeds)·k, smooth k ≤ 10⁴, window `g²` | 3.5 s | 135 | 389 |
| [`LeafRunsSynthesis.kt`](publication/experiments/LeafRunsSynthesis.kt) | Full algorithm (exponents ≤ 5) + one extra seed `v` | 31 min | 216 | 953 |
| Same, depth 2 | + pairs `{v, w}` at iteration 12 only (12 iterations) | 2.2 h | 219 | **1367** |
| Same, depth 2, cap 3 | + pairs at every iteration, exponents ≤ 3 | 2.5 h | 285 | **1697** |

- **Meet in the middle:** from `max = 13` on, only differences of nearly equal products land in the window. The seeds are split into two halves, enumerated separately, matched on `log π_A − log π_B`, then confirmed with exact integers. The results match the full algorithm iteration for iteration: 7 iterations take 0.15 s instead of ~21 minutes.
- **One subset only:** far cheaper, but misses more primes: 7 iterations are gap-free up to 167, vs. 199 for the full algorithm.
- **Excess search:** the exponents that produce primes sit on the smallest seeds (2, 3, 5), and the extra factor `k` is small and smooth. Searching those directly, with the wider `g²` window, gets past 307, where the other non-leaf methods stop. Multi-day runs (k up to 10¹¹, 25 iterations) reach 160 primes, gap-free up to 523, then find nothing new after iteration 15: the expected hits per iteration fall below 1.
- **Exponent patterns** ([`prime_synthesis_collect_all_patterns.py`](publication/experiments/prime_synthesis_collect_all_patterns.py), 105 million values): only the gcd `d` of all exponents matters. `xᵈ − yᵈ` is divisible by `x − y`, and `xᵈ + yᵈ` by `x + y` when `d` has an odd factor, so those are essentially never prime. Everything else is prime as often as size and coprimality to the seeds predict.
- **Prime-only exponents:** restricting exponents to 1 and the seed primes misses 173, whose only witnesses need exponents 4 or 6.
- **Gaussian integers** ([`gaussian_prime_synthesis.py`](publication/experiments/gaussian_prime_synthesis.py)): the same recipe over Z[i] finds 138 Gaussian primes in 9 iterations, complete by norm up to 293. It appears to stall like the integer version (8 new primes in iteration 9, against 70 in iteration 8).
- **Leaf searches** ([`LeafRunsSynthesis.kt`](publication/experiments/LeafRunsSynthesis.kt), after [`prime_number_algorithm_2.kt`](https://github.com/EtherBit/On-Immeasurable-Magnitudes/blob/master/prime_number_algorithm_2.kt)): each iteration repeats the search with one extra seed `v`, for every prime found but not yet a seed. Euclid's argument still holds, so no composite appears. 16 iterations find 219 primes, gap-free up to 953 (plain search: 115 and 283), among them 541 = 2·5³·13·17²·23·149 − 3·7·11⁴·19²·29. The extra hits fall while each iteration costs 2.5–6× more, so leaves delay the stall rather than remove it.
- **Leaf pairs:** two extra seeds `{v, w}` work much better than more iterations, since they add freedom without raising the window. At iteration 12 they find every prime in the window `(37, 1369]` ([report](publication/experiments/leaf_runs_synthesis_results_capped5_pending_depth2_12iter.md)), and exponents capped at 3 do it in 150 s instead of 2.2 hours (cap 2 leaves 20 gaps). With pairs at every iteration, 15 iterations find 285 primes, gap-free up to 1697 ([report](publication/experiments/leaf_runs_synthesis_results_capped3_pending_depth2_15iter.md)). The windows fill through iteration 13, then the hits fall: pairs push the stall out by about three iterations.

## Open Questions

- **The Exponent Question:** is there a schedule of exponent bounds `E(k)` such that, at every iteration, the prime right after the current `max` has already been found? That is all the no-composite guarantee needs. A stronger form asks whether every prime is eventually found; a prime `p` can only be found in an iteration with `max < p ≤ max²`.
- **Targeted search:** for a given partition, can the exponents that land a candidate inside the window be determined directly, without enumerating all `Eⁿ` combinations? Meet in the middle (see [Experiments](#experiments)) cuts the enumeration from `(2E)^n` to `(2E)^(n/2)`, but it still enumerates.
- **The wall at 541:** can a missing prime such as 541 be built at all as π_A − π_B from the seeds below it, and with what exponents? This is an S-unit equation (`x − y = q` with `x`, `y` built from a fixed set of primes), for which LLL-based methods (de Weger) bound the exponents of every solution. With one extra prime it can: the leaf searches build 541 from the seeds up to 29 and 149, with exponents at most 5; with two, every prime up to 1697 is built from the seeds up to 43, with exponents at most 3. Whether a fixed number of extra primes always suffices is the open form of the question.
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
