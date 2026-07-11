import java.math.BigInteger
import kotlin.collections.indices
import kotlin.sequences.toList

/**
 * Generates all unique binary partitions of a set.
 */
private fun <T> binaryPartitions(list: List<T>): Sequence<Pair<List<T>, List<T>>> =
    kotlin.sequences.sequence {
        if (list.size < 2) return@sequence
        val first = list[0]
        val rest = list.subList(1, list.size)
        val numPartitions = 1L shl rest.size

        for (i in 1 until numPartitions) {
            val left = mutableListOf<T>()
            val right = mutableListOf<T>(first)
            for (j in rest.indices) {
                if ((i shr j) and 1L == 1L) left.add(rest[j]) else right.add(rest[j])
            }
            yield(left to right)
        }
    }

/**
 * Generate all exponent combinations (odometer approach)
 */
private fun exponentCombinations(n: Int, maxExp: Int): Sequence<List<Int>> =
    kotlin.sequences.sequence {
        if (n == 0) return@sequence
        val indices = IntArray(n) { 1 }
        while (true) {
            yield(indices.toList())
            var i = n - 1
            while (i >= 0 && indices[i] == maxExp) {
                indices[i] = 1
                i--
            }
            if (i < 0) break
            indices[i]++
        }
    }

/**
 * Synthesizes primes using arbitrary-precision arithmetic to prevent overflow.
 */
private fun computePrimes(seeds: List<BigInteger>, maxExp: Int): Sequence<BigInteger> {
    if (seeds.isEmpty()) return kotlin.sequences.emptySequence()
    val maxP = seeds.maxOrNull() ?: return kotlin.sequences.emptySequence()
    val minR = maxP.add(BigInteger.ONE)
    val maxR = maxP.multiply(maxP)

    return sequence {
        for ((left, right) in binaryPartitions(seeds)) {
            val totalSize = left.size + right.size
            for (expVector in exponentCombinations(totalSize, maxExp)) {
                val leftExps = expVector.take(left.size)
                val rightExps = expVector.takeLast(right.size)

                val leftProd = left.zip(leftExps).map { (p, e) -> p.pow(e) }
                    .reduce { acc, b -> acc.multiply(b) }
                val rightProd = right.zip(rightExps).map { (p, e) -> p.pow(e) }
                    .reduce { acc, b -> acc.multiply(b) }

                val sumSigma = leftProd.add(rightProd)
                if (sumSigma >= minR && sumSigma <= maxR) yield(sumSigma)

                val diffSigma = leftProd.subtract(rightProd).abs()
                if (diffSigma >= minR && diffSigma <= maxR) yield(diffSigma)
            }
        }
    }
}

fun main() {
    var currentMaxExp = 1
    val maxIterations = 5
    var current = listOf(BigInteger.ONE, BigInteger.valueOf(2))
    var accPrimes = emptyList<BigInteger>()

    for (i in 1..maxIterations) {
        val found = computePrimes(current, currentMaxExp++).toList()
        val distinctFound = found.sorted().distinct()

        val currentSet = current.toSet()
        val diff = distinctFound.filter { it !in currentSet }
        val next = if (diff.isEmpty()) current else current + diff.min()

        accPrimes = accPrimes + distinctFound
        current = next
    }
    println("Discovered primes: ${(listOf(BigInteger.valueOf(2)) + accPrimes).distinct().sorted()}")
}