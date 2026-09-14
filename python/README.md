# Python Implementation

## Overview

This is the Python implementation of the Prime Partition Algorithm.

## Prerequisites

- **Python 3.7+** (uses type hints)
- **No external dependencies** - uses only standard library

### Verify Installation (macOS)

```bash
python3 --version
# Should show Python 3.7 or higher
```

## How to Run

### Direct Execution

```bash
python3 prime_partition.py
```
## Expected Output

```
=== PYTHON VERSION ===
Hello primes: [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, ...]
Total discovered: 64
Found composites: []
```


## Algorithm Parameters

- **Initial seed**: `[1, 2]`
- **Iterations**: 10
- **Max exponent**: 2

> **Note:** the max exponent is fixed at 2 here for a fast demo. Raising **Iterations** well beyond 10 without also raising this bound can break the algorithm's completeness guarantees. See [`publication/`](../publication) for the corrected, complete version (with an adaptive exponent schedule) and the full paper, *"A Useless Recipe for Primes."*