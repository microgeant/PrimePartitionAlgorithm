import kotlin.math.abs
import kotlin.math.sqrt

/**
 * Kotlin implementation of Prime Partition Algorithm
 */
object PrimePartition {

    @JvmStatic
    fun main(args: Array<String>) {
        println("=== KOTLIN VERSION ===")
        val (primes, counts) = runAlgorithm(10, listOf(1L, 2L))
        printResults(primes, counts)
    }

    private fun printResults(primes: List<Long>, counts: Map<Long, Int>) {
        val sortedPrimes = primes.sorted().distinct()
        println("Hello primes: $sortedPrimes")
        println("Total discovered: ${sortedPrimes.size}")
        println("Occurrence counts: ${counts.toSortedMap()}")
        println("Found composites: ${primes.filter { !isPrime(it) }}")
    }

    /**
     * Run algorithm for n iterations
     */
    fun runAlgorithm(iterations: Int, initial: List<Long>): Pair<List<Long>, Map<Long, Int>> {
        var current = initial
        var accPrimes = emptyList<Long>()
        var accCounts = emptyMap<Long, Int>()

        for (i in 1..iterations) {
            val found = computePrimes(current).toList()
            val distinct = found.sorted().distinct()

            // Update counts
            val newCounts = mutableMapOf<Long, Int>()
            newCounts.putAll(accCounts)
            distinct.forEach { p ->
                newCounts[p] = (newCounts[p] ?: 0) + 1
            }

            // Find next prime to add
            val currentSet = current.toSet()
            val distinctSet = found.toSet()
            val diff = distinctSet - currentSet
            val next = if (diff.isEmpty()) current else current + diff.min()

            // Update state
            accPrimes = accPrimes + distinct
            accCounts = newCounts
            current = next
        }

        return accPrimes to accCounts
    }

    /**
     * Compute all primes from the current seed set
     */
    private fun computePrimes(seeds: List<Long>): Sequence<Long> {
        if (seeds.isEmpty()) return emptySequence()

        val maxP = seeds.maxOrNull() ?: return emptySequence()
        val minR = maxP + 1
        val maxR = maxP * maxP - 1

        return sequence {
            for ((left, right) in binaryPartitions(seeds)) {
                for (exps in exponentCombinations(seeds.size, 2)) {
                    val n = seeds.size
                    val (leftExps, rightExps) = exps.splitPair(left.size)

                    val leftProd = productPow(left, leftExps)
                    val rightProd = productPow(right, rightExps)

                    for (candidate in listOf(leftProd + rightProd, abs(leftProd - rightProd))) {
                        if (candidate >= minR && candidate <= maxR && isPrime(candidate)) {
                            yield(candidate)
                        }
                    }
                }
            }
        }
    }

    /**
     * Generate all binary partitions of a list
     */
    private fun <T> binaryPartitions(list: List<T>): Sequence<Pair<List<T>, List<T>>> = sequence {
        if (list.size < 2) return@sequence

        val size = list.size
        val half = size / 2

        for (splitIdx in 1..half) {
            for (left in combinations(splitIdx, list)) {
                val remaining = list.filterNot { it in left }
                for (right in combinations(size - splitIdx, remaining)) {
                    yield(left to right)
                }
            }
        }
    }

    /**
     * Generate all k-combinations of a list
     */
    private fun <T> combinations(k: Int, list: List<T>): Sequence<List<T>> = sequence {
        if (k == 0) {
            yield(emptyList())
            return@sequence
        }
        if (list.isEmpty()) return@sequence

        val first = list.first()
        val rest = list.drop(1)

        // Include first element
        for (combo in combinations(k - 1, rest)) {
            yield(listOf(first) + combo)
        }

        // Exclude first element
        for (combo in combinations(k, rest)) {
            yield(combo)
        }
    }

    /**
     * Generate all exponent combinations
     */
    private fun exponentCombinations(n: Int, maxExp: Int): Sequence<List<Int>> = sequence {
        val exponents = (1..maxExp).toList()
        replicateM(n, exponents).forEach { yield(it) }
    }

    /**
     * Compute product with powers
     */
    private fun productPow(list: List<Long>, exps: List<Int>): Long {
        return list.zip(exps).fold(1L) { acc, (x, e) -> acc * fastPow(x, e) }
    }

    /**
     * Fast exponentiation by squaring
     */
    private fun fastPow(base: Long, exp: Int): Long {
        return when {
            exp == 0 -> 1L
            exp == 1 -> base
            exp % 2 == 0 -> {
                val half = fastPow(base, exp / 2)
                half * half
            }
            else -> base * fastPow(base, exp - 1)
        }
    }

    /**
     * Optimized primality test (6k±1 pattern)
     */
    private fun isPrime(n: Long): Boolean {
        if (n < 2) return false
        if (n == 2L || n == 3L) return true
        if (n % 2 == 0L || n % 3 == 0L) return false
        if (n < 9) return true

        val limit = isqrt(n)

        // Start at 5, check 6k-1 and 6k+1
        var k = 5L
        while (k <= limit) {
            if (n % k == 0L || n % (k + 2) == 0L) return false
            k += 6
        }

        return true
    }

    /**
     * Integer square root
     */
    private fun isqrt(n: Long): Long = sqrt(n.toDouble()).toLong()

    /**
     * Helper: replicateM (Cartesian product of n copies of a list)
     */
    private fun <T> replicateM(n: Int, list: List<T>): List<List<T>> {
        if (n == 0) return listOf(emptyList())
        if (n == 1) return list.map { listOf(it) }

        val result = mutableListOf<List<T>>()
        val firstElement = list.first()

        // Recursively build combinations
        fun recurse(remaining: Int, current: List<T>): List<List<T>> {
            if (remaining == 0) return listOf(current)

            return list.flatMap { element ->
                recurse(remaining - 1, current + element)
            }
        }

        return recurse(n, emptyList())
    }

    /**
     * Helper: Split list into two parts at index
     */
    private fun <T> List<T>.splitPair(n: Int): Pair<List<T>, List<T>> {
        return subList(0, n) to subList(n, this.size)
    }
}

/**
 * Entry point
 */
fun main() {
    PrimePartition.main(emptyArray())
}