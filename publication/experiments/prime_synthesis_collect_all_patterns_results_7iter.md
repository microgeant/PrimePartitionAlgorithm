# prime_synthesis_collect_all_patterns.py — 7-Iteration Run Results

Window-less, with the paper's adaptive exponents (iteration k: exponents 1..k on every seed, both sides). Every sum and difference is collected; the smallest new value becomes the next seed. Counts are per exponent vector (one sum and one difference each), not per distinct value.

**Ratio** = primes observed / primes expected from size alone (prod p/(p-1) / ln N for values coprime to the seeds; 1 below g²). 1.00 means the exponents add nothing beyond size; 0 means never prime.

Total wall-clock time: **3032.3s**

## Per-Iteration Summary

| Iteration | Seeds | E | Values (vectors × 2) | Prime | Distinct values | Next seed | Next seed prime? | Time (s) |
|---|---|---|---|---|---|---|---|---|
| 1 | 1, 2 | 1 | 1 | 1 (100.0%) | 1 | 3 | yes | 0.0 |
| 2 | 1, 2, 3 | 2 | 14 | 13 (92.9%) | 8 | 5 | yes | 0.0 |
| 3 | 1, 2, 3, 5 | 3 | 213 | 144 (67.6%) | 139 | 7 | yes | 0.0 |
| 4 | 1, 2, 3, 5, 7 | 4 | 4092 | 1903 (46.5%) | 3344 | 11 | yes | 0.0 |
| 5 | 1, 2, 3, 5, 7, 11 | 5 | 99996 | 30804 (30.8%) | 93890 | 13 | yes | 1.2 |
| 6 | 1, 2, 3, 5, 7, 11, 13 | 6 | 2985981 | 663652 (22.2%) | 2947041 | 17 | yes | 51.1 |
| 7 | 1, 2, 3, 5, 7, 11, 13, 17 | 7 | 105413501 | 17321404 (16.4%) | 105235227 | 19 | yes | 2331.3 |

## All values

| Group | Values | Prime | Prime rate | Expected from size | Ratio |
|---|---|---|---|---|---|
| diff | 54251889 | 9026381 | 16.6% | 9163311 | **0.99** |
| sum | 54251909 | 8991540 | 16.6% | 9116140 | **0.99** |

## By gcd of all exponents

| Group | Values | Prime | Prime rate | Expected from size | Ratio |
|---|---|---|---|---|---|
| diff, gcd = 1 | 54077599 | 9026373 | 16.7% | 9133709 | **0.99** |
| diff, gcd = 2 | 163726 | 6 | 0.0% | 27989 | **0.00** |
| diff, gcd = 3 | 10172 | 1 | 0.0% | 1556 | **0.00** |
| diff, gcd = 4 | 120 | 0 | 0.0% | 23 | **0.00** |
| diff, gcd = 5 | 112 | 0 | 0.0% | 16 | **0.00** |
| diff, gcd = 6 | 96 | 0 | 0.0% | 11 | **0.00** |
| diff, gcd = 7 | 64 | 1 | 1.6% | 6 | **0.17** |
| sum, gcd = 1 | 54077619 | 8961287 | 16.6% | 9086691 | **0.99** |
| sum, gcd = 2 | 163726 | 30231 | 18.5% | 27843 | **1.09** |
| sum, gcd = 3 | 10172 | 0 | 0.0% | 1550 | **0.00** |
| sum, gcd = 4 | 120 | 22 | 18.3% | 23 | **0.97** |
| sum, gcd = 5 | 112 | 0 | 0.0% | 16 | **0.00** |
| sum, gcd = 6 | 96 | 0 | 0.0% | 11 | **0.00** |
| sum, gcd = 7 | 64 | 0 | 0.0% | 6 | **0.00** |

## All exponents even vs. not

| Group | Values | Prime | Prime rate | Expected from size | Ratio |
|---|---|---|---|---|---|
| diff, all even | 163942 | 6 | 0.0% | 28023 | **0.00** |
| diff, some odd | 54087947 | 9026375 | 16.7% | 9135287 | **0.99** |
| sum, all even | 163942 | 30253 | 18.5% | 27876 | **1.09** |
| sum, some odd | 54087967 | 8961287 | 16.6% | 9088263 | **0.99** |

