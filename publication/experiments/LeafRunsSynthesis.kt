import java.math.BigInteger
import java.util.TreeSet
import kotlin.math.pow

/*
 * The paper's algorithm (../PrimeSynthesis.kt) with "leaf runs", after the leaf searches in
 * https://github.com/EtherBit/On-Immeasurable-Magnitudes/blob/master/prime_number_algorithm_2.kt.
 *
 * Iteration k (seeds S, largest m, E = min(k, cap)): the main search on S, as in the paper, plus one
 * leaf search on S + {v} for each leaf value v. Leaf values: every value first found in iteration
 * k - 1 that is not a seed ("new", default), every pending value ("pending"), or none ("none", the
 * paper's algorithm). Every search uses the window (m, m^2] of S, so a leaf adds a seed, not window.
 * Leaf hits join the found values like main hits; the smallest pending value becomes the next seed.
 *
 * Correctness: as in the paper, every seed sits on one side, so no seed divides a candidate, and a
 * leaf value v is itself a value found earlier. A composite in (m, m^2] coprime to S has a prime
 * factor below m outside S, so the window is cut to g^2 - 1 if the seeds ever skip a value g
 * (g: the smallest non-seed n >= 2 coprime to the seeds; one gcd per n, no candidate is divided).
 * Primality (BigInteger.isProbablePrime) is used only in the report.
 *
 * Usage: kotlinc StallExponentSweep.kt LeafRunsSynthesis.kt -include-runtime -d leaf.jar
 *        java -cp leaf.jar LeafRunsSynthesisKt [iterations] [cap] [new|pending|none] [threads] > report.md
 */

/** Sums and differences in (lo, hi], every exponent vector enumerated (small seed sets only). */
private fun brute(primes: List<Long>, maxExp: Int, lo: BigInteger, hi: BigInteger): Map<BigInteger, String> {
    val found = HashMap<BigInteger, String>()
    val pows = primes.map { p -> List(maxExp + 1) { BigInteger.valueOf(p).pow(it) } }
    fun rec(i: Int, a: BigInteger, b: BigInteger) {
        if (i == primes.size) {
            for ((v, op) in listOf(a.add(b) to " + ", a.subtract(b).abs() to " - "))
                if (v > lo && v <= hi) found.putIfAbsent(v, "${factorString(a.max(b), primes)}$op${factorString(a.min(b), primes)}")
            return
        }
        for (e in 1..maxExp) {
            rec(i + 1, a.multiply(pows[i][e]), b)
            if (i > 0) rec(i + 1, a, b.multiply(pows[i][e])) // a side swap gives the same values
        }
    }
    rec(0, BigInteger.ONE, BigInteger.ONE)
    return found
}

private fun search(primes: List<Long>, maxExp: Int, lo: BigInteger, hi: BigInteger, threads: Int): Map<BigInteger, String> {
    val prod = primes.fold(BigInteger.ONE) { acc, p -> acc.multiply(BigInteger.valueOf(p)) }
    if (primes.size >= 4 && prod.shiftLeft(2) > hi.multiply(hi)) return sweep(primes, maxExp, threads, lo, hi).found
    val vectors = maxExp * (2.0 * maxExp).pow(primes.size - 1)
    require(vectors <= 5e7) { "sums can still land and $vectors vectors are too many to enumerate" }
    return brute(primes, maxExp, lo, hi)
}

