# Jai Implementation

## Overview

This is the Jai implementation of the Prime Partition Algorithm.

## Prerequisites

- The Jai compiler (in closed beta; see https://github.com/Jai-Community/Jai-Community-Library/wiki)

## Building and Running

```bash
jai prime_partition.jai
./prime_partition
```

## Expected Output

```
=== JAI VERSION ===
Hello primes: [2, 3, 5, 7, 11, 13, ...]
Total discovered: 64
Occurrence counts:
  ...
Found composites: []
```

## Algorithm Parameters

- **Initial seed**: `[1, 2]`
- **Iterations**: 10
- **Max exponent**: 2

> **Note:** the max exponent is fixed at 2 here for a fast demo. Raising **Iterations** well beyond 10 without also raising this bound can break the algorithm's completeness guarantees. See [`publication/`](../publication) for the complete version (with an adaptive exponent schedule) and the full paper, *"A Useless Recipe for Primes."*