## By number of exponents above 1

| Group | Values | Prime | Prime rate | Expected from size | Ratio |
|---|---|---|---|---|---|
| diff, 0 above 1 | 122 | 90 | 73.8% | 92 | **0.97** |
| diff, 1 above 1 | 4089 | 1969 | 48.2% | 1960 | **1.00** |
| diff, 2 above 1 | 63421 | 21785 | 34.3% | 21883 | **1.00** |
| diff, 3 above 1 | 574972 | 152452 | 26.5% | 155066 | **0.98** |
| diff, 4 above 1 | 3224166 | 703297 | 21.8% | 715957 | **0.98** |
| diff, 5 above 1 | 11067327 | 2060129 | 18.6% | 2095198 | **0.98** |
| diff, 6 above 1 | 21401888 | 3491411 | 16.3% | 3538966 | **0.99** |
| diff, 7 above 1 | 17915904 | 2595248 | 14.5% | 2634190 | **0.99** |
| sum, 0 above 1 | 127 | 88 | 69.3% | 94 | **0.94** |
| sum, 1 above 1 | 4092 | 1830 | 44.7% | 1905 | **0.96** |
| sum, 2 above 1 | 63426 | 21050 | 33.2% | 21438 | **0.98** |
| sum, 3 above 1 | 574976 | 151045 | 26.3% | 153079 | **0.99** |
| sum, 4 above 1 | 3224168 | 701580 | 21.8% | 709881 | **0.99** |
| sum, 5 above 1 | 11067328 | 2054787 | 18.6% | 2082467 | **0.99** |
| sum, 6 above 1 | 21401888 | 3473058 | 16.2% | 3522655 | **0.99** |
| sum, 7 above 1 | 17915904 | 2588102 | 14.4% | 2624622 | **0.99** |

## By the exponent on 2

| Group | Values | Prime | Prime rate | Expected from size | Ratio |
|---|---|---|---|---|---|
| diff, 2^1 | 7788914 | 1345400 | 17.3% | 1367262 | **0.98** |
| diff, 2^2 | 7788915 | 1330353 | 17.1% | 1350418 | **0.99** |
| diff, 2^3 | 7788912 | 1314593 | 16.9% | 1333734 | **0.99** |
| diff, 2^4 | 7788878 | 1300627 | 16.7% | 1317204 | **0.99** |
| diff, 2^5 | 7788367 | 1279842 | 16.4% | 1300638 | **0.98** |
| diff, 2^6 | 7778367 | 1260726 | 16.2% | 1281510 | **0.98** |
| diff, 2^7 | 7529536 | 1194840 | 15.9% | 1212545 | **0.99** |
| sum, 2^1 | 7788921 | 1338562 | 17.2% | 1359626 | **0.98** |
| sum, 2^2 | 7788920 | 1328774 | 17.1% | 1343065 | **0.99** |
| sum, 2^3 | 7788916 | 1303984 | 16.7% | 1326659 | **0.98** |
| sum, 2^4 | 7788880 | 1295484 | 16.6% | 1310395 | **0.99** |
| sum, 2^5 | 7788368 | 1272498 | 16.3% | 1294096 | **0.98** |
| sum, 2^6 | 7778368 | 1263210 | 16.2% | 1275279 | **0.99** |
| sum, 2^7 | 7529536 | 1189028 | 15.8% | 1207020 | **0.99** |

## 2 alone on its side vs. with other seeds

| Group | Values | Prime | Prime rate | Expected from size | Ratio |
|---|---|---|---|---|---|
| diff, 2 alone | 873609 | 103447 | 11.8% | 104922 | **0.99** |
| diff, 2 with others | 53378280 | 8922934 | 16.7% | 9058388 | **0.99** |
| sum, 2 alone | 873612 | 104017 | 11.9% | 104925 | **0.99** |
| sum, 2 with others | 53378297 | 8887523 | 16.7% | 9011215 | **0.99** |
