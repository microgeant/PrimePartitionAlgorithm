import java.math.BigInteger
import kotlin.math.ln

/*
 * Meet-in-the-middle fulcrum targeting, faithful to the paper (../PrimeSynthesis.kt).
 *
 * Same algorithm: seeds start at {1, 2}; every seed sits on exactly one side of a binary
 * partition with an exponent 1..E; candidates are pi_A + pi_B and |pi_A - pi_B| inside
 * (m, m^2]; the smallest pending value joins the seeds each iteration. No primality test:
 * every seed divides exactly one side, so no candidate has a prime factor <= m (Euclid).
 *
 * Only the search is faster. A fulcrum pi_A with reach pi_B lands a difference in the
 * window only when the two products are nearly equal:
 * - pi_A * pi_B >= prod(seeds), so pi_A + pi_B >= 2 * sqrt(prod(seeds)) (AM-GM). Once that
 *   exceeds m^2 no sum can land, and only differences remain.
 * - log(pi_A) - log(pi_B) = sum over seeds of (+/-) e_i * log(p_i) splits over the SEEDS,
 *   so each half of the seeds is enumerated separately ((2E)^(n/2) states), one half is
 *   sorted, and states whose log-ratios nearly cancel are matched by binary search.
 * - If m < |a - b| <= m^2 with b = min(a, b), then |log(a / b)| <= m^2 / b, and
 *   b * (b + m^2) >= a * b >= prod(seeds) bounds b from below, giving the tolerance.
 * Logs only narrow the search; every match is checked exactly with BigInteger.
 *
 * Usage: kotlinc FulcrumTargetingMitm.kt -include-runtime -d fulcrum.jar
 *        java -jar fulcrum.jar [iterations] [max_exp_cap]
 */

private class Half(val primes: List<Long>, val maxExp: Int, val fixFirstSide: Boolean) {
    /** Number of (side, exponent) choices for prime i; digit d < E means side A with e = d + 1. */
    fun radix(i: Int) = if (fixFirstSide && i == 0) maxExp else 2 * maxExp

    /** Signed log-ratio of every assignment, flat, in mixed radix (last prime varies fastest). */
    fun logRatios(): DoubleArray {
        var r = DoubleArray(1)
        for ((i, p) in primes.withIndex()) {
            val lp = ln(p.toDouble())
            val choices = DoubleArray(radix(i)) { d -> if (d < maxExp) (d + 1) * lp else -(d - maxExp + 1) * lp }
            val next = DoubleArray(r.size * choices.size)
            var k = 0
            for (x in r) for (c in choices) next[k++] = x + c
            r = next
        }
        return r
    }

    /** Exact products (pi_A, pi_B) for a flat state index. */
    fun decode(index: Long): Pair<BigInteger, BigInteger> {
        var idx = index
        var a = BigInteger.ONE
        var b = BigInteger.ONE
        for (i in primes.indices.reversed()) {
            val d = (idx % radix(i)).toInt()
            idx /= radix(i)
            val p = BigInteger.valueOf(primes[i])
            if (d < maxExp) a = a.multiply(p.pow(d + 1)) else b = b.multiply(p.pow(d - maxExp + 1))
        }
        return a to b
    }
}

/** Sort [keys] ascending, applying the same permutation to [idx] (quicksort, no boxing). */
private fun sortByKey(keys: DoubleArray, idx: IntArray) {
    fun swap(i: Int, j: Int) {
        val k = keys[i]; keys[i] = keys[j]; keys[j] = k
        val v = idx[i]; idx[i] = idx[j]; idx[j] = v
    }
    fun sort(lo0: Int, hi0: Int) {
        var lo = lo0
        var hi = hi0
        while (hi - lo > 16) {
            val mid = (lo + hi) ushr 1
            if (keys[mid] < keys[lo]) swap(mid, lo)
            if (keys[hi] < keys[lo]) swap(hi, lo)
            if (keys[hi] < keys[mid]) swap(hi, mid)
            val pivot = keys[mid]
            var i = lo
            var j = hi
            while (i <= j) {
                while (keys[i] < pivot) i++
                while (keys[j] > pivot) j--
                if (i <= j) { swap(i, j); i++; j-- }
            }
            if (j - lo < hi - i) { sort(lo, j); lo = i } else { sort(i, hi); hi = j } // recurse on the smaller side
        }
        for (a in lo + 1..hi) {
            val k = keys[a]
            val v = idx[a]
            var b = a - 1
            while (b >= lo && keys[b] > k) { keys[b + 1] = keys[b]; idx[b + 1] = idx[b]; b-- }
            keys[b + 1] = k
            idx[b + 1] = v
        }
    }
    sort(0, keys.size - 1)
}

