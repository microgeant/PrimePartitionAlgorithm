from itertools import product as itertools_product


def binary_partitions(lst):
    """Generates all unique binary partitions of a list."""
    if len(lst) < 2:
        return
    first = lst[0]
    rest = lst[1:]
    num_partitions = 1 << len(rest)
    for i in range(1, num_partitions):
        left = []
        right = [first]
        for j in range(len(rest)):
            if (i >> j) & 1:
                left.append(rest[j])
            else:
                right.append(rest[j])
        yield (left, right)


def exponent_combinations(n, max_exp):
    """Generate all exponent vectors (odometer approach)."""
    if n == 0:
        return
    indices = [1] * n
    while True:
        yield list(indices)
        i = n - 1
        while i >= 0 and indices[i] == max_exp:
            indices[i] = 1
            i -= 1
        if i < 0:
            break
        indices[i] += 1


def compute_primes(seeds, max_exp):
    """Synthesizes candidates within the quadratic window (max_p, max_p^2]."""
    if not seeds:
        return []
    max_p = max(seeds)
    min_r = max_p + 1
    max_r = max_p * max_p
    results = []
    for left, right in binary_partitions(seeds):
        total_size = len(left) + len(right)
        for exp_vector in exponent_combinations(total_size, max_exp):
            left_exps = exp_vector[:len(left)]
            right_exps = exp_vector[len(left):]
            left_prod = 1
            for p, e in zip(left, left_exps):
                left_prod *= p ** e
            right_prod = 1
            for p, e in zip(right, right_exps):
                right_prod *= p ** e
            sum_sigma = left_prod + right_prod
            if min_r <= sum_sigma <= max_r:
                results.append(sum_sigma)
            diff_sigma = abs(left_prod - right_prod)
            if min_r <= diff_sigma <= max_r:
                results.append(diff_sigma)
    return results


def main():
    current_max_exp = 1
    max_iterations = 5
    current = [1, 2]
    acc_primes = []

    for i in range(1, max_iterations + 1):
        found = compute_primes(current, current_max_exp)
        current_max_exp += 1
        distinct_found = sorted(set(found))
        current_set = set(current)
        diff = [x for x in distinct_found if x not in current_set]
        if diff:
            current = current + [min(diff)]
        acc_primes.extend(distinct_found)

    all_primes = sorted(set([2] + acc_primes))
    print(f"Discovered primes: {all_primes}")


if __name__ == "__main__":
    main()