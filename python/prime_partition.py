#!/usr/bin/env python3
"""
Python implementation of Prime Partition Algorithm
"""

from typing import List, Tuple, Dict
from itertools import combinations, product
from collections import Counter
import math


def main():
    print("=== PYTHON VERSION ===")
    primes, counts = run_algorithm(iterations=10, initial=[1, 2])
    
    sorted_primes = sorted(set(primes))
    print(f"Hello primes: {sorted_primes}")
    print(f"Total discovered: {len(sorted_primes)}")
    print(f"Found composites: {[p for p in primes if not is_prime(p)]}")


def run_algorithm(iterations: int, initial: List[int]) -> Tuple[List[int], Dict[int, int]]:
    """Run the partition algorithm for specified iterations."""
    current = initial.copy()
    acc_primes = []
    acc_counts = Counter()
    
    for _ in range(iterations):
        found = compute_primes(current)
        distinct = list(set(found))
        
        # Update occurrence counts
        acc_counts.update(distinct)
        
        # Accumulate primes
        acc_primes.extend(distinct)
        
        # Find next prime to add
        new_primes = set(distinct) - set(current)
        if new_primes:
            min_new = min(new_primes)
            current.append(min_new)
    
    return acc_primes, dict(acc_counts)


def compute_primes(seeds: List[int], max_exponent: int = 2) -> List[int]:
    """Generate and filter prime candidates from seed set."""
    if not seeds:
        return []
    
    max_prime = max(seeds)
    range_start = max_prime + 1
    range_end = max_prime * max_prime - 1
    
    candidates = []
    
    for left, right in binary_partitions(seeds):
        for exps in exponent_combinations(len(seeds), max_exponent):
            left_exps = exps[:len(left)]
            right_exps = exps[len(left):]
            
            left_prod = 1
            for num, exp in zip(left, left_exps):
                left_prod *= fast_pow(num, exp)
            
            right_prod = 1
            for num, exp in zip(right, right_exps):
                right_prod *= fast_pow(num, exp)
            
            candidates.append(left_prod + right_prod)
            candidates.append(abs(left_prod - right_prod))
    
    # Filter and deduplicate
    primes = sorted(set(
        c for c in candidates
        if range_start <= c <= range_end and is_prime(c)
    ))
    
    return primes


def binary_partitions(lst: List[int]) -> List[Tuple[List[int], List[int]]]:
    """Generate all binary partitions of a list."""
    if len(lst) < 2:
        return []
    
    result = []
    for i in range(1, len(lst) // 2 + 1):
        for left in combinations(lst, i):
            right = [x for x in lst if x not in left]
            if len(right) == len(lst) - i:
                result.append((list(left), right))
    
    return result


def exponent_combinations(size: int, max_exp: int) -> List[Tuple[int, ...]]:
    """Generate all combinations of exponents."""
    if size <= 0:
        return []
    return list(product(range(1, max_exp + 1), repeat=size))


def fast_pow(base: int, exp: int) -> int:
    """Fast exponentiation using exponentiation by squaring."""
    if exp == 0:
        return 1
    if exp == 1:
        return base
    if exp % 2 == 0:
        half = fast_pow(base, exp // 2)
        return half * half
    else:
        return base * fast_pow(base, exp - 1)


def is_prime(n: int) -> bool:
    """Optimized primality test."""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    sqrt_n = int(math.sqrt(n))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    
    return True


if __name__ == "__main__":
    main()
