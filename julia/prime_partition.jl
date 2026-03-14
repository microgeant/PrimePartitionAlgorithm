#!/usr/bin/env julia

"""
Julia implementation of Prime Partition Algorithm
"""

using Printf

# ============================================================================
# Core Algorithm Functions
# ============================================================================

"""
    fast_pow(base::Int64, exp::Int)::Int64

Fast exponentiation using exponentiation by squaring.
Time complexity: O(log exp)
"""
function fast_pow(base::Int64, exp::Int)::Int64
    if exp == 0
        return 1
    elseif exp == 1
        return base
    elseif iseven(exp)
        half = fast_pow(base, exp ÷ 2)
        return half * half
    else
        return base * fast_pow(base, exp - 1)
    end
end

"""
    is_prime(n::Int64)::Bool

Optimized primality test using trial division up to √n.
Only tests odd divisors after checking 2.
Time complexity: O(√n)
"""
function is_prime(n::Int64)::Bool
    if n ≤ 1
        return false
    elseif n == 2
        return true
    elseif iseven(n)
        return false
    end
    
    sqrt_n = isqrt(n)
    for i in 3:2:sqrt_n
        if n % i == 0
            return false
        end
    end
    
    return true
end

"""
    combinations(list::Vector{T}, k::Int)::Vector{Vector{T}} where T

Generate all k-combinations of a list.
"""
function combinations(list::Vector{T}, k::Int)::Vector{Vector{T}} where T
    if k == 0
        return [T[]]
    elseif isempty(list)
        return Vector{Vector{T}}()
    end
    
    result = Vector{Vector{T}}()
    head = list[1]
    tail = list[2:end]
    
    # With head
    for combo in combinations(tail, k - 1)
        push!(result, vcat([head], combo))
    end
    
    # Without head
    append!(result, combinations(tail, k))
    
    return result
end

"""
    binary_partitions(list::Vector{T})::Vector{Tuple{Vector{T}, Vector{T}}} where T

Generate all binary partitions of a list.
Returns pairs of (left_group, right_group).
"""
function binary_partitions(list::Vector{T})::Vector{Tuple{Vector{T}, Vector{T}}} where T
    if length(list) < 2
        return Tuple{Vector{T}, Vector{T}}[]
    end
    
    result = Tuple{Vector{T}, Vector{T}}[]
    n = length(list)
    
    for i in 1:(n ÷ 2)
        for left in combinations(list, i)
            right = setdiff(list, left)
            if length(right) == n - i
                push!(result, (left, right))
            end
        end
    end
    
    return result
end

"""
    exponent_combinations(size::Int, max_exp::Int)::Vector{Vector{Int}}

Generate all combinations of exponents [1..max_exp] of given size.
"""
function exponent_combinations(size::Int, max_exp::Int)::Vector{Vector{Int}}
    if size <= 0
        return Vector{Vector{Int}}()
    end
    
    # Use Iterators.product for Cartesian product
    ranges = [1:max_exp for _ in 1:size]
    result = Vector{Vector{Int}}()
    
    for combo in Iterators.product(ranges...)
        push!(result, collect(combo))
    end
    
    return result
end

"""
    compute_primes(seeds::Vector{Int64}, max_exponent::Int=2)::Vector{Int64}

Generate and filter prime candidates from seed set using binary partitions
and powered products.
"""
function compute_primes(seeds::Vector{Int64}, max_exponent::Int=2)::Vector{Int64}
    if isempty(seeds)
        return Int64[]
    end
    
    max_prime = maximum(seeds)
    range_start = max_prime + 1
    range_end = max_prime^2 - 1
    
    candidates = Int64[]
    
    for (left, right) in binary_partitions(seeds)
        for exps in exponent_combinations(length(seeds), max_exponent)
            left_exps = exps[1:length(left)]
            right_exps = exps[length(left)+1:end]
            
            # Compute powered products
            left_prod = prod(fast_pow(left[i], left_exps[i]) for i in 1:length(left))
            right_prod = prod(fast_pow(right[i], right_exps[i]) for i in 1:length(right))
            
            # Generate candidates
            push!(candidates, left_prod + right_prod)
            push!(candidates, abs(left_prod - right_prod))
        end
    end
    
    # Filter and deduplicate
    filtered = filter(c -> range_start ≤ c ≤ range_end, candidates)
    unique_candidates = unique(filtered)
    primes = filter(is_prime, unique_candidates)
    
    return sort(primes)
end

"""
    run_algorithm(iterations::Int, initial::Vector{Int64}, max_exponent::Int=2)

Run the partition algorithm for specified iterations.
Returns tuple of (all_primes, occurrence_counts).
"""
function run_algorithm(iterations::Int, initial::Vector{Int64}, max_exponent::Int=2)
    current = copy(initial)
    acc_primes = Int64[]
    acc_counts = Dict{Int64, Int}()
    
    for iter in 1:iterations
        found = compute_primes(current, max_exponent)
        distinct = unique(found)
        
        # Update occurrence counts
        for prime in found
            acc_counts[prime] = get(acc_counts, prime, 0) + 1
        end
        
        # Accumulate primes
        append!(acc_primes, distinct)
        
        # Find next prime to add
        new_primes = setdiff(distinct, current)
        if !isempty(new_primes)
            min_new = minimum(new_primes)
            push!(current, min_new)
        end
    end
    
    return (acc_primes, acc_counts)
end

# ============================================================================
# Main Execution
# ============================================================================

function main()
    println("=== JULIA VERSION ===")
    
    # Run algorithm
    (primes, counts) = run_algorithm(10, Int64[1, 2], 2)
    
    # Get unique sorted primes
    sorted_primes = sort(unique(primes))
    
    # Display results
    println("Hello primes: ", sorted_primes)
    println("Total discovered: ", length(sorted_primes))
    
    # Check for composites (should be none)
    composites = filter(p -> !is_prime(p), primes)
    println("Found composites: ", composites)
    
    # Optional: Show occurrence counts
    # println("\nOccurrence counts:")
    # for (prime, count) in sort(collect(counts))
    #     println("  $prime: $count")
    # end
end

# Run if executed as script
if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
