use std::collections::{HashMap, HashSet};

/// Rust implementation of Prime Partition Algorithm

fn main() {
    println!("=== RUST VERSION ===");
    let (primes, _counts) = run_algorithm(10, vec![1, 2]);
    
    let mut sorted_primes: Vec<i64> = primes.iter().cloned().collect::<HashSet<_>>().into_iter().collect();
    sorted_primes.sort_unstable();
    
    println!("Hello primes: {:?}", sorted_primes);
    println!("Total discovered: {}", sorted_primes.len());
    
    let composites: Vec<i64> = primes.iter()
        .filter(|&&p| !is_prime(p))
        .cloned()
        .collect();
    println!("Found composites: {:?}", composites);
}

/// Run the algorithm for specified iterations
fn run_algorithm(iterations: usize, initial: Vec<i64>) -> (Vec<i64>, HashMap<i64, usize>) {
    let mut current = initial;
    let mut acc_primes = Vec::new();
    let mut acc_counts = HashMap::new();
    
    for _ in 0..iterations {
        let found = compute_primes(&current, 2);
        let distinct: HashSet<i64> = found.iter().cloned().collect();
        
        // Update occurrence counts
        for &prime in &found {
            *acc_counts.entry(prime).or_insert(0) += 1;
        }
        
        // Accumulate primes
        acc_primes.extend(distinct.iter());
        
        // Find next prime to add
        let current_set: HashSet<i64> = current.iter().cloned().collect();
        let new_primes: Vec<i64> = distinct.difference(&current_set).cloned().collect();
        
        if let Some(&min_new) = new_primes.iter().min() {
            current.push(min_new);
        } else {
            break; // No new primes found in range
        }
    }
    
    (acc_primes, acc_counts)
}

/// Generate and filter prime candidates from seed set
fn compute_primes(seeds: &[i64], max_exponent: u32) -> Vec<i64> {
    if seeds.is_empty() {
        return Vec::new();
    }
    
    let max_prime = *seeds.iter().max().unwrap();
    let range_start = max_prime + 1;
    let range_end = max_prime.checked_mul(max_prime).map(|v| v - 1).unwrap_or(i64::MAX);
    
    let mut candidates = Vec::new();
    
    for (left, right) in binary_partitions(seeds) {
        for exps in exponent_combinations(seeds.len(), max_exponent) {
            let (left_exps, right_exps) = exps.split_at(left.len());
            
            let left_prod = left.iter()
                .zip(left_exps.iter())
                .try_fold(1i64, |acc, (&num, &exp)| {
                    fast_pow(num, exp).and_then(|p| acc.checked_mul(p))
                });
            
            let right_prod = right.iter()
                .zip(right_exps.iter())
                .try_fold(1i64, |acc, (&num, &exp)| {
                    fast_pow(num, exp).and_then(|p| acc.checked_mul(p))
                });
            
            if let (Some(lp), Some(rp)) = (left_prod, right_prod) {
                if let Some(sum) = lp.checked_add(rp) {
                    candidates.push(sum);
                }
                candidates.push((lp - rp).abs());
            }
        }
    }
    
    // Filter and deduplicate
    let mut primes: Vec<i64> = candidates.into_iter()
        .filter(|&c| c >= range_start && c <= range_end)
        .collect::<HashSet<_>>()
        .into_iter()
        .filter(|&c| is_prime(c))
        .collect();
    
    primes.sort_unstable();
    primes
}

/// Generate all binary partitions of a slice
fn binary_partitions(list: &[i64]) -> Vec<(Vec<i64>, Vec<i64>)> {
    if list.len() < 2 {
        return Vec::new();
    }
    
    let mut result = Vec::new();
    
    for i in 1..=list.len() / 2 {
        for left in combinations(list, i) {
            let left_set: HashSet<i64> = left.iter().cloned().collect();
            let right: Vec<i64> = list.iter()
                .filter(|x| !left_set.contains(x))
                .cloned()
                .collect();
            
            if right.len() == list.len() - i {
                result.push((left, right));
            }
        }
    }
    
    result
}

/// Generate k-combinations of a slice
fn combinations(list: &[i64], k: usize) -> Vec<Vec<i64>> {
    if k == 0 {
        return vec![Vec::new()];
    }
    if list.is_empty() {
        return Vec::new();
    }
    
    let mut result = Vec::new();
    let head = list[0];
    let tail = &list[1..];
    
    // With head
    for mut combo in combinations(tail, k - 1) {
        combo.insert(0, head);
        result.push(combo);
    }
    
    // Without head
    result.extend(combinations(tail, k));
    
    result
}

/// Generate all combinations of exponents
fn exponent_combinations(size: usize, max_exp: u32) -> Vec<Vec<u32>> {
    if size == 0 {
        return Vec::new();
    }
    
    let mut result = vec![Vec::new()];
    
    for _ in 0..size {
        let mut new_result = Vec::new();
        for combo in result {
            for exp in 1..=max_exp {
                let mut new_combo = combo.clone();
                new_combo.push(exp);
                new_result.push(new_combo);
            }
        }
        result = new_result;
    }
    
    result
}

/// Fast exponentiation using exponentiation by squaring (Checked)
fn fast_pow(base: i64, exp: u32) -> Option<i64> {
    match exp {
        0 => Some(1),
        1 => Some(base),
        _ if exp % 2 == 0 => {
            let half = fast_pow(base, exp / 2)?;
            half.checked_mul(half)
        }
        _ => {
            let prev = fast_pow(base, exp - 1)?;
            base.checked_mul(prev)
        }
    }
}

/// Optimized primality test
fn is_prime(n: i64) -> bool {
    if n <= 1 {
        return false;
    }
    if n == 2 {
        return true;
    }
    if n % 2 == 0 {
        return false;
    }
    
    let sqrt_n = (n as f64).sqrt() as i64;
    
    for i in (3..=sqrt_n).step_by(2) {
        if n % i == 0 {
            return false;
        }
    }
    
    true
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_is_prime() {
        assert!(!is_prime(1));
        assert!(is_prime(2));
        assert!(is_prime(3));
        assert!(!is_prime(4));
        assert!(is_prime(5));
        assert!(is_prime(7));
        assert!(!is_prime(9));
        assert!(is_prime(11));
    }
    
    #[test]
    fn test_fast_pow() {
        assert_eq!(fast_pow(2, 0), Some(1));
        assert_eq!(fast_pow(2, 1), Some(2));
        assert_eq!(fast_pow(2, 3), Some(8));
        assert_eq!(fast_pow(3, 2), Some(9));
        assert_eq!(fast_pow(i64::MAX, 2), None);
    }
    
    #[test]
    fn test_binary_partitions() {
        let partitions = binary_partitions(&[1, 2]);
        assert_eq!(partitions.len(), 2);
        assert!(partitions.contains(&(vec![1], vec![2])));
        assert!(partitions.contains(&(vec![2], vec![1])));
    }
    
    #[test]
    fn test_compute_primes() {
        let primes = compute_primes(&[1, 2], 2);
        assert!(primes.contains(&3));
    }
}
