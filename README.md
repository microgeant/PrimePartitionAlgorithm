# Prime Partition Algorithm

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Preprint](https://img.shields.io/badge/preprint-Zenodo-blue)](https://zenodo.org/records/20727496)
[![Languages](https://img.shields.io/badge/implementations-9-brightgreen)](#implementations)

**Grow prime numbers instead of sieving for them.**

Every prime generator you've used works by elimination: list a range of integers, cross out the composites, keep what's left. The Prime Partition Algorithm flips that around. Starting from the seed set `{1, 2}`, it *constructs* new primes algebraically — partitioning the set, exponentiating and multiplying within each half, then combining the results — and lets the set of known primes grow itself, iteration by iteration.

No sieve. No trial range. Just a seed and a few algebraic operations.

![Demo](publication/demo/demo.gif)

## Overview

Prime generation algorithms typically fall into two categories: sieving methods (e.g. the classic [Sieve of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)) that systematically eliminate composites, and primality testing of structured sequences. This project introduces a third, lateral approach: **partition-based constructive generation** through algebraic operations on binary set partitions.

This was originally published [here](https://github.com/EtherBit/A-Most-Curious-Algorithm) and [here](https://github.com/EtherBit/On-Immeasurable-Magnitudes). A formal preprint, *"A Useless Recipe for Primes,"* is available on [Zenodo](https://zenodo.org/records/20727496) and in this repo under [`publication/`](publication).

## The Algorithm in a Nutshell

Starting with a seed set (e.g., `{1, 2}`):

1. **Partition** the set into two groups (all possible ways)
2. **Exponentiate** elements (raise to powers 1–E)
3. **Multiply** within each group to get two products
4. **Combine** via sum and absolute difference
5. **Filter** for primes in the range `(max, max²)`
6. **Grow** the seed set with newly discovered primes
7. **Repeat** for multiple iterations

Each iteration reaches further into the number line — new primes born from the arithmetic of the ones before them.

![Recipe](publication/demo/recipe.gif)

## Quick Start

No dependencies required — grab the Python version and run it:

```bash
git clone git@github.com:microgeant/PrimePartitionAlgorithm.git
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
│   ├── demo/                             # demo gif + number line visualization
│   ├── prime_synthesis.py
│   └── PrimeSynthesis.kt
└── LICENSE
```

## Performance & Limitations

![Complexity](publication/demo/complexity.gif)

This is a constructive curiosity, not a practical prime generator. Each iteration partitions a seed set of size `n`, raises elements to exponents up to `E`, and filters every combination for primality — roughly `2(2E)^n` candidates per step, giving a cumulative cost of `O(N · (2E)^N)` over `N` iterations. Every newly discovered prime makes the next one exponentially more expensive to find (the paper's "Price of Magic").

In practice, [`publication/prime_synthesis.py`](publication/prime_synthesis.py) (the complete version, with an adaptive exponent schedule) takes **~21 minutes** across 7 iterations to synthesize every prime up to **283** — over 20 of those minutes in the last iteration alone. A Sieve of Eratosthenes finds the same primes in well under a millisecond. Full numbers in [`publication/prime_synthesis_results.md`](publication/prime_synthesis_results.md).

| | Prime Partition Algorithm | Sieve of Eratosthenes |
|---|---|---|
| Complexity | `O(N · (2E)^N)` — exponential | `O(n log log n)` — near-linear |
| Primes up to 283 | ~21 minutes | microseconds |
| Good for | studying the structure of primes (e.g., how primes are born from their predecessors) | generating primes efficiently |

The sieve wins on every practical axis, and it isn't close — see *"The Combinatorial Explosion: An Exponential Barrier"* in [the preprint](publication/A%20Useless%20Recipe%20for%20Primes.pdf).

**A sharper limitation:** the per-language demos in this repo hard-code `max_exponent = 2` for speed and readability (see each language's README), but that bound is exactly what the completeness guarantee depends on. Capped too low, later iterations can silently find *zero* primes instead of erroring — a 13-iteration run capped at `max_exp=2` finds 0 new primes at iteration 12 (see [`publication/prime_synthesis_results_capped2_13iter.md`](publication/prime_synthesis_results_capped2_13iter.md)). The adaptive-schedule version in [`publication/`](publication) avoids this.

**Ongoing work:** I've experimented with pruning the exponent search to just the subset likely to land inside the target window, instead of sweeping the full `1..E` range, to cut down on wasted candidates. The early results weren't consistent enough to trust yet, so that pruning isn't part of this repo's algorithm — it may show up here once it holds up.

## Next Steps

- [x] Add Kotlin Implementation
- [x] Add Python Implementation
- [x] Add C Implementation
- [x] Add Haskell Implementation
- [x] Add Scheme Implementation
- [x] Add Rust Implementation
- [x] Add Julia Implementation
- [x] Add Zig Implementation
- [x] Add Jai Implementation
- [x] Add Explanation (preprint paper)

## Citing

If you use this work, please cite the Zenodo preprint: https://zenodo.org/records/20727496

## License

[MIT](LICENSE)
