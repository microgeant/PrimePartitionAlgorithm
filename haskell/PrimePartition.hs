{-# LANGUAGE BangPatterns #-}

import Data.List (foldl')
import qualified Data.Set as Set
import qualified Data.Map.Strict as Map
import Control.Monad (replicateM)

-- Main entry point
main :: IO ()
main = do
    putStrLn "=== HASKELL VERSION ===" 
    let (primes, counts) = runAlgorithm 10 [1, 2]
    putStrLn $ "Hello primes: " ++ show (Set.toAscList $ Set.fromList primes)
    putStrLn $ "Total discovered: " ++ show (length $ Set.fromList primes)
    putStrLn $ "Occurrence counts: " ++ show (Map.toAscList counts)
    putStrLn $ "Found composites: " ++ show (filter (not . isPrimeOpt) primes)

-- Run algorithm for n iterations
runAlgorithm :: Int -> [Integer] -> ([Integer], Map.Map Integer Int)
runAlgorithm n initial = foldl' step (initial, [], Map.empty) [1..n]
                         & \(_, primes, counts) -> (primes, counts)
  where
    step (!current, !accPrimes, !accCounts) _ =
        let found = computePrimesOpt current
            distinct = Set.toList $ Set.fromList found
            !newCounts = Map.unionWith (+) accCounts $ 
                        Map.fromListWith (+) [(p, 1) | p <- found]
            difference = Set.toList $ Set.fromList distinct `Set.difference` Set.fromList current
            nextPrime = if null difference then Nothing else Just (minimum difference)
            nextCurrent = maybe current (\p -> current ++ [p]) nextPrime
        in (nextCurrent, accPrimes ++ distinct, newCounts)

-- OPTIMIZED: Use Set operations for distinct + sort in one pass
computePrimesOpt :: [Integer] -> [Integer]
computePrimesOpt seeds
    | null seeds = []
    | otherwise = 
        let maxPrime = maximum seeds
            rangeStart = maxPrime + 1
            rangeEnd = maxPrime * maxPrime - 1
        in Set.toAscList $ Set.fromList $
           [ candidate
           | (left, right) <- binaryPartitionsOptimized seeds
           , exps <- exponentCombinations (length seeds) 2
           , let (leftExps, rightExps) = splitAt (length left) exps
           , let leftProd = product $ zipWith (^) left leftExps
           , let rightProd = product $ zipWith (^) right rightExps
           , candidate <- [leftProd + rightProd, abs (leftProd - rightProd)]
           , candidate > maxPrime && candidate < maxPrime * maxPrime
           , isPrimeOpt candidate
           ]

-- OPTIMIZED: Use Set operations for partitioning
binaryPartitionsOptimized :: Ord a => [a] -> [([a], [a])]
binaryPartitionsOptimized xs
    | length xs < 2 = []
    | otherwise =
        let xsSet = Set.fromList xs
        in [ (Set.toList leftSet, Set.toList rightSet)
           | i <- [1 .. length xs `div` 2]
           , leftSet <- map Set.fromList (combinations i xs)
           , let rightSet = xsSet `Set.difference` leftSet
           , Set.size rightSet == length xs - i
           ]

-- Generate k-combinations
combinations :: Int -> [a] -> [[a]]
combinations 0 _ = [[]]
combinations _ [] = []
combinations n (x:xs) = map (x:) (combinations (n-1) xs) ++ combinations n xs

-- Generate all exponent combinations
exponentCombinations :: Int -> Int -> [[Int]]
exponentCombinations n maxE = replicateM n [1..maxE]

-- OPTIMIZED: 6k±1 wheel factorization
isPrimeOpt :: Integer -> Bool
isPrimeOpt n
    | n <= 1 = False
    | n == 2 = True
    | even n = False
    | n == 3 = True
    | n `mod` 3 == 0 = False
    | otherwise = go 5
  where
    sqrtN = isqrt n
    go i
        | i > sqrtN = True
        | n `mod` i == 0 || n `mod` (i + 2) == 0 = False
        | otherwise = go (i + 6)

-- Integer square root
isqrt :: Integer -> Integer
isqrt = floor . sqrt . fromIntegral

-- Helper for function composition
(&) :: a -> (a -> b) -> b
x & f = f x
infixl 1 &
