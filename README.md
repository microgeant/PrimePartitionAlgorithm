# Prime Partition Algorithm

A partition-based algorithm for generating prime numbers

## Overview

Prime generation algorithms typically fall into two categories: sieving methods (e.g. the classic [sieve of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)) that systematically and exhaustively eliminate composites, and primality testing of structured sequences. We introduce a third, lateral approach: partition-based constructive generation through algebraic operations on binary set partitions.

This was originally published [here](https://github.com/EtherBit/A-Most-Curious-Algorithm) and [here](https://github.com/EtherBit/On-Immeasurable-Magnitudes)

## The Algorithm in a Nutshell

Starting with a seed set (e.g., `{1, 2}`):

1. **Partitions** the set into two groups (all possible ways)
2. **Exponentiates** elements (raises to powers 1-E)
3. **Multiplies** within each group to get two products
4. **Combines** via sum and absolute difference
5. **Filters** for primes in range `(max, max²)`
6. **Grows** the seed set with newly discovered primes
7. **Repeats** for multiple iterations

## Next Steps

- [x] Add Kotlin Implementation
- [x] Add Python Implementation
- [x] Add C Implementation
- [x] Add Haskell Implementation
- [x] Add Scheme Implementation
- [x] Add Rust Implementation
- [x] Add Julia Implementation
- [x] Add Zig Implementation
- [ ] Add Explanation
