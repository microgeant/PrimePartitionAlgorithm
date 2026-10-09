# prime_synthesis_left_exp.py — 7-Iteration Run Results

Variant: exponents applied to the **left subset only**; the right subset is a plain product (all exponents = 1).

Total wall-clock time: **2.25s**

Final accumulated prime set size: **52**


**✅ Primality check PASSED — all discovered numbers verified prime.**

**❌ Completeness check FAILED — missing primes: 173, 179, 191, 211, 223, 229, 239, 269, 277 up to 283.**


## Comparison with the Original (`../prime_synthesis_results.md`)

| | Original (exponents on both subsets) | Left-only exponents |
|---|---|---|
| Total time (7 iterations) | 1253.29s (~20.9 min) | 2.25s |
| Primes found | 59 | 52 |
| Seeds added | 3, 5, 7, 11, 13, 17, 19 | 3, 5, 7, 11, 13, 17, 19 |

- Primes found by the original but **missed** by left-only: 173, 179, 191, 229, 239, 269, 277
- Primes found by left-only but not by the original: none
- Primes found by both, but in a later iteration with left-only: 157 (iter 6 → 7)
- 211 and 223 are missed by **both** versions at 7 iterations.

## Per-Iteration Summary

| Iteration | Seeds before | max_exp | Time (s) | # Distinct Found | Added to Seeds |
|---|---|---|---|---|---|
| 1 | 1, 2 | 1 | 0.0000 | 1 | 3 |
| 2 | 1, 2, 3 | 2 | 0.0000 | 2 | 5 |
| 3 | 1, 2, 3, 5 | 3 | 0.0000 | 6 | 7 |
| 4 | 1, 2, 3, 5, 7 | 4 | 0.0004 | 11 | 11 |
| 5 | 1, 2, 3, 5, 7, 11 | 5 | 0.0061 | 23 | 13 |
| 6 | 1, 2, 3, 5, 7, 11, 13 | 6 | 0.1019 | 24 | 17 |
| 7 | 1, 2, 3, 5, 7, 11, 13, 17 | 7 | 2.1451 | 28 | 19 |

## All Numbers Discovered (sorted)

| # | Value | First Found In Iteration | Used as Seed? |
|---|---|---|---|
| 1 | 2 | seed (initial) | yes |
| 2 | 3 | 1 | yes |
| 3 | 5 | 2 | yes |
| 4 | 7 | 2 | yes |
| 5 | 11 | 3 | yes |
| 6 | 13 | 3 | yes |
| 7 | 17 | 3 | yes |
| 8 | 19 | 3 | yes |
| 9 | 23 | 3 |  |
| 10 | 29 | 4 |  |
| 11 | 31 | 4 |  |
| 12 | 37 | 4 |  |
| 13 | 41 | 4 |  |
| 14 | 43 | 4 |  |
| 15 | 47 | 4 |  |
| 16 | 53 | 5 |  |
| 17 | 59 | 5 |  |
| 18 | 61 | 5 |  |
| 19 | 67 | 5 |  |
| 20 | 71 | 5 |  |
| 21 | 73 | 5 |  |
| 22 | 79 | 5 |  |
| 23 | 83 | 5 |  |
| 24 | 89 | 5 |  |
| 25 | 97 | 5 |  |
| 26 | 101 | 5 |  |
| 27 | 103 | 5 |  |
| 28 | 107 | 5 |  |
| 29 | 109 | 5 |  |
| 30 | 113 | 5 |  |
| 31 | 127 | 6 |  |
| 32 | 131 | 6 |  |
| 33 | 137 | 6 |  |
| 34 | 139 | 6 |  |
| 35 | 149 | 6 |  |
| 36 | 151 | 6 |  |
| 37 | 157 | 7 |  |
| 38 | 163 | 6 |  |
| 39 | 167 | 6 |  |
| 40 | 181 | 7 |  |
| 41 | 193 | 7 |  |
| 42 | 197 | 7 |  |
| 43 | 199 | 7 |  |
| 44 | 227 | 7 |  |
| 45 | 233 | 7 |  |
| 46 | 241 | 7 |  |
| 47 | 251 | 7 |  |
| 48 | 257 | 7 |  |
| 49 | 263 | 7 |  |
| 50 | 271 | 7 |  |
| 51 | 281 | 7 |  |
| 52 | 283 | 7 |  |

## Per-Iteration Discovered Values


### Iteration 1 (seeds: [1, 2], max_exp=1, time=0.0000s)

3

### Iteration 2 (seeds: [1, 2, 3], max_exp=2, time=0.0000s)

5, 7

### Iteration 3 (seeds: [1, 2, 3, 5], max_exp=3, time=0.0000s)

7, 11, 13, 17, 19, 23

### Iteration 4 (seeds: [1, 2, 3, 5, 7], max_exp=4, time=0.0004s)

11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47

### Iteration 5 (seeds: [1, 2, 3, 5, 7, 11], max_exp=5, time=0.0061s)

13, 17, 19, 29, 31, 37, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113

### Iteration 6 (seeds: [1, 2, 3, 5, 7, 11, 13], max_exp=6, time=0.1019s)

17, 19, 23, 29, 41, 43, 53, 59, 61, 67, 73, 79, 83, 101, 107, 113, 127, 131, 137, 139, 149, 151, 163, 167

### Iteration 7 (seeds: [1, 2, 3, 5, 7, 11, 13, 17], max_exp=7, time=2.1451s)

19, 41, 59, 73, 83, 89, 97, 103, 107, 109, 113, 131, 137, 139, 157, 181, 193, 197, 199, 227, 233, 241, 251, 257, 263, 271, 281, 283
