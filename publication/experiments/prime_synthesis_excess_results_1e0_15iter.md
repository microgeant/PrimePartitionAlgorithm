# prime_synthesis_excess.py — 15-Iteration Run (excess k <= K = 10^0) Results

Full algorithm (every seed on exactly one side, exponent >= 1, as in the paper), searched by **excess**: pi_A * pi_B = prod(seeds) * k for every seed-smooth k <= K = 10^0, i.e. the extra exponents beyond 1 multiply to at most K. Computed with the per-k meet-in-the-middle split search in `prime_synthesis_excess.py` (verified against all 783 witnesses of the X = 10^12 size-bound run, for every seed set, at K = 1, 10^2 and 10^4).

Total wall-clock time: **0.00s**

Peak memory: **~10 MB**

Final accumulated prime set size: **24**


**✅ Primality check PASSED — all discovered numbers verified prime.**

**Gap-free up to 17** (first missing prime: 19); 36 primes missing below the largest found (281).


Missing primes: 19, 43, 53, 59, 61, 71, 73, 79, 109, 113, 127, 131, 137, 139, 149, 151, 157, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 229, 233, 239, 241, 251, 257, 269, 271, 277


## Per-Iteration Summary

| Iteration | Seeds before | K | Time (s) | # Distinct Found | Added to Seeds |
|---|---|---|---|---|---|
| 1 | 1, 2 | 1e0 | 0.0000 | 1 | 3 |
| 2 | 1, 2, 3 | 1e0 | 0.0000 | 2 | 5 |
| 3 | 1, 2, 3, 5 | 1e0 | 0.0000 | 4 | 7 |
| 4 | 1, 2, 3, 5, 7 | 1e0 | 0.0000 | 7 | 11 |
| 5 | 1, 2, 3, 5, 7, 11 | 1e0 | 0.0000 | 10 | 13 |
| 6 | 1, 2, 3, 5, 7, 11, 13 | 1e0 | 0.0000 | 5 | 17 |
| 7 | 1, 2, 3, 5, 7, 11, 13, 17 | 1e0 | 0.0000 | 2 | 23 |
| 8 | 1, 2, 3, 5, 7, 11, 13, 17, 23 | 1e0 | 0.0000 | 2 | 29 |
| 9 | 1, 2, 3, 5, 7, 11, 13, 17, 23, 29 | 1e0 | 0.0000 | 0 | 31 |
| 10 | 1, 2, 3, 5, 7, 11, 13, 17, 23, 29, 31 | 1e0 | 0.0000 | 1 | 37 |
| 11 | 1, 2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37 | 1e0 | 0.0010 | 0 | 41 |
| 12 | 1, 2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37, 41 | 1e0 | 0.0010 | 0 | 47 |
| 13 | 1, 2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37, 41, 47 | 1e0 | 0.0000 | 0 | 67 |
| 14 | 1, 2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37, 41, 47, 67 | 1e0 | 0.0000 | 0 | 83 |
| 15 | 1, 2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37, 41, 47, 67, 83 | 1e0 | 0.0000 | 0 | 89 |

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
| 8 | 23 | 4 | yes |
| 9 | 29 | 4 | yes |
| 10 | 31 | 4 | yes |
| 11 | 37 | 4 | yes |
| 12 | 41 | 4 | yes |
| 13 | 47 | 4 | yes |
| 14 | 67 | 6 | yes |
| 15 | 83 | 5 | yes |
| 16 | 89 | 5 | yes |
| 17 | 97 | 5 |  |
| 18 | 101 | 5 |  |
| 19 | 103 | 5 |  |
| 20 | 107 | 5 |  |
| 21 | 163 | 6 |  |
| 22 | 227 | 8 |  |
| 23 | 263 | 7 |  |
| 24 | 281 | 8 |  |

## Per-Iteration Discovered Values


### Iteration 1 (seeds: [1, 2], K=1e0, time=0.0000s)

3

### Iteration 2 (seeds: [1, 2, 3], K=1e0, time=0.0000s)

5, 7

### Iteration 3 (seeds: [1, 2, 3, 5], K=1e0, time=0.0000s)

7, 11, 13, 17

### Iteration 4 (seeds: [1, 2, 3, 5, 7], K=1e0, time=0.0000s)

11, 23, 29, 31, 37, 41, 47

### Iteration 5 (seeds: [1, 2, 3, 5, 7, 11], K=1e0, time=0.0000s)

13, 31, 37, 47, 83, 89, 97, 101, 103, 107

### Iteration 6 (seeds: [1, 2, 3, 5, 7, 11, 13], K=1e0, time=0.0000s)

17, 41, 67, 101, 163

### Iteration 7 (seeds: [1, 2, 3, 5, 7, 11, 13, 17], K=1e0, time=0.0000s)

107, 263

### Iteration 8 (seeds: [1, 2, 3, 5, 7, 11, 13, 17, 23], K=1e0, time=0.0000s)

227, 281

### Iteration 9 (seeds: [1, 2, 3, 5, 7, 11, 13, 17, 23, 29], K=1e0, time=0.0000s)

*(none)*

### Iteration 10 (seeds: [1, 2, 3, 5, 7, 11, 13, 17, 23, 29, 31], K=1e0, time=0.0000s)

47

### Iteration 11 (seeds: [1, 2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37], K=1e0, time=0.0010s)

*(none)*

### Iteration 12 (seeds: [1, 2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37, 41], K=1e0, time=0.0010s)

*(none)*

### Iteration 13 (seeds: [1, 2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37, 41, 47], K=1e0, time=0.0000s)

*(none)*

### Iteration 14 (seeds: [1, 2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37, 41, 47, 67], K=1e0, time=0.0000s)

*(none)*

### Iteration 15 (seeds: [1, 2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37, 41, 47, 67, 83], K=1e0, time=0.0000s)

*(none)*
