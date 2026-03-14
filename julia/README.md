# Julia Implementation

## Overview

This is the Julia implementation of the Prime Partition Algorithm

## Prerequisites

- **Julia** 1.6+ (LTS) or 1.9+ (stable)
- No external packages required - uses only Julia Base

### Installation (macOS)

#### Using Official Installer (Recommended)

```bash
# Download from julia lang.org
# Visit: https://julialang.org/downloads/

# Or using Homebrew
brew install julia
```

#### Verify Installation

```bash
julia --version
# Should output: julia version 1.x.x
```

## How to Run

```bash
# Make executable
chmod +x prime_partition.jl

# Run directly
./prime_partition.jl
```


## Expected Output

```
=== JULIA VERSION ===
Hello primes: [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, ...]
Total discovered: 64
Found composites: Int64[]
```

## Algorithm Parameters

- **Initial seed**: `[1, 2]`
- **Iterations**: 10
- **Max exponent**: 2

