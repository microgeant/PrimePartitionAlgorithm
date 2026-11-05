import java.math.BigInteger
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.atomic.AtomicLong
import kotlin.concurrent.thread
import kotlin.math.abs
import kotlin.math.exp
import kotlin.math.ln

/*
 * Exponent sweep at a stalled iteration of the paper's algorithm (../PrimeSynthesis.kt).
 *
 * The seed set is held fixed at an iteration where the search finds nothing (default: iteration
 * 14, seeds 1..43, window (43, 1849], where exponents capped at 5 land no hit), and the maximum
 * exponent E is raised: E = from, from + 1, ..., to. For each E every exponent vector is searched
 * exactly, as in the paper: each seed on one side with exponent 1..E, candidates |pi_A - pi_B| in
 * (m, m^2]. (Sums cannot land: 2 * sqrt(prod(seeds)) > m^2.) No primality test.
 *
 * Search: x = log(pi_A) - log(pi_B) and S = log(pi_A * pi_B) are sums over the seeds. A difference
 * lands only if |x| <= m^2 / min(pi_A, pi_B) ~ m^2 * exp(-(S - |x|) / 2), so the tolerance shrinks
 * with the size of the products. The seeds are split into four quarters; the halves Q1+Q2 and
 * Q3+Q4 are streamed in sorted order of x with a heap (Schroeppel-Shamir), so memory is about
 * (2E)^(n/4) instead of (2E)^(n/2), and pairs with nearly cancelling x are checked against their
 * own tolerance, then exactly with BigInteger.
 *
 * Usage: kotlinc StallExponentSweep.kt -include-runtime -d sweep.jar
 *        java -jar sweep.jar [from_E] [to_E] [threads] [seeds, comma-separated]
 */

private class Quarter(val primes: List<Long>, val maxExp: Int, val fixFirstSide: Boolean) {
    /** Digit d < E: side A with e = d + 1; otherwise side B with e = d - E + 1. */
    fun radix(i: Int) = if (fixFirstSide && i == 0) maxExp else 2 * maxExp

    val size = primes.indices.fold(1) { acc, i -> acc * radix(i) }
    val x = DoubleArray(size)
    val s = DoubleArray(size)

    init {
        for (idx in 0 until size) {
            var r = idx
            var xv = 0.0
            var sv = 0.0
            for (i in primes.indices.reversed()) {
                val d = r % radix(i)
                r /= radix(i)
                val lp = ln(primes[i].toDouble())
                if (d < maxExp) { xv += (d + 1) * lp; sv += (d + 1) * lp } else { xv -= (d - maxExp + 1) * lp; sv += (d - maxExp + 1) * lp }
            }
            x[idx] = xv
            s[idx] = sv
        }
    }

    fun decode(index: Int): Pair<BigInteger, BigInteger> {
        var idx = index
        var a = BigInteger.ONE
        var b = BigInteger.ONE
        for (i in primes.indices.reversed()) {
            val d = idx % radix(i)
            idx /= radix(i)
            val p = BigInteger.valueOf(primes[i])
            if (d < maxExp) a = a.multiply(p.pow(d + 1)) else b = b.multiply(p.pow(d - maxExp + 1))
        }
        return a to b
    }
}

/** Indices of [keys] in ascending key order. */
private fun argsort(keys: DoubleArray): IntArray =
    keys.indices.sortedBy { keys[it] }.toIntArray()

/**
 * Ascending stream of sign * (qa.x[i] + qb.x[j]) over i in [aIdx] and all j (heap over i).
 * After next(): value, s (sum of S), i, j (quarter indices).
 */
private class SumStream(val qa: Quarter, aIdx: IntArray, val qb: Quarter, val sign: Double) {
    private val bOrder = argsort(DoubleArray(qb.size) { sign * qb.x[it] })
    private val bKey = DoubleArray(qb.size) { sign * qb.x[bOrder[it]] }
    private var n = aIdx.size
    private val hv = DoubleArray(n)
    private val ha = IntArray(n)
    private val hb = IntArray(n) // position in bOrder

