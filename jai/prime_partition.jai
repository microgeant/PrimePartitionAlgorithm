#import "Basic";
#import "Math";
#import "Hash_Table";
#import "Sort";

// --- Math Utilities ---

is_prime :: (n: s64) -> bool {
    if n < 2 return false;
    if n == 2 || n == 3 return true;
    if n % 2 == 0 || n % 3 == 0 return false;
    if n < 9 return true;

    limit := cast(s64) sqrt(cast(float64) n);
    k: s64 = 5;
    while k <= limit {
        if n % k == 0 || n % (k + 2) == 0 return false;
        k += 6;
    }
    return true;
}

fast_pow :: (base: s64, exp: s64) -> s64 {
    if exp == 0 return 1;
    if exp == 1 return base;
    if exp % 2 == 0 {
        half := fast_pow(base, exp / 2);
        return half * half;
    }
    return base * fast_pow(base, exp - 1);
}

product_pow :: (values: [] s64, exps: [] s64) -> s64 {
    acc: s64 = 1;
    for values {
        acc *= fast_pow(it, exps[it_index]);
    }
    return acc;
}

i_abs :: (x: s64) -> s64 {
    if x < 0 return -x;
    return x;
}

// --- Combinatorics Helpers ---

// Pass data via user_data pointer because Jai procedures don't capture scope
combinations :: (list: [] s64, k: s64, data: *void, callback: (combination: [] s64, remaining: [] s64, user_data: *void)) {
    indices := NewArray(k, s64);
    defer array_free(indices);
    for 0..k-1 indices[it] = it;

    while true {
        combo := NewArray(k, s64);
        remaining := NewArray(list.count - k, s64);
        
        c_idx, r_idx := 0, 0;
        for i: 0..list.count-1 {
            found := false;
            for idx: indices if idx == i { found = true; break; }
            if found {
                combo[c_idx] = list[i];
                c_idx += 1;
            } else {
                remaining[r_idx] = list[i];
                r_idx += 1;
            }
        }

        callback(combo, remaining, data);
        array_free(combo);
        array_free(remaining);

        i := k - 1;
        while i >= 0 && indices[i] == i + list.count - k {
            i -= 1;
        }
        if i < 0 break;
        indices[i] += 1;
        for j: i+1..k-1 indices[j] = indices[i] + j - i;
    }
}

generate_exponent_combinations :: (n: s64, max_exp: s64, data: *void, callback: (exps: [] s64, user_data: *void)) {
    current := NewArray(n, s64);
    defer array_free(current);
    for 0..n-1 current[it] = 1;

    while true {
        callback(current, data);
        
        idx := n - 1;
        while idx >= 0 {
            current[idx] += 1;
            if current[idx] <= max_exp break;
            current[idx] = 1;
            idx -= 1;
        }
        if idx < 0 break;
    }
}

// --- Core Algorithm ---

Compute_State :: struct {
    seeds: [] s64;
    found_primes: *[..] s64;
    min_r: s64;
    max_r: s64;
}

Exp_State :: struct {
    parent: *Compute_State;
    left: [] s64;
    right: [] s64;
}

compute_primes :: (seeds: [] s64) -> [..] s64 {
    found_primes: [..] s64;
    if seeds.count < 2 return found_primes;

    max_p: s64 = -1;
    for seeds if it > max_p max_p = it;
    
    state: Compute_State;
    state.seeds = seeds;
    state.found_primes = *found_primes;
    state.min_r = max_p + 1;
    state.max_r = max_p * max_p - 1;

    for split_idx: 1..seeds.count/2 {
        combinations(seeds, split_idx, *state, (left: [] s64, right: [] s64, data: *void) {
            s := cast(*Compute_State) data;
            
            e_state: Exp_State;
            e_state.parent = s;
            e_state.left = left;
            e_state.right = right;

            generate_exponent_combinations(s.seeds.count, 2, *e_state, (exps: [] s64, e_data: *void) {
                es := cast(*Exp_State) e_data;
                
                // Use array_view to avoid copying
                left_exps  := array_view(exps, 0, es.left.count);
                right_exps := array_view(exps, es.left.count, es.right.count);

                lp := product_pow(es.left, left_exps);
                rp := product_pow(es.right, right_exps);

                c1 := lp + rp;
                c2 := i_abs(lp - rp);

                if c1 >= es.parent.min_r && c1 <= es.parent.max_r {
                    array_add(es.parent.found_primes, c1);
                }
                if c2 >= es.parent.min_r && c2 <= es.parent.max_r {
                    array_add(es.parent.found_primes, c2);
                }
            });
        });
    }
    return found_primes;
}

run_algorithm :: (iterations: int, initial: [] s64) -> (acc_primes: [..] s64, counts: Table(s64, int)) {
    current_seeds: [..] s64;
    for initial array_add(*current_seeds, it);
    
    acc_primes: [..] s64;
    counts: Table(s64, int);
    init(*counts);

    for i: 1..iterations {
        found := compute_primes(current_seeds);
        defer array_free(found);

        distinct_in_iteration: Table(s64, bool);
        init(*distinct_in_iteration);
        defer deinit(*distinct_in_iteration);

        for p: found {
            if !table_contains(*distinct_in_iteration, p) {
                table_set(*distinct_in_iteration, p, true);
                array_add(*acc_primes, p);
                
                count, exists := table_find(*counts, p);
                if exists table_set(*counts, p, count + 1);
                else table_set(*counts, p, 1);
            }
        }

        // Standard Jai quick_sort comparison
        quick_sort(found, (a: s64, b: s64) -> int {
            if a < b return -1;
            if a > b return 1;
            return 0;
        });
        
        next_to_add: s64 = -1;
        for p: found {
            in_seeds := false;
            for s: current_seeds if s == p { in_seeds = true; break; }
            if !in_seeds {
                next_to_add = p;
                break;
            }
        }

        if next_to_add != -1 {
            array_add(*current_seeds, next_to_add);
        }
    }

    return acc_primes, counts;
}

main :: () {
    print("=== JAI VERSION ===\n");
    
    initial_seeds: [] s64 = .[1, 2];
    primes, counts := run_algorithm(10, initial_seeds);

    distinct_primes: [..] s64;
    for primes {
        exists := false;
        for dp: distinct_primes if dp == it { exists = true; break; }
        if !exists array_add(*distinct_primes, it);
    }
    quick_sort(distinct_primes, (a: s64, b: s64) -> int {
        if a < b return -1;
        if a > b return 1;
        return 0;
    });

    print("Hello primes: %\n", distinct_primes);
    print("Total discovered: %\n", distinct_primes.count);
    
    print("Occurrence counts:\n");
    for count, p: counts {
        print("  %: %\n", p, count);
    }

    composites: [..] s64;
    for p: primes if !is_prime(p) array_add(*composites, p);
    print("Found composites: %\n", composites);
}