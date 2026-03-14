const std = @import("std");
const ArrayList = std.ArrayList;
const Allocator = std.mem.Allocator;

/// Zig implementation of Prime Partition Algorithm

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    std.debug.print("=== ZIG VERSION ===\n", .{});

    var initial = ArrayList(u64){ .items = &.{}, .capacity = 0 };
    defer initial.deinit(allocator);
    try initial.append(allocator, 1);
    try initial.append(allocator, 2);

    var result = try runAlgorithm(allocator, 10, &initial);
    defer result.primes.deinit(allocator);
    defer result.counts.deinit();

    // Get unique sorted primes
    var unique_set = std.AutoHashMap(u64, void).init(allocator);
    defer unique_set.deinit();

    for (result.primes.items) |prime| {
        try unique_set.put(prime, {});
    }

    var sorted_primes = ArrayList(u64){ .items = &.{}, .capacity = 0 };
    defer sorted_primes.deinit(allocator);

    var iter = unique_set.keyIterator();
    while (iter.next()) |key| {
        try sorted_primes.append(allocator, key.*);
    }
    std.mem.sort(u64, sorted_primes.items, {}, comptime std.sort.asc(u64));

    std.debug.print("Hello primes: [", .{});
    for (sorted_primes.items, 0..) |prime, i| {
        if (i > 0) std.debug.print(", ", .{});
        std.debug.print("{}", .{prime});
    }
    std.debug.print("]\n", .{});
    std.debug.print("Total discovered: {}\n", .{sorted_primes.items.len});

    // Check for composites
    std.debug.print("Found composites: [", .{});
    var first = true;
    for (result.primes.items) |num| {
        if (!isPrime(num)) {
            if (!first) std.debug.print(", ", .{});
            std.debug.print("{}", .{num});
            first = false;
        }
    }
    std.debug.print("]\n", .{});
}

const AlgorithmResult = struct {
    primes: ArrayList(u64),
    counts: std.AutoHashMap(u64, u64),
};

fn runAlgorithm(allocator: Allocator, iterations: usize, initial: *const ArrayList(u64)) !AlgorithmResult {
    var current = ArrayList(u64){ .items = &.{}, .capacity = 0 };
    defer current.deinit(allocator);

    // Copy initial values
    for (initial.items) |item| {
        try current.append(allocator, item);
    }

    var acc_primes = ArrayList(u64){ .items = &.{}, .capacity = 0 };
    errdefer acc_primes.deinit(allocator);

    var acc_counts = std.AutoHashMap(u64, u64).init(allocator);
    errdefer acc_counts.deinit();

    var i: usize = 0;
    while (i < iterations) : (i += 1) {
        var found = try computePrimes(allocator, &current);
        defer found.deinit(allocator);

        // Get distinct values
        var distinct_set = std.AutoHashMap(u64, void).init(allocator);
        defer distinct_set.deinit();

        for (found.items) |prime| {
            try distinct_set.put(prime, {});
        }

        var distinct = ArrayList(u64){ .items = &.{}, .capacity = 0 };
        defer distinct.deinit(allocator);

        var iter = distinct_set.keyIterator();
        while (iter.next()) |key| {
            try distinct.append(allocator, key.*);
        }

        // Update occurrence counts
        for (distinct.items) |prime| {
            const count = acc_counts.get(prime) orelse 0;
            try acc_counts.put(prime, count + 1);
        }

        // Accumulate primes
        for (distinct.items) |prime| {
            try acc_primes.append(allocator, prime);
        }

        // Find next prime to add
        var current_set = std.AutoHashMap(u64, void).init(allocator);
        defer current_set.deinit();

        for (current.items) |item| {
            try current_set.put(item, {});
        }

        var new_primes = ArrayList(u64){ .items = &.{}, .capacity = 0 };
        defer new_primes.deinit(allocator);

        for (distinct.items) |prime| {
            if (!current_set.contains(prime)) {
                try new_primes.append(allocator, prime);
            }
        }

        if (new_primes.items.len > 0) {
            const min_new = std.mem.min(u64, new_primes.items);
            try current.append(allocator, min_new);
        }
    }

    return AlgorithmResult{
        .primes = acc_primes,
        .counts = acc_counts,
    };
}