fun main(args: Array<String>) {
    val iterations = args.getOrNull(0)?.toInt() ?: 15
    val cap = args.getOrNull(1)?.toInt() ?: 5
    val mode = args.getOrNull(2) ?: "new"
    val threads = args.getOrNull(3)?.toInt() ?: Runtime.getRuntime().availableProcessors()
    require(mode in listOf("new", "pending", "none"))

    val seeds = mutableListOf(2L) // and 1 (1^e = 1: a side holding only 1 has product 1)
    val acc = TreeSet<BigInteger>(listOf(BigInteger.TWO))
    val pending = TreeSet<BigInteger>()
    var lastNew = emptySet<BigInteger>()
    val leafOnly = sortedMapOf<BigInteger, String>() // first found by a leaf search: "v = ...; witness"
    val rows = mutableListOf<String>()
    val t0 = System.nanoTime()

    for (k in 1..iterations) {
        val e = minOf(k, cap)
        val m = seeds.max()
        val prod = seeds.fold(BigInteger.ONE) { a, p -> a.multiply(BigInteger.valueOf(p)) }
        var g = 2L
        while (g in seeds || prod.gcd(BigInteger.valueOf(g)) != BigInteger.ONE) g++
        val lo = BigInteger.valueOf(m)
        val hi = minOf(lo.multiply(lo), BigInteger.valueOf(g * g - 1))

        val t = System.nanoTime()
        val main = search(seeds, e, lo, hi, threads)
        val leaves = when (mode) {
            "new" -> lastNew.map { it.toLong() }.filter { it !in seeds }.sorted()
            "pending" -> pending.map { it.toLong() }
            else -> emptyList()
        }
        val leafHits = HashMap<BigInteger, String>()
        for (v in leaves) {
            for ((d, w) in search(seeds + v, e, lo, hi, threads))
                if (d !in main) leafHits.putIfAbsent(d, "v = $v; $d = $w")
        }
        val all = main.keys + leafHits.keys
        val new = all.filter { it !in acc }.toSortedSet()
        val newByLeaf = new.filter { it !in main }
        for (d in newByLeaf) leafOnly[d] = "iteration $k, ${leafHits[d]}"
        acc.addAll(all)
        pending.addAll(all.filter { it.toLong() !in seeds })
        val next = pending.pollFirst()
        val dt = (System.nanoTime() - t) / 1e9
        rows.add("| $k | ${seeds.size + 1} (max $m) | $e | ($lo, $hi] | ${main.size} | ${leaves.size} | " +
            "${(leafHits.keys - main.keys).size} | ${new.size} | ${newByLeaf.size} | ${next ?: "—"} | ${"%.1f".format(dt)} |")
        System.err.println("iter $k: seeds=${seeds.size + 1} max=$m E=$e window=($lo, $hi] main=${main.size} leaves=${leaves.size} " +
            "leaf_extra=${(leafHits.keys - main.keys).size} new=${new.size} new_by_leaf=$newByLeaf next=$next time=${"%.1f".format(dt)}s")
        lastNew = new
        if (next == null) break
        seeds.add(next.toLong())
    }

    val total = (System.nanoTime() - t0) / 1e9
    val bad = acc.filter { !it.isProbablePrime(50) }
    var gap = BigInteger.TWO
    while (gap in acc) gap = gap.nextProbablePrime()
    val largest = acc.last()
    val missing = generateSequence(gap) { it.nextProbablePrime() }.takeWhile { it < largest }.filter { it !in acc }.toList()
    val o = mutableListOf(
        "# LeafRunsSynthesis.kt — $iterations iterations, exponent cap $cap, leaves: $mode\n",
        "The paper's algorithm with exponents 1..min(k, $cap) at iteration k, plus a leaf search on seeds + {v} " +
            "for each leaf value v (see the source). Every search uses the paper's window (m, m²] of the seeds.\n",
        "Total wall-clock time: **${"%.1f".format(total)}s** ($threads threads)\n",
        "Primes found: **${acc.size}** (including the seed 2); " +
            (if (bad.isEmpty()) "**all verified prime**" else "**NOT prime: ${bad.joinToString()}**") + "\n",
        "Gap-free up to **${acc.filter { it < gap }.max()}** (first missing: $gap); largest $largest; " +
            "${missing.size} primes missing below it\n",
        "Found only by leaf searches: **${leafOnly.size}**\n",
        "## Per-Iteration Summary\n",
        "| Iteration | Seeds | E | Window | Main hits | Leaves | Extra leaf hits | New | New by leaf only | Added to seeds | Time (s) |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    )
    o.addAll(rows)
    o.add("\n## Found Only by Leaf Searches\n")
    o.addAll(leafOnly.map { (d, w) -> "- $d: $w" }.ifEmpty { listOf("None.") })
    o.add("\n## Missing Primes Below the Largest Found\n")
    o.add(missing.joinToString(", ").ifEmpty { "None." })
    o.add("\n## All Primes Found\n")
    o.add(acc.joinToString(", "))
    println(o.joinToString("\n"))
}
