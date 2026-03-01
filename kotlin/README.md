# Kotlin Implementation

## Overview

This is the Kotlin implementation of the Prime Partition Algorithm. It uses binary partitions and powered products to discover primes constructively.

## Prerequisites

- **Kotlin compiler** (kotlinc)
- **Java Runtime Environment** (JRE) 11 or higher

### Installation (macOS)

```bash
# Using Homebrew
brew install kotlin
```

## How to Run

### Compile and Run
```bash
# Compile to bytecode
kotlinc PrimePartition.kt -d .

# Run the compiled class
kotlin PrimePartitionKt
```

## Expected Output

```
=== KOTLIN VERSION ===
Hello primes: [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, ...]
Total discovered: 64
Occurrence counts: {3=2, 5=3, 7=4, ...}
Found composites: []
```


## Algorithm Parameters

- **Initial seed**: `[1, 2]`
- **Iterations**: 10
- **Max exponent**: 2

