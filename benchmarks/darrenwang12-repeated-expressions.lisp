(define (loop n acc)
  (if (= n 0)
      acc
      (loop (sub1 n)
            (+ acc
               (+ (+ (+ (+ n 3) (- n 1))
                     (+ (- n 4) (+ n 2)))
                  (+ (+ (+ n 3) (- n 1))
                     (+ (- n 4) (+ n 2))))))))

(print (loop 500000 0))
