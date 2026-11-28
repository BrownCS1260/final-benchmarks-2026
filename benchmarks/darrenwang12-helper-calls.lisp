(define (helper x)
  (add1 x))

(define (add3 x)
  (+ (helper x) 2))

(define (loop n acc)
  (if (= n 0)
      acc
      (loop (sub1 n) (add3 acc))))

(print (loop 500000 0))
