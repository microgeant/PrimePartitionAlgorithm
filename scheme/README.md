# Racket (Scheme) Implementation

## Overview

This is the Racket (Scheme) implementation of the Prime Partition Algorithm.

## Prerequisites

- **Racket** (recommended Scheme implementation)

### Installation (macOS)

```bash
# Using Homebrew
brew install racket
```

## How to Run

### With Racket (Recommended)

```bash
racket prime-partition.scm
```

### Compile for Better Performance

```bash
# Compile to bytecode
raco make prime-partition.scm

# Run compiled version
racket prime-partition.scm
```

### Create Standalone Executable

```bash
raco exe prime-partition.scm
./prime-partition
```

## Expected Output

```
=== RACKET VERSION ===
Hello primes: (3 5 7 11 13 17 19 23 29 31 ...)
Total discovered: 64
Found composites: ()
```
## Algorithm Parameters

- **Initial seed**: `[1, 2]`
- **Iterations**: 10
- **Max exponent**: 2

> **Note:** the max exponent is fixed at 2 here for a fast demo. Raising **Iterations** well beyond 10 without also raising this bound can break the algorithm's completeness guarantees. See [`publication/`](../publication) for the corrected, complete version (with an adaptive exponent schedule) and the full paper, *"A Useless Recipe for Primes."*