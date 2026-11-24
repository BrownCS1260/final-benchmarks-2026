(define (square x) (* x x))
(define (add2 x) (add1 (add1 x)))
(define (dist2 x y) (+ (square x) (square y)))

(define (inner i j acc)
  (if (zero? j)
      acc
      (let ((x (add2 i)))
        (inner i (sub1 j) (+ acc (dist2 j x))))))

(define (outer i acc)
  (if (zero? i)
      acc
      (outer (sub1 i) (+ acc (inner i 1000 0)))))

(print (outer 1000 0))