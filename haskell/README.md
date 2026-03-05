# Haskell Implementation

## Overview

This is the Haskell implementation of the Prime Partition Algorithm.

## Prerequisites

- **GHC** (Glasgow Haskell Compiler)
- **Cabal** (build tool) - optional but recommended

### Installation (macOS)

#### Using GHCup (Recommended)

```bash
# Install GHCup
curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh

# Restart terminal, then verify
ghc --version
```

#### Using Homebrew

```bash
brew install ghc cabal-install
```

## How to Run

### Option 1: Direct Compilation

```bash
# Compile with optimizations
ghc -O2 PrimePartition.hs -o PrimePartition

# Run
./PrimePartition
```

### Option 2: Using runhaskell (Interpreter)

```bash
runhaskell PrimePartition.hs
```

### Option 3: Using GHCi (Interactive REPL)

```bash
ghci PrimePartition.hs
# In REPL:
*Main> main
# Exit:
*Main> :q
```

## Expected Output

```
=== HASKELL VERSION ===
Hello primes: [3,5,7,11,13,17,19,23,29,31, ...]
Total discovered: 64
Occurrence counts: [(3,1),(5,1),(7,2),(11,2),(13,3),(17,4), ...]
Found composites: []
```
## Algorithm Parameters

- **Initial seed**: `[1, 2]`
- **Iterations**: 10
- **Max exponent**: 2