    var value = 0.0; var s = 0.0; var i = 0; var j = 0

    init {
        for ((k, a) in aIdx.withIndex()) { hv[k] = sign * qa.x[a] + bKey[0]; ha[k] = a; hb[k] = 0 }
        for (k in n / 2 - 1 downTo 0) siftDown(k)
    }

    fun hasNext() = n > 0
    fun peek() = hv[0]

    fun next() {
        value = hv[0]; i = ha[0]; j = bOrder[hb[0]]
        s = qa.s[i] + qb.s[j]
        val pos = hb[0] + 1
        if (pos < qb.size) { hb[0] = pos; hv[0] = sign * qa.x[ha[0]] + bKey[pos] }
        else { n--; hv[0] = hv[n]; ha[0] = ha[n]; hb[0] = hb[n] }
        if (n > 0) siftDown(0)
    }

    private fun siftDown(k0: Int) {
        var k = k0
        val v = hv[k]; val a = ha[k]; val b = hb[k]
        while (true) {
            var c = 2 * k + 1
            if (c >= n) break
            if (c + 1 < n && hv[c + 1] < hv[c]) c++
            if (hv[c] >= v) break
            hv[k] = hv[c]; ha[k] = ha[c]; hb[k] = hb[c]
            k = c
        }
        hv[k] = v; ha[k] = a; hb[k] = b
    }
}

internal class Result(val found: Map<BigInteger, String>, val pairs: Long, val exact: Long)

/** "2^3 * 5 * ..." for a product of the seeds (report only). */
internal fun factorString(n: BigInteger, primes: List<Long>): String {
    var r = n
    val parts = mutableListOf<String>()
    for (p in primes) {
        val bp = BigInteger.valueOf(p)
        var e = 0
        while (r.mod(bp).signum() == 0) { r = r.divide(bp); e++ }
        if (e > 0) parts.add(if (e == 1) "$p" else "$p^$e")
    }
    return parts.joinToString("*").ifEmpty { "1" }
}

