#lang racket

;; Prime Partition Algorithm - Racket Implementation
;; Simplified version without generators

(provide main)

;; Main entry point
(define (main)
  (displayln "=== RACKET VERSION ===")
  (define result (run-algorithm 10 '(1 2)))
  (match-define (list primes counts) result)
  (displayln (format "Hello primes: ~a" (sort (remove-duplicates primes) <)))
  (displayln (format "Total discovered: ~a" (length (remove-duplicates primes))))
  (displayln (format "Found composites: ~a" (filter (compose not is-prime?) primes))))

;; Run algorithm for n iterations
(define (run-algorithm iterations initial)
  (let loop ([i 0]
             [current initial]
             [acc-primes '()]
             [acc-counts (hash)])
    (if (= i iterations)
        (list acc-primes acc-counts)
        (let* ([found (compute-primes current)]
               [distinct (remove-duplicates found)]
               [new-counts (for/fold ([counts acc-counts])
                                    ([prime found])
                             (hash-update counts prime add1 0))]
               [difference (set-subtract distinct current)]
               [next-prime (if (null? difference) #f (apply min difference))]
               [next-current (if next-prime (append current (list next-prime)) current)])
          (loop (add1 i) next-current (append acc-primes distinct) new-counts)))))

;; Compute all primes from the current seed set
(define (compute-primes seeds)
  (if (null? seeds)
      '()
      (let* ([max-prime (apply max seeds)]
             [range-start (add1 max-prime)]
             [range-end (sub1 (* max-prime max-prime))]
             [candidates
              (for*/list ([partition (in-list (binary-partitions seeds))]
                         [exps (in-list (exponent-combinations (length seeds) 2))]
                         #:do [(match-define (list left right) partition)
                               (define-values (left-exps right-exps) 
                                 (split-at exps (length left)))
                               (define left-prod 
                                 (for/product ([num left] [exp left-exps]) 
                                   (expt num exp)))
                               (define right-prod 
                                 (for/product ([num right] [exp right-exps]) 
                                   (expt num exp)))]
                         [candidate (in-list (list (+ left-prod right-prod)
                                                  (abs (- left-prod right-prod))))]
                         #:when (and (> candidate max-prime) 
                                   (< candidate (* max-prime max-prime))
                                   (is-prime? candidate)))
                candidate)])
        (sort (remove-duplicates candidates) <))))

;; Generate all binary partitions
(define (binary-partitions lst)
  (if (< (length lst) 2)
      '()
      (for*/list ([i (in-range 1 (add1 (quotient (length lst) 2)))]
                  [left (in-list (combinations i lst))]
                  #:do [(define right (set-subtract lst left))]
                  #:when (= (length right) (- (length lst) i)))
        (list left right))))

;; Generate k-combinations
(define (combinations k lst)
  (cond
    [(zero? k) '(())]
    [(null? lst) '()]
    [else (append (map (λ (rest) (cons (car lst) rest))
                      (combinations (sub1 k) (cdr lst)))
                 (combinations k (cdr lst)))]))

;; Generate all exponent combinations
(define (exponent-combinations size max-exp)
  (if (<= size 0)
      '()
      (let helper ([remaining size])
        (if (zero? remaining)
            '(())
            (let ([sub-combos (helper (sub1 remaining))])
              (for*/list ([exp (in-range 1 (add1 max-exp))]
                         [combo (in-list sub-combos)])
                (cons exp combo)))))))

;; Optimized primality test
(define (is-prime? n)
  (cond
    [(<= n 1) #f]
    [(= n 2) #t]
    [(even? n) #f]
    [else (for/and ([i (in-range 3 (add1 (integer-sqrt n)) 2)])
            (not (zero? (modulo n i))))]))

;; Set subtraction
(define (set-subtract lst1 lst2)
  (filter (λ (x) (not (member x lst2))) lst1))

;; Run the program
(main)