/** First index with arr[i] >= v. */
private fun lowerBound(arr: DoubleArray, v: Double): Int {
    var lo = 0
    var hi = arr.size
    while (lo < hi) { val mid = (lo + hi) ushr 1; if (arr[mid] < v) lo = mid + 1 else hi = mid }
    return lo
}

/** Plain enumeration over (side, exponent) per prime; used only while sums can still land. */
private fun bruteForce(primes: List<Long>, maxExp: Int, lo: BigInteger, hi: BigInteger): Set<BigInteger> {
    val half = Half(primes, maxExp, fixFirstSide = false)
    val total = (0 until primes.size).fold(1L) { acc, i -> acc * half.radix(i) }
    val found = HashSet<BigInteger>()
    for (s in 0 until total) {
        val (a, b) = half.decode(s)
        for (v in listOf(a.add(b), a.subtract(b).abs())) if (v > lo && v <= hi) found.add(v)
    }
    return found
}

/** Window candidates pi_A +/- pi_B in (m, m^2] for one iteration; same set as the brute force. */
private fun partitionTargets(seeds: List<Long>, maxExp: Int): Set<BigInteger> {
    val m = BigInteger.valueOf(seeds.max())
    val lo = m
    val hi = m.multiply(m)
    val primes = seeds.filter { it != 1L } // 1^e = 1 on either side; it only keeps both sides non-empty
    if (primes.isEmpty()) return emptySet()
    val prod = primes.fold(BigInteger.ONE) { acc, p -> acc.multiply(BigInteger.valueOf(p)) }
    if (prod.shiftLeft(2) <= hi.multiply(hi)) return bruteForce(primes, maxExp, lo, hi)

    val halfHi = hi.shiftRight(1)
    val bMin = prod.add(hi.multiply(hi).shiftRight(2)).sqrt().subtract(halfHi).subtract(BigInteger.ONE).max(BigInteger.ONE)
    val tol = hi.toDouble() / bMin.toDouble() * (1 + 1e-9) + 1e-12

    // h2 (the smaller half) is materialized and sorted; h1 is streamed as prefix x suffix.
    val k = primes.size - primes.size / 2
    val h1 = primes.subList(0, k)
    val h2 = Half(primes.subList(k, primes.size), maxExp, fixFirstSide = false)
    val r2 = h2.logRatios()
    val order = IntArray(r2.size) { it }
    sortByKey(r2, order)

    val j1 = maxOf(h1.size / 2, 1)
    val h1Full = Half(h1, maxExp, fixFirstSide = true) // a global side swap gives the same |a - b|
    val ra = Half(h1.subList(0, j1), maxExp, fixFirstSide = true).logRatios()
    val rb = Half(h1.subList(j1, h1.size), maxExp, fixFirstSide = false).logRatios()

    val found = HashSet<BigInteger>()
    for (ia in ra.indices) {
        val xa = ra[ia]
        for (ib in rb.indices) {
            val x = xa + rb[ib]
            var j = lowerBound(r2, -x - tol)
            if (j == r2.size || r2[j] > -x + tol) continue
            val (a1, b1) = h1Full.decode(ia.toLong() * rb.size + ib)
            while (j < r2.size && r2[j] <= -x + tol) {
                val (a2, b2) = h2.decode(order[j].toLong())
                val d = a1.multiply(a2).subtract(b1.multiply(b2)).abs()
                if (d > lo && d <= hi) found.add(d)
                j++
            }
        }
    }
    return found
}

fun main(args: Array<String>) {
    val maxIterations = args.getOrNull(0)?.toInt() ?: 7
    val cap = args.getOrNull(1)?.toInt()
    var maxExp = 1
    var current = listOf(1L, 2L)
    val pending = sortedSetOf<BigInteger>() // discovered-but-not-yet-seeded values, accumulated across iterations
    val acc = sortedSetOf(BigInteger.valueOf(2))
    val t0 = System.nanoTime()

    for (i in 1..maxIterations) {
        val exp = if (cap == null) maxExp else minOf(maxExp, cap)
        val t = System.nanoTime()
        val found = partitionTargets(current, exp).sorted()
        val dt = (System.nanoTime() - t) / 1e9
        println("iter $i: seeds=$current max_exp=$exp time=${"%.3f".format(dt)}s found=${found.size}: $found")

        val currentSet = current.map { BigInteger.valueOf(it) }.toSet()
        pending.addAll(found.filter { it !in currentSet })
        if (pending.isNotEmpty()) {
            val nextSeed = pending.first()
            pending.remove(nextSeed)
            current = current + nextSeed.longValueExact()
        }
        acc.addAll(found)
        maxExp++
    }
    println("Total time: ${"%.2f".format((System.nanoTime() - t0) / 1e9)}s")
    println("Discovered primes (${acc.size}): $acc")
}