/** Differences in (lo, hi]; default window (m, m^2]. Also used by LeafRunsSynthesis.kt. */
internal fun sweep(
    primes: List<Long>, maxExp: Int, threads: Int,
    lo: BigInteger = BigInteger.valueOf(primes.max()), hi: BigInteger = lo.multiply(lo),
): Result {
    val prod = primes.fold(BigInteger.ONE) { acc, p -> acc.multiply(BigInteger.valueOf(p)) }
    require(prod.shiftLeft(2) > hi.multiply(hi)) { "sums can still land; use FulcrumTargetingMitm.kt" }
    val bMin = prod.add(hi.multiply(hi).shiftRight(2)).sqrt().subtract(hi.shiftRight(1)).subtract(BigInteger.ONE)
    val hiD = hi.toDouble()
    val tol = hiD / bMin.toDouble() * (1 + 1e-9) + 1e-12 // global bound: min(pi_A, pi_B) >= bMin

    val n = primes.size
    val c1 = (n + 3) / 4
    val c2 = (n + 1) / 2
    val c3 = (3 * n + 3) / 4
    val q1 = Quarter(primes.subList(0, c1), maxExp, fixFirstSide = true) // a global side swap gives the same |a - b|
    val q2 = Quarter(primes.subList(c1, c2), maxExp, false)
    val q3 = Quarter(primes.subList(c2, c3), maxExp, false)
    val q4 = Quarter(primes.subList(c3, n), maxExp, false)

    val found = ConcurrentHashMap<BigInteger, String>()
    val pairs = AtomicLong()
    val exact = AtomicLong()
    val failure = java.util.concurrent.atomic.AtomicReference<Throwable>()
    val workers = (0 until threads).map { t ->
        thread {
          try {
            val h1 = SumStream(q1, (t until q1.size step threads).toList().toIntArray(), q2, 1.0)  // x1 ascending
            val h2 = SumStream(q3, IntArray(q3.size) { it }, q4, -1.0)                             // -x2 ascending
            // Sliding window of h2 items with -x2 within tol of x1.
            var cap = 1024
            var wv = DoubleArray(cap); var ws = DoubleArray(cap); var wi = IntArray(cap); var wj = IntArray(cap)
            var head = 0; var tail = 0
            var myPairs = 0L; var myExact = 0L
            while (h1.hasNext()) {
                h1.next()
                val x1 = h1.value
                while (h2.hasNext() && h2.peek() <= x1 + tol) {
                    h2.next()
                    if (h2.value < x1 - tol) continue // x1 only grows: never needed
                    if (tail == cap) { // compact or grow
                        val len = tail - head
                        if (len * 2 > cap) cap *= 2
                        wv = wv.copyInto(DoubleArray(cap), 0, head, tail); ws = ws.copyInto(DoubleArray(cap), 0, head, tail)
                        wi = wi.copyInto(IntArray(cap), 0, head, tail); wj = wj.copyInto(IntArray(cap), 0, head, tail)
                        head = 0; tail = len
                    }
                    wv[tail] = h2.value; ws[tail] = h2.s; wi[tail] = h2.i; wj[tail] = h2.j; tail++
                }
                while (head < tail && wv[head] < x1 - tol) head++
                for (k in head until tail) {
                    myPairs++
                    val ax = abs(x1 - wv[k])
                    val sTot = h1.s + ws[k]
                    // |a - b| <= hi needs |x| <= hi / min(a, b) = hi * exp(-(S - |x|) / 2); slack covers rounding.
                    if (ax > hiD * exp(-(sTot - ax) / 2) * (1 + 1e-6) + 1e-9) continue
                    myExact++
                    val (a1, b1) = q1.decode(h1.i)
                    val (a2, b2) = q2.decode(h1.j)
                    val (a3, b3) = q3.decode(wi[k])
                    val (a4, b4) = q4.decode(wj[k])
                    val a = a1.multiply(a2).multiply(a3).multiply(a4)
                    val b = b1.multiply(b2).multiply(b3).multiply(b4)
                    val d = a.subtract(b).abs()
                    if (d > lo && d <= hi) found.putIfAbsent(d, "${factorString(a.max(b), primes)} - ${factorString(a.min(b), primes)}")
                }
            }
            pairs.addAndGet(myPairs)
            exact.addAndGet(myExact)
          } catch (e: Throwable) { failure.compareAndSet(null, e) }
        }
    }
    workers.forEach { it.join() }
    failure.get()?.let { throw IllegalStateException("worker failed at E=$maxExp", it) }
    return Result(found, pairs.get(), exact.get())
}

fun main(args: Array<String>) {
    val from = args.getOrNull(0)?.toInt() ?: 5
    val to = args.getOrNull(1)?.toInt() ?: 8
    val threads = args.getOrNull(2)?.toInt() ?: Runtime.getRuntime().availableProcessors()
    // Default: the seeds of iteration 14 (gap-free, so the same for any exponent cap); 1 is omitted (1^e = 1).
    val primes = args.getOrNull(3)?.split(",")?.map { it.trim().toLong() }
        ?: listOf(2L, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)
    println("seeds=1, ${primes.joinToString(", ")} window=(${primes.max()}, ${primes.max() * primes.max()}] threads=$threads")
    for (e in from..to) {
        val t = System.nanoTime()
        val r = sweep(primes, e, threads)
        val dt = (System.nanoTime() - t) / 1e9
        println("E=$e time=${"%.1f".format(dt)}s pairs=${r.pairs} exact_checks=${r.exact} found=${r.found.size}: ${r.found.keys.sorted()}")
        for (v in r.found.keys.sorted()) println("  $v = ${r.found[v]}")
        System.out.flush()
    }
}
