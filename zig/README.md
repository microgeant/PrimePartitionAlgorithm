# Zig Implementation

## Overview

This is the Rust implementation of the Prime Partition Algorithm.

## Prerequisites

- Zig compiler (tested with Zig 0.11.0 or later)
- Download from: https://ziglang.org/download/

## Building and Running

#### Using Homebrew

```bash
brew install rust
```

### Compile and Run

```bash
zig build-exe prime_partition.zig
./prime_partition
```

### Run Directly (without building)

```bash
zig run prime_partition.zig
```

### Build with Optimizations

```bash
# Release with safety checks
zig build-exe prime_partition.zig -O ReleaseSafe

# Release with maximum speed
zig build-exe prime_partition.zig -O ReleaseFast

# Release with small binary size
zig build-exe prime_partition.zig -O ReleaseSmall
```

## Expected Output

```
=== ZIG VERSION ===
Hello primes: [2, 3, 5, 7, 11, 13, ...]
Total discovered: 64
Found composites: []
```

## Algorithm Parameters

- **Initial seed**: `[1, 2]`
- **Iterations**: 10
- **Max exponent**: 2


