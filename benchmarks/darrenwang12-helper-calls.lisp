(define (helper x)
  (add1 x))

(define (add3 x)
  (+ (helper x) 2))

(define (adjust x y)
  (+ (add3 x) (helper y)))

(define (loop n acc)
  (if (= n 0)
      acc
      (loop (sub1 n) (adjust acc 1))))

(print (loop 500000 0))