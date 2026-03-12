# Rust Implementation

## Overview

This is the Rust implementation of the Prime Partition Algorithm.

## Prerequisites

- **Rust** 1.70+
- **Cargo**

### Installation (macOS)

#### Using rustup (Recommended)

```bash
# Install rustup (Rust installer)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Restart terminal or source
source ~/.cargo/env

# Verify installation
rustc --version
cargo --version
```

#### Using Homebrew

```bash
brew install rust
```

## How to Run

### Option 1: Using Cargo (Recommended)

```bash
# Debug build (faster compilation)
cargo run

# Release build (optimized, much faster execution)
cargo run --release
```

### Option 2: Direct Compilation

```bash
# Debug build
rustc prime_partition.rs -o prime_partition_debug
./prime_partition_debug

# Release build with optimizations
rustc -O prime_partition.rs -o prime_partition
./prime_partition
```

## Expected Output

```
=== RUST VERSION ===
Hello primes: [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, ...]
Total discovered: 64
Found composites: []
```

## Algorithm Parameters

- **Initial seed**: `[1, 2]`
- **Iterations**: 10
- **Max exponent**: 2