fn computePrimes(allocator: Allocator, seeds: *const ArrayList(u64)) !ArrayList(u64) {
    const max_exponent: u64 = 2;

    if (seeds.items.len == 0) {
        return ArrayList(u64){ .items = &.{}, .capacity = 0 };
    }

    const max_prime = std.mem.max(u64, seeds.items);
    const range_start = max_prime + 1;
    const range_end = max_prime * max_prime - 1;

    var candidates = ArrayList(u64){ .items = &.{}, .capacity = 0 };
    defer candidates.deinit(allocator);

    var partitions = try binaryPartitions(allocator, seeds);
    defer {
        for (partitions.items) |*partition| {
            partition.left.deinit(allocator);
            partition.right.deinit(allocator);
        }
        partitions.deinit(allocator);
    }

    for (partitions.items) |partition| {
        var exps = try exponentCombinations(allocator, seeds.items.len, max_exponent);
        defer {
            for (exps.items) |*exp| {
                exp.deinit(allocator);
            }
            exps.deinit(allocator);
        }

        for (exps.items) |exp| {
            const left_exps = exp.items[0..partition.left.items.len];
            const right_exps = exp.items[partition.left.items.len..];

            var left_prod: u128 = 1;
            for (partition.left.items, 0..) |num, idx| {
                const pow_result = fastPow128(num, left_exps[idx]);
                left_prod *%= pow_result;
                // Only break if it exceeds u64 max to avoid actual overflow
                if (left_prod > std.math.maxInt(u64)) break;
            }

            var right_prod: u128 = 1;
            for (partition.right.items, 0..) |num, idx| {
                const pow_result = fastPow128(num, right_exps[idx]);
                right_prod *%= pow_result;
                // Only break if it exceeds u64 max to avoid actual overflow
                if (right_prod > std.math.maxInt(u64)) break;
            }

            // Skip if either product overflowed u64
            if (left_prod > std.math.maxInt(u64) or right_prod > std.math.maxInt(u64)) {
                continue;
            }

            const sum = left_prod + right_prod;
            const diff = if (left_prod > right_prod) left_prod - right_prod else right_prod - left_prod;
            
            // Only check final results against range
            if (sum >= range_start and sum <= range_end and sum <= std.math.maxInt(u64)) {
                try candidates.append(allocator, @intCast(sum));
            }
            if (diff >= range_start and diff <= range_end and diff <= std.math.maxInt(u64)) {
                try candidates.append(allocator, @intCast(diff));
            }
        }
    }

    // Filter and deduplicate
    var prime_set = std.AutoHashMap(u64, void).init(allocator);
    defer prime_set.deinit();

    for (candidates.items) |candidate| {
        if (candidate >= range_start and candidate <= range_end and isPrime(candidate)) {
            try prime_set.put(candidate, {});
        }
    }

    var primes = ArrayList(u64){ .items = &.{}, .capacity = 0 };
    var iter = prime_set.keyIterator();
    while (iter.next()) |key| {
        try primes.append(allocator, key.*);
    }

    std.mem.sort(u64, primes.items, {}, comptime std.sort.asc(u64));

    return primes;
}

const Partition = struct {
    left: ArrayList(u64),
    right: ArrayList(u64),
};

fn binaryPartitions(allocator: Allocator, list: *const ArrayList(u64)) !ArrayList(Partition) {
    var result = ArrayList(Partition){ .items = &.{}, .capacity = 0 };

    if (list.items.len < 2) {
        return result;
    }

    const n = list.items.len;
    const half = n / 2;

    // Generate all combinations using bit patterns
    var i: usize = 1;
    const max_val = (@as(usize, 1) << @intCast(n)) - 1;
    while (i <= max_val) : (i += 1) {
        var left_count: usize = 0;
        var j: usize = 0;
        while (j < n) : (j += 1) {
            if ((i & (@as(usize, 1) << @intCast(j))) != 0) {
                left_count += 1;
            }
        }

        // Only consider partitions where left size is 1 to half
        if (left_count >= 1 and left_count <= half) {
            var left = ArrayList(u64){ .items = &.{}, .capacity = 0 };
            var right = ArrayList(u64){ .items = &.{}, .capacity = 0 };

            j = 0;
            while (j < n) : (j += 1) {
                if ((i & (@as(usize, 1) << @intCast(j))) != 0) {
                    try left.append(allocator, list.items[j]);
                } else {
                    try right.append(allocator, list.items[j]);
                }
            }

            if (right.items.len > 0) {
                try result.append(allocator, Partition{ .left = left, .right = right });
            } else {
                left.deinit(allocator);
                right.deinit(allocator);
            }
        }
    }

    return result;
}

fn exponentCombinations(allocator: Allocator, size: usize, max_exp: u64) !ArrayList(ArrayList(u64)) {
    var result = ArrayList(ArrayList(u64)){ .items = &.{}, .capacity = 0 };

    if (size == 0) {
        return result;
    }

    // Calculate total number of combinations
    var total: usize = 1;
    var i: usize = 0;
    while (i < size) : (i += 1) {
        total *= max_exp;
    }

    // Generate all combinations
    var combo_idx: usize = 0;
    while (combo_idx < total) : (combo_idx += 1) {
        var exps = ArrayList(u64){ .items = &.{}, .capacity = 0 };
        var temp = combo_idx;
        i = 0;
        while (i < size) : (i += 1) {
            const exp = @as(u64, @intCast((temp % max_exp) + 1));
            try exps.append(allocator, exp);
            temp /= max_exp;
        }
        try result.append(allocator, exps);
    }

    return result;
}

fn fastPow128(base: u64, exp: u64) u128 {
    if (exp == 0) return 1;
    if (exp == 1) return base;
    if (exp % 2 == 0) {
        const half = fastPow128(base, exp / 2);
        return half *% half;
    } else {
        return @as(u128, base) *% fastPow128(base, exp - 1);
    }
}

fn fastPow(base: u64, exp: u64) u64 {
    if (exp == 0) return 1;
    if (exp == 1) return base;
    if (exp % 2 == 0) {
        const half = fastPow(base, exp / 2);
        return half * half;
    } else {
        return base * fastPow(base, exp - 1);
    }
}

fn isPrime(n: u64) bool {
    if (n <= 1) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;

    const sqrt_n = @as(u64, @intFromFloat(@sqrt(@as(f64, @floatFromInt(n)))));
    var i: u64 = 3;
    while (i <= sqrt_n) : (i += 2) {
        if (n % i == 0) return false;
    }

    return true;
}
