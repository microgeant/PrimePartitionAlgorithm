/*
 * Prime Partition Algorithm - C Implementation
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <math.h>

// ============================================================================
// Dynamic Array Implementation
// ============================================================================

typedef struct {
    uint64_t *data;
    size_t size;
    size_t capacity;
} Array;

static inline Array* array_create(size_t initial_capacity) {
    Array *arr = malloc(sizeof(Array));
    arr->data = malloc(initial_capacity * sizeof(uint64_t));
    arr->size = 0;
    arr->capacity = initial_capacity;
    return arr;
}

static inline void array_push(Array *arr, uint64_t value) {
    if (arr->size >= arr->capacity) {
        arr->capacity *= 2;
        arr->data = realloc(arr->data, arr->capacity * sizeof(uint64_t));
    }
    arr->data[arr->size++] = value;
}

static inline void array_free(Array *arr) {
    free(arr->data);
    free(arr);
}

// ============================================================================
// Hash Set Implementation (for deduplication)
// ============================================================================

#define HASH_SIZE 65536

typedef struct HashNode {
    uint64_t key;
    struct HashNode *next;
} HashNode;

typedef struct {
    HashNode *buckets[HASH_SIZE];
} HashSet;

static inline HashSet* hashset_create(void) {
    HashSet *set = calloc(1, sizeof(HashSet));
    return set;
}

static inline uint32_t hash_function(uint64_t key) {
    key ^= key >> 33;
    key *= 0xff51afd7ed558ccdULL;
    key ^= key >> 33;
    key *= 0xc4ceb9fe1a85ec53ULL;
    key ^= key >> 33;
    return key & (HASH_SIZE - 1);
}

static inline bool hashset_contains(HashSet *set, uint64_t key) {
    uint32_t index = hash_function(key);
    HashNode *node = set->buckets[index];
    while (node) {
        if (node->key == key) return true;
        node = node->next;
    }
    return false;
}

static inline void hashset_insert(HashSet *set, uint64_t key) {
    if (hashset_contains(set, key)) return;
    
    uint32_t index = hash_function(key);
    HashNode *node = malloc(sizeof(HashNode));
    node->key = key;
    node->next = set->buckets[index];
    set->buckets[index] = node;
}

static inline void hashset_free(HashSet *set) {
    for (int i = 0; i < HASH_SIZE; i++) {
        HashNode *node = set->buckets[i];
        while (node) {
            HashNode *next = node->next;
            free(node);
            node = next;
        }
    }
    free(set);
}

// ============================================================================
// Binary Partition Structure
// ============================================================================

typedef struct {
    Array *left;
    Array *right;
} Partition;

// ============================================================================
// Core Algorithm Functions
// ============================================================================

static inline __uint128_t fast_pow_128(uint64_t base, uint64_t exp) {
    if (exp == 0) return 1;
    if (exp == 1) return base;
    if (exp % 2 == 0) {
        __uint128_t half = fast_pow_128(base, exp / 2);
        return half * half;
    } else {
        return (__uint128_t)base * fast_pow_128(base, exp - 1);
    }
}

static inline bool is_prime(uint64_t n) {
    if (n <= 1) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    
    uint64_t sqrt_n = (uint64_t)sqrt((double)n);
    for (uint64_t i = 3; i <= sqrt_n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

static inline int compare_uint64(const void *a, const void *b) {
    uint64_t ua = *(const uint64_t*)a;
    uint64_t ub = *(const uint64_t*)b;
    return (ua > ub) - (ua < ub);
}

static Array* binary_partitions(const Array *list) {
    Array *partitions = array_create(64);
    
    if (list->size < 2) return partitions;
    
    size_t n = list->size;
    size_t half = n / 2;
    size_t max_val = (1ULL << n) - 1;
    
    for (size_t i = 1; i <= max_val; i++) {
        size_t left_count = __builtin_popcountll(i);
        
        if (left_count >= 1 && left_count <= half) {
            Array *left = array_create(left_count);
            Array *right = array_create(n - left_count);
            
            for (size_t j = 0; j < n; j++) {
                if (i & (1ULL << j)) {
                    array_push(left, list->data[j]);
                } else {
                    array_push(right, list->data[j]);
                }
            }
            
            if (right->size > 0) {
                // Store partition info encoded as pointer (we'll decode later)
                Partition *p = malloc(sizeof(Partition));
                p->left = left;
                p->right = right;
                array_push(partitions, (uint64_t)p);
            } else {
                array_free(left);
                array_free(right);
            }
        }
    }
    
    return partitions;
}

static Array* exponent_combinations(size_t size, uint64_t max_exp) {
    Array *result = array_create(256);
    
    if (size == 0) return result;
    
    size_t total = 1;
    for (size_t i = 0; i < size; i++) {
        total *= max_exp;
    }
    
    for (size_t combo_idx = 0; combo_idx < total; combo_idx++) {
        Array *exps = array_create(size);
        size_t temp = combo_idx;
        
        for (size_t i = 0; i < size; i++) {
            uint64_t exp = (temp % max_exp) + 1;
            array_push(exps, exp);
            temp /= max_exp;
        }
        
        array_push(result, (uint64_t)exps);
    }
    
    return result;
}

static Array* compute_primes(const Array *seeds) {
    const uint64_t max_exponent = 2;
    
    if (seeds->size == 0) {
        return array_create(1);
    }
    
    // Find max prime
    uint64_t max_prime = seeds->data[0];
    for (size_t i = 1; i < seeds->size; i++) {
        if (seeds->data[i] > max_prime) {
            max_prime = seeds->data[i];
        }
    }
    
    uint64_t range_start = max_prime + 1;
    uint64_t range_end = max_prime * max_prime - 1;
    
    Array *candidates = array_create(1024);
    
    // Generate binary partitions
    Array *partitions = binary_partitions(seeds);
    
    // For each partition
    for (size_t p = 0; p < partitions->size; p++) {
        Partition *partition = (Partition*)partitions->data[p];
        
        // Generate exponent combinations
        Array *exps = exponent_combinations(seeds->size, max_exponent);
        
        // For each exponent combination
        for (size_t e = 0; e < exps->size; e++) {
            Array *exp = (Array*)exps->data[e];
            
            // Calculate products using u128 to avoid overflow
            __uint128_t left_prod = 1;
            for (size_t i = 0; i < partition->left->size; i++) {
                __uint128_t pow_result = fast_pow_128(partition->left->data[i], exp->data[i]);
                left_prod *= pow_result;
                if (left_prod > UINT64_MAX) break;
            }
            
            __uint128_t right_prod = 1;
            for (size_t i = 0; i < partition->right->size; i++) {
                size_t exp_idx = partition->left->size + i;
                __uint128_t pow_result = fast_pow_128(partition->right->data[i], exp->data[exp_idx]);
                right_prod *= pow_result;
                if (right_prod > UINT64_MAX) break;
            }
            
            // Skip if overflow
            if (left_prod > UINT64_MAX || right_prod > UINT64_MAX) {
                continue;
            }
            
            __uint128_t sum = left_prod + right_prod;
            __uint128_t diff = (left_prod > right_prod) ? (left_prod - right_prod) : (right_prod - left_prod);
            
            if (sum >= range_start && sum <= range_end && sum <= UINT64_MAX) {
                array_push(candidates, (uint64_t)sum);
            }
            if (diff >= range_start && diff <= range_end && diff <= UINT64_MAX) {
                array_push(candidates, (uint64_t)diff);
            }
        }
        
        // Free exponent combinations
        for (size_t e = 0; e < exps->size; e++) {
            array_free((Array*)exps->data[e]);
        }
        array_free(exps);
    }
    
    // Free partitions
    for (size_t p = 0; p < partitions->size; p++) {
        Partition *partition = (Partition*)partitions->data[p];
        array_free(partition->left);
        array_free(partition->right);
        free(partition);
    }
    array_free(partitions);
    
    // Filter for primes and deduplicate
    HashSet *prime_set = hashset_create();
    
    for (size_t i = 0; i < candidates->size; i++) {
        uint64_t candidate = candidates->data[i];
        if (is_prime(candidate)) {
            hashset_insert(prime_set, candidate);
        }
    }
    
    array_free(candidates);
    
    // Convert hash set back to array
    Array *primes = array_create(64);
    for (int i = 0; i < HASH_SIZE; i++) {
        HashNode *node = prime_set->buckets[i];
        while (node) {
            array_push(primes, node->key);
            node = node->next;
        }
    }
    
    hashset_free(prime_set);
    
    // Sort results
    qsort(primes->data, primes->size, sizeof(uint64_t), compare_uint64);
    
    return primes;
}

static Array* run_algorithm(size_t iterations, const Array *initial) {
    Array *current = array_create(initial->capacity);
    for (size_t i = 0; i < initial->size; i++) {
        array_push(current, initial->data[i]);
    }
    
    Array *acc_primes = array_create(256);
    
    for (size_t iter = 0; iter < iterations; iter++) {
        Array *found = compute_primes(current);
        
        // Get distinct values
        HashSet *distinct_set = hashset_create();
        for (size_t i = 0; i < found->size; i++) {
            hashset_insert(distinct_set, found->data[i]);
        }
        
        Array *distinct = array_create(64);
        for (int i = 0; i < HASH_SIZE; i++) {
            HashNode *node = distinct_set->buckets[i];
            while (node) {
                array_push(distinct, node->key);
                node = node->next;
            }
        }
        
        // Accumulate primes
        for (size_t i = 0; i < distinct->size; i++) {
            array_push(acc_primes, distinct->data[i]);
        }
        
        // Find new primes not in current
        HashSet *current_set = hashset_create();
        for (size_t i = 0; i < current->size; i++) {
            hashset_insert(current_set, current->data[i]);
        }
        
        uint64_t min_new = UINT64_MAX;
        bool found_new = false;
        for (size_t i = 0; i < distinct->size; i++) {
            if (!hashset_contains(current_set, distinct->data[i])) {
                if (distinct->data[i] < min_new) {
                    min_new = distinct->data[i];
                    found_new = true;
                }
            }
        }
        
        if (found_new) {
            array_push(current, min_new);
        }
        
        hashset_free(current_set);
        hashset_free(distinct_set);
        array_free(distinct);
        array_free(found);
    }
    
    array_free(current);
    return acc_primes;
}

// ============================================================================
// Main Function
// ============================================================================

int main(void) {
    printf("=== C VERSION ===\n");
    
    // Initialize with [1, 2]
    Array *initial = array_create(2);
    array_push(initial, 1);
    array_push(initial, 2);
    
    // Run algorithm
    Array *result = run_algorithm(10, initial);
    
    // Get unique sorted primes
    HashSet *unique_set = hashset_create();
    for (size_t i = 0; i < result->size; i++) {
        hashset_insert(unique_set, result->data[i]);
    }
    
    Array *sorted_primes = array_create(64);
    for (int i = 0; i < HASH_SIZE; i++) {
        HashNode *node = unique_set->buckets[i];
        while (node) {
            array_push(sorted_primes, node->key);
            node = node->next;
        }
    }
    
    qsort(sorted_primes->data, sorted_primes->size, sizeof(uint64_t), compare_uint64);
    
    // Print results
    printf("Hello primes: [");
    for (size_t i = 0; i < sorted_primes->size; i++) {
        if (i > 0) printf(", ");
        printf("%llu", (unsigned long long)sorted_primes->data[i]);
    }
    printf("]\n");
    printf("Total discovered: %zu\n", sorted_primes->size);
    
    // Check for composites
    printf("Found composites: [");
    bool first = true;
    for (size_t i = 0; i < result->size; i++) {
        if (!is_prime(result->data[i])) {
            if (!first) printf(", ");
            printf("%llu", (unsigned long long)result->data[i]);
            first = false;
        }
    }
    printf("]\n");
    
    // Cleanup
    hashset_free(unique_set);
    array_free(sorted_primes);
    array_free(result);
    array_free(initial);
    
    return 0;
}
