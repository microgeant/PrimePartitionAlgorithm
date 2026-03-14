# Prime Partition Algorithm

A partition-based algorithm for generating prime numbers

## Overview

Prime generation algorithms typically fall into two categories: sieving methods (e.g. the classic [sieve of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)) that systematically and exhaustively eliminate composites, and primality testing of structured sequences. We introduce a third, lateral approach: partition-based constructive generation through algebraic operations on binary set partitions.

If we had to compare the method, we could say that, in essence, it is a bit similar to the [chaos game](https://en.wikipedia.org/wiki/Sierpi%C5%84ski_triangle#Chaos_game) of the [Sierpiński triangle](https://en.wikipedia.org/wiki/Sierpi%C5%84ski_triangle), where prime numbers are analogous to the computed points (attractors) that draws the (ever-denser) emergent triangles in the self-similar figure while the composites are anologous to the (empty) triangular areas we never reach while playing the game to "infinity's end."

## The Algorithm

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
- [ ] Add Zig Implementation
- [ ] Add Explanation